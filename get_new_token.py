#!/usr/bin/env python3
"""
AMITY DRINKS - Helper pro získání nového Meta API tokenu
========================================================

Tento skript vám pomůže získat nový access token s potřebnými oprávněními.
"""

import sys
import webbrowser

# Barvy pro terminál
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def print_step(number, text):
    print(f"{Colors.BOLD}\n📌 KROK {number}: {text}{Colors.END}\n")

def main():
    print_header("AMITY DRINKS - Získání nového Access Tokenu")

    print_warning("Váš současný access token vypršel!")
    print()
    print_info("Musíme vygenerovat nový token s potřebnými oprávněními.")
    print()

    # Načtení App ID z .env
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('META_APP_ID='):
                    app_id = line.split('=')[1].strip()
                    break
    except:
        print_error("Nepodařilo se načíst APP_ID z .env souboru")
        app_id = input("Zadejte Meta App ID: ").strip()

    print_step(1, "Přejděte do Meta Graph API Exploreru")
    print_info(f"App ID: {Colors.BOLD}{app_id}{Colors.END}")
    print()

    # URL pro Graph API Explorer
    explorer_url = f"https://developers.facebook.com/tools/explorer/"

    print(f"🌐 URL: {Colors.BOLD}{explorer_url}{Colors.END}")
    print()

    choice = input("Otevřít URL v prohlížeči? (y/n): ").strip().lower()
    if choice == 'y':
        webbrowser.open(explorer_url)

    print_step(2, "V Graph API Exploreru:")
    print(f"   1. Nahoře vpravo klikněte na {Colors.BOLD}'Meta App'{Colors.END}")
    print(f"   2. Vyberte vaši aplikaci (App ID: {app_id})")
    print(f"   3. Klikněte na {Colors.BOLD}'Generate Access Token'{Colors.END}")
    print()

    print_step(3, "Vyberte TATO oprávnění:")
    required_permissions = [
        "instagram_basic",
        "instagram_manage_comments",
        "instagram_manage_insights",
        "pages_show_list",
        "pages_read_engagement",
        "business_management"
    ]

    for perm in required_permissions:
        print(f"   ✓ {Colors.GREEN}{perm}{Colors.END}")
    print()

    print_step(4, "Po vygenerování tokenu:")
    print(f"   1. Zkopírujte {Colors.BOLD}'User Token'{Colors.END}")
    print(f"   2. Token vypadá jako dlouhý řetězec začínající 'EAAc...'")
    print(f"   3. Vložte ho do příkazu níže")
    print()

    print("="*70)
    print()

    token = input(f"{Colors.BOLD}Vložte nový Access Token zde:{Colors.END}\n").strip()

    if not token:
        print_error("Token nemůže být prázdný!")
        sys.exit(1)

    if not token.startswith('EAAc'):
        print_warning("Token by měl začínat 'EAAc' - zkontrolujte, že jste zkopírovali správný token")
        choice = input("Pokračovat i přesto? (y/n): ").strip().lower()
        if choice != 'y':
            sys.exit(1)

    # Prodloužení tokenu na 60 dní
    print()
    print_step(5, "Prodlužuji token na 60 dní...")

    import requests

    try:
        with open('.env', 'r') as f:
            env_content = f.read()
            for line in env_content.split('\n'):
                if line.startswith('META_APP_SECRET='):
                    app_secret = line.split('=')[1].strip()
                    break
    except:
        print_error("Nepodařilo se načíst APP_SECRET z .env")
        sys.exit(1)

    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': token
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if 'access_token' in data:
            long_lived_token = data['access_token']
            expires_in = data.get('expires_in', 0)
            days = expires_in // 86400

            print_success(f"Token prodloužen na {days} dní!")

            # Aktualizace .env souboru
            print()
            print_step(6, "Aktualizuji .env soubor...")

            env_lines = []
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('META_ACCESS_TOKEN='):
                        env_lines.append(f'META_ACCESS_TOKEN={long_lived_token}\n')
                    else:
                        env_lines.append(line)

            with open('.env', 'w') as f:
                f.writelines(env_lines)

            print_success(".env soubor aktualizován!")

            # Test připojení
            print()
            print_step(7, "Testuji nové připojení...")

            import subprocess
            result = subprocess.run(
                ['./venv/bin/python3', 'main.py', '--mode', 'test'],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print_success("API připojení funguje!")
                print()
                print("="*70)
                print()
                print(f"{Colors.GREEN}{Colors.BOLD}✅ HOTOVO! Token je připraven k použití.{Colors.END}")
                print()
                print_info("Nyní můžete spustit monitoring:")
                print(f"   {Colors.BOLD}python main.py --mode check{Colors.END}")
                print()
            else:
                print_error("API test selhal - zkontrolujte oprávnění")
                print()
                print("Výstup:")
                print(result.stdout)
                print(result.stderr)
        else:
            print_error("Chyba při prodlužování tokenu")
            print(f"Odpověď: {data}")

    except Exception as e:
        print_error(f"Chyba: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
