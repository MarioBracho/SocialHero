"""
Konfigurace aplikace - načítání z .env souboru nebo Streamlit secrets
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Načtení .env souboru
load_dotenv()

# Helper funkce pro načítání config hodnot
def get_config_value(key, default=None):
    """Načte hodnotu ze Streamlit secrets nebo .env nebo použije default"""
    # Pokusit se načíst ze streamlit secrets (pro web deployment)
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except:
        pass

    # Fallback na environment variables (.env)
    return os.getenv(key, default)

class Config:
    """Centrální konfigurace aplikace"""

    # Meta API - s fallback hodnotami pro demo režim
    META_APP_ID = get_config_value('META_APP_ID')
    META_APP_SECRET = get_config_value('META_APP_SECRET')
    META_ACCESS_TOKEN = get_config_value('META_ACCESS_TOKEN')
    META_BUSINESS_ID = get_config_value('META_BUSINESS_ID')
    FACEBOOK_PAGE_ACCESS_TOKEN = get_config_value('FACEBOOK_PAGE_ACCESS_TOKEN')
    INSTAGRAM_BUSINESS_ACCOUNT_ID = get_config_value('INSTAGRAM_BUSINESS_ACCOUNT_ID')
    INSTAGRAM_USERNAME = get_config_value('INSTAGRAM_USERNAME', 'amitydrinks.cz')
    FACEBOOK_PAGE_ID = get_config_value('FACEBOOK_PAGE_ID')
    API_VERSION = get_config_value('API_VERSION', 'v18.0')

    # Email
    EMAIL_ENABLED = get_config_value('EMAIL_ENABLED', 'true').lower() == 'true'
    EMAIL_FROM = get_config_value('EMAIL_FROM', 'amity.monitor@gmail.com')
    EMAIL_TO = get_config_value('EMAIL_TO', 'marian@amitydrinks.cz')
    EMAIL_PASSWORD = get_config_value('EMAIL_PASSWORD', '')
    SMTP_SERVER = get_config_value('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(get_config_value('SMTP_PORT', '587'))

    # Monitoring
    CHECK_INTERVAL_HOURS = int(get_config_value('CHECK_INTERVAL_HOURS', '12'))
    FIRST_CHECK_TIME = get_config_value('FIRST_CHECK_TIME', '09:00')
    SECOND_CHECK_TIME = get_config_value('SECOND_CHECK_TIME', '17:00')
    AUTO_REFRESH_SECONDS = int(get_config_value('AUTO_REFRESH_SECONDS', '60'))
    FILE_WATCH_INTERVAL_SECONDS = int(get_config_value('FILE_WATCH_INTERVAL_SECONDS', '60'))

    # Dashboard
    DASHBOARD_PORT = int(get_config_value('DASHBOARD_PORT', '8501'))
    DASHBOARD_THEME = get_config_value('DASHBOARD_THEME', 'light')

    # Notifikace
    DESKTOP_NOTIFICATIONS = get_config_value('DESKTOP_NOTIFICATIONS', 'true').lower() == 'true'
    SLACK_ENABLED = get_config_value('SLACK_ENABLED', 'false').lower() == 'true'
    SLACK_WEBHOOK_URL = get_config_value('SLACK_WEBHOOK_URL', '')

    # Pokročilé
    DEBUG = get_config_value('DEBUG', 'false').lower() == 'true'
    LOG_LEVEL = get_config_value('LOG_LEVEL', 'INFO')

    # Cesty
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / 'data'
    REPORTS_DIR = BASE_DIR / 'reports'
    LOGS_DIR = BASE_DIR / 'logs'
    CONFIG_DIR = BASE_DIR / 'config'

    # Influencer Master file
    INFLUENCERS_FILE = BASE_DIR / 'Influencer boss' / 'influencers_master.xlsx'

    # Google Sheets Configuration
    GOOGLE_SHEETS_ENABLED = get_config_value('GOOGLE_SHEETS_ENABLED', 'true').lower() == 'true'
    GOOGLE_SHEETS_SHEET_ID = get_config_value('GOOGLE_SHEETS_SHEET_ID', '')
    GOOGLE_SHEETS_CREDENTIALS_JSON = get_config_value('GOOGLE_SHEETS_CREDENTIALS_JSON', '')
    GOOGLE_SHEETS_WORKSHEET_NAME = get_config_value('GOOGLE_SHEETS_WORKSHEET_NAME', 'Aktivní influenceři')
    SERVICE_ACCOUNT_FILE = CONFIG_DIR / 'service_account.json'

    # Databáze
    DATABASE_PATH = DATA_DIR / 'influencer_monitor.db'

    @classmethod
    def validate(cls, strict=False):
        """
        Ověří, že všechny potřebné konfigurace jsou nastaveny

        Args:
            strict (bool): Pokud True, vyhodí chybu. Pokud False, pouze varuje.
        """
        errors = []

        if not cls.META_APP_ID:
            errors.append("META_APP_ID není nastaveno")
        if not cls.META_APP_SECRET:
            errors.append("META_APP_SECRET není nastaveno")
        if not cls.META_ACCESS_TOKEN:
            errors.append("META_ACCESS_TOKEN není nastaveno")
        if not cls.INSTAGRAM_BUSINESS_ACCOUNT_ID:
            errors.append("INSTAGRAM_BUSINESS_ACCOUNT_ID není nastaveno")
        if not cls.FACEBOOK_PAGE_ID:
            errors.append("FACEBOOK_PAGE_ID není nastaveno")

        if errors:
            error_msg = f"Chybí konfigurace:\n" + "\n".join(f"  - {e}" for e in errors)
            if strict:
                raise ValueError(error_msg)
            else:
                print(f"⚠️  Varování: {error_msg}")
                print("ℹ️  Dashboard bude fungovat v omezeném režimu bez Meta API.")
                return False

        return True

    @classmethod
    def create_directories(cls):
        """Vytvoří potřebné adresáře, pokud neexistují"""
        for dir_path in [cls.DATA_DIR, cls.REPORTS_DIR, cls.LOGS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Vytvoření podadresářů pro reporty
        (cls.REPORTS_DIR / 'monthly').mkdir(exist_ok=True)
        (cls.REPORTS_DIR / 'weekly').mkdir(exist_ok=True)
        (cls.REPORTS_DIR / 'custom').mkdir(exist_ok=True)

# Validace a vytvoření adresářů při importu
if __name__ != "__main__":
    try:
        Config.validate(strict=False)  # Non-strict mode - pouze varuje, nevyhazuje chybu
        Config.create_directories()
    except Exception as e:
        print(f"⚠️  Varování při inicializaci Config: {e}")
