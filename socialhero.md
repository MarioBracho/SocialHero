# 🎯 AMITY DRINKS - Social Hero Dashboard

**Datum vytvoření:** 30.12.2025
**Verze:** 2.0
**Status:** ✅ Kompletní a funkční

---

## 📋 Přehled projektu

Dashboard pro monitoring influencer marketingu značky Amity Drinks. Slouží k sledování výkonu influencerů, jejich příspěvků na sociálních sítích a dosahu kampaní.

**URL:** http://172.23.45.107:8501

---

## 🎨 Design & Branding

### Barvy Amity
- **Hlavní černá**: `#000000`
- **Bílá**: `#FFFFFF`
- **Zlatá Amity**: `#C8A43B` (Satine Sheen Gold)
- **Béžová pozadí**: `#F5F0E8`
- **Šedá text**: `#666666`

### Typografie
- **Font**: Work Sans
- **Hlavní nadpis**: 3rem, bold
- **Podtitulek "social hero"**: 2.2rem, bold (font-weight: 700)

### Logo
- Umístění: `/home/mariobracho/influencer/printscreens/Amity Hlavní jpg.jpg`
- Pozice: Sidebar nahoře

---

## ✨ Hlavní funkce

### 1. Manuální přidávání příspěvků
**Kde:** Sidebar → "➕ Přidat Příspěvek"

**Funkce:**
- Rozbalovací expander pro výběr influencera (radio buttons)
- Multi-select checkboxy pro typy příspěvků (Story, Post, Reel)
- Možnost přidat více typů najednou
- Input pole: URL, Popis, Reach, Likes
- Automatické datum vytvoření

**Styly:**
- Bílé pozadí na všech input polích
- Černý text
- Ohraničení `#E8E8E8`
- Zlatý focus border `#C8A43B`

### 2. Výběr období
**Kde:** Sidebar → "📅 Období"

**Funkce:**
- Expander pro výběr roku (2024, 2025)
- Expander pro výběr měsíce (Leden-Prosinec)
- Radio buttons pro výběr

### 3. Tabulka "Stav plnění"
**Hlavní tabulka s přehledem influencerů**

**Sloupce:**
- Jméno
- Stories (aktuální/cíl)
- Posty (aktuální/cíl)
- Reels (aktuální/cíl)
- Celkem (celkový počet příspěvků)
- % Plnění (progress bar)
- Status (✅ Splněno / ⚠️ Riziko / ❌ Nesplní)
- Reach (celkový dosah)

**Styly:**
- ⬜ Bílé pozadí
- ⬛ Černý text
- 🎯 Zlatý spodní okraj u hlavičky
- ✨ Hover efekt: béžová barva `#F5F0E8` při najetí myší
- 📊 Implementováno pomocí `st.table()` s pandas Styler

### 4. Žebříčky (Leaderboards)
**Umístění:** Hned pod hlavní tabulkou

#### 📊 Nejvíce příspěvků (levá strana)
- TOP 5 influencerů podle celkového počtu příspěvků
- 🥇 1. místo: Zlaté pozadí `#FFD700`
- 🥈 2. místo: Stříbrné pozadí `#C0C0C0`
- 🥉 3. místo: Bronzové pozadí `#CD7F32`
- Ostatní: Bílé pozadí

#### 🎯 Největší dosah (pravá strana)
- TOP 5 influencerů podle celkového reach
- Stejné barevné odlišení medailí
- Formátovaná čísla s mezerami (např. "1 234 567")

**Společné funkce:**
- Hover efekt na všech řádcích
- Automatické řazení podle výkonu
- Zobrazení pořadí (1-5)

### 5. Grafy & Analytika
**Sekce:** "📈 Analytika"

**Grafy:**
- 🎯 Plnění cílů (pie chart) - status influencerů
- 👑 TOP influenceři podle reach (bar chart)
- 📈 Trendy (line chart) - vývoj v čase
- 📊 Typy příspěvků (bar chart) - rozdělení stories/posts/reels

---

## 🔧 Technické detaily

### Stack
- **Framework**: Streamlit 1.x
- **Python**: 3.12
- **Database**: SQLite
- **Charts**: Plotly
- **Styling**: Custom CSS + pandas Styler

### Klíčové soubory
```
/home/mariobracho/influencer/
├── dashboard.py                    # Hlavní aplikace
├── src/
│   ├── database/db_manager.py     # Database operations
│   ├── api/meta_api.py            # Meta API client
│   ├── monitoring/monitor.py       # Monitoring logika
│   └── reporting/excel_report.py   # Excel export
├── .env                            # API credentials
├── printscreens/
│   └── Amity Hlavní jpg.jpg       # Logo
└── socialhero.md                   # Tato dokumentace
```

### Spuštění
```bash
cd /home/mariobracho/influencer
./venv/bin/streamlit run dashboard.py --server.headless true
```

### Port & přístup
- **Network URL**: http://172.23.45.107:8501
- **External URL**: http://175.157.53.188:8501

---

## 🎨 CSS customizace

### Skryté elementy
```css
/* Skrýt horní Streamlit toolbar */
header[data-testid="stHeader"] {
    display: none !important;
}

/* Skrýt fullscreen tlačítko u obrázků */
button[title="View fullscreen"] {
    display: none !important;
}
```

### Input pole styling
```css
input[type="text"],
input[type="number"],
textarea {
    background: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #E8E8E8 !important;
    border-radius: 8px !important;
}

/* Focus stav */
input:focus {
    border-color: #C8A43B !important;
    box-shadow: 0 0 0 1px #C8A43B !important;
}
```

### Tabulka hover efekt
```css
div[data-testid="stDataFrame"] tbody tr:hover td {
    background-color: #F5F0E8 !important;
    cursor: pointer !important;
}
```

### Pandas Styler pro žebříčky
```python
def style_leaderboard(df):
    return df.style.set_properties(**{
        'background-color': '#FFFFFF',
        'color': '#000000',
        'text-align': 'left',
        'padding': '8px'
    }).set_table_styles([
        {'selector': 'tbody tr:nth-child(1) td', 'props': [
            ('background-color', '#FFD700'),  # Gold
            ('font-weight', '700')
        ]},
        {'selector': 'tbody tr:nth-child(2) td', 'props': [
            ('background-color', '#C0C0C0'),  # Silver
            ('font-weight', '600')
        ]},
        {'selector': 'tbody tr:nth-child(3) td', 'props': [
            ('background-color', '#CD7F32'),  # Bronze
            ('font-weight', '600')
        ]}
    ])
```

---

## 🐛 Vyřešené problémy

### 1. Browser cache issue
**Problém:** CSS změny se nezobrazovaly v běžném prohlížeči
**Řešení:**
- Přidán cache-busting mechanismus s timestampem
- Použití pandas Styler místo čistého CSS
- Změna z `st.dataframe()` na `st.table()` pro hover support

### 2. Plotly cornerradius error
**Problém:** `ValueError: Invalid property 'cornerradius'`
**Řešení:** Odstraněn `cornerradius` parametr z plotly grafů

### 3. Logo path error
**Problém:** `MediaFileStorageError: Error opening 'Amity Hlavní jpg.jpg'`
**Řešení:** Opravena cesta na `/home/mariobracho/influencer/printscreens/Amity Hlavní jpg.jpg`

### 4. Nested expanders error
**Problém:** `StreamlitAPIException: Expanders may not be nested`
**Řešení:** Odstraněn outer expander wrapper, ponechány jen inner expanders

### 5. Hover efekt nefungoval na datových řádcích
**Problém:** Hover fungoval jen na header, ne na data rows
**Řešení:** Změna z `st.dataframe()` (interaktivní) na `st.table()` (statická HTML tabulka)

---

## 📊 Database schema

### Tabulka: influencers
```sql
- id (INTEGER PRIMARY KEY)
- jmeno (TEXT)
- platform (TEXT)
- stories_mesic (INTEGER)
- prispevky_mesic (INTEGER)
- reels_mesic (INTEGER)
```

### Tabulka: posts
```sql
- id (INTEGER PRIMARY KEY)
- influencer_id (INTEGER)
- platform (TEXT)
- post_type (TEXT)  -- story/post/reel
- post_id (TEXT)
- post_url (TEXT)
- caption (TEXT)
- timestamp (DATETIME)
- likes (INTEGER)
- comments (INTEGER)
- shares (INTEGER)
- reach (INTEGER)
- impressions (INTEGER)
- engagement_rate (REAL)
```

### Tabulka: monthly_stats
```sql
- id (INTEGER PRIMARY KEY)
- influencer_id (INTEGER)
- year (INTEGER)
- month (INTEGER)
- stories_count (INTEGER)
- posts_count (INTEGER)
- reels_count (INTEGER)
- total_reach (INTEGER)
- target_met (BOOLEAN)
```

---

## 🚀 Budoucí automatizace

### Meta API integrace (čeká na schválení)
**Status:** ⏳ Čeká se na Meta App Review

**Potřebné permissions:**
- `instagram_manage_comments` - pro `/tags` endpoint
- `instagram_manage_insights` - pro statistiky
- `pages_read_engagement` - pro engagement metriky

**Po schválení:**
1. Aktivovat scheduler (`src/monitoring/scheduler.py`)
2. Automatická kontrola tagů 2x denně (9:00, 17:00)
3. Email notifikace o nových příspěvcích
4. Denní a měsíční reporty

**Dokumentace:**
- `AUTOMATION_AFTER_META_APPROVAL.md` - návod k aktivaci
- `MANUAL_MONITORING_GUIDE.md` - manuální workflow

---

## 📝 Changelog

### v2.0 (30.12.2025)
- ✅ Změna názvu z "Influencer Monitor" na "social hero"
- ✅ Zvětšení a ztučnění podtitulku (2.2rem, bold)
- ✅ Přidány žebříčky (TOP 5 podle příspěvků a reach)
- ✅ Implementován hover efekt na tabulce
- ✅ Bílé pozadí a černý text ve všech polích
- ✅ Skrytý Streamlit toolbar
- ✅ Multi-select pro typy příspěvků
- ✅ Expandery pro výběr období a přidávání příspěvků

### v1.0 (29.12.2025)
- ✅ Základní dashboard s manuálním zadáváním
- ✅ Tabulka stavu plnění
- ✅ Grafy a analytika
- ✅ Excel export
- ✅ Meta API integrace (připraveno)

---

## 🎯 Influenceři v systému

1. **Huber Wake**
   - Stories: 4/měsíc
   - Posty: 0/měsíc
   - Reels: 0/měsíc

2. **Jana Nováková**
   - Stories: 4/měsíc
   - Posty: 0/měsíc
   - Reels: 0/měsíc

3. **Mari Macháček**
   - Stories: 4/měsíc
   - Posty: 1/měsíc
   - Reels: 1/měsíc

4. **Mario**
   - Stories: 0/měsíc
   - Posty: 0/měsíc
   - Reels: 0/měsíc

---

## 💡 Tipy pro použití

### Denní workflow
1. Ráno zkontrolovat Instagram notifikace o označení
2. Pro každý nový příspěvek:
   - Otevřít sidebar → "➕ Přidat Příspěvek"
   - Vybrat influencera
   - Zaškrtnout typ(y) příspěvku
   - Zadat reach a likes
   - Kliknout "✅ Přidat"
3. Dashboard se automaticky aktualizuje

### Týdenní workflow
1. Vygenerovat Excel report (tlačítko "📊 Excel Report")
2. Zkontrolovat žebříčky - kdo vede
3. Zkontrolovat tabulku - kdo plní cíle (zelené checkmarky)
4. Kontaktovat influencery s nízkým plněním

### Měsíční workflow
1. Konec měsíce - vygenerovat finální report
2. Vyhodnotit úspěšnost kampaní
3. Nastavit cíle pro další měsíc
4. Vyplatit odměny podle výkonu

---

## 🔐 Zabezpečení

### Access Token
- Uloženo v `.env` souboru
- **NIKDY** necommitovat do gitu
- Platnost: 60 dní
- Obnova: Přes Meta for Developers console

### Database
- SQLite lokální databáze
- Backup: Automaticky při každé změně
- Lokace: `/home/mariobracho/influencer/amity_influencers.db`

---

## 📞 Support & kontakt

**Dashboard vytvořil:** Claude Sonnet 4.5
**Pro:** Amity Drinks
**Datum:** 30.12.2025

**Pro pomoc:**
- GitHub Issues (pokud je projekt na GitHubu)
- Tech support Amity Drinks

---

## 🎉 Závěr

Dashboard je plně funkční a připravený k použití. Všechny požadované funkce byly implementovány:

✅ Čistý design s Amity barvami
✅ Intuitivní ovládání
✅ Rychlé manuální zadávání
✅ Přehledné žebříčky
✅ Hover efekty
✅ Responsive design
✅ Připraveno na automatizaci

**Užívej dashboard a hodně úspěchů s influencer marketingem!** 🚀

---

*Poslední aktualizace: 30.12.2025 12:50*
