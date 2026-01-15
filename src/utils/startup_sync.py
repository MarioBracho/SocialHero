"""
Startup synchronization - načte influencer data při startu aplikace
"""
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config import Config
from src.utils.logger import main_logger
from src.database.postgres_manager import UniversalDatabaseManager


def run_startup_sync():
    """
    Spustí synchronizaci dat při startu aplikace

    Fallback strategy:
    1. Try Google Sheets (primary source)
    2. If fails → Try Excel file (fallback)
    3. If fails → Use existing database (last resort)

    Returns:
        Dict with sync results:
        {
            'success': bool,
            'source': 'google_sheets' | 'excel' | 'database',
            'added': int,
            'updated': int,
            'error': str | None
        }
    """
    main_logger.info("=" * 60)
    main_logger.info("🚀 Starting application initialization...")
    main_logger.info("=" * 60)

    db = UniversalDatabaseManager()

    # Try Google Sheets first (if enabled)
    if Config.GOOGLE_SHEETS_ENABLED:
        main_logger.info("📊 Attempting Google Sheets sync...")
        try:
            import signal
            from src.utils.google_sheets_loader import GoogleSheetsLoader

            def timeout_handler(signum, frame):
                raise TimeoutError("Google Sheets sync timed out after 30 seconds")

            # Set timeout for Google Sheets sync (30 seconds)
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(30)

            try:
                sheets_loader = GoogleSheetsLoader()
                stats = sheets_loader.sync_to_database(db)
                signal.alarm(0)  # Cancel timeout

                main_logger.info("=" * 60)
                main_logger.info(f"✅ Google Sheets sync successful!")
                main_logger.info(f"   Added: {stats['added']} influencers")
                main_logger.info(f"   Updated: {stats['updated']} influencers")
                main_logger.info("=" * 60)

                return {
                    'success': True,
                    'source': 'google_sheets',
                    'added': stats['added'],
                    'updated': stats['updated'],
                    'error': None
                }
            except TimeoutError as e:
                signal.alarm(0)  # Cancel timeout
                raise e

        except Exception as e:
            main_logger.warning(f"⚠️  Google Sheets sync failed: {str(e)}")
            main_logger.info("   Falling back to Excel file...")
    else:
        main_logger.info("ℹ️  Google Sheets sync disabled (GOOGLE_SHEETS_ENABLED=false)")

    # Fallback to Excel file
    if Config.INFLUENCERS_FILE.exists():
        main_logger.info("📁 Attempting Excel file sync...")
        try:
            from src.utils.influencer_loader import InfluencerLoader

            excel_loader = InfluencerLoader()
            stats = excel_loader.sync_to_database(db)

            main_logger.info("=" * 60)
            main_logger.info(f"✅ Excel sync successful!")
            main_logger.info(f"   Added: {stats['added']} influencers")
            main_logger.info(f"   Updated: {stats['updated']} influencers")
            main_logger.info("=" * 60)

            return {
                'success': True,
                'source': 'excel',
                'added': stats.get('added', 0),
                'updated': stats.get('updated', 0),
                'error': None
            }

        except Exception as e:
            main_logger.warning(f"⚠️  Excel sync failed: {str(e)}")
            main_logger.info("   Using existing database...")
    else:
        main_logger.info(f"ℹ️  Excel file not found: {Config.INFLUENCERS_FILE}")

    # Last resort: use existing database
    try:
        db.connect()
        influencers = db.get_all_influencers(active_only=False)
        db.close()

        influencer_count = len(influencers)

        main_logger.info("=" * 60)
        main_logger.info(f"ℹ️  Using existing database")
        main_logger.info(f"   Found {influencer_count} influencers in database")
        main_logger.info("=" * 60)

        return {
            'success': True,
            'source': 'database',
            'added': 0,
            'updated': 0,
            'error': None
        }

    except Exception as e:
        error_msg = f"Database initialization failed: {str(e)}"
        main_logger.error(f"❌ {error_msg}")
        main_logger.info("=" * 60)

        return {
            'success': False,
            'source': 'none',
            'added': 0,
            'updated': 0,
            'error': error_msg
        }
