# 🍹 AMITY DRINKS - INFLUENCER MONITORING TOOL

Automatický nástroj pro sledování aktivity influencerů na sociálních sítích (Instagram, Facebook, TikTok) s živým dashboardem a měsíčním reportingem.

---

## 📦 CO JSTE DOSTALI

Tento balíček obsahuje **4 klíčové soubory** pro start vašeho projektu:

### 1️⃣ **influencers_template.csv**
- Základní CSV šablona pro rychlý import influencerů
- Použijte pro testování nebo jako backup

### 2️⃣ **influencers_master.xlsx** 
- **HLAVNÍ SOUBOR** - živá tabulka pro správu influencerů
- 5 listů:
  - ✅ **Aktivní influenceři** - zde spravujete své influencery
  - 🗂️ **Ukončené spolupráce** - archiv
  - 📝 **Šablona pro nové** - návod jak přidat nového
  - 📊 **Aktuální plnění** - real-time dashboard (auto-update)
  - ⚙️ **Nastavení** - přehled konfigurace
- **Aplikace automaticky sleduje změny v tomto souboru!**

### 3️⃣ **CLAUDE_CODE_SPEC.md**
- **KOMPLETNÍ SPECIFIKACE** pro Claude Code
- Detailní popis všech funkcí
- Technická architektura projektu
- Příklady a use-cases

### 4️⃣ **META_API_SETUP.md**
- **KROK-ZA-KROKEM NÁVOD** na vytvoření Meta Business API
- Detailní screenshoty instrukce
- Troubleshooting
- Získání všech potřebných API klíčů

---

## 🚀 QUICK START

### Krok 1: Příprava API přístupů (30-45 minut)

**Následujte návod v souboru `META_API_SETUP.md`**

Na konci budete mít:
```
✅ META_APP_ID
✅ META_APP_SECRET  
✅ META_ACCESS_TOKEN (60 dní platnost)
✅ INSTAGRAM_BUSINESS_ACCOUNT_ID
✅ FACEBOOK_PAGE_ID
```

### Krok 2: Příprava influencerů (5 minut)

1. **Otevřete:** `influencers_master.xlsx`
2. **Jděte na list:** "Aktivní influenceři"
3. **Vyplňte své influencery** (nebo použijte vzorová data pro test)
4. **Uložte soubor**

Příklad řádku:
```
ID: 1
Jméno: Jana Nováková
Instagram: @jana.novakova
Facebook: Jana Nováková
TikTok: @jananovakova
Stories/měsíc: 4
Posty/měsíc: 1
Reels/měsíc: 0
Email: jana@email.cz
Datum začátku: 2025-01-01
Poznámky: Standardní spolupráce
Status: Aktivní
```

### Krok 3: Předání Claude Code (2 minuty)

1. **Otevřete Claude Code** v terminálu
2. **Zadejte:**

```bash
claude-code

# V Claude Code řekněte:
"Potřebuji vytvořit Python aplikaci podle specifikace. 
Prosím přečti si soubor CLAUDE_CODE_SPEC.md a vytvoř kompletní projekt."
```

3. **Připojte tyto soubory:**
   - `CLAUDE_CODE_SPEC.md`
   - `influencers_master.xlsx`
   - `META_API_SETUP.md` (pro referenci)

### Krok 4: Konfigurace (5 minut)

Po vytvoření projektu Claude Code:

1. **Vytvořte `config/.env`** soubor
2. **Zkopírujte API údaje** z Meta API setup
3. **Vyplňte vše podle template v specifikaci**

### Krok 5: Spuštění (1 minuta)

```bash
# Aktivace virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Test připojení
python scripts/test_connection.py

# Spuštění monitoringu
python main.py --mode check

# Spuštění dashboardu
streamlit run dashboard.py
```

**Dashboard se otevře na:** `http://localhost:8501`

---

## 🎯 HLAVNÍ FUNKCE

### ✅ Co aplikace umí:

1. **Automatický monitoring (2x denně)**
   - Kontrola označení @amitydrinks na IG, FB, TT
   - Detekce stories, postů, reels
   - Ukládání metrik (likes, comments, reach)

2. **Živý web dashboard**
   - Real-time přehled plnění cílů
   - Kalendářové zobrazení (denní aktivita)
   - Detail každého influencera
   - Grafy a statistiky

3. **Měsíční reporting**
   - Automatický Excel report 1. den v měsíci
   - Export kdykoliv na vyžádání
   - PDF verze pro prezentace

4. **Notifikace**
   - Email při novém příspěvku
   - Denní souhrn aktivity
   - Týdenní report
   - Alerty při problémech

5. **Živá správa influencerů**
   - Přidání nového = edit Excel + auto-reload
   - Žádný restart aplikace potřeba
   - Historie všech změn

---

## 📊 DASHBOARD PŘEHLED

Po spuštění `streamlit run dashboard.py` uvidíte:

```
┌─────────────────────────────────────────────────┐
│  AMITY DRINKS - Influencer Dashboard            │
├─────────────────────────────────────────────────┤
│  📈 CELKOVÝ PŘEHLED                             │
│  ✅ Splněno: 15  ⚠️ Riziko: 8  ❌ Nesplní: 2   │
│                                                  │
│  📅 KALENDÁŘ                                     │
│  [Vizuální denní tracking s barevnými indikátory]│
│                                                  │
│  👥 INFLUENCEŘI                                  │
│  [Tabulka s real-time stavem plnění]           │
│                                                  │
│  📊 GRAFY & ANALYTIKA                           │
│  [Reach, engagement, trendy]                    │
└─────────────────────────────────────────────────┘
```

### Dashboard funkce:

- ✅ **Auto-refresh** každých 60 sekund
- ✅ **Kalendář** - kliknutím na den zobrazíte detail příspěvků
- ✅ **Export** - tlačítko pro okamžitý Excel export
- ✅ **Filtrování** - podle statusu, platformy, období
- ✅ **Vyhledávání** - najděte konkrétního influencera
- ✅ **Detail view** - kompletní historie příspěvků

---

## 📁 STRUKTURA PROJEKTU

Po vytvoření Claude Code:

```
amity-influencer-monitor/
│
├── config/
│   ├── .env                          # API klíče (TAJNÉ!)
│   ├── settings.yaml                 # Nastavení
│   └── influencers_master.xlsx       # HLAVNÍ SOUBOR
│
├── src/
│   ├── api/                          # Instagram/FB/TikTok API
│   ├── database/                     # SQLite databáze
│   ├── monitoring/                   # Monitoring logika
│   ├── reporting/                    # Excel/PDF reporty
│   ├── notifications/                # Email/Desktop notifikace
│   ├── dashboard/                    # Streamlit web app
│   └── utils/                        # Pomocné funkce
│
├── data/
│   └── influencer_monitor.db         # Databáze
│
├── reports/                          # Generované reporty
│   ├── monthly/
│   ├── weekly/
│   └── custom/
│
├── logs/                             # Logy
│
├── main.py                           # Monitoring (spustit)
├── dashboard.py                      # Dashboard (spustit)
└── requirements.txt                  # Python závislosti
```

---

## 🔄 TYPICKÝ WORKFLOW

### Ranní rutina (automatická):

```
09:00 - Automatické spuštění monitoringu
      ↓
Kontrola Instagram/Facebook/TikTok za posledních 12h
      ↓
Nalezeno 8 nových příspěvků
      ↓
Uložení do databáze + aktualizace statistik
      ↓
Email notifikace: "8 nových příspěvků detekováno!"
      ↓
Desktop notifikace: popup
      ↓
Dashboard auto-refresh → vidíte změny okamžitě
```

### Kontrola v dashboardu (kdykoliv):

```
Otevřete http://localhost:8501
      ↓
Přehled: 15 splněno, 8 riziko, 2 nesplní
      ↓
Klikněte na kalendář → vidíte denní aktivitu
      ↓
Klikněte na konkrétní influencera → detail historie
      ↓
Tlačítko "Export" → stáhněte aktuální report
```

### Přidání nového influencera:

```
Otevřete influencers_master.xlsx
      ↓
List "Šablona pro nové" → zkopírujte řádek
      ↓
List "Aktivní influenceři" → vložte a vyplňte
      ↓
Uložte soubor
      ↓
Za 60 sekund → aplikace načte nového influencera
      ↓
Dashboard → nový influencer se objeví
```

### Konec měsíce (automatický):

```
1. ledna 08:00 - Automatické generování reportu
      ↓
Vytvoření: Amity_Report_2025_12.xlsx
      ↓
Email s reportem → management
      ↓
Report obsahuje:
  • Přehled plnění
  • Detail po platformách
  • Problémové případy
  • Grafy a statistiky
```

---

## 📧 NOTIFIKACE

### Co dostanete:

1. **Real-time (okamžitě)**
   - Nový příspěvek detekován
   - Desktop popup + email

2. **Denní souhrn (18:00)**
   - Počet příspěvků za den
   - TOP příspěvek dne
   - Alerty

3. **Týdenní report (pondělí 9:00)**
   - Statistiky týdne
   - TOP 3 influenceři
   - Kdo potřebuje pozornost

4. **Měsíční report (1. den v měsíci 8:00)**
   - Kompletní Excel report
   - PDF verze
   - Přehled plnění

5. **Alerty**
   - Influencer je pod cílem (3 dny před koncem měsíce)
   - Žádná aktivita 7+ dní
   - Nízké engagement

---

## 🛠️ ÚDRŽBA

### Obnova API tokenu (každých 60 dní):

```bash
# Automatická metoda:
python scripts/refresh_token.py

# Nebo manuálně:
1. Jděte na: developers.facebook.com/tools/accesstoken
2. Extend Access Token
3. Zkopírujte nový token do .env
4. Restartujte aplikaci
```

### Záloha dat:

```bash
# Automatická záloha běží denně
# Manuální záloha:
python scripts/backup_database.py

# Vytvoří: backups/backup_2025_01_29.zip
```

### Update aplikace:

```bash
# Pokud Claude Code vydá novou verzi:
git pull  # nebo stáhněte nové soubory
pip install -r requirements.txt --upgrade
python scripts/migrate_database.py  # pokud je třeba
```

---

## 🚨 TROUBLESHOOTING

### "API token expired"
```
Řešení: Obnovte token (viz návod META_API_SETUP.md)
python scripts/refresh_token.py
```

### "Influencer nebyl detekován"
```
Možné příčiny:
1. Neoznačil správný účet @amitydrinks
2. Používá jiný handle než v databázi
3. Příspěvek je privátní
4. API lag - zkuste za 10 minut

Kontrola:
python main.py --mode check --debug
```

### "Dashboard nenahrává data"
```
1. Je spuštěný monitoring?
   python main.py --mode auto
   
2. Existuje databáze?
   ls data/influencer_monitor.db
   
3. Správné cesty?
   Zkontrolujte config/.env
```

### "Excel změny se nenačítají"
```
1. Je správný path v .env?
2. Je soubor otevřený? (zavřete ho)
3. Restart aplikace:
   Ctrl+C → python main.py --mode auto
```

---

## 💡 TIPY & TRIKY

### Tip 1: Testování bez real dat
```python
# V main.py zapněte test mode:
python main.py --mode test

# Vygeneruje dummy data pro testování dashboardu
```

### Tip 2: Vlastní export formáty
```python
# Dashboard → Export → Vlastní formát
# Můžete přidat PDF, CSV, JSON exports
```

### Tip 3: Slack integrace
```python
# V .env přidejte:
SLACK_ENABLED=true
SLACK_WEBHOOK_URL=your_webhook_url

# Budete dostávat notifikace i do Slacku
```

### Tip 4: Mobilní přístup
```python
# Dashboard je web-based, takže:
# 1. Zjistěte lokální IP: ipconfig (Windows) / ifconfig (Mac)
# 2. Otevřete na mobilu: http://192.168.1.X:8501
# 3. Bookmark → máte mobilní přístup!
```

---

## 📚 DALŠÍ DOKUMENTACE

- **Kompletní specifikace:** `CLAUDE_CODE_SPEC.md`
- **API setup:** `META_API_SETUP.md`
- **API dokumentace:** https://developers.facebook.com/docs/instagram-api
- **Claude Code:** https://claude.ai/code

---

## ✅ CHECKLIST PŘED SPUŠTĚNÍM

```
☐ Meta API přístupy získány (META_API_SETUP.md)
☐ .env soubor vytvořen a vyplněn
☐ influencers_master.xlsx vyplněn (alespoň testovací data)
☐ Virtual environment vytvořen
☐ Dependencies nainstalovány (pip install -r requirements.txt)
☐ Databáze inicializována (python scripts/setup_database.py)
☐ Test připojení úspěšný (python scripts/test_connection.py)
☐ .gitignore obsahuje .env a citlivé soubory
```

---

## 🎉 TO JE VŠE!

Máte všechno, co potřebujete pro vytvoření kompletního influencer monitoring systému!

### Co teď?

1. ✅ **Následujte `META_API_SETUP.md`** → získejte API přístupy
2. ✅ **Vyplňte `influencers_master.xlsx`** → vaši influenceři
3. ✅ **Předejte `CLAUDE_CODE_SPEC.md` Claude Code** → vytvoří aplikaci
4. ✅ **Spusťte a užívejte si automatizaci!** 🚀

### Potřebujete pomoc?

- 📖 Přečtěte si detailní specifikaci v `CLAUDE_CODE_SPEC.md`
- 🔧 Troubleshooting je v `META_API_SETUP.md`
- 💬 Zeptejte se Claude Code na konkrétní problémy

---

**Hodně štěstí s projektem! 🍹✨**

*Vytvořeno s pomocí Claude | 29.12.2025*
