# 🚀 Meta App Review - Průvodce pro Amity Drinks

**Datum:** 06.01.2026
**Cíl:** Získat plný přístup k Instagram Graph API pro automatickou detekci tagged posts

---

## 📋 Co potřebujeme

### Aktuální stav:
- ✅ Business verification (Amity Drinks s.r.o., ID: 2057935615056781)
- ✅ Základní Instagram API přístup
- ✅ Long-lived access token
- ⚠️ Nemáme oprávnění pro `/tags` endpoint

### Potřebná oprávnění (Permissions):

1. **instagram_basic** ✅ (už máme)
   - Základní přístup k profilu a media

2. **instagram_manage_insights** (POTŘEBUJEME)
   - Přístup k insights (reach, impressions, engagement)
   - Nutné pro detailní metriky příspěvků

3. **instagram_content_publish** (volitelné)
   - Automatické publikování obsahu
   - Zatím nepotřebujeme

4. **pages_read_engagement** (POTŘEBUJEME)
   - Přístup k tagged posts na Facebook stránce
   - Detekce kdy někdo označí Amity Drinks

---

## 🎯 Krok za Krokem - App Review Process

### KROK 1: Vytvoření/Kontrola Meta App

1. Jdi na [Meta for Developers](https://developers.facebook.com/)
2. Klikni **"My Apps"** → **"Create App"** (nebo otevři existující)
3. Vyber typ: **"Business"**
4. Vyplň:
   - App Name: `Amity Drinks Influencer Monitor`
   - App Contact Email: `mario@amitydrinks.cz`
   - Business Account: `Amity Drinks s.r.o. (2057935615056781)`

---

### KROK 2: Konfigurace App

**2.1 Add Products:**
- Přidej **Instagram Graph API**
- Přidej **Facebook Login**

**2.2 App Settings:**
```
App Domains: amitydrinks.cz
Privacy Policy URL: https://amitydrinks.cz/privacy (vytvoříme)
Terms of Service URL: https://amitydrinks.cz/terms (vytvoříme)
```

**2.3 App Review → Permissions and Features:**
Klikni **"Request Advanced Access"** pro:
- ✅ `instagram_basic`
- ✅ `instagram_manage_insights`
- ✅ `pages_read_engagement`

---

### KROK 3: Příprava App Review Submission

Meta vyžaduje:

#### 3.1 Use Case Description

**Název use case:** "Influencer Performance Tracking"

**Detailed Description:**
```
Our application (Amity Drinks Influencer Monitor) helps us track
when influencers mention or tag our Instagram business account
(@amitydrinks.cz) in their posts and stories.

We need access to:
1. Tagged media - to detect when influencers tag @amitydrinks.cz
2. Insights - to measure reach and engagement of tagged posts
3. Page engagement - to track mentions on our Facebook page

This data helps us:
- Track influencer marketing campaign performance
- Calculate ROI on influencer partnerships
- Generate monthly performance reports for our marketing team
- Compensate influencers based on actual reach and engagement

We DO NOT:
- Publish content automatically
- Access other users' private data
- Scrape or store unnecessary information
```

#### 3.2 Demonstrační Video (Screencast)

Meta vyžaduje video ukazující:

**Co nahrát (2-3 minuty):**
1. Login do dashboardu
2. Kliknutí na "Synchronizovat Instagram"
3. Zobrazení nalezených tagged posts
4. Detail příspěvku s metrikami (likes, reach, comments)
5. Vygenerování reportu

**Nástroj na nahrávání:**
- Mac: QuickTime Player (Cmd+Shift+5)
- Windows: Xbox Game Bar (Win+G)
- Online: Loom.com (zdarma)

**Kde nahrát:**
- YouTube (unlisted link)
- Google Drive (public sharing)
- Loom.com

#### 3.3 Test User Instructions

Meta reviewer potřebuje otestovat app:

**Instrukce pro reviewera:**
```
1. Login credentials will be provided in the secure attachment
2. Go to https://dashboard.amitydrinks.cz
3. Click "🔄 Synchronizovat Instagram" button in sidebar
4. System will fetch tagged posts from @amitydrinks.cz
5. View detected influencer posts with insights
6. Click "📊 Excel Report" to download performance data
```

**Test User Creation:**
1. V Meta App → Roles → Test Users
2. Create Test User
3. Přidej test user jako Instagram tester

---

### KROK 4: Odeslání App Review

1. Meta for Developers → Your App → **App Review**
2. Klikni **"Permissions and Features"**
3. Pro každé permission klikni **"Request Advanced Access"**
4. Vyplň:
   - **Use Case:** Influencer Performance Tracking
   - **Description:** (použij text z 3.1)
   - **Screencast:** (nahraj video link)
   - **Test Instructions:** (použij text z 3.3)
   - **Test User:** (vytvoř test user)

5. **Submit for Review**

---

### KROK 5: Co Meta Kontroluje

Review trvá **3-7 pracovních dní**

Meta kontroluje:
- ✅ Je app skutečná a funkční?
- ✅ Používáme data jen pro stated use case?
- ✅ Máme privacy policy?
- ✅ Jsou bezpečnostní opatření na místě?
- ✅ Neporušujeme Platform Terms?

**Nejčastější důvody odmítnutí:**
- ❌ Nefunkční demo video
- ❌ Chybějící privacy policy
- ❌ Nesprávné use case (příliš obecné)
- ❌ Test user nemůže otestovat app

---

## 📄 Potřebné Dokumenty

### 1. Privacy Policy (`privacy.md`)

**Základní struktura:**
```markdown
# Privacy Policy - Amity Drinks Influencer Monitor

Effective Date: 06.01.2026

## What Data We Collect
- Instagram business account data (@amitydrinks.cz)
- Tagged posts and stories mentioning our account
- Public engagement metrics (likes, comments, reach)

## How We Use Data
- Track influencer marketing campaign performance
- Generate internal performance reports
- Calculate influencer compensation

## Data We DON'T Collect
- Private user information
- Direct messages
- Personal data of Instagram users

## Data Storage
- Data stored securely on EU servers
- Access restricted to authorized team members
- Regular security audits

## Your Rights
Contact: mario@amitydrinks.cz
```

### 2. Terms of Service (`terms.md`)

**Základní struktura:**
```markdown
# Terms of Service - Amity Drinks Influencer Monitor

## Service Description
Internal tool for Amity Drinks s.r.o. to track influencer
marketing performance on Instagram and Facebook.

## Acceptable Use
- Only authorized Amity Drinks employees may access
- Data may not be shared with third parties
- Comply with Meta Platform Terms

## Data Usage
- We comply with Meta Platform Terms
- We respect user privacy
- We only collect publicly available data

Contact: mario@amitydrinks.cz
```

---

## 🎬 Checklist před Submission

- [ ] App vytvořena a nakonfigurována
- [ ] Privacy Policy vytvořena a nahraná na web
- [ ] Terms of Service vytvořena
- [ ] Demo video nahrané (2-3 min)
- [ ] Test user vytvořen a funguje
- [ ] Dashboard je přístupný a funkční
- [ ] Use case popis připraven
- [ ] Test instructions napsané

---

## ⚡ Rychlý Start - Co udělat TEĎKA

### Priorita 1: Vytvoř Privacy Policy

```bash
# Vytvoř jednoduchou stránku
cd /home/mariobracho/influencer
mkdir -p public
nano public/privacy.html
```

**Jednoduchá HTML:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Privacy Policy - Amity Drinks</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #C8A43B; }
    </style>
</head>
<body>
    <h1>Privacy Policy - Amity Drinks Influencer Monitor</h1>
    <p><strong>Effective Date:</strong> January 6, 2026</p>

    <h2>What Data We Collect</h2>
    <ul>
        <li>Instagram business account data (@amitydrinks.cz)</li>
        <li>Tagged posts and stories mentioning our account</li>
        <li>Public engagement metrics (likes, comments, reach)</li>
    </ul>

    <h2>How We Use Data</h2>
    <ul>
        <li>Track influencer marketing campaign performance</li>
        <li>Generate internal performance reports</li>
        <li>Calculate influencer compensation</li>
    </ul>

    <h2>Data We DON'T Collect</h2>
    <ul>
        <li>Private user information</li>
        <li>Direct messages</li>
        <li>Personal data of Instagram users</li>
    </ul>

    <h2>Contact</h2>
    <p>Email: mario@amitydrinks.cz</p>
</body>
</html>
```

### Priorita 2: Nahraj na Web

Možnosti:
1. **Vedos.cz hosting** (pokud máš přístup)
2. **GitHub Pages** (zdarma, 5 minut setup)
3. **Netlify/Vercel** (zdarma)

### Priorita 3: Nahraj Demo Video

1. Spusť dashboard
2. Nahraj 2-3 min screencast:
   - Login
   - Kliknutí na sync
   - Zobrazení dat
3. Upload na YouTube (unlisted)

---

## 📞 Potřebuješ Pomoc?

**Pokud Meta odmítne:**
- Přečti důvod v reviewu
- Uprav podle feedback
- Re-submit (neomezený počet pokusů)

**Typické dotazy Meta:**
- "Why do you need this permission?"
  → Odpověď: Track influencer marketing ROI
- "Can you achieve this without this permission?"
  → Odpověď: No, we need tagged media for automatic detection

---

## ⏱️ Časová osa

| Krok | Čas |
|------|-----|
| Vytvoření Privacy/Terms | 30 min |
| Upload na web | 15 min |
| Nahrání demo video | 20 min |
| Vytvoření test user | 10 min |
| Vyplnění App Review formuláře | 30 min |
| **TOTAL** | **~2 hodiny** |
| Meta Review čekání | **3-7 dní** |

---

## 🎯 Co Získáme po Schválení

✅ **Automatická detekce:**
- Influencer označí @amitydrinks.cz → automaticky detekováno
- Žádné manuální přidávání @mentions
- Real-time synchronizace

✅ **Plné insights:**
- Reach, impressions, engagement
- Demografické data
- Best performing posts

✅ **Facebook integrace:**
- Tagged posts na Facebook stránce
- Facebook stories
- Kompletní cross-platform tracking

---

**Ready to start?** 🚀

Začni vytvořením Privacy Policy a pak ti pomůžu s dalšími kroky!
