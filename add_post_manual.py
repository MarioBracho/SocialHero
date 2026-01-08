#!/usr/bin/env python3
"""
Manuální přidání příspěvku do databáze
Použij když API nemůže detekovat tag
"""
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.database.db_manager import DatabaseManager

def add_manual_post():
    """Manuálně přidá příspěvek"""
    db = DatabaseManager()
    db.connect()

    print("="*60)
    print("📝 MANUÁLNÍ PŘIDÁNÍ PŘÍSPĚVKU")
    print("="*60)
    print()

    # Zobrazení influencerů
    influencers = db.get_all_influencers()
    print("👥 Dostupní influenceři:")
    for inf in influencers:
        print(f"   {inf['id']}. {inf['jmeno']} (@{inf['instagram_handle']})")
    print()

    # Vstup od uživatele
    influencer_id = int(input("ID influencera: "))
    platform = input("Platforma (instagram/facebook/tiktok): ").lower()
    post_type = input("Typ (story/post/reel): ").lower()
    caption = input("Caption (text příspěvku): ")
    post_url = input("URL příspěvku (volitelné): ")

    # Datum a čas
    date_str = input("Datum (YYYY-MM-DD, Enter=dnes): ").strip()
    if not date_str:
        timestamp = datetime.now()
    else:
        timestamp = datetime.strptime(date_str, "%Y-%m-%d")

    # Metriky (volitelné)
    likes = input("Likes (Enter=0): ").strip()
    likes = int(likes) if likes else 0

    comments = input("Comments (Enter=0): ").strip()
    comments = int(comments) if comments else 0

    reach = input("Reach (Enter=0): ").strip()
    reach = int(reach) if reach else 0

    # Příprava dat
    post_data = {
        'influencer_id': influencer_id,
        'platform': platform,
        'post_type': post_type,
        'post_id': f'manual_{int(timestamp.timestamp())}',
        'post_url': post_url if post_url else '',
        'caption': caption,
        'timestamp': timestamp,
        'likes': likes,
        'comments': comments,
        'shares': 0,
        'reach': reach,
        'impressions': 0,
        'engagement_rate': 0
    }

    # Uložení
    post_id = db.add_post(post_data)

    if post_id:
        print()
        print("✅ Příspěvek úspěšně přidán!")
        print(f"   ID: {post_id}")

        # Aktualizace statistik
        db.update_monthly_stats(influencer_id, timestamp.year, timestamp.month)
        print("✅ Statistiky aktualizovány")
    else:
        print("⚠️  Příspěvek už možná existuje")

    db.close()
    print()
    print("="*60)

if __name__ == "__main__":
    try:
        add_manual_post()
    except KeyboardInterrupt:
        print("\n\n⚠️  Zrušeno")
    except Exception as e:
        print(f"\n❌ Chyba: {e}")
