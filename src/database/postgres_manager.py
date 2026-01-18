"""
Universal Database Manager - podporuje SQLite i PostgreSQL
"""
import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config import Config

# PostgreSQL support
try:
    import psycopg2
    import psycopg2.extras
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

class UniversalDatabaseManager:
    """Database Manager - automaticky používá PostgreSQL (Railway) nebo SQLite (local)"""

    def __init__(self):
        # Detekce prostředí
        self.database_url = os.getenv('DATABASE_URL')
        self.is_postgres = bool(self.database_url and POSTGRES_AVAILABLE)

        if not self.is_postgres:
            # SQLite (lokální development)
            self.db_path = Config.DATABASE_PATH

        self.connection = None

        # Try to initialize database with fallback to SQLite on error
        try:
            self._ensure_database_exists()
        except Exception as e:
            if self.is_postgres:
                # PostgreSQL failed, fallback to SQLite
                print(f"WARNING: PostgreSQL connection failed ({str(e)}), falling back to SQLite")
                self.is_postgres = False
                self.db_path = Config.DATABASE_PATH
                self.database_url = None
                self._ensure_database_exists()
            else:
                raise

    def _ensure_database_exists(self):
        """Vytvoří databázi a tabulky, pokud neexistují"""
        if not self.is_postgres:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connect()
        self._create_tables()
        self.close()

    def connect(self):
        """Připojení k databázi"""
        if self.connection is None:
            if self.is_postgres:
                # PostgreSQL with timeout
                self.connection = psycopg2.connect(
                    self.database_url,
                    cursor_factory=psycopg2.extras.RealDictCursor,
                    connect_timeout=10  # 10 second timeout
                )
            else:
                # SQLite
                self.connection = sqlite3.connect(str(self.db_path))
                self.connection.row_factory = sqlite3.Row
        elif self.is_postgres and self.connection:
            # Reset connection if in error state
            try:
                self.connection.rollback()
            except:
                pass
        return self.connection

    def rollback(self):
        """Rollback current transaction"""
        if self.connection:
            try:
                self.connection.rollback()
            except:
                pass

    def close(self):
        """Uzavření připojení"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def _create_tables(self):
        """Vytvoření všech tabulek"""
        cursor = self.connection.cursor()

        if self.is_postgres:
            # PostgreSQL syntax
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS influencers (
                    id SERIAL PRIMARY KEY,
                    jmeno TEXT NOT NULL,
                    instagram_handle TEXT,
                    facebook_handle TEXT,
                    tiktok_handle TEXT,
                    stories_mesic INTEGER DEFAULT 0,
                    prispevky_mesic INTEGER DEFAULT 0,
                    reels_mesic INTEGER DEFAULT 0,
                    email TEXT,
                    datum_zacatku DATE,
                    poznamky TEXT,
                    aktivni TEXT DEFAULT 'ano',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id SERIAL PRIMARY KEY,
                    influencer_id INTEGER NOT NULL,
                    platform TEXT NOT NULL,
                    post_type TEXT NOT NULL,
                    post_id TEXT NOT NULL,
                    post_url TEXT,
                    caption TEXT,
                    timestamp TIMESTAMP NOT NULL,
                    likes INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    shares INTEGER DEFAULT 0,
                    reach INTEGER DEFAULT 0,
                    impressions INTEGER DEFAULT 0,
                    engagement_rate REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    creator_username TEXT,
                    creator_id INTEGER,
                    detection_method TEXT,
                    FOREIGN KEY (influencer_id) REFERENCES influencers (id),
                    FOREIGN KEY (creator_id) REFERENCES influencers (id),
                    UNIQUE (post_id, platform)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS monthly_stats (
                    id SERIAL PRIMARY KEY,
                    influencer_id INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    stories_count INTEGER DEFAULT 0,
                    posts_count INTEGER DEFAULT 0,
                    reels_count INTEGER DEFAULT 0,
                    total_reach INTEGER DEFAULT 0,
                    total_engagement INTEGER DEFAULT 0,
                    target_met BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (influencer_id) REFERENCES influencers (id),
                    UNIQUE (influencer_id, year, month)
                )
            ''')
        else:
            # SQLite syntax (původní)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS influencers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jmeno TEXT NOT NULL,
                    instagram_handle TEXT,
                    facebook_handle TEXT,
                    tiktok_handle TEXT,
                    stories_mesic INTEGER DEFAULT 0,
                    prispevky_mesic INTEGER DEFAULT 0,
                    reels_mesic INTEGER DEFAULT 0,
                    email TEXT,
                    datum_zacatku DATE,
                    poznamky TEXT,
                    aktivni TEXT DEFAULT 'ano',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    influencer_id INTEGER NOT NULL,
                    platform TEXT NOT NULL,
                    post_type TEXT NOT NULL,
                    post_id TEXT NOT NULL,
                    post_url TEXT,
                    caption TEXT,
                    timestamp DATETIME NOT NULL,
                    likes INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    shares INTEGER DEFAULT 0,
                    reach INTEGER DEFAULT 0,
                    impressions INTEGER DEFAULT 0,
                    engagement_rate REAL DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    creator_username TEXT,
                    creator_id INTEGER,
                    detection_method TEXT,
                    FOREIGN KEY (influencer_id) REFERENCES influencers (id),
                    FOREIGN KEY (creator_id) REFERENCES influencers (id),
                    UNIQUE (post_id, platform)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS monthly_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    influencer_id INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    stories_count INTEGER DEFAULT 0,
                    posts_count INTEGER DEFAULT 0,
                    reels_count INTEGER DEFAULT 0,
                    total_reach INTEGER DEFAULT 0,
                    total_engagement INTEGER DEFAULT 0,
                    target_met BOOLEAN DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (influencer_id) REFERENCES influencers (id),
                    UNIQUE (influencer_id, year, month)
                )
            ''')

        self.connection.commit()

    # === Metody pro influencery ===

    def add_influencer(self, data: Dict) -> int:
        """Přidá nového influencera"""
        cursor = self.connection.cursor()

        if self.is_postgres:
            cursor.execute('''
                INSERT INTO influencers (
                    jmeno, instagram_handle, facebook_handle, tiktok_handle,
                    stories_mesic, prispevky_mesic, reels_mesic,
                    email, datum_zacatku, poznamky, aktivni
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                data['jmeno'], data.get('instagram_handle', ''),
                data.get('facebook_handle', ''), data.get('tiktok_handle', ''),
                data.get('stories_mesic', 0), data.get('prispevky_mesic', 0),
                data.get('reels_mesic', 0), data.get('email', ''),
                data.get('datum_zacatku'), data.get('poznamky', ''),
                data.get('aktivni', 'ano')
            ))
            influencer_id = cursor.fetchone()['id']
        else:
            cursor.execute('''
                INSERT INTO influencers (
                    jmeno, instagram_handle, facebook_handle, tiktok_handle,
                    stories_mesic, prispevky_mesic, reels_mesic,
                    email, datum_zacatku, poznamky, aktivni
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['jmeno'], data.get('instagram_handle', ''),
                data.get('facebook_handle', ''), data.get('tiktok_handle', ''),
                data.get('stories_mesic', 0), data.get('prispevky_mesic', 0),
                data.get('reels_mesic', 0), data.get('email', ''),
                data.get('datum_zacatku'), data.get('poznamky', ''),
                data.get('aktivni', 'ano')
            ))
            influencer_id = cursor.lastrowid

        self.connection.commit()
        return influencer_id

    def get_all_influencers(self, active_only: bool = True) -> List[Dict]:
        """Vrátí seznam všech influencerů"""
        cursor = self.connection.cursor()

        query = "SELECT * FROM influencers"
        if active_only:
            query += " WHERE aktivni = 'ano'"
        query += " ORDER BY jmeno"

        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def get_influencer_by_id(self, influencer_id: int) -> Optional[Dict]:
        """Vrátí influencera podle ID"""
        cursor = self.connection.cursor()
        placeholder = '%s' if self.is_postgres else '?'
        cursor.execute(f"SELECT * FROM influencers WHERE id = {placeholder}", (influencer_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_influencer(self, influencer_id: int, data: Dict):
        """Aktualizuje influencera"""
        cursor = self.connection.cursor()
        placeholder = '%s' if self.is_postgres else '?'

        set_parts = []
        values = []
        for key, value in data.items():
            set_parts.append(f"{key} = {placeholder}")
            values.append(value)

        values.append(influencer_id)

        query = f"UPDATE influencers SET {', '.join(set_parts)} WHERE id = {placeholder}"
        cursor.execute(query, values)
        self.connection.commit()

    # === Metody pro příspěvky ===

    def add_post(self, data: Dict) -> Optional[int]:
        """Přidá nový příspěvek"""
        cursor = self.connection.cursor()

        try:
            if self.is_postgres:
                cursor.execute('''
                    INSERT INTO posts (
                        influencer_id, platform, post_type, post_id, post_url,
                        caption, timestamp, likes, comments, shares, reach,
                        impressions, engagement_rate
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                ''', (
                    data['influencer_id'], data['platform'], data['post_type'],
                    data['post_id'], data.get('post_url', ''), data.get('caption', ''),
                    data['timestamp'], data.get('likes', 0), data.get('comments', 0),
                    data.get('shares', 0), data.get('reach', 0),
                    data.get('impressions', 0), data.get('engagement_rate', 0)
                ))
                post_id = cursor.fetchone()['id']
            else:
                cursor.execute('''
                    INSERT INTO posts (
                        influencer_id, platform, post_type, post_id, post_url,
                        caption, timestamp, likes, comments, shares, reach,
                        impressions, engagement_rate
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['influencer_id'], data['platform'], data['post_type'],
                    data['post_id'], data.get('post_url', ''), data.get('caption', ''),
                    data['timestamp'], data.get('likes', 0), data.get('comments', 0),
                    data.get('shares', 0), data.get('reach', 0),
                    data.get('impressions', 0), data.get('engagement_rate', 0)
                ))
                post_id = cursor.lastrowid

            self.connection.commit()
            return post_id
        except Exception as e:
            print(f"Error adding post: {e}")
            return None

    def add_post_with_creator(self, data: Dict) -> Optional[int]:
        """
        Přidá nový příspěvek včetně creator info (pro automatickou detekci)

        Args:
            data: Dictionary s daty o příspěvku, včetně:
                - creator_username: Instagram @handle autora
                - creator_id: ID influencera (nebo None pokud neznámý)
                - detection_method: 'webhook', 'api_tags', 'api_stories', 'caption_regex'
                ... + standardní fieldy z add_post

        Returns:
            ID nově vytvořeného příspěvku nebo None při chybě
        """
        cursor = self.connection.cursor()

        try:
            if self.is_postgres:
                cursor.execute('''
                    INSERT INTO posts (
                        influencer_id, platform, post_type, post_id, post_url,
                        caption, timestamp, likes, comments, shares, reach,
                        impressions, engagement_rate,
                        creator_username, creator_id, detection_method
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (post_id, platform) DO NOTHING
                    RETURNING id
                ''', (
                    data['influencer_id'], data['platform'], data['post_type'],
                    data['post_id'], data.get('post_url', ''), data.get('caption', ''),
                    data['timestamp'], data.get('likes', 0), data.get('comments', 0),
                    data.get('shares', 0), data.get('reach', 0),
                    data.get('impressions', 0), data.get('engagement_rate', 0),
                    data.get('creator_username'), data.get('creator_id'),
                    data.get('detection_method', 'unknown')
                ))
                result = cursor.fetchone()
                post_id = result['id'] if result else None
            else:
                cursor.execute('''
                    INSERT OR IGNORE INTO posts (
                        influencer_id, platform, post_type, post_id, post_url,
                        caption, timestamp, likes, comments, shares, reach,
                        impressions, engagement_rate,
                        creator_username, creator_id, detection_method
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['influencer_id'], data['platform'], data['post_type'],
                    data['post_id'], data.get('post_url', ''), data.get('caption', ''),
                    data['timestamp'], data.get('likes', 0), data.get('comments', 0),
                    data.get('shares', 0), data.get('reach', 0),
                    data.get('impressions', 0), data.get('engagement_rate', 0),
                    data.get('creator_username'), data.get('creator_id'),
                    data.get('detection_method', 'unknown')
                ))
                post_id = cursor.lastrowid if cursor.lastrowid > 0 else None

            self.connection.commit()
            return post_id
        except Exception as e:
            print(f"Error adding post with creator: {e}")
            return None

    def get_influencer_by_instagram_handle(self, handle: str) -> Optional[Dict]:
        """
        Najde influencera podle Instagram handle

        Args:
            handle: Instagram handle (@dustyfeet_23 nebo dustyfeet_23)

        Returns:
            Dictionary s daty o influencerovi nebo None pokud nenalezen
        """
        cursor = self.connection.cursor()
        placeholder = '%s' if self.is_postgres else '?'

        # Odstranit @ pokud je v handle a normalizovat na lowercase
        clean_handle = handle.lstrip('@').lower()

        cursor.execute(
            f"SELECT * FROM influencers WHERE LOWER(instagram_handle) = {placeholder}",
            (clean_handle,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_posts_by_month(self, year: int, month: int) -> List[Dict]:
        """Vrátí příspěvky za daný měsíc"""
        cursor = self.connection.cursor()
        placeholder = '%s' if self.is_postgres else '?'

        if self.is_postgres:
            # PostgreSQL syntax
            cursor.execute(f'''
                SELECT p.*, i.jmeno as influencer_name
                FROM posts p
                JOIN influencers i ON p.influencer_id = i.id
                WHERE EXTRACT(YEAR FROM p.timestamp::timestamp) = {placeholder}
                AND EXTRACT(MONTH FROM p.timestamp::timestamp) = {placeholder}
                ORDER BY p.timestamp DESC
            ''', (year, month))
        else:
            # SQLite syntax
            cursor.execute(f'''
                SELECT p.*, i.jmeno as influencer_name
                FROM posts p
                JOIN influencers i ON p.influencer_id = i.id
                WHERE strftime('%Y', p.timestamp) = {placeholder}
                AND strftime('%m', p.timestamp) = {placeholder}
                ORDER BY p.timestamp DESC
            ''', (str(year), f"{month:02d}"))

        return [dict(row) for row in cursor.fetchall()]

    # === Metody pro měsíční statistiky ===

    def update_monthly_stats(self, influencer_id: int, year: int, month: int):
        """Aktualizuje měsíční statistiky influencera"""
        cursor = self.connection.cursor()
        placeholder = '%s' if self.is_postgres else '?'

        # Spočítat statistiky z příspěvků
        if self.is_postgres:
            cursor.execute(f'''
                SELECT
                    COUNT(CASE WHEN post_type = 'story' THEN 1 END) as stories_count,
                    COUNT(CASE WHEN post_type = 'post' THEN 1 END) as posts_count,
                    COUNT(CASE WHEN post_type = 'reel' THEN 1 END) as reels_count,
                    COALESCE(SUM(reach), 0) as total_reach,
                    COALESCE(SUM(likes + comments), 0) as total_engagement
                FROM posts
                WHERE influencer_id = {placeholder}
                AND EXTRACT(YEAR FROM timestamp::timestamp) = {placeholder}
                AND EXTRACT(MONTH FROM timestamp::timestamp) = {placeholder}
            ''', (influencer_id, year, month))
        else:
            cursor.execute(f'''
                SELECT
                    COUNT(CASE WHEN post_type = 'story' THEN 1 END) as stories_count,
                    COUNT(CASE WHEN post_type = 'post' THEN 1 END) as posts_count,
                    COUNT(CASE WHEN post_type = 'reel' THEN 1 END) as reels_count,
                    COALESCE(SUM(reach), 0) as total_reach,
                    COALESCE(SUM(likes + comments), 0) as total_engagement
                FROM posts
                WHERE influencer_id = {placeholder}
                AND strftime('%Y', timestamp) = {placeholder}
                AND strftime('%m', timestamp) = {placeholder}
            ''', (influencer_id, str(year), f"{month:02d}"))

        stats = dict(cursor.fetchone())

        # Získat cíle influencera
        cursor.execute(f"SELECT stories_mesic, prispevky_mesic, reels_mesic FROM influencers WHERE id = {placeholder}",
                      (influencer_id,))
        targets = dict(cursor.fetchone())

        # Zkontrolovat splnění cílů
        target_met = (
            stats['stories_count'] >= targets['stories_mesic'] and
            stats['posts_count'] >= targets['prispevky_mesic'] and
            stats['reels_count'] >= targets['reels_mesic']
        )

        # Upsert statistiky
        if self.is_postgres:
            cursor.execute('''
                INSERT INTO monthly_stats (
                    influencer_id, year, month, stories_count, posts_count,
                    reels_count, total_reach, total_engagement, target_met
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (influencer_id, year, month)
                DO UPDATE SET
                    stories_count = EXCLUDED.stories_count,
                    posts_count = EXCLUDED.posts_count,
                    reels_count = EXCLUDED.reels_count,
                    total_reach = EXCLUDED.total_reach,
                    total_engagement = EXCLUDED.total_engagement,
                    target_met = EXCLUDED.target_met,
                    updated_at = CURRENT_TIMESTAMP
            ''', (influencer_id, year, month, stats['stories_count'],
                  stats['posts_count'], stats['reels_count'], stats['total_reach'],
                  stats['total_engagement'], target_met))
        else:
            cursor.execute('''
                INSERT OR REPLACE INTO monthly_stats (
                    influencer_id, year, month, stories_count, posts_count,
                    reels_count, total_reach, total_engagement, target_met
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (influencer_id, year, month, stats['stories_count'],
                  stats['posts_count'], stats['reels_count'], stats['total_reach'],
                  stats['total_engagement'], target_met))

        self.connection.commit()

    def get_monthly_stats(self, year: int, month: int) -> List[Dict]:
        """Vrátí měsíční statistiky všech influencerů"""
        cursor = self.connection.cursor()
        placeholder = '%s' if self.is_postgres else '?'

        cursor.execute(f'''
            SELECT
                i.jmeno,
                i.stories_mesic,
                i.prispevky_mesic,
                i.reels_mesic,
                COALESCE(m.stories_count, 0) as stories_count,
                COALESCE(m.posts_count, 0) as posts_count,
                COALESCE(m.reels_count, 0) as reels_count,
                COALESCE(m.total_reach, 0) as total_reach,
                COALESCE(m.total_engagement, 0) as total_engagement,
                COALESCE(m.target_met, false) as target_met
            FROM influencers i
            LEFT JOIN monthly_stats m ON i.id = m.influencer_id
                AND m.year = {placeholder} AND m.month = {placeholder}
            WHERE i.aktivni = 'ano'
            ORDER BY i.jmeno
        ''', (year, month))

        return [dict(row) for row in cursor.fetchall()]
