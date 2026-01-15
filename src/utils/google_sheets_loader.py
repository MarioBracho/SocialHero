"""
Načítání influencerů z Google Sheets
"""
import json
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config import Config
from src.utils.logger import main_logger
import pandas as pd


class GoogleSheetsLoader:
    """Načítá influencery z Google Sheets"""

    def __init__(self):
        self.sheet_id = Config.GOOGLE_SHEETS_SHEET_ID
        self.worksheet_name = Config.GOOGLE_SHEETS_WORKSHEET_NAME
        self.client = None
        self.sheet = None
        self.worksheet = None

    def _connect(self):
        """Připojení k Google Sheets pomocí service account"""
        if not Config.GOOGLE_SHEETS_ENABLED:
            raise Exception("Google Sheets integration is disabled")

        if not self.sheet_id:
            raise Exception("GOOGLE_SHEETS_SHEET_ID is not configured")

        # Scopes pro Google Sheets API
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]

        try:
            # Try environment variable first (Railway)
            if Config.GOOGLE_SHEETS_CREDENTIALS_JSON:
                main_logger.info("Using Google Sheets credentials from environment variable")
                creds_dict = json.loads(Config.GOOGLE_SHEETS_CREDENTIALS_JSON)
                credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
            # Fallback to file (local development)
            elif Config.SERVICE_ACCOUNT_FILE.exists():
                main_logger.info(f"Using Google Sheets credentials from file: {Config.SERVICE_ACCOUNT_FILE}")
                credentials = Credentials.from_service_account_file(
                    str(Config.SERVICE_ACCOUNT_FILE),
                    scopes=scopes
                )
            else:
                raise Exception(
                    "No Google Sheets credentials found. "
                    "Set GOOGLE_SHEETS_CREDENTIALS_JSON environment variable or "
                    f"place service_account.json in {Config.SERVICE_ACCOUNT_FILE}"
                )

            # Create gspread client
            self.client = gspread.authorize(credentials)
            main_logger.info("✅ Google Sheets client authorized")

            # Open spreadsheet
            self.sheet = self.client.open_by_key(self.sheet_id)
            main_logger.info(f"✅ Google Sheet opened: {self.sheet.title}")

            # Get worksheet - try exact match first, then case-insensitive
            try:
                self.worksheet = self.sheet.worksheet(self.worksheet_name)
                main_logger.info(f"✅ Worksheet accessed: {self.worksheet_name}")
            except gspread.exceptions.WorksheetNotFound:
                # Try case-insensitive match
                available = self.sheet.worksheets()
                worksheet_lower = self.worksheet_name.lower()
                for ws in available:
                    if ws.title.lower() == worksheet_lower:
                        self.worksheet = ws
                        main_logger.info(f"✅ Worksheet accessed (case-insensitive match): {ws.title}")
                        break
                else:
                    raise gspread.exceptions.WorksheetNotFound(
                        f"Worksheet '{self.worksheet_name}' not found. Available: {[ws.title for ws in available]}"
                    )

        except gspread.exceptions.SpreadsheetNotFound:
            raise Exception(
                f"Google Sheet not found (ID: {self.sheet_id}). "
                "Make sure the sheet exists and is shared with the service account email."
            )
        except gspread.exceptions.WorksheetNotFound as e:
            raise Exception(str(e))
        except json.JSONDecodeError:
            raise Exception(
                "Invalid JSON in GOOGLE_SHEETS_CREDENTIALS_JSON. "
                "Make sure you copied the entire JSON file content."
            )
        except Exception as e:
            raise Exception(f"Google Sheets connection failed: {str(e)}")

    def load_influencers(self) -> List[Dict]:
        """
        Načte influencery z Google Sheets

        Returns:
            Seznam influencerů jako slovníky
        """
        try:
            # Connect to Google Sheets
            self._connect()

            # Get all values from worksheet
            all_values = self.worksheet.get_all_values()

            if not all_values or len(all_values) < 2:
                main_logger.warning("Google Sheet is empty or has only header row")
                return []

            # First row is header
            headers = all_values[0]
            rows = all_values[1:]

            main_logger.info(f"Načítám influencery z Google Sheets (worksheet: {self.worksheet_name})")
            main_logger.info(f"Headers: {headers}")

            # Create DataFrame for easier parsing
            df = pd.DataFrame(rows, columns=headers)

            # Create case-insensitive column mapping
            col_map = {col.lower().strip(): col for col in df.columns}

            # Helper function to get column value with flexible matching
            def get_col(row, *possible_names):
                """Get column value trying multiple possible column names (case-insensitive)"""
                for name in possible_names:
                    name_lower = name.lower().strip()
                    if name_lower in col_map:
                        actual_col = col_map[name_lower]
                        val = row.get(actual_col)
                        if val is not None and val != '':
                            return val
                return ''

            influencers = []

            for idx, row in df.iterrows():
                # Skip empty rows
                jmeno = get_col(row, 'Jméno', 'jmeno', 'Name')
                if not jmeno or jmeno == '':
                    continue

                # Parse date
                datum = get_col(row, 'Datum začátku', 'datum zacatku', 'datum začátku', 'Date')
                if datum and datum != '':
                    datum = str(datum).strip()
                else:
                    datum = None

                influencer = {
                    'jmeno': str(jmeno).strip(),
                    'instagram_handle': self._clean_handle(get_col(row, 'Instagram', 'IG')),
                    'facebook_handle': str(get_col(row, 'Facebook', 'FB')).strip(),
                    'tiktok_handle': self._clean_handle(get_col(row, 'TikTok', 'Tik Tok', 'TT')),
                    'stories_mesic': self._parse_number(get_col(row, 'Stories/měsíc', 'stories/mesic', 'Stories', 'stories')),
                    'prispevky_mesic': self._parse_number(get_col(row, 'Posty/měsíc', 'posty/mesic', 'Posty', 'posty', 'Posts')),
                    'reels_mesic': self._parse_number(get_col(row, 'Reels/měsíc', 'reels/mesic', 'Reels', 'reels')),
                    'email': str(get_col(row, 'Email', 'E-mail')).strip(),
                    'datum_zacatku': datum,
                    'poznamky': str(get_col(row, 'Poznámky', 'poznamky', 'Notes')).strip(),
                    'aktivni': str(get_col(row, 'Status', 'status', 'Stav', 'stav') or 'Aktivní').strip().lower().replace('*', '') == 'aktivní'
                }

                influencers.append(influencer)

            main_logger.info(f"✅ Načteno {len(influencers)} influencerů z Google Sheets")
            return influencers

        except Exception as e:
            main_logger.error(f"Chyba při načítání z Google Sheets: {str(e)}")
            return []

    def _clean_handle(self, handle: str) -> str:
        """Vyčistí Instagram/TikTok handle (odstraní @, whitespace)"""
        if not handle or handle == '':
            return ''

        handle = str(handle).strip()

        # Remove @ from beginning
        if handle.startswith('@'):
            handle = handle[1:]

        return handle.lower()

    def _parse_number(self, value) -> int:
        """Parsuje číslo z hodnoty (ignoruje non-numeric znaky jako *)"""
        if not value or value == '':
            return 0

        # If already a number
        if isinstance(value, (int, float)):
            return int(value)

        # If string, remove non-numeric characters
        value_str = str(value).strip()

        # Remove everything except digits
        numeric_only = ''.join(c for c in value_str if c.isdigit())

        if numeric_only:
            return int(numeric_only)

        return 0

    def sync_to_database(self, db_manager):
        """
        Synchronizuje influencery z Google Sheets do databáze

        Args:
            db_manager: Instance DatabaseManager

        Returns:
            Dict with statistics {'added': int, 'updated': int}
        """
        influencers = self.load_influencers()

        if not influencers:
            main_logger.warning("Žádní influenceři k synchronizaci z Google Sheets")
            return {'added': 0, 'updated': 0}

        db_manager.connect()

        # Get existing influencers from DB
        existing = {inf['instagram_handle']: inf for inf in db_manager.get_all_influencers(active_only=False)}

        added = 0
        updated = 0

        for inf in influencers:
            ig_handle = inf.get('instagram_handle')

            if not ig_handle:
                continue

            if ig_handle in existing:
                # Update existing
                db_inf = existing[ig_handle]
                db_manager.update_influencer(db_inf['id'], inf)
                updated += 1
            else:
                # Add new
                db_manager.add_influencer(inf)
                added += 1

        db_manager.close()

        main_logger.info(f"✅ Google Sheets sync completed: {added} added, {updated} updated")
        return {'added': added, 'updated': updated}
