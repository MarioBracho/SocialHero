#!/usr/bin/env python3
"""
AMITY DRINKS - Influencer Monitor
Hlavní vstupní bod aplikace
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

# Přidání src do path
sys.path.append(str(Path(__file__).parent))

from src.monitoring.monitor import InfluencerMonitor
from src.monitoring.scheduler import MonitorScheduler
from src.database.db_manager import DatabaseManager
from src.utils.influencer_loader import InfluencerLoader
from src.utils.config import Config
from src.utils.logger import main_logger
from src.api.meta_api import MetaAPIClient
from src.reporting.excel_report import ExcelReporter
from src.notifications.email_notifier import EmailNotifier

def test_connection():
    """Otestuje API připojení"""
    print("🔧 Testuji Meta API připojení...")
    print("-" * 60)

    api = MetaAPIClient()

    # Test připojení
    if api.test_connection():
        print("✅ API připojení funguje!")

        # Kontrola tokenu
        token_info = api.check_token_validity()

        print()
        print("📋 Informace:")
        print(f"   Instagram: @{Config.INSTAGRAM_USERNAME}")
        print(f"   Instagram ID: {Config.INSTAGRAM_BUSINESS_ACCOUNT_ID}")
        print(f"   Facebook Page ID: {Config.FACEBOOK_PAGE_ID}")
        print()
        return True
    else:
        print("❌ API připojení selhalo!")
        print()
        print("💡 Zkontrolujte:")
        print("   1. .env soubor obsahuje správné údaje")
        print("   2. Access token není expirovaný")
        print("   3. Instagram je propojený s Facebook stránkou")
        return False

def sync_influencers():
    """Synchronizuje influencery z Excel do databáze"""
    print("📊 Synchronizuji influencery z Excel...")
    print("-" * 60)

    loader = InfluencerLoader()
    db = DatabaseManager()

    loader.sync_to_database(db)

    # Výpis influencerů
    db.connect()
    influencers = db.get_all_influencers()
    db.close()

    print()
    print(f"✅ Celkem influencerů v databázi: {len(influencers)}")
    print()

    if influencers:
        print("👥 Aktivní influenceři:")
        for inf in influencers:
            ig = f"@{inf['instagram_handle']}" if inf.get('instagram_handle') else "-"
            print(f"   • {inf['jmeno']:20} | IG: {ig:20} | Stories: {inf['stories_mesic']}, Posty: {inf['prispevky_mesic']}")

    print()

def run_monitoring_check(hours: int = 12):
    """Spustí monitoring check"""
    print(f"🔍 Spouštím monitoring check (posledních {hours} hodin)...")
    print("=" * 60)

    monitor = InfluencerMonitor()
    results = monitor.run_check(since_hours=hours)

    print()
    print("📊 VÝSLEDKY:")
    print("-" * 60)
    print(f"✅ Úspěch: {'Ano' if results['success'] else 'Ne'}")
    print(f"📱 Instagram příspěvků: {len(results['instagram_posts'])}")
    print(f"👍 Facebook příspěvků: {len(results['facebook_posts'])}")
    print(f"📈 Celkem nových: {results['total_posts']}")

    if results['instagram_posts']:
        print()
        print("📸 Instagram příspěvky:")
        for post in results['instagram_posts']:
            print(f"   • {post['post_type']:10} | {post['caption'][:50] if post.get('caption') else 'Bez popisku'}")

    if results['facebook_posts']:
        print()
        print("👍 Facebook příspěvky:")
        for post in results['facebook_posts']:
            print(f"   • {post['caption'][:50] if post.get('caption') else 'Bez popisku'}")

    if results['errors']:
        print()
        print("⚠️  Chyby:")
        for error in results['errors']:
            print(f"   • {error}")

    print()
    print("=" * 60)

def show_stats():
    """Zobrazí aktuální statistiky"""
    print("📊 Statistiky influencerů")
    print("=" * 60)

    db = DatabaseManager()
    db.connect()

    now = datetime.now()
    stats = db.get_monthly_stats(now.year, now.month)

    if not stats:
        print("⚠️  Zatím žádná data pro tento měsíc")
        db.close()
        return

    print(f"\n📅 Měsíc: {now.month}/{now.year}\n")

    for stat in stats:
        jmeno = stat['jmeno']
        target_stories = stat['stories_mesic']
        target_posts = stat['prispevky_mesic']
        target_reels = stat['reels_mesic']

        actual_stories = stat['stories_count']
        actual_posts = stat['posts_count']
        actual_reels = stat['reels_count']

        print(f"👤 {jmeno}")
        print(f"   Stories: {actual_stories}/{target_stories}")
        print(f"   Posty:   {actual_posts}/{target_posts}")
        print(f"   Reels:   {actual_reels}/{target_reels}")
        print(f"   Status:  {'✅ Splněno' if stat['target_met'] else '⚠️  Nesplněno'}")
        print()

    db.close()

def generate_report(year: int = None, month: int = None):
    """Generuje měsíční Excel report"""
    print("📊 Generuji měsíční Excel report...")
    print("-" * 60)

    reporter = ExcelReporter()
    report_path = reporter.generate_monthly_report(year, month)

    print()
    print(f"✅ Report vygenerován: {report_path}")
    print()

def start_scheduler():
    """Spustí automatický scheduler"""
    print("⏰ Spouštím automatický scheduler...")
    print("-" * 60)
    print()

    scheduler = MonitorScheduler()
    scheduler.run()

def main():
    """Hlavní funkce"""
    parser = argparse.ArgumentParser(description='Amity Drinks Influencer Monitor')

    parser.add_argument('--mode',
                       choices=['test', 'sync', 'check', 'stats', 'report', 'auto'],
                       default='check',
                       help='Režim: test=test API, sync=sync, check=monitoring, stats=statistiky, report=Excel report, auto=automatický scheduler')

    parser.add_argument('--hours', type=int, default=12,
                       help='Kolik hodin zpět kontrolovat (výchozí: 12)')

    parser.add_argument('--year', type=int, default=None,
                       help='Rok pro report (výchozí: aktuální)')

    parser.add_argument('--month', type=int, default=None,
                       help='Měsíc pro report (výchozí: aktuální)')

    args = parser.parse_args()

    print()
    print("=" * 60)
    print(" " * 15 + "🍹 AMITY DRINKS")
    print(" " * 10 + "Influencer Monitor v1.0")
    print("=" * 60)
    print()

    # Validace konfigurace
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ Chyba konfigurace:\n{e}")
        print()
        print("💡 Spusťte nejdřív: python auto_setup_api.py")
        sys.exit(1)

    # Spuštění podle režimu
    if args.mode == 'test':
        if not test_connection():
            sys.exit(1)

    elif args.mode == 'sync':
        sync_influencers()

    elif args.mode == 'check':
        # Nejdřív sync influencerů
        sync_influencers()
        print()

        # Pak monitoring
        run_monitoring_check(args.hours)

    elif args.mode == 'stats':
        show_stats()

    elif args.mode == 'report':
        generate_report(args.year, args.month)

    elif args.mode == 'auto':
        # Automatický scheduler - běží nepřetržitě
        start_scheduler()
        return  # Neukončuje se

    print()
    print("✅ Hotovo!")
    print()

if __name__ == "__main__":
    main()
