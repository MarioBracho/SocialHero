#!/usr/bin/env python3
"""
Test Meta API Connection
Otestuje připojení k Meta API a ověří platnost tokenu
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.api.meta_api import MetaAPIClient
from datetime import datetime

def main():
    print("=" * 60)
    print("AMITY DRINKS - Meta API Connection Test")
    print("=" * 60)
    print()

    # Inicializace klienta
    client = MetaAPIClient()

    print(f"📱 Instagram Business Account ID: {client.ig_account_id}")
    print(f"📘 Facebook Page ID: {client.fb_page_id}")
    print(f"🔑 App ID: {client.app_id}")
    print(f"🌐 API Version: {client.api_version}")
    print()

    # 1. Kontrola platnosti tokenu
    print("=" * 60)
    print("1️⃣  KONTROLA PLATNOSTI TOKENU")
    print("=" * 60)

    token_info = client.check_token_validity()

    if token_info and token_info.get('is_valid'):
        print("✅ Token je platný!")

        expires_at = token_info.get('expires_at', 0)
        if expires_at > 0:
            expiry_date = datetime.fromtimestamp(expires_at)
            days_left = (expiry_date - datetime.now()).days
            print(f"📅 Vyprší: {expiry_date.strftime('%d.%m.%Y %H:%M')}")
            print(f"⏰ Zbývá: {days_left} dní")

            if days_left < 10:
                print(f"⚠️  VAROVÁNÍ: Token vyprší za méně než 10 dní!")
                print("   Doporučuji získat nový long-lived token.")
        else:
            print("✅ Token nemá expiraci (long-lived token)")

        print(f"\n📋 Oprávnění (scopes):")
        scopes = token_info.get('scopes', [])
        for scope in scopes:
            print(f"   - {scope}")

    else:
        print("❌ Token NENÍ platný!")
        print("   Musíš získat nový access token.")
        return False

    print()

    # 2. Test Instagram API
    print("=" * 60)
    print("2️⃣  TEST INSTAGRAM API")
    print("=" * 60)

    ig_profile = client.get_instagram_profile()

    if ig_profile:
        print(f"✅ Instagram profil načten")
        print(f"   👤 Username: @{ig_profile.get('username')}")
        print(f"   📸 Počet příspěvků: {ig_profile.get('media_count', 'N/A')}")
        print(f"   👥 Followers: {ig_profile.get('followers_count', 'N/A')}")
    else:
        print("❌ Nepodařilo se načíst Instagram profil")
        return False

    print()

    # 3. Test načtení Instagram media
    print("=" * 60)
    print("3️⃣  TEST INSTAGRAM MEDIA")
    print("=" * 60)

    media = client.get_instagram_media(limit=5)

    if media:
        print(f"✅ Načteno {len(media)} příspěvků")
        for i, post in enumerate(media[:3], 1):
            caption = post.get('caption', 'Bez popisku')[:50]
            media_type = post.get('media_type', 'N/A')
            timestamp = post.get('timestamp', 'N/A')[:10]
            print(f"\n   {i}. {media_type} - {timestamp}")
            print(f"      {caption}...")
    else:
        print("⚠️  Žádné příspěvky nenalezeny")

    print()

    # 4. Test Instagram tagged media (důležité pro monitoring!)
    print("=" * 60)
    print("4️⃣  TEST INSTAGRAM TAGGED MEDIA")
    print("=" * 60)
    print("   (Příspěvky kde je @amitydrinks.cz označen)")

    try:
        tagged = client.get_instagram_tags(limit=10)

        if tagged:
            print(f"✅ Nalezeno {len(tagged)} označených příspěvků")
            for i, post in enumerate(tagged[:3], 1):
                caption = post.get('caption', 'Bez popisku')[:50]
                username = post.get('username', 'N/A')
                print(f"\n   {i}. Od: {username}")
                print(f"      {caption}...")
        else:
            print("ℹ️  Žádné označené příspěvky (nebo nemáš oprávnění)")
            print("   To je v pořádku - můžeme použít jiné metody")
    except Exception as e:
        print(f"⚠️  Endpoint /tags není dostupný: {str(e)}")
        print("   Použijeme alternativní metody pro detekci")

    print()

    # 5. Test Facebook API
    print("=" * 60)
    print("5️⃣  TEST FACEBOOK API")
    print("=" * 60)

    fb_page = client.get_facebook_page_info()

    if fb_page:
        print(f"✅ Facebook stránka načtena")
        print(f"   📘 Název: {fb_page.get('name')}")
        print(f"   👥 Fans: {fb_page.get('fan_count', 'N/A')}")
    else:
        print("❌ Nepodařilo se načíst Facebook stránku")

    print()

    # 6. Test Facebook tagged posts
    print("=" * 60)
    print("6️⃣  TEST FACEBOOK TAGGED POSTS")
    print("=" * 60)

    fb_tagged = client.get_facebook_tagged_posts(limit=5)

    if fb_tagged:
        print(f"✅ Nalezeno {len(fb_tagged)} označených příspěvků")
        for i, post in enumerate(fb_tagged[:3], 1):
            message = post.get('message', 'Bez textu')[:50]
            from_name = post.get('from', {}).get('name', 'N/A')
            print(f"\n   {i}. Od: {from_name}")
            print(f"      {message}...")
    else:
        print("ℹ️  Žádné označené příspěvky na Facebooku")

    print()
    print("=" * 60)
    print("✅ TEST DOKONČEN!")
    print("=" * 60)
    print()
    print("📊 SHRNUTÍ:")
    print("   - Token platnost: ✅")
    print(f"   - Instagram API: {'✅' if ig_profile else '❌'}")
    print(f"   - Facebook API: {'✅' if fb_page else '❌'}")
    print(f"   - Instagram media: {'✅' if media else '❌'}")
    print(f"   - Facebook tagged: {'✅' if fb_tagged else 'ℹ️'}")
    print()

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test přerušen uživatelem")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Chyba během testu: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
