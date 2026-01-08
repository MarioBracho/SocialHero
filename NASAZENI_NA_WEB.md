# 🚀 Amity Drinks Social Hero - Návod na nasazení na web

Kompletní návod krok po kroku, jak nasadit dashboard na internet s ochranou heslem.

---

## 📋 Co budete potřebovat

### 1. Software na vašem počítači
- ✅ Python 3.8 nebo novější
- ✅ Git
- ✅ Web prohlížeč

### 2. Online účty (ZDARMA)
- ✅ GitHub účet (pro ukládání kódu) - https://github.com
- ✅ Streamlit Cloud účet (pro hosting webu) - https://streamlit.io/cloud

**NEBO alternativně:**
- ✅ Railway účet (alternativa ke Streamlit Cloud) - https://railway.app

### 3. Vaše přihlašovací údaje
- Meta API klíče (už máte v `.env` souboru)
- Heslo pro přístup na dashboard (vymyslete si)

---

## 🔐 KROK 1: Přidání ochrany heslem

Dashboard momentálně nemá žádnou autentizaci. Přidáme jednoduchý, ale účinný systém přihlášení.

### 1.1 Vytvořte soubor `.streamlit/secrets.toml`

```bash
mkdir -p .streamlit
```

Vytvořte soubor `.streamlit/secrets.toml` s tímto obsahem:

```toml
# ===========================================
# PŘIHLAŠOVACÍ ÚDAJE
# ===========================================
[passwords]
username = "amity"
password = "VaseHeslo123!"  # ← ZMĚŇTE TOTO NA VAŠE VLASTNÍ HESLO!

# ===========================================
# META API CREDENTIALS
# ===========================================
META_APP_ID = "2035208633880002"
META_APP_SECRET = "b01381154ce058d2b3e318c1a2507ce6"
META_ACCESS_TOKEN = "EAAc7AuZBqjcIBQXZBM8Y23w44TTHvpGXcm9tFTf4RpsJZAGRxC2LuKX7xubnwTjZA1kJHJy1JsYxaK5IRiELbNy8ZCXWPAZAF4G3G8AINNkaZC2ZAlNskMon0ViYbdr7lZBNwMZASVH4LzwzLrOnhP8lVUOPHoZAo003Dxz9tiY24Vva3SOpvRlSK0SYGTZCDnhP"
FACEBOOK_PAGE_ACCESS_TOKEN = "EAAc7AuZBqjcIBQSmLLtg5P8qXJWNQA5SGeHvDMychZCdZB1gws5ubCUZCCpWJ8hsT3DdhBslbIlHcuYgfRB0vkzUFmkBOfJ3VQ00oewQOdZCNvEEEZBDEZBvvxQABUsW2T1PobZBJaOP9jf1XJacL7qokGXoppQxDZAaVZBk4etuDFerxqJu8bZBLJ0PMCxyfQHWEZCmj4pr"
INSTAGRAM_BUSINESS_ACCOUNT_ID = "17841401076549915"
INSTAGRAM_USERNAME = "amitydrinks.cz"
FACEBOOK_PAGE_ID = "965137150187108"
META_BUSINESS_ID = "2057935615056781"

# ===========================================
# EMAIL NOTIFICATIONS
# ===========================================
EMAIL_ENABLED = true
EMAIL_FROM = "amity.monitor@gmail.com"
EMAIL_TO = "marketing@amitydrinks.cz"
EMAIL_PASSWORD = "your_gmail_app_password_here"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ===========================================
# DASHBOARD SETTINGS
# ===========================================
DASHBOARD_PORT = 8501
DASHBOARD_THEME = "light"
AUTO_REFRESH_SECONDS = 60
DEBUG = false
LOG_LEVEL = "INFO"
API_VERSION = "v18.0"
```

⚠️ **DŮLEŽITÉ**: Změňte heslo na své vlastní!

### 1.2 Upravte dashboard.py pro přihlášení

Na ZAČÁTEK souboru `dashboard.py` (před import streamlit) přidejte tento kód:

```python
#!/usr/bin/env python3
"""
AMITY DRINKS - Streamlit Dashboard
Živý web dashboard pro monitoring influencerů
"""
import streamlit as st
import hashlib

# ===========================================
# AUTENTIZACE - MUSÍ BÝT NA ZAČÁTKU!
# ===========================================

def check_password():
    """Kontrola přihlášení"""

    # Zkontrolovat, jestli už je přihlášen
    if "authenticated" in st.session_state and st.session_state.authenticated:
        return True

    # Načtení credentials ze secrets
    try:
        correct_username = st.secrets["passwords"]["username"]
        correct_password = st.secrets["passwords"]["password"]
    except:
        # Fallback pro lokální development
        correct_username = "amity"
        correct_password = "demo123"

    # Přihlašovací formulář
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #F5F0E8 0%, #E8DCC8 100%);
            }
        </style>
    """, unsafe_allow_html=True)

    # Centered login box
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)

        st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <div style='font-size: 4rem; margin-bottom: 1rem;'>🍹</div>
                <h1 style='color: #C8A43B; margin: 0; font-size: 2.5rem;'>AMITY DRINKS</h1>
                <p style='color: #666; font-size: 1.8rem; font-weight: 700; margin-top: 0.5rem;'>social hero</p>
                <p style='color: #999; font-size: 0.9rem;'>Přihlaste se pro přístup k dashboardu</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("👤 Uživatelské jméno", key="username_input")
            password = st.text_input("🔒 Heslo", type="password", key="password_input")
            submit = st.form_submit_button("🚀 Přihlásit se", use_container_width=True)

            if submit:
                if username == correct_username and password == correct_password:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Nesprávné přihlašovací údaje")

    return False

# Kontrola přihlášení - pokud není přihlášen, zobrazí login a zastaví se
if not check_password():
    st.stop()

# ===========================================
# HLAVNÍ APLIKACE (pokračuje normálně...)
# ===========================================

# ZDE POKRAČUJE ZBYTEK VAŠEHO dashboard.py KÓDU...
```

---

## 📦 KROK 2: Příprava projektu pro nasazení

### 2.1 Vytvořte requirements.txt pro produkci

Vytvořte soubor `requirements_web.txt`:

```txt
streamlit==1.29.0
pandas==2.1.4
plotly==5.18.0
requests==2.31.0
python-dotenv==1.0.0
openpyxl==3.1.2
python-dateutil==2.8.2
pytz==2023.3
```

### 2.2 Vytvořte .gitignore

Ujistěte se, že váš `.gitignore` obsahuje:

```
.env
*.db
__pycache__/
venv/
.streamlit/secrets.toml
data/
logs/
reports/
*.pyc
.DS_Store
```

### 2.3 Vytvořte konfiguraci Streamlit

Vytvořte soubor `.streamlit/config.toml`:

```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"

[theme]
primaryColor = "#C8A43B"
backgroundColor = "#F5F0E8"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#000000"
font = "sans serif"
```

---

## 🌐 KROK 3: Nasazení na Streamlit Cloud (DOPORUČENO)

### 3.1 Nahrajte projekt na GitHub

```bash
# Inicializace git repozitáře (pokud ještě není)
cd /home/mariobracho/influencer
git init

# Přidání všech souborů
git add .

# První commit
git commit -m "Initial commit - Amity Social Hero Dashboard"

# Vytvoření repozitáře na GitHubu
# 1. Jděte na https://github.com
# 2. Klikněte na "New repository"
# 3. Pojmenujte: "amity-social-hero"
# 4. Nechte PRIVATE (důležité!)
# 5. Klikněte "Create repository"

# Propojení s GitHub
git remote add origin https://github.com/VASE_UZIVATELSKE_JMENO/amity-social-hero.git
git branch -M main
git push -u origin main
```

### 3.2 Nasazení na Streamlit Cloud

1. **Přihlaste se na Streamlit Cloud**
   - Jděte na https://streamlit.io/cloud
   - Klikněte "Sign up" nebo "Sign in with GitHub"
   - Autorizujte přístup k vašemu GitHub účtu

2. **Vytvořte novou aplikaci**
   - Klikněte "New app"
   - Vyberte váš GitHub repozitář: `amity-social-hero`
   - Main file path: `dashboard.py`
   - Klikněte "Advanced settings"

3. **Nastavte Secrets (KRITICKY DŮLEŽITÉ!)**
   - V Advanced settings najděte sekci "Secrets"
   - Zkopírujte CELÝ obsah vašeho `.streamlit/secrets.toml`
   - Vložte ho do pole "Secrets"
   - Klikněte "Save"

4. **Deploy!**
   - Klikněte "Deploy"
   - Počkejte 2-5 minut na build
   - Váš web bude dostupný na: `https://NAZEV-APLIKACE.streamlit.app`

### 3.3 Vlastní doména (volitelné)

V Streamlit Cloud Settings můžete nastavit vlastní doménu:
- Jděte do App settings
- Klikněte "Custom subdomain"
- Nastavte např: `amity-hero.streamlit.app`

---

## 🚂 ALTERNATIVA: Nasazení na Railway

Railway je alternativa, která nabízí více kontroly a možnost vlastní domény zdarma.

### 4.1 Vytvořte Procfile

```
web: streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0
```

### 4.2 Vytvořte railway.json

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100
  }
}
```

### 4.3 Nasazení na Railway

1. Jděte na https://railway.app
2. Přihlaste se přes GitHub
3. Klikněte "New Project"
4. Vyberte "Deploy from GitHub repo"
5. Vyberte váš repozitář `amity-social-hero`
6. Railway automaticky detekuje Python projekt
7. V Settings → Variables přidejte všechny proměnné z `.streamlit/secrets.toml`
8. Deploy proběhne automaticky

---

## 🔒 KROK 4: Zabezpečení

### 4.1 Důležitá bezpečnostní opatření

✅ **GitHub repozitář MUSÍ být PRIVATE!**
   - Nikdy nesdílejte API klíče veřejně

✅ **Změňte přihlašovací heslo**
   - V `.streamlit/secrets.toml` změňte password na silné heslo

✅ **Pravidelně aktualizujte Meta API Token**
   - Meta tokeny vyprší za 60 dní
   - Aktualizujte v Streamlit Cloud Secrets

### 4.2 Jak změnit heslo po nasazení

1. Jděte do Streamlit Cloud
2. Klikněte na vaši aplikaci
3. Settings → Secrets
4. Změňte hodnotu `password`
5. Klikněte "Save"
6. Aplikace se automaticky restartuje

---

## 📊 KROK 5: Přístup k dashboardu

### 5.1 URL adresa

Po nasazení bude váš dashboard dostupný na:
- **Streamlit Cloud**: `https://NAZEV.streamlit.app`
- **Railway**: `https://NAZEV.up.railway.app`

### 5.2 Přihlášení

- **Uživatelské jméno**: `amity` (nebo co jste nastavili)
- **Heslo**: `VaseHeslo123!` (nebo co jste nastavili)

### 5.3 Sdílení s týmem

URL můžete sdílet s kýmkoli:
- Všichni budou potřebovat uživatelské jméno a heslo
- Pro více uživatelů můžete přidat více credentials do `secrets.toml`

---

## 🔄 KROK 6: Aktualizace aplikace

Když provedete změny v kódu:

```bash
# Uložte změny
git add .
git commit -m "Popis změny"
git push

# Streamlit Cloud automaticky detekuje změnu a re-deployuje aplikaci!
```

---

## 🎯 KROK 7: Monitoring a údržba

### 7.1 Sledování logů

- **Streamlit Cloud**: App Settings → Logs
- **Railway**: Klikněte na deployment → View Logs

### 7.2 Pravidelná údržba

- **Každých 60 dní**: Obnovte Meta API token
  - Spusťte lokálně: `python auto_setup_api.py`
  - Aktualizujte v Streamlit Cloud Secrets

- **Týdně**: Zkontrolujte, že dashboard funguje správně

### 7.3 Záloha databáze

Databáze `data/influencer_monitor.db` není na webu persistentní!

**Řešení**:
1. Pro produkci použijte PostgreSQL (Railway nabízí zdarma)
2. Nebo pravidelně stahujte backupy z lokálního serveru

---

## ❓ Časté problémy a řešení

### "ModuleNotFoundError"
→ Přidejte chybějící modul do `requirements_web.txt`

### "Invalid credentials"
→ Zkontrolujte Secrets v Streamlit Cloud Settings

### "Meta API error"
→ Token vypršel, obnovte přes `auto_setup_api.py`

### Dashboard se nenačítá
→ Zkontrolujte Logs v Streamlit Cloud

### Přihlášení nefunguje
→ Zkontrolujte, že secrets.toml je správně nastavený

---

## 📞 Shrnutí - Rychlý checklist

- [ ] Vytvořit `.streamlit/secrets.toml` s heslem
- [ ] Přidat autentizaci do `dashboard.py`
- [ ] Vytvořit GitHub repozitář (PRIVATE!)
- [ ] Nahrát kód na GitHub
- [ ] Zaregistrovat se na Streamlit Cloud
- [ ] Vytvořit novou aplikaci
- [ ] Nastavit Secrets
- [ ] Deploy
- [ ] Otestovat přihlášení
- [ ] Sdílet URL s týmem

---

## 🎉 Hotovo!

Váš Amity Drinks Social Hero dashboard je nyní živý na internetu a chráněný heslem!

**URL**: `https://vas-nazev.streamlit.app`
**Login**: `amity` / `VaseHeslo123!`

---

**Vytvořeno pro:** Amity Drinks Marketing Team
**Verze:** 2.0
**Datum:** 8.1.2026
