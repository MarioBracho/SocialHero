# AMITY DRINKS - INFLUENCER MONITORING TOOL
## Kompletní specifikace pro Claude Code

---

## 🎯 CÍLE PROJEKTU

Vytvořit **Python aplikaci** pro automatické sledování aktivity influencerů na sociálních sítích (Instagram, Facebook, TikTok) s těmito hlavními funkcemi:

1. **Automatický monitoring** - 2x denně kontrola označení
2. **Živý dashboard** - okamžitý přehled plnění cílů
3. **Vizuální denní tracking** - kalendářové zobrazení aktivit
4. **Měsíční reporting** - automatické Excel reporty
5. **Notifikace** - real-time upozornění na nové příspěvky

---

## 📋 FUNKČNÍ POŽADAVKY

### 1. SPRÁVA INFLUENCERŮ

**Import a správa dat:**
- Čtení z CSV/Excel souboru `influencers_master.xlsx`
- Automatická detekce změn v souboru (každých 60 sekund)
- Hot-reload - okamžité načtení nových influencerů bez restartu
- SQLite databáze pro historii a cache

**Struktura dat influencera:**
```python
{
    "id": int,
    "jmeno": str,
    "instagram_handle": str,  # @username
    "facebook_handle": str,   # název stránky nebo prázdné
    "tiktok_handle": str,     # @username nebo prázdné
    "stories_mesic": int,     # požadovaný počet stories
    "prispevky_mesic": int,   # požadovaný počet postů
    "reels_mesic": int,       # požadovaný počet reels
    "email": str,             # pro notifikace (volitelné)
    "datum_zacatku": date,    # začátek spolupráce
    "poznamky": str,          # libovolné poznámky
    "aktivni": bool           # ano/ne
}
```

---

### 2. AUTOMATICKÝ MONITORING (2x denně)

**Časování:**
- První check: 9:00
- Druhý check: 17:00
- Možnost manuálního spuštění kdykoliv

**Proces monitoringu:**

1. **Instagram:**
   - Připojení k Instagram Graph API
   - Vyhledání tagů/zmínek @amitydrinks
   - Endpoint: `/{ig-user-id}/tags?fields=id,caption,media_type,media_url,timestamp,like_count,comments_count`
   - Identifikace typu: STORY / IMAGE / VIDEO / CAROUSEL_ALBUM
   - Stažení metrik (dosah kde dostupný)

2. **Facebook:**
   - Facebook Graph API
   - Vyhledání zmínek Amity Drinks page
   - Endpoint: `/{page-id}/tagged?fields=message,created_time,shares,likes.summary(true),comments.summary(true)`

3. **TikTok (volitelné):**
   - TikTok Business API
   - Vyhledání hashtagů #AmityDrinks

**Detekce a klasifikace:**
```python
# Automatická identifikace:
- Je to STORY? (zmizí za 24h)
- Je to PŘÍSPĚVEK? (trvalý post)
- Je to REEL? (video formát)
- Kdo je autor? (mapování na databázi influencerů)
- Obsahuje označení Amity Drinks?
- Datum a čas zveřejnění
```

**Uložení do databáze:**
```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    influencer_id INTEGER,
    platform TEXT,  -- 'instagram', 'facebook', 'tiktok'
    post_type TEXT, -- 'story', 'post', 'reel'
    post_url TEXT,
    post_id TEXT,
    caption TEXT,
    timestamp DATETIME,
    likes INTEGER,
    comments INTEGER,
    shares INTEGER,
    reach INTEGER,
    impressions INTEGER,
    detected_at DATETIME,
    FOREIGN KEY (influencer_id) REFERENCES influencers(id)
);
```

---

### 3. ŽIVÝ WEB DASHBOARD 🖥️

**Technologie:** Flask nebo Streamlit (doporučuji Streamlit pro rychlost)

**URL:** `http://localhost:5000` nebo `http://localhost:8501` (Streamlit)

**Struktura dashboardu:**

#### **📊 Hlavní stránka - Přehled**

```
┌─────────────────────────────────────────────────────────────┐
│  AMITY DRINKS - Influencer Dashboard          🔄 Auto-refresh│
│  Měsíc: Prosinec 2025                         ⚙️ Nastavení   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📈 CELKOVÝ PŘEHLED                                          │
│  ┌──────────────┬──────────────┬──────────────┐            │
│  │ ✅ Splněno   │ ⚠️ Riziko    │ ❌ Nesplněno │            │
│  │     15       │      8       │      2       │            │
│  └──────────────┴──────────────┴──────────────┘            │
│                                                               │
│  📅 AKTIVITA DNES                                            │
│  • 14:32 - @jana.novakova přidala story (IG)               │
│  • 11:15 - @petr.svoboda přidal reel (IG)                  │
│  • 09:22 - @marketapro přidala příspěvek (FB)              │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  👥 INFLUENCEŘI (25 aktivních)                  🔍 Hledat   │
│                                                               │
│  Jméno              Stories    Posty     Reels    Status    │
│  ─────────────────────────────────────────────────────────  │
│  Jana Nováková      4/4 ✅     1/1 ✅    0/0 ✅   SPLNĚNO   │
│  Petr Svoboda       2/4 ⚠️     1/1 ✅    1/1 ✅   RIZIKO    │
│  Markéta Proch.     6/6 ✅     2/2 ✅    0/0 ✅   SPLNĚNO   │
│  Tomáš Novák        1/4 ❌     0/1 ❌    0/0 -    NESPLNÍ   │
│  Lucie Černá        2/2 ✅     1/1 ✅    0/0 ✅   SPLNĚNO   │
│                                                               │
│  [Detail] [Export] [Poslat připomínku]                      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

#### **📅 Kalendářové zobrazení - Denní tracking**

**KLÍČOVÁ FUNKCE: Vizuální kontrola označování po dnech**

```
┌─────────────────────────────────────────────────────────────┐
│  📅 KALENDÁŘ AKTIVIT - Prosinec 2025                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Po  Út  St  Čt  Pá  So  Ne                                 │
│  ──  ──  ──  ──   1   2   3                                 │
│                   🟢  🟢  🟡                                 │
│                   3   5   2                                  │
│                                                               │
│   4   5   6   7   8   9  10                                 │
│  🟢  🟢  🟢  🟡  🟢  🔴  🟢                                 │
│   4   6   3   2   5   0   4                                  │
│                                                               │
│  11  12  13  14  15  16  17                                 │
│  🟢  🟢  🟢  🟢  🟡  🟢  🟢                                 │
│   5   4   6   3   2   4   5                                  │
│                                                               │
│  18  19  20  21  22  23  24                                 │
│  🟢  🔴  🟢  🟢  🟢  🟡  🟢                                 │
│   4   0   5   6   4   1   3                                  │
│                                                               │
│  🟢 = 3+ příspěvků/den                                       │
│  🟡 = 1-2 příspěvky/den                                      │
│  🔴 = 0 příspěvků/den                                        │
│  Číslo = počet detekovaných označení                         │
│                                                               │
│  Kliknutím na den zobrazíte detail všech příspěvků          │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

**Po kliknutí na den:**
```
┌─────────────────────────────────────────────────────────────┐
│  📅 Detail: 15. prosince 2025 (čtvrtek)                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ⏰ 14:32 | @jana.novakova (Instagram Story)                │
│     💬 "Dnes osvěžení s @amitydrinks 🍹"                    │
│     👁️ 2,340 zobrazení                                      │
│     [Zobrazit] [Screenshot]                                  │
│                                                               │
│  ⏰ 11:15 | @petr.svoboda (Instagram Reel)                  │
│     💬 "Recenze Amity Drinks Lemon! #amitydrinks"           │
│     ❤️ 523 | 💬 34 | 👁️ 8,921                              │
│     [Zobrazit] [Screenshot]                                  │
│                                                               │
│  ⏰ 09:22 | @marketapro (Facebook Post)                     │
│     💬 "Ranní rutina s Amity Drinks ☀️"                     │
│     ❤️ 156 | 💬 23 | 🔄 12                                  │
│     [Zobrazit] [Screenshot]                                  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

#### **👤 Detail influencera**

```
┌─────────────────────────────────────────────────────────────┐
│  👤 Jana Nováková (@jana.novakova)              [Upravit]   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📊 PLNĚNÍ CÍLŮ - Prosinec 2025                             │
│                                                               │
│  Instagram Stories:  4/4  ████████████ 100% ✅              │
│  Příspěvky:         1/1  ████████████ 100% ✅              │
│  Reels:             0/0  ──────────── N/A                   │
│                                                               │
│  📈 METRIKY                                                  │
│  • Celkový reach:        18,453                             │
│  • Průměrné engagement:  4.2%                               │
│  • Nejlepší příspěvek:   8,921 zobrazení (Reel 15.12.)     │
│                                                               │
│  📅 HISTORIE PŘÍSPĚVKŮ                                       │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Datum      Typ      Platforma  Likes  Views  Link  │    │
│  ├────────────────────────────────────────────────────┤    │
│  │ 15.12 14:32 Story    Instagram  -     2,340   🔗   │    │
│  │ 12.12 09:15 Story    Instagram  -     1,890   🔗   │    │
│  │ 08.12 16:22 Post     Instagram  523   8,921   🔗   │    │
│  │ 05.12 11:05 Story    Instagram  -     2,100   🔗   │    │
│  │ 02.12 13:44 Story    Instagram  -     1,756   🔗   │    │
│  └────────────────────────────────────────────────────┘    │
│                                                               │
│  📧 KONTAKT: jana@email.cz                                  │
│  📝 POZNÁMKY: Standardní spolupráce                         │
│  📅 SPOLUPRÁCE OD: 01.01.2025                               │
│                                                               │
│  [📊 Export PDF] [📧 Poslat report] [✏️ Upravit]           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

### 4. EXPORTY A REPORTY 📊

#### **A) Automatický měsíční report (Excel)**

**Generování:** Automaticky 1. den v měsíci v 8:00 + kdykoliv na vyžádání

**Název souboru:** `Amity_Report_2025_12.xlsx`

**Struktura Excel souboru:**

**List 1: "Přehled"**
```
A1: Amity Drinks - Měsíční report influencerů
A2: Období: Prosinec 2025
A3: Generováno: 01.01.2026 08:00

A5: CELKOVÁ STATISTIKA
A6: Počet aktivních influencerů: 25
A7: Splnili cíle: 15 (60%)
A8: Nesplnili cíle: 10 (40%)
A9: Celkový počet příspěvků: 156
A10: Celkový reach: 345,678

A12: INFLUENCEŘI
A13: Jméno | Stories (cíl/skut.) | Posty (cíl/skut.) | Reels (cíl/skut.) | Celkem | % Plnění | Status | Reach | Engagement

[Data s barevným formátováním:]
- Zelená: 100% splnění
- Žlutá: 50-99% splnění  
- Červená: 0-49% splnění
```

**List 2: "Detail - Instagram"**
```
Všechny Instagram příspěvky s metrikami
```

**List 3: "Detail - Facebook"**
```
Všechny Facebook příspěvky s metrikami
```

**List 4: "Detail - TikTok"**
```
Všechny TikTok příspěvky s metrikami
```

**List 5: "Problémové případy"**
```
Seznam influencerů, kteří nesplnili cíle
+ doporučené akce
```

**List 6: "Grafy"**
```
- Graf plnění v čase
- Top 10 influencerů podle reach
- Rozdělení podle platforem
- Trend engagement
```

#### **B) Export kdykoliv na vyžádání**

**Formáty:**
1. **Excel** (.xlsx) - kompletní data
2. **CSV** (.csv) - pro další zpracování
3. **PDF** (.pdf) - pro prezentaci/tisk
4. **JSON** (.json) - pro API/integrace

**Tlačítka v dashboardu:**
- "📊 Export aktuální měsíc"
- "📊 Export konkrétní období"
- "📊 Export jednotlivého influencera"
- "📊 Export pro accounting" (jednoduchý přehled pro fakturaci)

---

### 5. NOTIFIKACE A ALERTY 🔔

#### **A) Real-time notifikace (při detekci nového příspěvku)**

**Email notifikace:**
```
Předmět: ✅ Nový příspěvek - Jana Nováková
Od: amity.monitor@yourdomain.com
Komu: marketing@amitydrinks.cz

Dobrý den,

byl detekován nový příspěvek s označením Amity Drinks:

👤 Influencer: Jana Nováková (@jana.novakova)
📱 Platforma: Instagram
📝 Typ: Story
🕐 Čas: 15.12.2025 14:32
💬 Text: "Dnes osvěžení s @amitydrinks 🍹"
🔗 Odkaz: [Zobrazit v dashboardu]

Aktuální plnění:
• Stories: 4/4 ✅
• Příspěvky: 1/1 ✅

─────────────────────────────
Tento email byl odeslán automaticky systémem Amity Influencer Monitor
```

**Desktop notifikace** (Windows/Mac):
```
🔔 Nový příspěvek!
Jana Nováková přidala story na Instagram
[Zobrazit detail]
```

**Slack integrace (volitelné):**
```
🎉 @jana.novakova právě přidala story s označením Amity Drinks!
Instagram | 14:32 | "Dnes osvěžení s @amitydrinks 🍹"
[Zobrazit] [Dashboard]
```

#### **B) Denní souhrn (každý den v 18:00)**

**Email:**
```
Předmět: 📊 Denní souhrn - 15.12.2025
Od: amity.monitor@yourdomain.com

AKTIVITA DNES:
─────────────────
✅ 8 nových příspěvků
📱 Instagram: 5 | Facebook: 2 | TikTok: 1
👥 Aktivních influencerů: 6

TOP PŘÍSPĚVEK DNE:
🏆 Petr Svoboda - Reel s 8,921 zobrazení

ALERTY:
⚠️ 3 influenceři jsou pod cílem
❌ Tomáš Novák zatím 0 příspěvků tento měsíc

[Zobrazit kompletní přehled v dashboardu]
```

#### **C) Týdenní report (každé pondělí v 9:00)**

**Email s přehledem týdne:**
```
Předmět: 📈 Týdenní report 9.-15.12.2025

TÝDEN V ČÍSLECH:
─────────────────
📊 Celkem příspěvků: 34
👥 Aktivních influencerů: 18/25
📈 Celkový reach: 89,456
💬 Engagement rate: 3.8%

TOP 3 INFLUENCEŘI TÝDNE:
1. 🥇 Markéta Procházková - 12 příspěvků, reach 24,567
2. 🥈 Jana Nováková - 8 příspěvků, reach 18,453  
3. 🥉 Petr Svoboda - 7 příspěvků, reach 15,892

POTŘEBUJÍ POZORNOST:
⚠️ Lucie Černá - pouze 1 příspěvek za týden
⚠️ Tomáš Novák - žádná aktivita

[Kompletní report v dashboardu]
```

#### **D) Alerty při problémech**

**Alert: Influencer je pod cílem (3 dny před koncem měsíce)**
```
Předmět: ⚠️ UPOZORNĚNÍ - Tomáš Novák nesplní cíle

Dobrý den,

influencer Tomáš Novák je výrazně pod dohodnutým cílem:

Stories: 1/4 (25%)
Příspěvky: 0/1 (0%)

Do konce měsíce zbývá: 3 dny

Doporučené akce:
• Poslat připomínku influencerovi
• Telefonický kontakt
• Připravit náhradní řešení

[Zobrazit detail] [Poslat připomínku]
```

**Alert: Žádná aktivita 7+ dní**
```
Předmět: 🚨 PROBLÉM - 7 dní bez aktivity

Jana Nováková nebyla aktivní posledních 7 dní.
Poslední příspěvek: 8.12.2025

Akce: Doporučujeme kontaktovat influencera
```

#### **E) Konfigurace notifikací**

**Nastavení v dashboardu nebo config souboru:**
```yaml
notifications:
  email:
    enabled: true
    recipients:
      - marketing@amitydrinks.cz
      - manager@amitydrinks.cz
    smtp:
      server: smtp.gmail.com
      port: 587
      username: amity.monitor@gmail.com
      password: ${EMAIL_PASSWORD}
  
  real_time:
    new_post: true          # notifikace při novém příspěvku
    mention_found: true     # když najdeme zmínku
  
  scheduled:
    daily_summary: 
      enabled: true
      time: "18:00"
    weekly_report:
      enabled: true
      day: "monday"
      time: "09:00"
    monthly_report:
      enabled: true
      day: 1
      time: "08:00"
  
  alerts:
    under_target_days_before_end: 3  # upozornění X dní před koncem měsíce
    no_activity_days: 7               # upozornění po X dnech bez aktivity
    low_engagement_threshold: 2.0     # alert pokud engagement < X%
  
  desktop:
    enabled: true           # Windows/Mac notifikace
  
  slack:
    enabled: false
    webhook_url: ""
```

---

### 6. DATABÁZOVÁ STRUKTURA

```sql
-- Influenceři
CREATE TABLE influencers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jmeno TEXT NOT NULL,
    instagram_handle TEXT,
    facebook_handle TEXT,
    tiktok_handle TEXT,
    stories_mesic INTEGER DEFAULT 0,
    prispevky_mesic INTEGER DEFAULT 0,
    reels_mesic INTEGER DEFAULT 0,
    email TEXT,
    datum_zacatku DATE,
    poznamky TEXT,
    aktivni BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Příspěvky
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    influencer_id INTEGER NOT NULL,
    platform TEXT NOT NULL,        -- 'instagram', 'facebook', 'tiktok'
    post_type TEXT NOT NULL,       -- 'story', 'post', 'reel'
    post_id TEXT NOT NULL,         -- ID z API
    post_url TEXT,
    caption TEXT,
    timestamp DATETIME NOT NULL,   -- kdy byl příspěvek zveřejněn
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    reach INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    engagement_rate REAL DEFAULT 0,
    detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (influencer_id) REFERENCES influencers(id),
    UNIQUE(platform, post_id)      -- prevence duplicit
);

-- Log monitoringu
CREATE TABLE monitoring_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT,                   -- 'success', 'error', 'warning'
    platform TEXT,
    message TEXT,
    details TEXT                   -- JSON s dalšími info
);

-- Notifikace historie
CREATE TABLE notification_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    type TEXT,                     -- 'email', 'desktop', 'slack'
    recipient TEXT,
    subject TEXT,
    message TEXT,
    status TEXT                    -- 'sent', 'failed'
);

-- Měsíční statistiky (cache pro rychlé načítání)
CREATE TABLE monthly_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    influencer_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    stories_count INTEGER DEFAULT 0,
    posts_count INTEGER DEFAULT 0,
    reels_count INTEGER DEFAULT 0,
    total_likes INTEGER DEFAULT 0,
    total_comments INTEGER DEFAULT 0,
    total_reach INTEGER DEFAULT 0,
    avg_engagement_rate REAL DEFAULT 0,
    target_met BOOLEAN DEFAULT 0,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (influencer_id) REFERENCES influencers(id),
    UNIQUE(influencer_id, year, month)
);
```

---

## 🛠️ TECHNICKÉ POŽADAVKY

### **Jazyk a Framework**
- **Python 3.10+**
- **Virtual environment** (venv nebo conda)

### **Klíčové knihovny**

```txt
# requirements.txt

# API komunikace
requests==2.31.0
facebook-sdk==3.1.0

# Databáze
sqlite3  # built-in

# Data processing
pandas==2.1.4
openpyxl==3.1.2
xlsxwriter==3.1.9

# Web dashboard
streamlit==1.29.0
# NEBO
flask==3.0.0
plotly==5.18.0

# Scheduling
schedule==1.2.0
APScheduler==3.10.4

# Notifikace
python-dotenv==1.0.0
sendgrid==6.11.0  # nebo SMTP
plyer==2.1.0  # desktop notifikace

# Utilities
pytz==2023.3
python-dateutil==2.8.2
watchdog==3.0.0  # sledování změn v souborech
colorama==0.4.6  # barevný výstup v terminále

# Reporting
matplotlib==3.8.2
seaborn==0.13.0
fpdf2==2.7.6  # PDF generování

# Optional
slack-sdk==3.26.1  # Slack integrace
```

### **Struktura projektu**

```
amity-influencer-monitor/
│
├── config/
│   ├── .env                          # API klíče (NIKDY necommitovat!)
│   ├── settings.yaml                 # Konfigurace aplikace
│   └── influencers_master.xlsx       # Živá tabulka influencerů
│
├── src/
│   ├── __init__.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── meta_api.py              # Instagram + Facebook API
│   │   ├── tiktok_api.py            # TikTok API
│   │   └── api_base.py              # Společná logika pro API
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db_manager.py            # Správa databáze
│   │   ├── models.py                # SQLAlchemy modely
│   │   └── migrations.py            # DB migrace
│   │
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── monitor.py               # Hlavní monitoring logika
│   │   ├── scheduler.py             # Časování (2x denně)
│   │   └── detector.py              # Detekce a klasifikace příspěvků
│   │
│   ├── reporting/
│   │   ├── __init__.py
│   │   ├── excel_report.py          # Excel generování
│   │   ├── pdf_report.py            # PDF generování
│   │   ├── csv_export.py            # CSV export
│   │   └── charts.py                # Grafy a vizualizace
│   │
│   ├── notifications/
│   │   ├── __init__.py
│   │   ├── email_notifier.py        # Email notifikace
│   │   ├── desktop_notifier.py      # Desktop notifikace
│   │   ├── slack_notifier.py        # Slack integrace
│   │   └── notification_manager.py  # Správa všech notifikací
│   │
│   ├── dashboard/
│   │   ├── __init__.py
│   │   ├── app.py                   # Hlavní Streamlit/Flask app
│   │   ├── pages/
│   │   │   ├── overview.py          # Přehledová stránka
│   │   │   ├── calendar.py          # Kalendářové zobrazení
│   │   │   ├── influencer_detail.py # Detail influencera
│   │   │   ├── analytics.py         # Analytika a grafy
│   │   │   └── settings.py          # Nastavení
│   │   ├── components/
│   │   │   ├── charts.py            # Komponenty grafů
│   │   │   ├── tables.py            # Tabulkové komponenty
│   │   │   └── alerts.py            # Alert komponenty
│   │   └── static/
│   │       ├── css/
│   │       └── js/
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py                # Načítání konfigurace
│       ├── logger.py                # Logging
│       ├── file_watcher.py          # Sledování změn v Excel
│       └── helpers.py               # Pomocné funkce
│
├── data/
│   └── influencer_monitor.db        # SQLite databáze
│
├── reports/
│   ├── monthly/
│   ├── weekly/
│   └── custom/
│
├── logs/
│   ├── monitor.log
│   ├── api.log
│   └── notifications.log
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_monitoring.py
│   └── test_reporting.py
│
├── scripts/
│   ├── setup_database.py            # Inicializace DB
│   ├── setup_api.py                 # Konfigurace API
│   └── test_connection.py           # Test API připojení
│
├── main.py                          # Hlavní entry point pro monitoring
├── dashboard.py                     # Entry point pro dashboard
├── requirements.txt
├── .env.example                     # Příklad .env souboru
├── .gitignore
└── README.md
```

---

## 🚀 INSTALACE A NASTAVENÍ

### **Krok 1: Instalace**

```bash
# Clone nebo stažení projektu
cd amity-influencer-monitor

# Vytvoření virtual environment
python -m venv venv

# Aktivace
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalace závislostí
pip install -r requirements.txt

# Inicializace databáze
python scripts/setup_database.py
```

### **Krok 2: Konfigurace .env**

```env
# config/.env

# Meta (Facebook + Instagram) API
META_APP_ID=your_app_id_here
META_APP_SECRET=your_app_secret_here
META_ACCESS_TOKEN=your_long_lived_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_ig_business_id_here
INSTAGRAM_USERNAME=amitydrinks
FACEBOOK_PAGE_ID=your_fb_page_id_here

# TikTok API (volitelné)
TIKTOK_API_KEY=your_tiktok_api_key
TIKTOK_API_SECRET=your_tiktok_secret

# Email notifikace
EMAIL_ENABLED=true
EMAIL_FROM=amity.monitor@gmail.com
EMAIL_TO=marketing@amitydrinks.cz,manager@amitydrinks.cz
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Slack (volitelné)
SLACK_ENABLED=false
SLACK_WEBHOOK_URL=

# Desktop notifikace
DESKTOP_NOTIFICATIONS=true

# Monitoring
CHECK_INTERVAL_HOURS=12  # 2x denně = každých 12 hodin
FIRST_CHECK_TIME=09:00
SECOND_CHECK_TIME=17:00

# Dashboard
DASHBOARD_PORT=8501
AUTO_REFRESH_SECONDS=60

# Debug
DEBUG=false
LOG_LEVEL=INFO
```

### **Krok 3: Příprava influencers_master.xlsx**

Zkopírujte poskytnutý template a vyplňte své influencery.

---

## 📱 POUŽITÍ

### **A) Spuštění monitoringu**

```bash
# Jednorázová kontrola
python main.py --mode check

# Automatický režim (2x denně)
python main.py --mode auto

# Měsíční report
python main.py --mode report --month 12 --year 2025
```

### **B) Spuštění dashboardu**

```bash
# Streamlit dashboard
streamlit run dashboard.py

# Automaticky otevře v prohlížeči: http://localhost:8501
```

### **C) Windows Task Scheduler (automatické spuštění)**

**Pro automatický monitoring 2x denně:**

1. Otevřete Task Scheduler
2. Create Basic Task:
   - Name: "Amity Monitor Morning"
   - Trigger: Daily at 9:00
   - Action: Start a program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `C:\path\to\main.py --mode check`

3. Opakujte pro 17:00

**Pro nepřetržitý běh dashboardu:**

```batch
REM create_startup.bat
@echo off
cd C:\path\to\amity-influencer-monitor
call venv\Scripts\activate
start pythonw dashboard.py
```

Přidejte .bat soubor do Startup složky.

---

## 📊 PŘÍKLADY POUŽITÍ

### **Scénář 1: Ranní kontrola**

```
9:00 - Automatický start monitoringu
     ↓
Připojení k Instagram API
     ↓
Vyhledání tagů @amitydrinks za posledních 12h
     ↓
Nalezeno 8 nových příspěvků:
  • @jana.novakova - Story (6:30)
  • @petr.svoboda - Reel (8:15)
  • @marketapro - Post (7:45)
  ...
     ↓
Uložení do databáze
     ↓
Aktualizace statistik
     ↓
Odeslání email notifikací o nových příspěvcích
     ↓
Desktop notifikace: "8 nových příspěvků!"
     ↓
Dashboard automaticky refresh
```

### **Scénář 2: Kontrola plnění v dashboardu**

```
Marketing manager otevře dashboard (10:00)
     ↓
Vidí přehled: 15 splněno, 8 riziko, 2 nesplní
     ↓
Klikne na kalendář
     ↓
Vidí, že včera byl 🔴 den (0 příspěvků)
     ↓
Dnes už 🟢 (8 příspěvků detekováno)
     ↓
Klikne na detail "Tomáš Novák"
     ↓
Vidí: 1/4 stories, 0/1 post - ❌ NESPLNÍ
     ↓
Klikne "Poslat připomínku"
     ↓
Email automaticky odeslán influencerovi
```

### **Scénář 3: Konec měsíce - report**

```
1. ledna 8:00 - Automatické spuštění měsíčního reportu
     ↓
Načtení všech dat z prosince
     ↓
Výpočet statistik pro každého influencera
     ↓
Generování Excel souboru:
  • List 1: Přehled (15 splnilo, 10 nesplnilo)
  • List 2-4: Detail podle platforem
  • List 5: Problémové případy
  • List 6: Grafy
     ↓
Uložení: reports/monthly/Amity_Report_2025_12.xlsx
     ↓
Email s reportem managementu
     ↓
Slack notifikace: "Měsíční report připraven! 📊"
```

---

## 🔒 BEZPEČNOST

### **Ochrana citlivých dat:**

```python
# NIKDY necommitovat do gitu:
config/.env
config/influencers_master.xlsx
data/influencer_monitor.db
logs/*.log

# .gitignore
config/.env
config/influencers_master.xlsx
data/
logs/
reports/
*.pyc
__pycache__/
venv/
```

### **API token management:**

- Použití long-lived tokenů (60 dní)
- Automatická obnova před expirací
- Zálohování access tokenů v bezpečném úložišti

### **Databáze:**

- Pravidelné zálohy (denně)
- Export do encrypted ZIP
- Uchovávání historických dat

---

## 📧 PODPORA A TROUBLESHOOTING

### **Časté problémy:**

**1. API token expired**
```
Error: Instagram API returned 190
Řešení: Obnovte access token v Meta Developer Console
```

**2. Influencer nebyl detekován**
```
Možné příčiny:
- Neoznačil správný účet @amitydrinks
- Používá jiný handle než v databázi
- Příspěvek je privátní
- API lag (zkuste za 10 minut)
```

**3. Dashboard nenahrává data**
```
Zkontrolujte:
- Je spuštěný monitoring? (python main.py --mode auto)
- Existuje databáze? (data/influencer_monitor.db)
- Správné cesty v config?
```

---

## 🎯 ROADMAP (budoucí vylepšení)

- [ ] Mobilní aplikace (React Native)
- [ ] AI analýza sentiment (pozitivní/negativní zmínky)
- [ ] Automatické screenshot zachytávání story
- [ ] Integration s Google Analytics
- [ ] Predikce - kdo nesplní cíle (ML model)
- [ ] Automatické fakturace podle plnění
- [ ] Multi-tenant (více značek)
- [ ] API endpoint pro externí systémy

---

## 📝 POZNÁMKY PRO CLAUDE CODE

Ahoj Claude Code! 👋

Zde je kompletní specifikace projektu. Prosím:

1. **Začni inicializací projektu:**
   - Vytvoř strukturu složek
   - Připrav requirements.txt
   - Vytvoř .env.example

2. **Priorita vývoje:**
   - ✅ VYSOKÁ: API integrace (Meta API) + databáze
   - ✅ VYSOKÁ: Monitoring logika
   - ✅ STŘEDNÍ: Dashboard (Streamlit)
   - ✅ STŘEDNÍ: Exporty (Excel)
   - ✅ NÍZKÁ: Notifikace
   - ✅ NÍZKÁ: Slack integrace

3. **Testuj postupně:**
   - Nejdřív test API připojení
   - Pak test detekce příspěvků
   - Nakonec celý flow

4. **Dokumentuj:**
   - Komentáře v kódu
   - README.md s příklady
   - Troubleshooting sekce

**Důležité:**
- Používej error handling všude
- Loguj všechny API requesty
- Rate limiting (Meta API má limity!)
- Cache kde možné (ušetří API volání)

Díky a hodně štěstí! 🚀

---

**Verze specifikace:** 1.0
**Datum:** 29.12.2025
**Pro:** Amity Drinks influencer monitoring
