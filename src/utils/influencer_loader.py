"""
Načítání influencerů z Excel souboru
"""
import pandas as pd
from typing import List, Dict
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config import Config
from src.utils.logger import main_logger

class InfluencerLoader:
    """Načítá influencery z Excel souboru"""

    def __init__(self, excel_path: Path = None):
        self.excel_path = excel_path or Config.INFLUENCERS_FILE

    def load_influencers(self) -> List[Dict]:
        """
        Načte influencery z Excel souboru

        Returns:
            Seznam influencerů jako slovníky
        """
        if not self.excel_path.exists():
            main_logger.error(f"Excel soubor nenalezen: {self.excel_path}")
            return []

        try:
            # Načtení listu "Aktivní influenceři"
            df = pd.read_excel(self.excel_path, sheet_name='Aktivní influenceři', engine='openpyxl')

            main_logger.info(f"Načítám influencery z {self.excel_path.name}")

            influencers = []

            for idx, row in df.iterrows():
                # Přeskočení prázdných řádků
                if pd.isna(row.get('Jméno')) or row.get('Jméno') == '':
                    continue

                # Zpracování data
                datum = row.get('Datum začátku')
                if not pd.isna(datum):
                    # Pokud je to pandas Timestamp, převést na string
                    if hasattr(datum, 'strftime'):
                        datum = datum.strftime('%Y-%m-%d')
                    else:
                        datum = str(datum)
                else:
                    datum = None

                influencer = {
                    'jmeno': str(row.get('Jméno', '')).strip(),
                    'instagram_handle': self._clean_handle(row.get('Instagram', '')),
                    'facebook_handle': str(row.get('Facebook', '')).strip() if not pd.isna(row.get('Facebook')) else '',
                    'tiktok_handle': self._clean_handle(row.get('TikTok', '')),
                    'stories_mesic': self._parse_number(row.get('Stories/měsíc', 0)),
                    'prispevky_mesic': self._parse_number(row.get('Posty/měsíc', 0)),
                    'reels_mesic': self._parse_number(row.get('Reels/měsíc', 0)),
                    'email': str(row.get('Email', '')).strip() if not pd.isna(row.get('Email')) else '',
                    'datum_zacatku': datum,
                    'poznamky': str(row.get('Poznámky', '')).strip() if not pd.isna(row.get('Poznámky')) else '',
                    'aktivni': str(row.get('Status', 'Aktivní')).strip().lower().replace('*', '') == 'aktivní'
                }

                influencers.append(influencer)

            main_logger.info(f"✅ Načteno {len(influencers)} influencerů")
            return influencers

        except Exception as e:
            main_logger.error(f"Chyba při načítání Excel: {str(e)}")
            return []

    def _clean_handle(self, handle: str) -> str:
        """Vyčistí Instagram/TikTok handle (odstraní @, whitespace)"""
        if pd.isna(handle) or handle == '':
            return ''

        handle = str(handle).strip()

        # Odstranění @ z začátku
        if handle.startswith('@'):
            handle = handle[1:]

        return handle.lower()

    def _parse_number(self, value) -> int:
        """Parsuje číslo z hodnoty (ignoruje non-numeric znaky jako *)"""
        if pd.isna(value) or value == '':
            return 0

        # Pokud je to už číslo
        if isinstance(value, (int, float)):
            return int(value)

        # Pokud je to string, odstraň non-numeric znaky
        value_str = str(value).strip()

        # Odstraň všechno kromě číslic
        numeric_only = ''.join(c for c in value_str if c.isdigit())

        if numeric_only:
            return int(numeric_only)

        return 0

    def sync_to_database(self, db_manager):
        """
        Synchronizuje influencery z Excel do databáze

        Args:
            db_manager: Instance DatabaseManager
        """
        influencers = self.load_influencers()

        if not influencers:
            main_logger.warning("Žádní influenceři k synchronizaci")
            return

        db_manager.connect()

        # Získání existujících influencerů z DB
        existing = {inf['instagram_handle']: inf for inf in db_manager.get_all_influencers(active_only=False)}

        added = 0
        updated = 0

        for inf in influencers:
            ig_handle = inf.get('instagram_handle')

            if not ig_handle:
                continue

            if ig_handle in existing:
                # Aktualizace existujícího
                db_inf = existing[ig_handle]
                db_manager.update_influencer(db_inf['id'], inf)
                updated += 1
            else:
                # Přidání nového
                db_manager.add_influencer(inf)
                added += 1

        db_manager.close()

        main_logger.info(f"Sync dokončena: {added} přidáno, {updated} aktualizováno")
