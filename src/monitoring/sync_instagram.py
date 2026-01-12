"""
Instagram Synchronization - Automatic creator detection and post tracking
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.api.meta_api import MetaAPIClient
from src.database.postgres_manager import UniversalDatabaseManager
from src.utils.logger import api_logger


class InstagramSync:
    """Automatická synchronizace Instagram dat s detekcí creatorů"""

    def __init__(self):
        self.api = MetaAPIClient()
        self.db = UniversalDatabaseManager()

    def sync(self, days_back: int = 7):
        """
        Hlavní synchronizační metoda - fallback když webhook nefunguje

        Strategie (v pořadí priority):
        1. Tagged posts (po App Review) - get_instagram_tags()
        2. Stories s tagged users - get_instagram_stories()
        3. Caption regex fallback - hledání @mentions v textu

        Args:
            days_back: Kolik dní zpět synchronizovat
        """
        api_logger.info(f"🔄 Spouštím Instagram sync (poslední {days_back} dní)")

        self.db.connect()

        try:
            total_processed = 0

            # 1. PRIORITA: Tagged posts (funguje až po App Review)
            total_processed += self._sync_tagged_posts()

            # 2. FALLBACK: Stories s tagged users
            total_processed += self._sync_stories()

            # 3. LAST RESORT: Caption regex
            total_processed += self._sync_with_caption_regex(days_back)

            api_logger.info(f"✅ Synchronizace dokončena: {total_processed} příspěvků zpracováno")

        except Exception as e:
            api_logger.error(f"❌ Sync error: {str(e)}")

        finally:
            self.db.close()

    def _sync_tagged_posts(self) -> int:
        """
        Synchronizuje tagged posts (vyžaduje App Review)

        Returns:
            Počet zpracovaných postů
        """
        api_logger.info("📱 Zkouším stáhnout tagged posts...")

        try:
            tagged_posts = self.api.get_instagram_tags(limit=50)

            if not tagged_posts:
                api_logger.info("ℹ️  Žádné tagged posts (možná čeká na App Review)")
                return 0

            api_logger.info(f"Nalezeno {len(tagged_posts)} tagged posts")
            processed = 0

            for post in tagged_posts:
                creator_username = post.get('username')

                if not creator_username:
                    api_logger.warning(f"Post {post.get('id')} nemá username")
                    continue

                # Najít influencera podle username
                influencer = self.db.get_influencer_by_instagram_handle(creator_username)

                if not influencer:
                    api_logger.warning(f"❓ Neznámý influencer: @{creator_username}")
                    # Uložit i bez creator_id (pro "pending" review)
                    self._save_post_with_creator(post, None, creator_username, 'api_tags')
                    processed += 1
                    continue

                # Uložit s plným creator info
                self._save_post_with_creator(post, influencer, creator_username, 'api_tags')
                processed += 1

            return processed

        except Exception as e:
            api_logger.error(f"Error syncing tagged posts: {str(e)}")
            return 0

    def _sync_stories(self) -> int:
        """
        Synchronizuje stories s tagged users

        Returns:
            Počet zpracovaných stories
        """
        api_logger.info("📸 Zkouším stáhnout stories...")

        try:
            stories = self.api.get_instagram_stories()

            if not stories:
                api_logger.info("ℹ️  Žádné aktivní stories")
                return 0

            api_logger.info(f"Nalezeno {len(stories)} stories")
            processed = 0

            for story in stories:
                tagged_users = story.get('tagged_users', [])

                if not tagged_users:
                    # Zkus fallback: hledat @mentions v caption
                    caption = story.get('caption', '')
                    if caption:
                        mentioned = self._extract_handles_from_caption(caption)
                        tagged_users = mentioned

                if not tagged_users:
                    continue

                # Pro každého tagged usera vytvoř záznam
                for username in tagged_users:
                    influencer = self.db.get_influencer_by_instagram_handle(username)

                    if not influencer:
                        api_logger.warning(f"❓ Neznámý influencer: @{username}")
                        self._save_post_with_creator(story, None, username, 'api_stories')
                    else:
                        self._save_post_with_creator(story, influencer, username, 'api_stories')

                    processed += 1

            return processed

        except Exception as e:
            api_logger.error(f"Error syncing stories: {str(e)}")
            return 0

    def _sync_with_caption_regex(self, days_back: int) -> int:
        """
        Fallback: Hledá @mentions v caption textu

        Args:
            days_back: Kolik dní zpět hledat

        Returns:
            Počet zpracovaných příspěvků
        """
        api_logger.info("🔍 Fallback: Hledám @mentions v captions...")

        try:
            since = datetime.now() - timedelta(days=days_back)
            media = self.api.get_instagram_media(limit=50, since=since)

            if not media:
                api_logger.info("ℹ️  Žádné media nalezeno")
                return 0

            processed = 0

            for post in media:
                caption = post.get('caption', '')

                if not caption:
                    continue

                # Extract @mentions
                mentioned_handles = self._extract_handles_from_caption(caption)

                if not mentioned_handles:
                    continue

                # Pro každý mentioned handle vytvoř záznam
                for handle in mentioned_handles:
                    influencer = self.db.get_influencer_by_instagram_handle(handle)

                    if influencer:
                        self._save_post_with_creator(post, influencer, handle, 'caption_regex')
                        processed += 1

            return processed

        except Exception as e:
            api_logger.error(f"Error syncing with caption regex: {str(e)}")
            return 0

    def _extract_handles_from_caption(self, caption: str) -> List[str]:
        """
        Extrahuje Instagram handles z textu pomocí regex

        Args:
            caption: Text příspěvku

        Returns:
            List of handles bez @ (např. ['dustyfeet_23'])
        """
        if not caption:
            return []

        # Pattern: @username (letters, numbers, underscore, dot)
        pattern = r'@([a-zA-Z0-9_.]+)'
        matches = re.findall(pattern, caption)

        # Remove duplicates, normalize to lowercase
        handles = list(set(h.lower() for h in matches))

        return handles

    def _save_post_with_creator(
        self,
        post: Dict,
        influencer: Optional[Dict],
        creator_username: str,
        detection_method: str
    ) -> Optional[int]:
        """
        Uloží příspěvek s creator info do databáze

        Args:
            post: Data z Meta API
            influencer: Dict s influencer daty (nebo None pokud neznámý)
            creator_username: Instagram handle autora
            detection_method: 'webhook', 'api_tags', 'api_stories', 'caption_regex'

        Returns:
            ID nově vytvořeného příspěvku nebo None
        """
        # Determine post type
        media_type = post.get('media_type', '').upper()
        if media_type == 'IMAGE' or media_type == 'CAROUSEL_ALBUM':
            post_type = 'post'
        elif media_type == 'VIDEO':
            # Could be reel or regular video - heuristic:
            # Reels are typically shorter, but we don't have duration here
            post_type = 'reel'  # Default to reel for videos
        elif 'story' in post.get('permalink', '').lower():
            post_type = 'story'
        else:
            post_type = 'post'  # Default

        # Get Amity Drinks influencer ID (the tagged account)
        # Assume ID=1 or query by name
        amity_influencer = self.db.get_influencer_by_instagram_handle('amitydrinks.cz')
        amity_id = amity_influencer['id'] if amity_influencer else 1

        post_data = {
            'creator_username': creator_username,
            'creator_id': influencer['id'] if influencer else None,
            'influencer_id': amity_id,  # Amity Drinks (tagged account)
            'platform': 'instagram',
            'post_type': post_type,
            'post_id': f"ig_{post.get('id')}",
            'post_url': post.get('permalink', ''),
            'caption': (post.get('caption', '') or '')[:500],
            'timestamp': post.get('timestamp', datetime.now().isoformat()),
            'likes': post.get('like_count', 0),
            'comments': post.get('comments_count', 0),
            'reach': post.get('reach', 0),
            'impressions': post.get('impressions', 0),
            'shares': post.get('shares', 0),
            'engagement_rate': 0,  # Calculate if needed
            'detection_method': detection_method
        }

        try:
            post_id = self.db.add_post_with_creator(post_data)

            if post_id and influencer:
                # Update monthly stats for the creator
                timestamp = datetime.fromisoformat(post.get('timestamp', datetime.now().isoformat()).replace('Z', '+00:00'))
                self.db.update_monthly_stats(
                    influencer['id'],
                    timestamp.year,
                    timestamp.month
                )

                api_logger.info(f"✅ Saved post from @{creator_username} (method: {detection_method})")
            elif post_id:
                api_logger.info(f"✅ Saved post from unknown @{creator_username} (pending review)")

            return post_id

        except Exception as e:
            api_logger.error(f"Error saving post: {str(e)}")
            return None

    def process_tagged_mention(self, mention_data: Dict):
        """
        Zpracuje webhook notifikaci o tagged mention

        Používá se když přijde webhook od Meta že někdo označil @amitydrinks.cz

        Args:
            mention_data: {
                'media_id': '...',
                'username': 'dustyfeet_23'
            }
        """
        media_id = mention_data.get('media_id')
        username = mention_data.get('username')

        if not media_id or not username:
            api_logger.error(f"Invalid mention data: {mention_data}")
            return

        api_logger.info(f"🏷️  Processing webhook mention: @{username} → media {media_id}")

        # 1. Fetch media details from API
        media = self.api.get_media_details_by_id(media_id)

        if not media:
            api_logger.error(f"Could not fetch media {media_id} from API")
            return

        # 2. Find influencer by username
        self.db.connect()

        try:
            influencer = self.db.get_influencer_by_instagram_handle(username)

            if not influencer:
                api_logger.warning(f"❓ Unknown influencer: @{username}")
                # Save without creator_id (pending review)
                self._save_post_with_creator(media, None, username, 'webhook')
            else:
                # Save with full creator info
                self._save_post_with_creator(media, influencer, username, 'webhook')

            api_logger.info(f"✅ Webhook mention processed: @{username}")

        except Exception as e:
            api_logger.error(f"Error processing webhook mention: {str(e)}")

        finally:
            self.db.close()


# Convenience function for dashboard
def sync_instagram_data(days_back: int = 7) -> int:
    """
    Convenience wrapper pro volání z dashboardu

    Args:
        days_back: Kolik dní zpět synchronizovat

    Returns:
        Počet zpracovaných příspěvků
    """
    sync = InstagramSync()
    sync.sync(days_back)
    return 0  # TODO: Return actual count
