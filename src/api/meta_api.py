"""
Meta (Facebook + Instagram) API Client
"""
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config import Config
from src.utils.logger import api_logger

class MetaAPIClient:
    """Klient pro Meta Graph API (Instagram + Facebook)"""

    def __init__(self):
        self.access_token = Config.META_ACCESS_TOKEN
        self.page_access_token = Config.FACEBOOK_PAGE_ACCESS_TOKEN or Config.META_ACCESS_TOKEN
        self.app_id = Config.META_APP_ID
        self.app_secret = Config.META_APP_SECRET
        self.ig_account_id = Config.INSTAGRAM_BUSINESS_ACCOUNT_ID
        self.fb_page_id = Config.FACEBOOK_PAGE_ID
        self.business_id = Config.META_BUSINESS_ID
        self.api_version = Config.API_VERSION
        self.base_url = f"https://graph.facebook.com/{self.api_version}"

        # Rate limiting
        self.requests_count = 0
        self.requests_window_start = time.time()
        self.max_requests_per_hour = 200

    def _check_rate_limit(self):
        """Kontrola rate limitu"""
        current_time = time.time()
        elapsed = current_time - self.requests_window_start

        if elapsed > 3600:  # Nové okno po hodině
            self.requests_count = 0
            self.requests_window_start = current_time

        if self.requests_count >= self.max_requests_per_hour:
            sleep_time = 3600 - elapsed
            api_logger.warning(f"Rate limit dosažen, čekám {sleep_time:.0f} sekund")
            time.sleep(sleep_time)
            self.requests_count = 0
            self.requests_window_start = time.time()

    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """
        Provede API request s error handlingem

        Args:
            url: API endpoint URL
            params: Query parametry

        Returns:
            JSON response nebo None při chybě
        """
        self._check_rate_limit()

        if params is None:
            params = {}

        params['access_token'] = self.access_token

        try:
            response = requests.get(url, params=params, timeout=30)
            self.requests_count += 1

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error_data = response.json()
                api_logger.warning(f"API chyba 400: {error_data.get('error', {}).get('message', 'Unknown error')}")
                return None
            elif response.status_code == 190:  # Token expired
                api_logger.error("Access token vypršel!")
                return None
            else:
                api_logger.error(f"API error {response.status_code}: {response.text}")
                return None

        except requests.exceptions.Timeout:
            api_logger.error("API request timeout")
            return None
        except requests.exceptions.RequestException as e:
            api_logger.error(f"Request exception: {str(e)}")
            return None

    # ============================================
    # INSTAGRAM API
    # ============================================

    def get_instagram_profile(self) -> Optional[Dict]:
        """Získá informace o Instagram Business profilu"""
        url = f"{self.base_url}/{self.ig_account_id}"
        params = {
            'fields': 'username,name,profile_picture_url,followers_count,follows_count,media_count'
        }

        api_logger.info("Načítám Instagram profil...")
        data = self._make_request(url, params)

        if data:
            api_logger.info(f"Instagram profil načten: @{data.get('username')}")
        return data

    def get_instagram_media(self, limit: int = 25, since: datetime = None) -> List[Dict]:
        """
        Získá příspěvky z Instagram účtu

        Args:
            limit: Maximální počet příspěvků
            since: Načíst pouze příspěvky novější než toto datum

        Returns:
            Seznam příspěvků
        """
        url = f"{self.base_url}/{self.ig_account_id}/media"
        params = {
            'fields': 'id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count',
            'limit': limit
        }

        if since:
            params['since'] = int(since.timestamp())

        api_logger.info(f"Načítám Instagram media (limit: {limit})...")
        data = self._make_request(url, params)

        if data and 'data' in data:
            posts = data['data']
            api_logger.info(f"Načteno {len(posts)} Instagram příspěvků")
            return posts

        return []

    def get_instagram_tags(self, limit: int = 50) -> List[Dict]:
        """
        Získá příspěvky, ve kterých byl účet označen (tagged)

        POZNÁMKA: Endpoint /tags vyžaduje speciální oprávnění, která musí schválit Meta.
        Alternativa: použít get_instagram_hashtag_search() nebo get_instagram_mentions()

        Args:
            limit: Maximální počet příspěvků

        Returns:
            Seznam tagovaných příspěvků
        """
        url = f"{self.base_url}/{self.ig_account_id}/tags"
        params = {
            'fields': 'id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count,username',
            'limit': limit
        }

        api_logger.info(f"Načítám Instagram tagy (limit: {limit})...")
        data = self._make_request(url, params)

        if data and 'data' in data:
            tags = data['data']
            api_logger.info(f"Nalezeno {len(tags)} Instagram tagů")
            return tags

        return []

    def search_instagram_hashtag(self, hashtag: str, limit: int = 50) -> List[Dict]:
        """
        Vyhledá příspěvky s daným hashtagemNOTE: Tato metoda vyžaduje Business Discovery API access

        Args:
            hashtag: Hashtag bez # (např. "amitydrinks")
            limit: Maximální počet příspěvků

        Returns:
            Seznam příspěvků s daným hashtagem
        """
        # Nejdřív musíme získat hashtag ID
        url = f"{self.base_url}/ig_hashtag_search"
        params = {
            'user_id': self.ig_account_id,
            'q': hashtag
        }

        api_logger.info(f"Vyhledávám hashtag #{hashtag}...")
        data = self._make_request(url, params)

        if not data or 'data' not in data or len(data['data']) == 0:
            api_logger.warning(f"Hashtag #{hashtag} nenalezen")
            return []

        hashtag_id = data['data'][0]['id']

        # Teď získáme top media pro tento hashtag
        url = f"{self.base_url}/{hashtag_id}/top_media"
        params = {
            'user_id': self.ig_account_id,
            'fields': 'id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count,username',
            'limit': limit
        }

        media_data = self._make_request(url, params)

        if media_data and 'data' in media_data:
            posts = media_data['data']
            api_logger.info(f"Nalezeno {len(posts)} příspěvků s #{hashtag}")
            return posts

        return []

    def get_business_account_tagged_media(self) -> List[Dict]:
        """
        Alternativní metoda - získá media ze business accountu
        a vyhledá v nich zmínky o influencerech

        Returns:
            Seznam media příspěvků
        """
        api_logger.info("Načítám media z business accountu...")
        return self.get_instagram_media(limit=50)

    def get_instagram_stories(self) -> List[Dict]:
        """
        Získá aktivní Instagram stories

        Note: Stories jsou dostupné pouze 24 hodin
        """
        url = f"{self.base_url}/{self.ig_account_id}/stories"
        params = {
            'fields': 'id,caption,media_type,media_url,timestamp,owner,username'
        }

        api_logger.info("Načítám Instagram stories...")
        data = self._make_request(url, params)

        if data and 'data' in data:
            stories = data['data']
            api_logger.info(f"Nalezeno {len(stories)} aktivních stories")
            return stories

        return []

    def get_story_details_with_tags(self, story_id: str) -> Optional[Dict]:
        """
        Získá detailní informace o story včetně tagged users

        Args:
            story_id: ID story

        Returns:
            Story data s tagged users (pokud dostupné)
        """
        url = f"{self.base_url}/{story_id}"
        params = {
            'fields': 'id,caption,media_type,timestamp,owner,username',
            'access_token': self.access_token
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                api_logger.warning(f"Story details error: {response.text}")
        except Exception as e:
            api_logger.error(f"Story details exception: {str(e)}")

        return None

    def get_instagram_insights(self, media_id: str) -> Optional[Dict]:
        """
        Získá insights (metriky) pro konkrétní příspěvek

        Args:
            media_id: ID příspěvku

        Returns:
            Insights data nebo None
        """
        url = f"{self.base_url}/{media_id}/insights"
        params = {
            'metric': 'impressions,reach,engagement'
        }

        data = self._make_request(url, params)

        if data and 'data' in data:
            insights = {}
            for metric in data['data']:
                insights[metric['name']] = metric['values'][0]['value']
            return insights

        return None

    # ============================================
    # FACEBOOK API
    # ============================================

    def get_facebook_page_info(self) -> Optional[Dict]:
        """Získá informace o Facebook stránce"""
        url = f"{self.base_url}/{self.fb_page_id}"
        params = {
            'fields': 'name,fan_count,about,website'
        }

        api_logger.info("Načítám Facebook stránku...")
        data = self._make_request(url, params)

        if data:
            api_logger.info(f"Facebook stránka načtena: {data.get('name')}")
        return data

    def get_facebook_tagged_posts(self, limit: int = 50, since: datetime = None) -> List[Dict]:
        """
        Získá příspěvky, ve kterých byla FB stránka označena

        Args:
            limit: Maximální počet příspěvků
            since: Načíst pouze příspěvky novější než toto datum

        Returns:
            Seznam tagovaných příspěvků
        """
        url = f"{self.base_url}/{self.fb_page_id}/tagged"
        params = {
            'fields': 'id,message,created_time,from,permalink_url,shares,likes.summary(true),comments.summary(true)',
            'limit': limit,
            'access_token': self.page_access_token  # Použití Page Access Token
        }

        if since:
            params['since'] = int(since.timestamp())

        api_logger.info(f"Načítám Facebook tagy (limit: {limit})...")

        # Pro tento endpoint nepoužíváme _make_request, protože potřebujeme Page Access Token
        try:
            response = requests.get(url, params=params, timeout=30)
            self.requests_count += 1

            if response.status_code == 200:
                data = response.json()
                if data and 'data' in data:
                    posts = data['data']
                    api_logger.info(f"Nalezeno {len(posts)} Facebook tagů")
                    return posts
            else:
                api_logger.warning(f"Facebook tagged posts error {response.status_code}: {response.text}")
        except Exception as e:
            api_logger.error(f"Facebook tagged posts exception: {str(e)}")

        return []

    def get_facebook_mentions(self, limit: int = 50) -> List[Dict]:
        """
        Získá zmínky o Facebook stránce

        Args:
            limit: Maximální počet zmínek

        Returns:
            Seznam zmínek
        """
        url = f"{self.base_url}/{self.fb_page_id}/feed"
        params = {
            'fields': 'id,message,created_time,from,permalink_url,shares,likes.summary(true),comments.summary(true)',
            'limit': limit
        }

        api_logger.info(f"Načítám Facebook feed (limit: {limit})...")
        data = self._make_request(url, params)

        if data and 'data' in data:
            posts = data['data']
            api_logger.info(f"Nalezeno {len(posts)} Facebook příspěvků")
            return posts

        return []

    # ============================================
    # UTILITY METODY
    # ============================================

    def test_connection(self) -> bool:
        """
        Otestuje připojení k API

        Returns:
            True pokud připojení funguje
        """
        api_logger.info("Testuji Meta API připojení...")

        # Test Instagram
        ig_profile = self.get_instagram_profile()
        if not ig_profile:
            api_logger.error("Instagram API test selhal")
            return False

        # Test Facebook
        fb_page = self.get_facebook_page_info()
        if not fb_page:
            api_logger.error("Facebook API test selhal")
            return False

        api_logger.info("✅ Meta API připojení OK!")
        return True

    def check_token_validity(self) -> Dict:
        """
        Zkontroluje platnost access tokenu

        Returns:
            Informace o tokenu (platnost, oprávnění, atd.)
        """
        url = f"{self.base_url}/debug_token"
        params = {
            'input_token': self.access_token,
            'access_token': f"{self.app_id}|{self.app_secret}"
        }

        api_logger.info("Kontroluji platnost tokenu...")
        data = self._make_request(url, params)

        if data and 'data' in data:
            token_data = data['data']
            if token_data.get('is_valid'):
                expires_at = token_data.get('expires_at', 0)
                if expires_at > 0:
                    expiry_date = datetime.fromtimestamp(expires_at)
                    days_left = (expiry_date - datetime.now()).days
                    api_logger.info(f"Token je platný ještě {days_left} dní (do {expiry_date.strftime('%d.%m.%Y')})")
                else:
                    api_logger.info("Token nemá expiraci (long-lived)")
                return token_data
            else:
                api_logger.error("Token není platný!")

        return {}
