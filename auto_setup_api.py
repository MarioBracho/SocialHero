#!/usr/bin/env python3
"""
AMITY DRINKS - Automatický Meta API Setup Script
================================================

Tento script automaticky dokončí setup Meta API:
1. Prodlouží short-lived token na 60 dní (long-lived token)
2. Získá Instagram Business Account ID
3. Získá Facebook Page ID
4. Vytvoří finální .env soubor
5. Otestuje připojení
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# Barvy pro terminál
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def get_user_input():
    """Získá potřebné údaje od uživatele"""
    print_header("KROK 1: Zadejte Meta API údaje")
    
    print_info("Tyto údaje jste získali v Meta Developer Console:")
    print()
    
    app_id = input(f"{Colors.BOLD}App ID:{Colors.END} ").strip()
    if not app_id:
        print_error("App ID je povinné!")
        sys.exit(1)
    
    app_secret = input(f"{Colors.BOLD}App Secret:{Colors.END} ").strip()
    if not app_secret:
        print_error("App Secret je povinné!")
        sys.exit(1)
    
    short_token = input(f"{Colors.BOLD}Short-Lived Access Token:{Colors.END} ").strip()
    if not short_token:
        print_error("Access Token je povinný!")
        sys.exit(1)
    
    return app_id, app_secret, short_token

def exchange_token(app_id, app_secret, short_token):
    """Vymění short-lived token za long-lived token (60 dní)"""
    print_header("KROK 2: Prodlužuji Access Token na 60 dní")
    
    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_token
    }
    
    try:
        print_info("Posílám request na Meta API...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if 'access_token' in data:
            long_token = data['access_token']
            expires_in = data.get('expires_in', 5184000)  # ~60 dní
            
            expiry_date = datetime.now() + timedelta(seconds=expires_in)
            
            print_success(f"Token úspěšně prodloužen!")
            print_info(f"Platnost: {expires_in // 86400} dní (do {expiry_date.strftime('%d.%m.%Y')})")
            
            return long_token
        else:
            print_error("Nepodařilo se získat long-lived token")
            print(f"Odpověď API: {json.dumps(data, indent=2)}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print_error(f"Chyba při komunikaci s API: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Odpověď serveru: {e.response.text}")
        sys.exit(1)

def get_pages(access_token):
    """Získá seznam Facebook stránek"""
    print_header("KROK 3: Získávám Facebook stránky")
    
    url = "https://graph.facebook.com/v18.0/me/accounts"
    params = {
        'access_token': access_token,
        'fields': 'id,name,access_token'
    }
    
    try:
        print_info("Načítám vaše Facebook stránky...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            pages = data['data']
            print_success(f"Nalezeno {len(pages)} stránek:")
            print()
            
            for i, page in enumerate(pages, 1):
                print(f"  {i}. {Colors.BOLD}{page['name']}{Colors.END}")
                print(f"     ID: {page['id']}")
                print()
            
            return pages
        else:
            print_warning("Nebyly nalezeny žádné Facebook stránky")
            print_info("Zkontrolujte, že máte administrátorská práva ke stránce Amity Drinks")
            return []
            
    except requests.exceptions.RequestException as e:
        print_error(f"Chyba při získávání stránek: {str(e)}")
        return []

def select_page(pages):
    """Umožní uživateli vybrat správnou stránku"""
    if not pages:
        return None, None
    
    if len(pages) == 1:
        page = pages[0]
        print_info(f"Automaticky vybírám jedinou dostupnou stránku: {page['name']}")
        return page['id'], page.get('access_token')
    
    print(f"{Colors.BOLD}Vyberte Amity Drinks stránku:{Colors.END}")
    
    while True:
        try:
            choice = input(f"Zadejte číslo stránky (1-{len(pages)}): ").strip()
            index = int(choice) - 1
            
            if 0 <= index < len(pages):
                page = pages[index]
                print_success(f"Vybrána stránka: {page['name']}")
                return page['id'], page.get('access_token')
            else:
                print_error(f"Zadejte číslo mezi 1 a {len(pages)}")
        except ValueError:
            print_error("Zadejte platné číslo")

def get_instagram_account(page_id, access_token):
    """Získá Instagram Business Account ID pro danou stránku"""
    print_header("KROK 4: Získávám Instagram Business Account")
    
    url = f"https://graph.facebook.com/v18.0/{page_id}"
    params = {
        'fields': 'instagram_business_account',
        'access_token': access_token
    }
    
    try:
        print_info(f"Hledám propojený Instagram účet...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if 'instagram_business_account' in data:
            ig_account_id = data['instagram_business_account']['id']
            print_success(f"Instagram Business Account nalezen!")
            print_info(f"Instagram Account ID: {ig_account_id}")
            
            # Získání detailů Instagram účtu
            ig_url = f"https://graph.facebook.com/v18.0/{ig_account_id}"
            ig_params = {
                'fields': 'username,name,followers_count,profile_picture_url',
                'access_token': access_token
            }
            
            ig_response = requests.get(ig_url, params=ig_params)
            if ig_response.ok:
                ig_data = ig_response.json()
                print_success(f"Username: @{ig_data.get('username', 'N/A')}")
                print_info(f"Název: {ig_data.get('name', 'N/A')}")
                print_info(f"Sledující: {ig_data.get('followers_count', 'N/A'):,}")
            
            return ig_account_id
        else:
            print_error("Instagram účet není propojen s touto Facebook stránkou!")
            print_warning("Řešení:")
            print("  1. Jděte na Facebook stránku Amity Drinks")
            print("  2. Nastavení → Instagram")
            print("  3. Připojte Instagram Business účet")
            print("  4. Spusťte tento script znovu")
            return None
            
    except requests.exceptions.RequestException as e:
        print_error(f"Chyba při získávání Instagram účtu: {str(e)}")
        return None

def test_api_access(ig_account_id, access_token):
    """Otestuje, že máme správná oprávnění"""
    print_header("KROK 5: Testování API přístupu")
    
    tests = [
        {
            'name': 'Instagram Basic Info',
            'url': f'https://graph.facebook.com/v18.0/{ig_account_id}',
            'params': {'fields': 'username,name', 'access_token': access_token}
        },
        {
            'name': 'Instagram Media',
            'url': f'https://graph.facebook.com/v18.0/{ig_account_id}/media',
            'params': {'fields': 'id,caption,timestamp', 'limit': 1, 'access_token': access_token}
        },
        {
            'name': 'Instagram Tags',
            'url': f'https://graph.facebook.com/v18.0/{ig_account_id}/tags',
            'params': {'fields': 'id,caption', 'limit': 1, 'access_token': access_token}
        }
    ]
    
    all_passed = True
    
    for test in tests:
        try:
            response = requests.get(test['url'], params=test['params'], timeout=10)
            if response.ok:
                print_success(f"{test['name']}: OK")
            else:
                print_warning(f"{test['name']}: Částečně funkční (kód {response.status_code})")
                all_passed = False
        except Exception as e:
            print_error(f"{test['name']}: Selhalo - {str(e)}")
            all_passed = False
    
    return all_passed

def create_env_file(app_id, app_secret, long_token, page_id, ig_account_id, ig_username):
    """Vytvoří finální .env soubor"""
    print_header("KROK 6: Vytváření .env souboru")
    
    env_content = f"""# ============================================
# META (FACEBOOK + INSTAGRAM) API CREDENTIALS
# ============================================
# Vygenerováno automaticky: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

META_APP_ID={app_id}
META_APP_SECRET={app_secret}
META_ACCESS_TOKEN={long_token}
INSTAGRAM_BUSINESS_ACCOUNT_ID={ig_account_id}
INSTAGRAM_USERNAME={ig_username}
FACEBOOK_PAGE_ID={page_id}


# ============================================
# EMAIL NOTIFICATIONS
# ============================================

EMAIL_ENABLED=true
EMAIL_FROM=amity.monitor@gmail.com
EMAIL_TO=marketing@amitydrinks.cz
EMAIL_PASSWORD=your_gmail_app_password_here

# Gmail SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587


# ============================================
# MONITORING SETTINGS
# ============================================

# Časování kontrol
CHECK_INTERVAL_HOURS=12
FIRST_CHECK_TIME=09:00
SECOND_CHECK_TIME=17:00

# Auto-refresh intervaly
AUTO_REFRESH_SECONDS=60
FILE_WATCH_INTERVAL_SECONDS=60


# ============================================
# DASHBOARD SETTINGS
# ============================================

DASHBOARD_PORT=8501
DASHBOARD_THEME=light


# ============================================
# NOTIFICATIONS
# ============================================

# Desktop notifikace
DESKTOP_NOTIFICATIONS=true

# Slack (volitelné)
SLACK_ENABLED=false
SLACK_WEBHOOK_URL=


# ============================================
# ADVANCED
# ============================================

DEBUG=false
LOG_LEVEL=INFO
API_VERSION=v18.0
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print_success(".env soubor úspěšně vytvořen!")
        print_info("Umístění: ./.env")
        print()
        print_warning("DŮLEŽITÉ:")
        print("  • Doplňte EMAIL_PASSWORD pro email notifikace")
        print("  • Nikdy nesdílejte .env soubor!")
        print("  • Přidejte .env do .gitignore")
        
        return True
    except Exception as e:
        print_error(f"Chyba při vytváření .env souboru: {str(e)}")
        return False

def print_summary(app_id, ig_account_id, ig_username, token_expiry_days):
    """Vypíše shrnutí setupu"""
    print_header("✅ SETUP DOKONČEN!")
    
    print(f"{Colors.BOLD}Shrnutí:{Colors.END}")
    print()
    print(f"  📱 App ID: {app_id}")
    print(f"  🔑 Access Token: Platný {token_expiry_days} dní")
    print(f"  📸 Instagram: @{ig_username}")
    print(f"  🆔 Instagram ID: {ig_account_id}")
    print()
    print(f"{Colors.GREEN}{Colors.BOLD}Co teď?{Colors.END}")
    print()
    print("  1. Zkontrolujte .env soubor")
    print("  2. Doplňte EMAIL_PASSWORD (volitelné)")
    print("  3. Spusťte aplikaci:")
    print()
    print(f"     {Colors.BLUE}python main.py --mode check{Colors.END}")
    print(f"     {Colors.BLUE}streamlit run dashboard.py{Colors.END}")
    print()
    print(f"{Colors.YELLOW}Připomínka:{Colors.END}")
    print(f"  Token vyprší za ~{token_expiry_days} dní")
    print(f"  Pro automatickou obnovu spusťte: {Colors.BLUE}python scripts/refresh_token.py{Colors.END}")
    print()

def main():
    """Hlavní funkce"""
    print()
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'AMITY DRINKS - AUTO SETUP META API':^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.END}")
    print()
    print_info("Tento script automaticky dokončí Meta API setup")
    print()
    
    # Krok 1: Získání údajů od uživatele
    app_id, app_secret, short_token = get_user_input()
    
    # Krok 2: Prodloužení tokenu
    long_token = exchange_token(app_id, app_secret, short_token)
    
    # Krok 3: Získání Facebook stránek
    pages = get_pages(long_token)
    
    # Krok 4: Výběr správné stránky
    page_id, page_token = select_page(pages)
    
    if not page_id:
        print_error("Nelze pokračovat bez Facebook stránky")
        sys.exit(1)
    
    # Použijeme page token pokud existuje, jinak long token
    working_token = page_token if page_token else long_token
    
    # Krok 5: Získání Instagram účtu
    ig_account_id = get_instagram_account(page_id, working_token)
    
    if not ig_account_id:
        print_error("Nelze pokračovat bez Instagram Business účtu")
        sys.exit(1)
    
    # Získání Instagram username
    ig_url = f"https://graph.facebook.com/v18.0/{ig_account_id}"
    ig_params = {
        'fields': 'username',
        'access_token': working_token
    }
    ig_response = requests.get(ig_url, params=ig_params)
    ig_username = ig_response.json().get('username', 'amitydrinks') if ig_response.ok else 'amitydrinks'
    
    # Krok 6: Test API přístupu
    test_api_access(ig_account_id, working_token)
    
    # Krok 7: Vytvoření .env souboru
    create_env_file(app_id, app_secret, long_token, page_id, ig_account_id, ig_username)
    
    # Krok 8: Závěrečné shrnutí
    print_summary(app_id, ig_account_id, ig_username, 60)
    
    print()
    print(f"{Colors.GREEN}{Colors.BOLD}🎉 Hotovo! Můžete začít používat aplikaci.{Colors.END}")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_warning("Setup přerušen uživatelem")
        sys.exit(0)
    except Exception as e:
        print()
        print_error(f"Neočekávaná chyba: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
