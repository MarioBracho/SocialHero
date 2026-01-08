"""
Hlavní monitoring logika pro detekci příspěvků influencerů
"""
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.api.meta_api import MetaAPIClient
from src.database.db_manager import DatabaseManager
from src.utils.config import Config
from src.utils.logger import monitor_logger

class InfluencerMonitor:
    """Monitoring influencer aktivity"""

    def __init__(self):
        self.api = MetaAPIClient()
        self.db = DatabaseManager()

    def check_instagram_tags(self, since_hours: int = 12) -> List[Dict]:
        """
        Zkontroluje Instagram tagy za posledních X hodin

        Args:
            since_hours: Kolik hodin zpět kontrolovat

        Returns:
            Seznam nových příspěvků
        """
        monitor_logger.info(f"🔍 Kontroluji Instagram tagy (posledních {since_hours}h)...")

        # Získání tagů z API
        tags = self.api.get_instagram_tags(limit=50)

        if not tags:
            monitor_logger.info("Žádné Instagram tagy nenalezeny")
            return []

        # Časový filtr
        since_time = datetime.now() - timedelta(hours=since_hours)
        new_posts = []

        self.db.connect()

        # Získání všech influencerů z DB
        influencers = self.db.get_all_influencers()
        influencer_map = {inf['instagram_handle'].lower(): inf for inf in influencers if inf.get('instagram_handle')}

        for tag in tags:
            try:
                # Parsování timestamp
                post_time = datetime.strptime(tag['timestamp'], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)

                # Filtr času
                if post_time < since_time:
                    continue

                # Zjištění autora
                username = tag.get('username', '').lower()

                if username not in influencer_map:
                    continue  # Není náš influencer

                influencer = influencer_map[username]

                # Určení typu příspěvku
                media_type = tag.get('media_type', 'IMAGE')
                post_type = self._determine_post_type(media_type)

                # Příprava dat pro DB
                post_data = {
                    'influencer_id': influencer['id'],
                    'platform': 'instagram',
                    'post_type': post_type,
                    'post_id': tag['id'],
                    'post_url': tag.get('permalink', ''),
                    'caption': tag.get('caption', ''),
                    'timestamp': post_time,
                    'likes': tag.get('like_count', 0),
                    'comments': tag.get('comments_count', 0),
                    'shares': 0,
                    'reach': 0,
                    'impressions': 0,
                    'engagement_rate': 0
                }

                # Přidání do DB (pokud ještě neexistuje)
                post_id = self.db.add_post(post_data)

                if post_id:
                    new_posts.append(post_data)
                    monitor_logger.info(f"✅ Nový příspěvek: @{username} - {post_type}")

            except Exception as e:
                monitor_logger.error(f"Chyba při zpracování tagu: {str(e)}")
                continue

        # Aktualizace měsíčních statistik
        current_year = datetime.now().year
        current_month = datetime.now().month

        for influencer in influencers:
            self.db.update_monthly_stats(influencer['id'], current_year, current_month)

        self.db.close()

        monitor_logger.info(f"🎯 Nalezeno {len(new_posts)} nových příspěvků")
        return new_posts

    def check_facebook_tags(self, since_hours: int = 12) -> List[Dict]:
        """
        Zkontroluje Facebook tagy za posledních X hodin

        Args:
            since_hours: Kolik hodin zpět kontrolovat

        Returns:
            Seznam nových příspěvků
        """
        monitor_logger.info(f"🔍 Kontroluji Facebook tagy (posledních {since_hours}h)...")

        since_time = datetime.now() - timedelta(hours=since_hours)
        tags = self.api.get_facebook_tagged_posts(limit=50, since=since_time)

        if not tags:
            monitor_logger.info("Žádné Facebook tagy nenalezeny")
            return []

        new_posts = []
        self.db.connect()

        # Získání influencerů
        influencers = self.db.get_all_influencers()
        influencer_map_fb = {inf['facebook_handle'].lower(): inf for inf in influencers if inf.get('facebook_handle')}

        for tag in tags:
            try:
                # Parsování timestamp
                post_time = datetime.strptime(tag['created_time'], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)

                if post_time < since_time:
                    continue

                # Zjištění autora
                author_name = tag.get('from', {}).get('name', '').lower()

                # Hledání v influencerech
                influencer = None
                for inf in influencers:
                    if inf.get('facebook_handle', '').lower() in author_name:
                        influencer = inf
                        break

                if not influencer:
                    continue

                # Příprava dat
                post_data = {
                    'influencer_id': influencer['id'],
                    'platform': 'facebook',
                    'post_type': 'post',
                    'post_id': tag['id'],
                    'post_url': tag.get('permalink_url', ''),
                    'caption': tag.get('message', ''),
                    'timestamp': post_time,
                    'likes': tag.get('likes', {}).get('summary', {}).get('total_count', 0),
                    'comments': tag.get('comments', {}).get('summary', {}).get('total_count', 0),
                    'shares': tag.get('shares', {}).get('count', 0),
                    'reach': 0,
                    'impressions': 0,
                    'engagement_rate': 0
                }

                post_id = self.db.add_post(post_data)

                if post_id:
                    new_posts.append(post_data)
                    monitor_logger.info(f"✅ Nový FB příspěvek: {influencer['jmeno']}")

            except Exception as e:
                monitor_logger.error(f"Chyba při zpracování FB tagu: {str(e)}")
                continue

        # Aktualizace statistik
        current_year = datetime.now().year
        current_month = datetime.now().month
        for influencer in influencers:
            self.db.update_monthly_stats(influencer['id'], current_year, current_month)

        self.db.close()

        monitor_logger.info(f"🎯 Nalezeno {len(new_posts)} nových FB příspěvků")
        return new_posts

    def run_check(self, since_hours: int = 12) -> Dict:
        """
        Spustí kompletní kontrolu (Instagram + Facebook)

        Args:
            since_hours: Kolik hodin zpět kontrolovat

        Returns:
            Souhrn výsledků
        """
        monitor_logger.info("="*60)
        monitor_logger.info("🚀 SPOUŠTÍM MONITORING CHECK")
        monitor_logger.info("="*60)

        results = {
            'timestamp': datetime.now(),
            'instagram_posts': [],
            'facebook_posts': [],
            'total_posts': 0,
            'success': True,
            'errors': []
        }

        try:
            # Instagram check
            ig_posts = self.check_instagram_tags(since_hours)
            results['instagram_posts'] = ig_posts

            # Facebook check
            fb_posts = self.check_facebook_tags(since_hours)
            results['facebook_posts'] = fb_posts

            results['total_posts'] = len(ig_posts) + len(fb_posts)

            monitor_logger.info("="*60)
            monitor_logger.info(f"✅ MONITORING DOKONČEN")
            monitor_logger.info(f"📊 Celkem nových příspěvků: {results['total_posts']}")
            monitor_logger.info(f"   - Instagram: {len(ig_posts)}")
            monitor_logger.info(f"   - Facebook: {len(fb_posts)}")
            monitor_logger.info("="*60)

        except Exception as e:
            monitor_logger.error(f"❌ Chyba během monitoringu: {str(e)}")
            results['success'] = False
            results['errors'].append(str(e))

        return results

    def _determine_post_type(self, media_type: str) -> str:
        """Určí typ příspěvku podle media_type"""
        media_type = media_type.upper()

        if media_type == 'IMAGE':
            return 'post'
        elif media_type == 'VIDEO':
            return 'reel'
        elif media_type == 'CAROUSEL_ALBUM':
            return 'post'
        else:
            return 'post'
