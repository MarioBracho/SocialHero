#!/usr/bin/env python3
"""
Získá Facebook Page Access Token
"""
import requests
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.utils.config import Config

def get_page_access_token():
    """Získá Page Access Token pro Facebook stránku"""

    print("=" * 60)
    print("Facebook Page Access Token Generator")
    print("=" * 60)
    print()

    # 1. Získání seznamu pages
    url = f"https://graph.facebook.com/v18.0/me/accounts"
    params = {
        'access_token': Config.META_ACCESS_TOKEN
    }

    print("📋 Načítám tvoje Facebook stránky...")
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"❌ Chyba: {response.text}")
        return None

    data = response.json()

    if 'data' not in data or len(data['data']) == 0:
        print("❌ Žádné Facebook stránky nenalezeny")
        print("   Ujisti se, že:")
        print("   1. Jsi admin Amity Drinks stránky")
        print("   2. Máš oprávnění 'pages_show_list'")
        return None

    # 2. Zobrazení dostupných stránek
    print(f"\n✅ Nalezeno {len(data['data'])} stránek:\n")

    for i, page in enumerate(data['data'], 1):
        page_id = page['id']
        page_name = page['name']
        page_token = page.get('access_token', 'N/A')

        print(f"{i}. {page_name}")
        print(f"   ID: {page_id}")
        print(f"   Token: {page_token[:20]}..." if page_token != 'N/A' else "   Token: N/A")

        # Pokud je to Amity Drinks stránka, ulož token
        if page_id == Config.FACEBOOK_PAGE_ID:
            print(f"   ⭐ TOTO JE AMITY DRINKS STRÁNKA!")

            print(f"\n" + "=" * 60)
            print("✅ PAGE ACCESS TOKEN NALEZEN!")
            print("=" * 60)
            print()
            print("Přidej tento token do .env souboru:")
            print()
            print(f"FACEBOOK_PAGE_ACCESS_TOKEN={page_token}")
            print()
            print("Tento token použij místo META_ACCESS_TOKEN pro Facebook API calls")
            print("=" * 60)

            return page_token

    print("\n⚠️  Amity Drinks stránka nenalezena v seznamu")
    print(f"   Hledám Page ID: {Config.FACEBOOK_PAGE_ID}")

    return None

if __name__ == "__main__":
    try:
        token = get_page_access_token()
        sys.exit(0 if token else 1)
    except Exception as e:
        print(f"\n❌ Chyba: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
