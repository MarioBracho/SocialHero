"""
SQLite Database Manager pro Amity Influencer Monitor
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config import Config
from src.utils.logger import db_logger

class DatabaseManager:
    """Správce SQLite databáze"""

    def __init__(self, db_path: Path = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.connection = None
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        """Vytvoří databázi a tabulky, pokud neexistují"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connect()
        self._create_tables()
        self.close()

    def connect(self):
        """Připojení k databázi"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def close(self):
        """Uzavření připojení"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def _create_tables(self):
        """Vytvoření všech tabulek"""
        cursor = self.connection.cursor()

        # Tabulka influencerů
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
                aktivni BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabulka příspěvků
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
                detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (influencer_id) REFERENCES influencers(id),
                UNIQUE(platform, post_id)
            )
        ''')

        # Tabulka monitoring logu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monitoring_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                platform TEXT,
                message TEXT,
                details TEXT
            )
        ''')

        # Tabulka notifikací
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notification_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                type TEXT,
                recipient TEXT,
                subject TEXT,
                message TEXT,
                status TEXT
            )
        ''')

        # Tabulka měsíčních statistik
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                influencer_id INTEGER NOT NULL,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                stories_count INTEGER DEFAULT 0,
                posts_count INTEGER DEFAULT 0,
                reels_count INTEGER DEFAULT 0,
                total_likes INTEGER DEFAULT 0,
                total_comments INTEGER DEFAULT 0,
                total_reach INTEGER DEFAULT 0,
                avg_engagement_rate REAL DEFAULT 0,
                target_met BOOLEAN DEFAULT 0,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (influencer_id) REFERENCES influencers(id),
                UNIQUE(influencer_id, year, month)
            )
        ''')

        self.connection.commit()
        db_logger.info("Databázové tabulky vytvořeny/ověřeny")

    # ============================================
    # INFLUENCEŘI - CRUD operace
    # ============================================

    def add_influencer(self, data: Dict) -> int:
        """Přidá nového influencera"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO influencers (
                jmeno, instagram_handle, facebook_handle, tiktok_handle,
                stories_mesic, prispevky_mesic, reels_mesic,
                email, datum_zacatku, poznamky, aktivni
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('jmeno'),
            data.get('instagram_handle'),
            data.get('facebook_handle'),
            data.get('tiktok_handle'),
            data.get('stories_mesic', 0),
            data.get('prispevky_mesic', 0),
            data.get('reels_mesic', 0),
            data.get('email'),
            data.get('datum_zacatku'),
            data.get('poznamky'),
            data.get('aktivni', True)
        ))
        self.connection.commit()
        db_logger.info(f"Influencer přidán: {data.get('jmeno')}")
        return cursor.lastrowid

    def get_all_influencers(self, active_only: bool = True) -> List[Dict]:
        """Získá všechny influencery"""
        cursor = self.connection.cursor()
        query = 'SELECT * FROM influencers'
        if active_only:
            query += ' WHERE aktivni = 1'
        query += ' ORDER BY jmeno'

        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def get_influencer_by_id(self, influencer_id: int) -> Optional[Dict]:
        """Získá influencera podle ID"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM influencers WHERE id = ?', (influencer_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_influencer(self, influencer_id: int, data: Dict):
        """Aktualizuje influencera"""
        fields = []
        values = []

        for key, value in data.items():
            if key != 'id':
                fields.append(f"{key} = ?")
                values.append(value)

        if fields:
            fields.append("updated_at = CURRENT_TIMESTAMP")
            values.append(influencer_id)

            query = f"UPDATE influencers SET {', '.join(fields)} WHERE id = ?"
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            db_logger.info(f"Influencer aktualizován: ID {influencer_id}")

    # ============================================
    # PŘÍSPĚVKY
    # ============================================

    def add_post(self, data: Dict) -> Optional[int]:
        """Přidá nový příspěvek (pokud už neexistuje)"""
        cursor = self.connection.cursor()

        # Kontrola, zda už příspěvek existuje
        cursor.execute('''
            SELECT id FROM posts
            WHERE platform = ? AND post_id = ?
        ''', (data['platform'], data['post_id']))

        if cursor.fetchone():
            db_logger.debug(f"Příspěvek už existuje: {data['post_id']}")
            return None

        cursor.execute('''
            INSERT INTO posts (
                influencer_id, platform, post_type, post_id, post_url,
                caption, timestamp, likes, comments, shares, reach,
                impressions, engagement_rate
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['influencer_id'],
            data['platform'],
            data['post_type'],
            data['post_id'],
            data.get('post_url'),
            data.get('caption'),
            data['timestamp'],
            data.get('likes', 0),
            data.get('comments', 0),
            data.get('shares', 0),
            data.get('reach', 0),
            data.get('impressions', 0),
            data.get('engagement_rate', 0)
        ))
        self.connection.commit()
        db_logger.info(f"Nový příspěvek přidán: {data['platform']} - {data['post_type']}")
        return cursor.lastrowid

    def get_posts_by_influencer(self, influencer_id: int, limit: int = None) -> List[Dict]:
        """Získá příspěvky influencera"""
        cursor = self.connection.cursor()
        query = '''
            SELECT * FROM posts
            WHERE influencer_id = ?
            ORDER BY timestamp DESC
        '''
        if limit:
            query += f' LIMIT {limit}'

        cursor.execute(query, (influencer_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_posts_by_month(self, year: int, month: int) -> List[Dict]:
        """Získá všechny příspěvky za daný měsíc"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT p.*, i.jmeno as influencer_name
            FROM posts p
            JOIN influencers i ON p.influencer_id = i.id
            WHERE strftime('%Y', p.timestamp) = ?
            AND strftime('%m', p.timestamp) = ?
            ORDER BY p.timestamp DESC
        ''', (str(year), f"{month:02d}"))
        return [dict(row) for row in cursor.fetchall()]

    # ============================================
    # MĚSÍČNÍ STATISTIKY
    # ============================================

    def update_monthly_stats(self, influencer_id: int, year: int, month: int):
        """Aktualizuje měsíční statistiky pro influencera"""
        cursor = self.connection.cursor()

        # Získání cílů influencera
        cursor.execute('''
            SELECT stories_mesic, prispevky_mesic, reels_mesic
            FROM influencers WHERE id = ?
        ''', (influencer_id,))
        targets = cursor.fetchone()

        if not targets:
            return

        # Spočítání skutečných hodnot
        cursor.execute('''
            SELECT
                SUM(CASE WHEN post_type = 'story' THEN 1 ELSE 0 END) as stories,
                SUM(CASE WHEN post_type = 'post' OR post_type = 'image' THEN 1 ELSE 0 END) as posts,
                SUM(CASE WHEN post_type = 'reel' OR post_type = 'video' THEN 1 ELSE 0 END) as reels,
                SUM(likes) as total_likes,
                SUM(comments) as total_comments,
                SUM(reach) as total_reach,
                AVG(engagement_rate) as avg_engagement
            FROM posts
            WHERE influencer_id = ?
            AND strftime('%Y', timestamp) = ?
            AND strftime('%m', timestamp) = ?
        ''', (influencer_id, str(year), f"{month:02d}"))

        stats = cursor.fetchone()

        stories_count = stats['stories'] or 0
        posts_count = stats['posts'] or 0
        reels_count = stats['reels'] or 0

        # Kontrola splnění cílů
        target_met = (
            stories_count >= targets['stories_mesic'] and
            posts_count >= targets['prispevky_mesic'] and
            reels_count >= targets['reels_mesic']
        )

        # Upsert statistik
        cursor.execute('''
            INSERT INTO monthly_stats (
                influencer_id, year, month, stories_count, posts_count, reels_count,
                total_likes, total_comments, total_reach, avg_engagement_rate, target_met
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(influencer_id, year, month) DO UPDATE SET
                stories_count = excluded.stories_count,
                posts_count = excluded.posts_count,
                reels_count = excluded.reels_count,
                total_likes = excluded.total_likes,
                total_comments = excluded.total_comments,
                total_reach = excluded.total_reach,
                avg_engagement_rate = excluded.avg_engagement_rate,
                target_met = excluded.target_met,
                updated_at = CURRENT_TIMESTAMP
        ''', (
            influencer_id, year, month,
            stories_count, posts_count, reels_count,
            stats['total_likes'] or 0,
            stats['total_comments'] or 0,
            stats['total_reach'] or 0,
            stats['avg_engagement'] or 0,
            target_met
        ))
        self.connection.commit()
        db_logger.info(f"Měsíční statistiky aktualizovány: influencer {influencer_id}, {year}-{month:02d}")

    def get_monthly_stats(self, year: int, month: int) -> List[Dict]:
        """Získá měsíční statistiky všech influencerů"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT ms.*, i.jmeno, i.stories_mesic, i.prispevky_mesic, i.reels_mesic
            FROM monthly_stats ms
            JOIN influencers i ON ms.influencer_id = i.id
            WHERE ms.year = ? AND ms.month = ?
        ''', (year, month))
        return [dict(row) for row in cursor.fetchall()]

    # ============================================
    # LOGGING
    # ============================================

    def log_monitoring(self, status: str, platform: str, message: str, details: str = None):
        """Zaloguje monitoring aktivitu"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO monitoring_log (status, platform, message, details)
            VALUES (?, ?, ?, ?)
        ''', (status, platform, message, details))
        self.connection.commit()

    def log_notification(self, type: str, recipient: str, subject: str,
                        message: str, status: str):
        """Zaloguje odeslanou notifikaci"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO notification_history (type, recipient, subject, message, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (type, recipient, subject, message, status))
        self.connection.commit()

    def __enter__(self):
        """Context manager support"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager support"""
        self.close()
