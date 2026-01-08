# 🔐 NÁVOD: Vytvoření Meta Business API přístupu
## Krok za krokem pro Amity Drinks Influencer Monitor

---

## 📋 CO BUDETE POTŘEBOVAT

Před začátkem si připravte:

- ✅ Facebook účet s admin právy k Amity Drinks stránce
- ✅ Instagram Business profil propojený s FB stránkou
- ✅ Email a telefon pro ověření (2FA)
- ✅ Cca 30-45 minut času
- ✅ Notebook/poznámkový blok na ukládání API klíčů

**DŮLEŽITÉ:** API klíče si bezpečně uložte! Nikdy je nesdílejte veřejně.

---

## 🎯 FÁZE 1: PŘÍPRAVA (5-10 minut)

### Krok 1.1: Ověření Facebook Business Setup

1. **Přejděte na:** https://business.facebook.com
2. **Ověřte, že máte:**
   - ✅ Business Manager účet pro Amity Drinks
   - ✅ Facebook stránku Amity Drinks
   - ✅ Administrátorská práva
3. **Pokud NEMÁTE Business Manager:**
   - Klikněte "Create Account"
   - Vyplňte: Název firmy, vaše jméno, email
   - Ověřte email

### Krok 1.2: Ověření Instagram Business propojení

1. **Otevřete Facebook stránku** Amity Drinks
2. **Jděte do Settings** (Nastavení)
3. **Najděte sekci "Instagram"**
4. **Ověřte, že je připojen Instagram Business účet**
5. **Pokud NENÍ připojen:**
   - Klikněte "Connect Account"
   - Přihlaste se k Instagram Business účtu
   - Potvrďte propojení

📝 **Poznámka:** Instagram MUSÍ být Business nebo Creator účet, ne osobní!

### Krok 1.3: Vytvoření Meta Developer účtu

1. **Přejděte na:** https://developers.facebook.com
2. **Klikněte "Get Started"** (pravý horní roh)
3. **Přihlaste se** Facebook účtem (ten s admin právy)
4. **Vyplňte registraci:**
   - Jméno: Vaše celé jméno
   - Email: Pracovní email (např. marketing@amitydrinks.cz)
   - Kategorie: "Business" nebo "Marketing"
5. **Přijměte podmínky**
6. **Ověřte email** - přijde potvrzovací link
7. **Potvrďte telefonní číslo** (SMS kód)

✅ **Checkpoint:** Měli byste být přihlášeni na developers.facebook.com

---

## 🚀 FÁZE 2: VYTVOŘENÍ APLIKACE (10-15 minut)

### Krok 2.1: Vytvoření nové aplikace

1. **Na dashboardu developers.facebook.com** klikněte:
   ```
   "My Apps" → "Create App"
   ```

2. **Vyberte typ aplikace:**
   - Zvolte: **"Business"**
   - Klikněte "Next"

3. **Vyplňte detaily:**
   ```
   Display Name:        Amity Influencer Monitor
   App Contact Email:   marketing@amitydrinks.cz
   Business Account:    [Vyberte Amity Drinks Business Manager]
   ```

4. **Klikněte "Create App"**

5. **Ověření bezpečnosti:**
   - Zadejte heslo k Facebook účtu
   - Případně 2FA kód

✅ **Checkpoint:** Měli byste vidět dashboard nové aplikace

### Krok 2.2: Získání App ID a App Secret

1. **V levém menu najděte "Settings" → "Basic"**

2. **Uvidíte:**
   ```
   App ID:      1234567890123456
   App Secret:  [Show] [Reset]
   ```

3. **ZKOPÍRUJTE App ID:**
   - Klikněte na ikonu kopírování
   - Uložte do poznámek jako: `META_APP_ID=1234567890123456`

4. **ZKOPÍRUJTE App Secret:**
   - Klikněte "Show"
   - Zadejte Facebook heslo
   - Zobrazí se: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`
   - Zkopírujte
   - Uložte jako: `META_APP_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

⚠️ **VAROVÁNÍ:** App Secret NIKDY nesdílejte! Je to jako heslo.

### Krok 2.3: Nastavení App Domain

1. **Stále v "Settings → Basic"**
2. **Najděte "App Domains"**
3. **Přidejte:**
   ```
   localhost
   ```
4. **Klikněte "Save Changes"**

### Krok 2.4: Přidání produktů

1. **V levém menu klikněte "Add Product"**

2. **Najděte "Instagram"** a klikněte **"Set Up"**

3. **Najděte "Facebook Login"** a klikněte **"Set Up"**

✅ **Checkpoint:** V levém menu byste měli vidět "Instagram" a "Facebook Login"

---

## 🔑 FÁZE 3: ZÍSKÁNÍ ACCESS TOKEN (15-20 minut)

### Krok 3.1: Otevření Graph API Explorer

1. **Přejděte na:** https://developers.facebook.com/tools/explorer

2. **Nebo v levém menu aplikace:** "Tools → Graph API Explorer"

3. **Ověřte nastavení v pravém horním rohu:**
   ```
   Meta App:    Amity Influencer Monitor
   User Token:  [Generate Token]
   ```

### Krok 3.2: Generování User Access Token

1. **Klikněte na "Generate Access Token"**

2. **Vyberte oprávnění (permissions):**

   **✅ ZAŠKRTNĚTE následující:**
   ```
   ☑ instagram_basic
   ☑ instagram_manage_insights  
   ☑ instagram_content_publish
   ☑ pages_read_engagement
   ☑ pages_show_list
   ☑ pages_read_user_content
   ☑ business_management
   ```

   **❌ NEZAŠKRTÁVEJTE:**
   - Nic co souvisí s "ads" (reklamy)
   - Nic co souvisí s "publish" (pokud nepotřebujete)

3. **Klikněte "Generate Access Token"**

4. **Přihlášení a schválení:**
   - Přihlaste se k Facebook
   - Přijměte všechna oprávnění
   - Klikněte "Continue as [Vaše jméno]"

5. **ZKOPÍRUJTE SHORT-LIVED TOKEN:**
   - Zobrazí se dlouhý text v poli "Access Token"
   - Začína: `EAAxxxxxxxxxxxxxxxxxxxxx`
   - Zkopírujte CELÝ
   - Dočasně uložte (použijeme za chvíli)

📝 **Poznámka:** Tento token vyprší za 1-2 hodiny. Potřebujeme ho prodloužit!

### Krok 3.3: Prodloužení tokenu na 60 dní (Long-Lived Token)

**METODA A: Přes Access Token Tool (Jednodušší)**

1. **Přejděte na:** https://developers.facebook.com/tools/accesstoken/

2. **Najděte váš User Token** v seznamu

3. **Klikněte "Extend Access Token"**

4. **Zkopírujte nový Long-Lived Token:**
   - Platnost: ~60 dní
   - Uložte jako: `META_ACCESS_TOKEN=EAAxxxxxx...`

**METODA B: Přes API volání (Pro pokročilé)**

```bash
# V prohlížeči otevřete tuto URL (nahraďte hodnoty):

https://graph.facebook.com/v18.0/oauth/access_token?
    grant_type=fb_exchange_token&
    client_id=YOUR_APP_ID&
    client_secret=YOUR_APP_SECRET&
    fb_exchange_token=YOUR_SHORT_LIVED_TOKEN

# Odpověď:
{
  "access_token": "EAAyour_long_lived_token_here",
  "token_type": "bearer",
  "expires_in": 5183944  // ~60 dní
}
```

✅ **Checkpoint:** Máte Long-Lived Token (60 dní platnost)

### Krok 3.4: Získání Instagram Business Account ID

1. **V Graph API Explorer** (https://developers.facebook.com/tools/explorer)

2. **Zadejte do pole dotazu:**
   ```
   me/accounts
   ```

3. **Klikněte "Submit"**

4. **V odpovědi najděte Amity Drinks stránku:**
   ```json
   {
     "data": [
       {
         "id": "123456789012345",
         "name": "Amity Drinks",
         ...
       }
     ]
   }
   ```

5. **ZKOPÍRUJTE ID** stránky (např. `123456789012345`)

6. **Nyní zadejte NOVÝ dotaz:**
   ```
   123456789012345?fields=instagram_business_account
   ```
   (Nahraďte číslem z předchozího kroku)

7. **Klikněte "Submit"**

8. **V odpovědi:**
   ```json
   {
     "instagram_business_account": {
       "id": "17841400000000000"
     },
     "id": "123456789012345"
   }
   ```

9. **ZKOPÍRUJTE Instagram Business Account ID:**
   - To je `17841400000000000`
   - Uložte jako: `INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000000`

✅ **Checkpoint:** Máte Instagram Business Account ID

### Krok 3.5: Test API přístupu

1. **V Graph API Explorer zadejte:**
   ```
   17841400000000000?fields=username,name,profile_picture_url,followers_count
   ```
   (Použijte vaše IG Business Account ID)

2. **Klikněte "Submit"**

3. **Měli byste vidět:**
   ```json
   {
     "username": "amitydrinks",
     "name": "Amity Drinks",
     "profile_picture_url": "https://...",
     "followers_count": 12543,
     "id": "17841400000000000"
   }
   ```

4. **Pokud vidíte data ✅ Funguje!**

5. **Pokud vidíte error:**
   - Zkontrolujte, že máte správná oprávnění
   - Zkontrolujte, že token není expirovaný
   - Zkontrolujte, že Instagram je správně propojený

---

## 🔧 FÁZE 4: KONFIGURACE APLIKACE (5 minut)

### Krok 4.1: Vytvoření .env souboru

1. **Otevřete projekt** `amity-influencer-monitor`

2. **Vytvořte soubor** `config/.env`

3. **Zkopírujte template:**

```env
# ============================================
# META (FACEBOOK + INSTAGRAM) API CREDENTIALS
# ============================================

# Z kroku 2.2:
META_APP_ID=1234567890123456
META_APP_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

# Z kroku 3.3 (Long-Lived Token):
META_ACCESS_TOKEN=EAAyour_60_day_long_lived_token_here_its_very_long

# Z kroku 3.4:
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000000
INSTAGRAM_USERNAME=amitydrinks

# Z kroku 3.4 (první dotaz):
FACEBOOK_PAGE_ID=123456789012345


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
```

4. **Vyplňte VŠECHNY hodnoty** které jste získali

5. **Uložte soubor**

⚠️ **DŮLEŽITÉ:** `.env` soubor obsahuje tajné údaje - NIKDY ho necommitujte do Gitu!

### Krok 4.2: Ověření .gitignore

```gitignore
# V souboru .gitignore by mělo být:

config/.env
config/influencers_master.xlsx
data/
logs/
*.pyc
__pycache__/
```

### Krok 4.3: Test připojení

1. **Otevřete terminál** v projektu

2. **Aktivujte virtual environment:**
   ```bash
   # Windows:
   venv\Scripts\activate
   
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Spusťte test script:**
   ```bash
   python scripts/test_connection.py
   ```

4. **Měli byste vidět:**
   ```
   ✅ Testing Meta API Connection...
   ✅ App ID: Valid
   ✅ App Secret: Valid
   ✅ Access Token: Valid (expires in 58 days)
   ✅ Instagram Account: @amitydrinks (12,543 followers)
   ✅ Facebook Page: Amity Drinks (5,678 likes)
   
   🎉 All connections successful!
   ```

✅ **Gratulujeme! API je plně nakonfigurováno!**

---

## 🔄 FÁZE 5: OBNOVA TOKENU (Každých 60 dní)

### Proč je potřeba obnova?

Long-Lived Token vyprší po **~60 dnech**. Musíte ho obnovit.

### Jak poznám, že token vyprší?

1. **Email notifikace** (7 dní před expirací)
2. **Dashboard warning**
3. **API error 190** (token už vypršel)

### Postup obnovy:

**METODA A: Automatická (doporučená)**

```bash
# Spusťte obnovovací script
python scripts/refresh_token.py

# Script automaticky:
# 1. Vezme aktuální token
# 2. Požádá o nový Long-Lived Token
# 3. Uloží do .env
# 4. Pošle notifikaci
```

**METODA B: Manuální**

1. Vraťte se na: https://developers.facebook.com/tools/accesstoken/
2. Najděte váš token
3. Klikněte "Extend Access Token"
4. Zkopírujte nový token
5. Aktualizujte `config/.env`

---

## ⚠️ TROUBLESHOOTING

### Problém 1: "Invalid OAuth access token"

**Příčina:** Token vypršel nebo je neplatný

**Řešení:**
```bash
1. Vygenerujte nový token (Fáze 3.2)
2. Prodlužte ho (Fáze 3.3)
3. Aktualizujte .env
4. Restartujte aplikaci
```

### Problém 2: "Permissions error"

**Příčina:** Chybí oprávnění

**Řešení:**
```bash
1. Jděte na: developers.facebook.com/tools/explorer
2. Klikněte "Get User Access Token"
3. Zaškrtněte VŠECHNA potřebná oprávnění (Fáze 3.2)
4. Vygenerujte nový token
```

### Problém 3: "Instagram account not found"

**Příčina:** Instagram není propojený s FB stránkou

**Řešení:**
```bash
1. Jděte na Facebook stránku Amity Drinks
2. Settings → Instagram
3. Connect Instagram Business Account
4. Ověřte propojení
5. Získejte nové IG Business Account ID (Fáze 3.4)
```

### Problém 4: "Rate limit exceeded"

**Příčina:** Příliš mnoho API requestů

**Řešení:**
```bash
Meta API limity:
- 200 calls/hour per user
- 4,800 calls/hour per app

Řešení:
1. Snižte frekvenci monitoringu
2. Implementujte cache
3. Použijte batch requests
```

### Problém 5: "App not in Development Mode"

**Příčina:** Aplikace je v Development režimu

**Řešení:**
```bash
1. Jděte do App Dashboard
2. Settings → Basic
3. Najděte "App Mode"
4. Přepněte na "Live" (až po testování!)

POZOR: V Live mode potřebujete Business Verification!
Pro testování: Přidejte testery v "Roles → Roles"
```

---

## 📚 UŽITEČNÉ ODKAZY

### Oficiální dokumentace:
- **Meta Graph API:** https://developers.facebook.com/docs/graph-api
- **Instagram Graph API:** https://developers.facebook.com/docs/instagram-api
- **Business API:** https://developers.facebook.com/docs/marketing-apis

### Tools:
- **Graph API Explorer:** https://developers.facebook.com/tools/explorer
- **Access Token Tool:** https://developers.facebook.com/tools/accesstoken
- **Permissions Reference:** https://developers.facebook.com/docs/permissions/reference

### Support:
- **Developer Community:** https://developers.facebook.com/community
- **Bug Reports:** https://developers.facebook.com/support/bugs

---

## ✅ CHECKLIST - Mám vše?

Před spuštěním aplikace zkontrolujte:

```
☐ Meta Developer účet vytvořen
☐ Aplikace "Amity Influencer Monitor" vytvořena
☐ App ID zkopírován do .env
☐ App Secret zkopírován do .env
☐ Long-Lived Access Token (60 dní) zkopírován do .env
☐ Instagram Business Account ID zkopírován do .env
☐ Facebook Page ID zkopírován do .env
☐ Instagram je propojený s FB stránkou
☐ Všechna oprávnění (permissions) schválena
☐ Test připojení úspěšný (python scripts/test_connection.py)
☐ .env soubor není v gitu (.gitignore)
☐ Email konfigurace nastavena (volitelné)
```

---

## 🎉 HOTOVO!

Gratulujeme! Máte plně nakonfigurované Meta Business API.

**Co teď?**

1. ✅ Otestujte monitoring:
   ```bash
   python main.py --mode check
   ```

2. ✅ Spusťte dashboard:
   ```bash
   streamlit run dashboard.py
   ```

3. ✅ Nastavte automatické spouštění (Windows Task Scheduler)

4. ✅ Užívejte si automatický monitoring! 🚀

---

## 💡 TIPY PRO POKROČILÉ

### Tip 1: Webhook pro real-time notifikace

Místo pollingu (pravidelné kontroly) použijte webhooks:

```python
# Instagram pošle notifikaci okamžitě když někdo taguje @amitydrinks
# Konfigurace v App Dashboard → Products → Webhooks
```

### Tip 2: Business Verification

Pro větší API limity a Live mode:

```
1. App Dashboard → Settings → Basic
2. Najděte "Business Verification"
3. Nahrajte firemní dokumenty
4. Čekejte 3-5 dnů na schválení
```

### Tip 3: Multiple Access Tokens

Pro různé členy týmu:

```bash
# Každý může mít svůj vlastní token
# V .env můžete mít:
META_ACCESS_TOKEN_MANAGER=token1
META_ACCESS_TOKEN_MARKETING=token2
```

---

**Verze návodu:** 1.0  
**Datum:** 29.12.2025  
**Pro:** Amity Drinks Influencer Monitor  
**Autor:** Claude & Marketing Team

📧 **Potřebujete pomoc?** Kontaktujte vývojáře nebo Meta Support.
