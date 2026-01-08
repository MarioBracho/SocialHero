# 🎬 Demo Video Script - Meta App Review

**Cíl:** Ukázat Meta reviewerům, jak používáme Instagram API pro tracking influencer kampaní

**Délka:** 2-3 minuty

**Jazyk:** Angličtina (Meta revieweři jsou mezinárodní tým)

---

## 🎯 Přesný Script (s časovými značkami)

### 00:00 - 00:15 | INTRO
**Co ukázat:** Login obrazovka dashboardu

**Co říct:**
```
"Hello, this is a demonstration of Amity Drinks Influencer Monitor -
an internal business tool we use to track Instagram influencer marketing campaigns.

I'll show you how we use the Instagram Graph API to monitor when
influencers tag our business account @amitydrinks.cz."
```

**Akce:**
- Otevři dashboard URL
- Ukaž login obrazovku (ale NEZADÁVEJ heslo ještě)

---

### 00:15 - 00:25 | LOGIN
**Co ukázat:** Přihlášení do systému

**Co říct:**
```
"First, I'll log in with my credentials. This dashboard is restricted
to authorized Amity Drinks employees only."
```

**Akce:**
- Zadej username a heslo
- Klikni "Login"
- Počkej, až se načte dashboard

---

### 00:25 - 00:45 | DASHBOARD OVERVIEW
**Co ukázat:** Hlavní dashboard s influencery a statistikami

**Co říct:**
```
"Here's our main dashboard. You can see our list of influencer partners
and their performance metrics. We track posts, reach, likes, and engagement
for each influencer who mentions our brand.

This data comes from the Instagram Graph API using the permissions
we're requesting: instagram_basic and instagram_manage_insights."
```

**Akce:**
- Ukáž sidebar s influencery
- Ukáž hlavní tabulku s daty
- Posuň dolů, aby viděli různé metriky

---

### 00:45 - 01:20 | INSTAGRAM SYNCHRONIZATION
**Co ukázat:** Tlačítko sync a proces synchronizace

**Co říct:**
```
"Now I'll demonstrate the core functionality. When I click this
'Synchronize Instagram' button, our system connects to the Instagram
Graph API and fetches posts where influencers have tagged our
business account @amitydrinks.cz.

This is why we need the instagram_basic permission - to read our
own Instagram business account data and detect tagged posts.

And instagram_manage_insights permission - to get engagement metrics
like reach, impressions, and engagement rate."
```

**Akce:**
- V sidebaru najdi "🔄 Synchronizovat Instagram"
- Klikni na tlačítko
- Ukaž loading spinner
- Počkej na výsledky (10-15 sekund)

---

### 01:20 - 01:40 | SYNCHRONIZATION RESULTS
**Co ukázat:** Výsledky synchronizace

**Co říct:**
```
"The synchronization is complete. As you can see, the system found
[X] posts where influencers tagged @amitydrinks.cz.

For each post, we capture publicly available data: the post URL,
timestamp, engagement metrics like likes and comments, and which
influencer created it.

This helps us track campaign performance and calculate ROI on
our influencer partnerships."
```

**Akce:**
- Ukaž výsledky sync (kolik příspěvků nalezeno)
- Pokud jsou nějaké chyby, vysvětli že je to normální

---

### 01:40 - 02:10 | VIEW INFLUENCER DETAILS
**Co ukázat:** Detail konkrétního influencera a jeho příspěvky

**Co říct:**
```
"Let me show you the detail for one influencer. Here we can see
all posts where this influencer tagged our brand.

For each post, we display:
- The post type: regular post, reel, or story
- Publication date
- Engagement metrics: likes, comments, reach
- Direct link to the original Instagram post

All of this data comes through the Instagram Graph API, and we
only access publicly available information about posts that mention
our own business account."
```

**Akce:**
- Vyber jednoho influencera ze seznamu
- Ukáž jeho příspěvky
- Klikni na detail příspěvku (pokud je dostupný)
- Ukaž metriky: likes, comments, datum

---

### 02:10 - 02:30 | EXCEL EXPORT
**Co ukázat:** Generování Excel reportu

**Co říct:**
```
"Finally, we can export this data to Excel for internal reporting.
This helps our marketing team analyze campaign performance and
make data-driven decisions about future influencer collaborations."
```

**Akce:**
- Klikni na "📊 Excel Report" (nebo podobné tlačítko)
- Ukaž, že se stáhl soubor
- Volitelně: Otevři Excel soubor a ukáž obsah (3-5 sekund)

---

### 02:30 - 02:50 | OUTRO + PRIVACY
**Co ukázat:** Zpět na dashboard

**Co říct:**
```
"To summarize: we use the Instagram Graph API to automatically detect
when influencers tag our business account, measure campaign performance,
and generate reports for our internal marketing team.

We only access publicly available data from our own Instagram business
account. We don't collect private user information, direct messages,
or any data beyond what users publicly share when they tag @amitydrinks.cz.

Our full privacy policy and terms of service are available at the URLs
provided in this app review submission.

Thank you for reviewing our application."
```

**Akce:**
- Ukaž dashboard ještě jednou
- Volitelně: Ukaž Privacy Policy URL v prohlížeči
- Konec nahrávání

---

## 📝 Alternativní Script (Bez Mluvy - Jen Text)

Pokud nechceš mluvit, můžeš použít **text anotace v Loom**:

### Screen 1: Login
**Text overlay:** "Amity Drinks Influencer Monitor - Internal Tool for Tracking Instagram Campaigns"

### Screen 2: Dashboard
**Text overlay:** "Dashboard shows influencer performance metrics from Instagram Graph API"

### Screen 3: Sync Button
**Text overlay:** "Clicking 'Synchronize Instagram' fetches tagged posts using instagram_basic permission"

### Screen 4: Results
**Text overlay:** "System detects posts where influencers tagged @amitydrinks.cz"

### Screen 5: Details
**Text overlay:** "Engagement metrics retrieved using instagram_manage_insights permission"

### Screen 6: Export
**Text overlay:** "Export data for internal marketing reports"

### Screen 7: Privacy
**Text overlay:** "Only publicly available data collected. Privacy Policy: [URL]"

---

## 🎯 Důležité Body (MUSÍ být ve videu)

✅ **Ukázat login** - prokázat, že je to interní tool
✅ **Ukázat sync proces** - core functionality
✅ **Ukázat data z Instagram API** - posts, metrics
✅ **Zmínit permissions** - proč je potřebujeme
✅ **Zdůraznit privacy** - pouze veřejná data z našeho účtu
✅ **Ukázat use case** - influencer marketing tracking

---

## ⚠️ Co NEŘÍKAT / NEUKAZOVAT

❌ Nevysvětluj technické detaily (Python, SQLite, atd.)
❌ Neukazuj kód nebo terminal
❌ Nezmiňuj problémy nebo bugy
❌ Neukazuj hesla nebo access tokeny
❌ Neukazuj osobní data influencerů (email, telefon)

---

## 🎬 Tipy pro Lepší Video

1. **Mluvit pomalu a jasně** - revieweři nejsou native English speakers
2. **Pauzy mezi kroky** - ať mají čas vidět, co se děje
3. **Kurzor myši viditelný** - ukaž kam klikáš
4. **Žádné rušivé zvuky** - vypni notifikace
5. **HD kvalita** - alespoň 720p
6. **Stabilní internet** - pro Loom upload

---

## 📊 Checklist před Nahráváním

- [ ] Dashboard je spuštěný a funguje
- [ ] Máš připravené login credentials
- [ ] V databázi jsou nějaká data (influenceři, příspěvky)
- [ ] Sync tlačítko funguje
- [ ] Excel export funguje
- [ ] Script je vytisknutý nebo na druhém monitoru
- [ ] Notifikace vypnuté (Windows Focus Assist)
- [ ] Prohlížeč v fullscreen módu
- [ ] Loom extension nainstalovaný

---

**Až budeš připraven nahrávat, řekni "ready" a spustíme dashboard!** 🎬
