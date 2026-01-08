#!/usr/bin/env python3
"""
Instagram Synchronization Script
Stahuje příspěvky z @amitydrinks.cz a detekuje označení influencerů
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.api.meta_api import MetaAPIClient
from src.database.db_manager import DatabaseManager
from datetime import datetime, timedelta
import json

class InstagramSyncManager:
    """Správce synchronizace Instagram dat"""

    def __init__(self):
        self.api = MetaAPIClient()
        self.db = DatabaseManager()
        self.stats = {
            'total_posts_checked': 0,
            'new_posts_found': 0,
            'influencers_matched': 0,
            'errors': 0
        }

    def sync(self, days_back: int = 7):
        """
        Hlavní synchronizační metoda

        Args:
            days_back: Kolik dní zpět kontrolovat (default 7)
        """
        print("=" * 60)
        print("🍹 AMITY DRINKS - Instagram Synchronization")
        print("=" * 60)
        print(f"📅 Kontroluji příspěvky za posledních {days_back} dní\n")

        # Připojení k databázi
        self.db.connect()

        # Načtení influencerů z databáze
        influencers = self.db.get_all_influencers()
        influencer_handles = {
            inf['instagram_handle'].lower(): inf
            for inf in influencers
            if inf.get('instagram_handle')
        }

        print(f"👥 Načteno {len(influencer_handles)} influencerů z databáze")
        print(f"   Handles: {', '.join(influencer_handles.keys())}\n")

        # Získání příspěvků z Amity IG účtu
        print("📱 Stahuji příspěvky z @amitydrinks.cz...")

        # Nepou číváme 'since' protože Instagram API to nepodporuje správně
        # Místo toho filtrujeme až po stažení
        media = self.api.get_instagram_media(limit=50)

        # Filtrování podle data
        if days_back:
            from datetime import timezone
            since_date = datetime.now(timezone.utc) - timedelta(days=days_back)
            media = [
                post for post in media
                if post.get('timestamp') and
                datetime.fromisoformat(post['timestamp'].replace('Z', '+00:00')) >= since_date
            ]
            print(f"   📅 Filtrováno na posledních {days_back} dní")

        if not media:
            print("⚠️  Žádné příspěvky nenalezeny")
        else:
            print(f"✅ Nalezeno {len(media)} příspěvků\n")
            self.stats['total_posts_checked'] = len(media)

            # Zpracování každého příspěvku
            for i, post in enumerate(media, 1):
                print(f"[{i}/{len(media)}] Zpracovávám příspěvek...")

                try:
                    self._process_post(post, influencer_handles)
                except Exception as e:
                    print(f"   ❌ Chyba: {str(e)}")
                    self.stats['errors'] += 1

        # Kontrola aktivních stories
        print("\n📸 Kontroluji aktivní stories...")
        stories = self.api.get_instagram_stories()

        if stories:
            print(f"✅ Nalezeno {len(stories)} aktivních stories\n")
            for i, story in enumerate(stories, 1):
                print(f"[Story {i}/{len(stories)}] Zpracovávám...")
                try:
                    self._process_story(story, influencer_handles)
                except Exception as e:
                    print(f"   ❌ Chyba: {str(e)}")
                    self.stats['errors'] += 1
        else:
            print("ℹ️  Žádné aktivní stories")

        # Aktualizace měsíčních statistik pro všechny influencery
        print("\n📊 Aktualizuji měsíční statistiky...")
        current_year = datetime.now().year
        current_month = datetime.now().month

        for influencer in influencers:
            self.db.update_monthly_stats(influencer['id'], current_year, current_month)

        self.db.close()

        # Výsledky
        self._print_results()
        return self.stats

    def _process_post(self, post: dict, influencer_handles: dict):
        """
        Zpracuje jednotlivý příspěvek a hledá influencery

        Args:
            post: Data příspěvku z Instagram API
            influencer_handles: Dict {handle: influencer_data}
        """
        post_id = post.get('id')
        caption = post.get('caption', '').lower()
        media_type = post.get('media_type', 'UNKNOWN')
        timestamp = post.get('timestamp')
        permalink = post.get('permalink', '')

        print(f"   📸 {media_type} - {timestamp[:10] if timestamp else 'N/A'}")

        # Získání detailních informací o příspěvku (včetně tagged users)
        detailed_post = self._get_post_details(post_id)

        if not detailed_post:
            print(f"   ⚠️  Nepodařilo se získat detaily")
            return

        # Hledání označených uživatelů
        tagged_users = detailed_post.get('tagged_users', [])

        # Kontrola v caption (fallback pokud tagged_users není dostupné)
        mentioned_handles = self._extract_handles_from_caption(caption)

        all_handles = set()

        # Přidání tagged users
        for tagged in tagged_users:
            username = tagged.get('username', '').lower()
            if username:
                all_handles.add(username)

        # Přidání mentions z caption
        all_handles.update(mentioned_handles)

        if not all_handles:
            print(f"   ℹ️  Žádné označení nenalezeno")
            return

        print(f"   🔍 Nalezeno označení: {', '.join(all_handles)}")

        # Párování s našimi influencery
        matched = False
        for handle in all_handles:
            if handle in influencer_handles:
                influencer = influencer_handles[handle]
                matched = True

                print(f"   ✅ MATCH! Influencer: {influencer['jmeno']} (@{handle})")

                # Uložení do databáze
                self._save_post_to_db(post, detailed_post, influencer)
                self.stats['influencers_matched'] += 1

        if matched:
            self.stats['new_posts_found'] += 1

    def _process_story(self, story: dict, influencer_handles: dict):
        """
        Zpracuje Instagram story a hledá influencery

        Args:
            story: Data story z Instagram API
            influencer_handles: Dict {handle: influencer_data}
        """
        story_id = story.get('id')
        caption = story.get('caption', '').lower()
        timestamp = story.get('timestamp')

        print(f"   📸 Story ID: {story_id[:15] if story_id else 'N/A'}...")
        print(f"   📅 Datum: {timestamp[:10] if timestamp else 'N/A'}")

        # Získání detailů
        detailed_story = self.api.get_story_details_with_tags(story_id)

        if not detailed_story:
            print(f"   ⚠️  Nepodařilo se získat detaily")
            return

        # Hledání influencerů v caption (@mentions)
        mentioned_handles = self._extract_handles_from_caption(caption)

        if not mentioned_handles:
            print(f"   ℹ️  Žádné @mentions nenalezeny")
            return

        print(f"   🔍 Nalezeno: {', '.join(f'@{h}' for h in mentioned_handles)}")

        # Párování s influencery
        matched = False
        for handle in mentioned_handles:
            if handle in influencer_handles:
                influencer = influencer_handles[handle]
                matched = True

                print(f"   ✅ MATCH! Influencer: {influencer['jmeno']} (@{handle})")

                # Uložení jako story příspěvek
                self._save_story_to_db(story, detailed_story, influencer)
                self.stats['influencers_matched'] += 1

        if matched:
            self.stats['new_posts_found'] += 1

    def _get_post_details(self, media_id: str) -> dict:
        """
        Získá detailní informace o příspěvku včetně tagged users

        Args:
            media_id: ID příspěvku

        Returns:
            Detailní data příspěvku
        """
        url = f"{self.api.base_url}/{media_id}"
        params = {
            'fields': 'id,caption,media_type,media_url,permalink,timestamp,'
                     'like_count,comments_count,username',
            'access_token': self.api.access_token
        }

        try:
            import requests
            response = requests.get(url, params=params, timeout=30)

            if response.status_code == 200:
                data = response.json()
                # tagged_users field může být nedostupný bez speciálních oprávnění
                # Proto ho načítáme samostatně pokud je dostupný
                return data
            else:
                error_data = response.json() if response.status_code != 500 else {}
                error_msg = error_data.get('error', {}).get('message', response.text[:100])
                print(f"      API Error {response.status_code}: {error_msg}")

        except Exception as e:
            print(f"      Exception: {str(e)}")

        return {}

    def _extract_handles_from_caption(self, caption: str) -> set:
        """
        Extrahuje @handles z caption textu

        Args:
            caption: Text příspěvku

        Returns:
            Set of handles (bez @)
        """
        import re

        # Regex pro @handle (alfanumerické znaky, podtržítka, tečky)
        pattern = r'@([a-z0-9_.]+)'
        matches = re.findall(pattern, caption)

        return set(matches)

    def _save_post_to_db(self, post: dict, detailed_post: dict, influencer: dict):
        """
        Uloží příspěvek do databáze

        Args:
            post: Základní data příspěvku
            detailed_post: Detailní data příspěvku
            influencer: Data influencera
        """
        # Mapování media_type na post_type
        media_type = post.get('media_type', 'POST').upper()

        type_mapping = {
            'IMAGE': 'post',
            'VIDEO': 'reel',
            'CAROUSEL_ALBUM': 'post',
            'STORY': 'story'
        }

        post_type = type_mapping.get(media_type, 'post')

        # Příprava dat pro uložení
        post_data = {
            'influencer_id': influencer['id'],
            'platform': 'instagram',
            'post_type': post_type,
            'post_id': f"ig_{post.get('id')}",
            'post_url': post.get('permalink', ''),
            'caption': post.get('caption', '')[:500],  # Omezení délky
            'timestamp': datetime.fromisoformat(post.get('timestamp', '').replace('Z', '+00:00')) if post.get('timestamp') else datetime.now(),
            'likes': detailed_post.get('like_count', 0),
            'comments': detailed_post.get('comments_count', 0),
            'shares': 0,
            'reach': 0,  # Insights vyžadují speciální endpoint
            'impressions': 0,
            'engagement_rate': 0
        }

        # Pokusit se získat insights
        try:
            insights = self.api.get_instagram_insights(post.get('id'))
            if insights:
                post_data['reach'] = insights.get('reach', 0)
                post_data['impressions'] = insights.get('impressions', 0)
                post_data['engagement_rate'] = self._calculate_engagement(
                    detailed_post.get('like_count', 0),
                    detailed_post.get('comments_count', 0),
                    insights.get('reach', 1)
                )
        except:
            pass  # Insights nejsou kritické

        # Uložení do databáze
        result = self.db.add_post(post_data)

        if result:
            print(f"      💾 Uloženo do databáze (ID: {result})")
        else:
            print(f"      ℹ️  Příspěvek již existuje v databázi")

    def _save_story_to_db(self, story: dict, detailed_story: dict, influencer: dict):
        """
        Uloží story do databáze jako příspěvek influencera

        Args:
            story: Základní data story
            detailed_story: Detailní data story
            influencer: Data influencera
        """
        # Příprava dat
        story_data = {
            'influencer_id': influencer['id'],
            'platform': 'instagram',
            'post_type': 'story',
            'post_id': f"ig_story_{story.get('id')}",
            'post_url': '',  # Stories nemají permalink
            'caption': story.get('caption', '')[:500],
            'timestamp': datetime.fromisoformat(
                story.get('timestamp', '').replace('Z', '+00:00')
            ) if story.get('timestamp') else datetime.now(),
            'likes': 0,  # Stories insights vyžadují speciální oprávnění
            'comments': 0,
            'shares': 0,
            'reach': 0,
            'impressions': 0,
            'engagement_rate': 0
        }

        # Uložení
        result = self.db.add_post(story_data)

        if result:
            print(f"      💾 Story uložena do databáze (ID: {result})")
        else:
            print(f"      ℹ️  Story již existuje v databázi")

    def _calculate_engagement(self, likes: int, comments: int, reach: int) -> float:
        """Vypočítá engagement rate"""
        if reach == 0:
            return 0.0
        return round(((likes + comments) / reach) * 100, 2)

    def _print_results(self):
        """Vypíše výsledky synchronizace"""
        print("\n" + "=" * 60)
        print("📊 VÝSLEDKY SYNCHRONIZACE")
        print("=" * 60)
        print(f"✅ Zkontrolováno příspěvků: {self.stats['total_posts_checked']}")
        print(f"🆕 Nových příspěvků: {self.stats['new_posts_found']}")
        print(f"👥 Influencerů detekováno: {self.stats['influencers_matched']}")
        print(f"❌ Chyb: {self.stats['errors']}")
        print("=" * 60)


def main():
    """Hlavní funkce pro ruční spuštění"""
    import argparse

    parser = argparse.ArgumentParser(description='Instagram Synchronization')
    parser.add_argument('--days', type=int, default=7,
                       help='Počet dní zpět pro kontrolu (default: 7)')

    args = parser.parse_args()

    try:
        sync_manager = InstagramSyncManager()
        stats = sync_manager.sync(days_back=args.days)

        # Exit code podle výsledků
        if stats['errors'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        print("\n\n⚠️  Synchronizace přerušena uživatelem")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Kritická chyba: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
