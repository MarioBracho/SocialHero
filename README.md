# 🍹 Amity Drinks - Influencer Monitor

Automatický nástroj pro sledování aktivity influencerů na sociálních sítích (Instagram, Facebook, TikTok).

## ✨ Funkce

- ✅ Automatický monitoring 2x denně
- ✅ Detekce označení @amitydrinks na Instagram a Facebook
- ✅ Živý web dashboard
- ✅ Měsíční Excel reporty
- ✅ Email notifikace
- ✅ SQLite databáze pro historii

## 🚀 Rychlý start

### 1. Instalace dependencies

```bash
pip install -r requirements.txt
```

### 2. Konfigurace API klíčů

Ujistěte se, že máte `.env` soubor s API klíči. Pokud ne, spusťte:

```bash
python auto_setup_api.py
```

### 3. Test připojení

```bash
python main.py --mode test
```

### 4. Synchronizace influencerů

```bash
python main.py --mode sync
```

### 5. Spuštění monitoringu

```bash
# Jednorázová kontrola
python main.py --mode check

# Kontrola posledních 24 hodin
python main.py --mode check --hours 24

# Zobrazení statistik
python main.py --mode stats
```

## 📊 Struktura projektu

```
amity-influencer-monitor/
├── src/
│   ├── api/          # Meta API klient
│   ├── database/     # SQLite databáze
│   ├── monitoring/   # Monitoring logika
│   ├── reporting/    # Excel/PDF reporty
│   ├── notifications/# Email notifikace
│   ├── dashboard/    # Streamlit dashboard
│   └── utils/        # Pomocné funkce
├── data/             # SQLite databáze
├── reports/          # Generované reporty
├── logs/             # Logy
├── main.py           # Hlavní vstupní bod
└── .env              # API klíče (TAJNÉ!)
```

## 📋 Konfigurace influencerů

Upravte soubor `Influencer boss/influencers_master.xlsx`:
- List "Aktivní influenceři" - spravujte své influencery
- Každá změna se automaticky načte při příštím spuštění

## 🔄 Automatický běh

### Windows Task Scheduler:

1. Otevřete Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 09:00
4. Action: Start program
   - Program: `C:\path\to\python.exe`
   - Arguments: `C:\path\to\main.py --mode check`

Opakujte pro 17:00.

## 📧 Email notifikace

V `.env` souboru nastavte:

```env
EMAIL_ENABLED=true
EMAIL_FROM=amity.monitor@gmail.com
EMAIL_TO=marketing@amitydrinks.cz
EMAIL_PASSWORD=your_gmail_app_password
```

## 🔐 Bezpečnost

- ⚠️ **NIKDY** necommitujte `.env` soubor!
- ⚠️ Access token vyprší za 60 dní
- ⚠️ Pro obnovu tokenu spusťte znovu `python auto_setup_api.py`

## 📚 Dokumentace

- **Meta API Setup:** `Influencer boss/META_API_SETUP.md`
- **Kompletní specifikace:** `Influencer boss/CLAUDE_CODE_SPEC.md`

## ⚠️ Troubleshooting

### "Invalid OAuth access token"
- Token vypršel
- Spusťte: `python auto_setup_api.py`

### "Influencer nebyl detekován"
- Zkontrolujte, že influencer používá správný @handle
- Instagram musí být Business účet
- Ověřte propojení s Facebook stránkou

### "Module not found"
```bash
pip install -r requirements.txt
```

## 📞 Podpora

Pro problémy nebo dotazy kontaktujte vývojový tým.

---

**Verze:** 1.0
**Vytvořeno:** 29.12.2025
**Pro:** Amity Drinks Marketing Team
