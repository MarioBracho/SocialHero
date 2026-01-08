"""
Scheduler pro automatické spouštění monitoringu
"""
import schedule
import time
from datetime import datetime
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.monitoring.monitor import InfluencerMonitor
from src.notifications.email_notifier import EmailNotifier
from src.reporting.excel_report import ExcelReporter
from src.utils.config import Config
from src.utils.logger import main_logger
from src.utils.influencer_loader import InfluencerLoader
from src.database.db_manager import DatabaseManager

class MonitorScheduler:
    """Scheduler pro pravidelný monitoring"""

    def __init__(self):
        self.monitor = InfluencerMonitor()
        self.notifier = EmailNotifier()
        self.reporter = ExcelReporter()
        self.loader = InfluencerLoader()
        self.db = DatabaseManager()

    def monitoring_job(self):
        """Úloha monitoringu - spustí se 2x denně"""
        main_logger.info("="*70)
        main_logger.info(f"AUTOMATICKÝ MONITORING - {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        main_logger.info("="*70)

        try:
            # 1. Sync influencerů z Excel
            main_logger.info("📊 Synchronizuji influencery z Excel...")
            self.loader.sync_to_database(self.db)

            # 2. Spuštění monitoringu
            results = self.monitor.run_check(since_hours=Config.CHECK_INTERVAL_HOURS)

            # 3. Odeslání notifikací pokud jsou nové příspěvky
            if results['total_posts'] > 0:
                all_posts = results['instagram_posts'] + results['facebook_posts']
                main_logger.info(f"📧 Odesílám email notifikaci o {len(all_posts)} příspěvcích...")
                self.notifier.send_new_post_notification(all_posts)

            main_logger.info("✅ Automatický monitoring dokončen")

        except Exception as e:
            main_logger.error(f"❌ Chyba během automatického monitoringu: {str(e)}")

    def daily_summary_job(self):
        """Denní souhrn - spustí se večer"""
        main_logger.info("📊 Odesílám denní souhrn...")

        try:
            self.notifier.send_daily_summary()
            main_logger.info("✅ Denní souhrn odeslán")
        except Exception as e:
            main_logger.error(f"❌ Chyba při odesílání denního souhrnu: {str(e)}")

    def monthly_report_job(self):
        """Měsíční report - spustí se 1. den v měsíci"""
        main_logger.info("📈 Generuji měsíční report...")

        try:
            # Generování reportu za minulý měsíc
            now = datetime.now()
            if now.month == 1:
                report_year = now.year - 1
                report_month = 12
            else:
                report_year = now.year
                report_month = now.month - 1

            report_path = self.reporter.generate_monthly_report(report_year, report_month)

            # Odeslání emailem
            main_logger.info("📧 Odesílám měsíční report emailem...")
            self.notifier.send_monthly_report_email(report_path)

            main_logger.info("✅ Měsíční report vygenerován a odeslán")

        except Exception as e:
            main_logger.error(f"❌ Chyba při generování měsíčního reportu: {str(e)}")

    def setup_schedule(self):
        """Nastavení rozvrhu úloh"""
        # Monitoring 2x denně
        schedule.every().day.at(Config.FIRST_CHECK_TIME).do(self.monitoring_job)
        schedule.every().day.at(Config.SECOND_CHECK_TIME).do(self.monitoring_job)

        # Denní souhrn každý den v 18:00
        schedule.every().day.at("18:00").do(self.daily_summary_job)

        # Měsíční report 1. den v měsíci v 8:00
        schedule.every().day.at("08:00").do(self._check_and_run_monthly_report)

        main_logger.info("📅 Scheduler nakonfigurován:")
        main_logger.info(f"   - Monitoring: {Config.FIRST_CHECK_TIME} a {Config.SECOND_CHECK_TIME}")
        main_logger.info(f"   - Denní souhrn: 18:00")
        main_logger.info(f"   - Měsíční report: 1. den v měsíci, 08:00")

    def _check_and_run_monthly_report(self):
        """Kontrola, zda je 1. den v měsíci a spuštění reportu"""
        if datetime.now().day == 1:
            self.monthly_report_job()

    def run(self):
        """Spustí scheduler (běží nepřetržitě)"""
        self.setup_schedule()

        main_logger.info("="*70)
        main_logger.info("🚀 SCHEDULER SPUŠTĚN")
        main_logger.info("="*70)
        main_logger.info("Čekám na naplánované úlohy...")
        main_logger.info("(Pro ukončení stiskněte Ctrl+C)")
        main_logger.info("="*70)

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Kontrola každou minutu

        except KeyboardInterrupt:
            main_logger.info("\n⚠️  Scheduler zastaven uživatelem")
            main_logger.info("="*70)

if __name__ == "__main__":
    scheduler = MonitorScheduler()
    scheduler.run()
