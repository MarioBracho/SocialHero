# 🚀 QUICK START GUIDE
## Amity Drinks Influencer Monitor

---

## ✅ PŘED SPUŠTĚNÍM

Ujistěte se, že máte:
- ✅ Python 3.10+
- ✅ `.env` soubor s API klíči (vytvořený přes `auto_setup_api.py`)
- ✅ `influencers_master.xlsx` vyplněný influencery

---

## 📦 1. INSTALACE

```bash
# Vytvoření virtual environment
python3 -m venv venv

# Aktivace
source venv/bin/activate  # Linux/Mac
# NEBO
venv\Scripts\activate  # Windows

# Instalace dependencies
pip install -r requirements.txt
```

---

## 🔧 2. PRVNÍ KROKY

### Test API připojení
```bash
python main.py --mode test
```

### Synchronizace influencerů z Excel
```bash
python main.py --mode sync
```

---

## 🎯 3. ZÁKLADNÍ POUŽITÍ

### Jednorázový monitoring check
```bash
# Kontrola posledních 12 hodin
python main.py --mode check

# Kontrola posledních 24 hodin
python main.py --mode check --hours 24
```

### Zobrazení statistik
```bash
python main.py --mode stats
```

### Generování Excel reportu
```bash
# Aktuální měsíc
python main.py --mode report

# Konkrétní měsíc
python main.py --mode report --year 2025 --month 11
```

---

## 📊 4. WEB DASHBOARD

```bash
# Spuštění dashboardu
streamlit run dashboard.py

# Otevře se v prohlížeči na: http://localhost:8501
```

**Dashboard obsahuje:**
- 📊 Celkový přehled (metriky, statistiky)
- 🎯 Stav plnění cílů
- 📈 Grafy a analytika
- 📱 Poslední příspěvky
- 📥 Export do Excel (tlačítko)

---

## ⏰ 5. AUTOMATICKÝ REŽIM

Spuštění scheduleru pro automatický monitoring 2x denně:

```bash
python main.py --mode auto
```

**Co se děje automaticky:**
- ✅ **09:00** - Ranní monitoring check
- ✅ **17:00** - Odpolední monitoring check
- ✅ **18:00** - Denní email souhrn
- ✅ **1. den v měsíci 08:00** - Měsíční Excel report

**Pro zastavení:** Ctrl+C

---

## 📧 6. EMAIL NOTIFIKACE

### Nastavení

V `.env` souboru:

```env
EMAIL_ENABLED=true
EMAIL_FROM=amity.monitor@gmail.com
EMAIL_TO=marketing@amitydrinks.cz
EMAIL_PASSWORD=your_gmail_app_password_here
```

### Gmail App Password

1. Jděte na: https://myaccount.google.com/apppasswords
2. Vyberte "Mail" a "Other"
3. Zkopírujte vygenerované heslo do `.env`

### Typy notifikací

- 📱 **Real-time** - Při detekci nového příspěvku
- 📊 **Denní souhrn** - Každý den v 18:00
- 📈 **Měsíční report** - 1. den v měsíci s Excel přílohou

---

## 🔄 7. AUTOMATICKÉ SPOUŠTĚNÍ (Windows)

### Pomocí Task Scheduler:

1. Otevřete **Task Scheduler**
2. **Create Basic Task**
3. **Name:** "Amity Monitor Morning"
4. **Trigger:** Daily at 09:00
5. **Action:** Start a program
   - **Program:** `C:\path\to\venv\Scripts\python.exe`
   - **Arguments:** `C:\path\to\main.py --mode check`
   - **Start in:** `C:\path\to\influencer`

6. Opakujte pro 17:00

---

## 🔄 8. AUTOMATICKÉ SPOUŠTĚNÍ (Linux/Mac)

### Pomocí cron:

```bash
# Editace crontab
crontab -e

# Přidání úloh:
# Ranní check v 9:00
0 9 * * * /path/to/venv/bin/python /path/to/main.py --mode check

# Odpolední check v 17:00
0 17 * * * /path/to/venv/bin/python /path/to/main.py --mode check
```

---

## 📁 9. STRUKTURA SOUBORŮ

```
influencer/
├── main.py                 # Hlavní vstup
├── dashboard.py            # Streamlit dashboard
├── .env                    # API klíče (TAJNÉ!)
├── requirements.txt        # Dependencies
│
├── src/
│   ├── api/               # Meta API klient
│   ├── database/          # SQLite databáze
│   ├── monitoring/        # Monitoring + scheduler
│   ├── reporting/         # Excel reporty
│   ├── notifications/     # Email notifikace
│   └── utils/             # Config, logger
│
├── data/
│   └── influencer_monitor.db  # SQLite databáze
│
├── reports/
│   ├── monthly/           # Měsíční reporty
│   ├── weekly/            # Týdenní reporty
│   └── custom/            # Vlastní exporty
│
├── logs/                  # Logy
│
└── Influencer boss/
    └── influencers_master.xlsx  # Excel s influencery
```

---

## ⚙️ 10. VŠECHNY PŘÍKAZY

```bash
# Test API
python main.py --mode test

# Sync influencerů
python main.py --mode sync

# Monitoring check
python main.py --mode check --hours 24

# Statistiky
python main.py --mode stats

# Excel report
python main.py --mode report --year 2025 --month 12

# Automatický scheduler (běží nepřetržitě)
python main.py --mode auto

# Web dashboard
streamlit run dashboard.py
```

---

## 🔍 11. TROUBLESHOOTING

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Invalid OAuth access token"
- Token vypršel (platí 60 dní)
- Řešení: `python auto_setup_api.py`

### "Instagram účet není propojen"
- Instagram musí být Business účet
- Propojte ho s Facebook stránkou

### "Email se neodesílá"
- Zkontrolujte `EMAIL_PASSWORD` v `.env`
- Použijte Gmail App Password

### Dashboard se nespustí
```bash
pip install streamlit plotly
streamlit run dashboard.py
```

---

## 📚 12. DALŠÍ DOKUMENTACE

- **README.md** - Základní přehled
- **META_API_SETUP.md** - Návod na Meta API setup
- **CLAUDE_CODE_SPEC.md** - Kompletní technická specifikace

---

## 💡 13. TIPY

### Rychlý vývoj
```bash
# Nechat běžet dashboard v jednom terminálu
streamlit run dashboard.py

# A scheduler v druhém
python main.py --mode auto
```

### Export dat
```bash
# Excel report
python main.py --mode report

# Najdete v: reports/monthly/Amity_Report_2025_12.xlsx
```

### Debugging
```bash
# V .env nastavte:
DEBUG=true
LOG_LEVEL=DEBUG

# Logy najdete v: logs/
```

---

## ✅ CHECKLIST

Před prvním spuštěním zkontrolujte:

```
☐ Virtual environment vytvořen a aktivován
☐ Dependencies nainstalovány
☐ .env soubor existuje a je vyplněný
☐ influencers_master.xlsx vyplněn
☐ API test úspěšný (python main.py --mode test)
☐ Sync influencerů úspěšný (python main.py --mode sync)
☐ .gitignore obsahuje .env (NIKDY necommitovat!)
```

---

## 🆘 PODPORA

Pokud narazíte na problém:

1. Zkontrolujte logy v `logs/`
2. Spusťte test: `python main.py --mode test`
3. Zkontrolujte `.env` soubor
4. Přečtěte TROUBLESHOOTING sekci

---

**Úspěšné monitorování! 🍹✨**

*Verze: 1.0 | Datum: 29.12.2025*
