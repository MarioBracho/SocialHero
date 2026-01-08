# ✅ Meta App Review - Checklist

## 📋 Před Odesláním

### 1. Dokumenty (HOTOVO ✅)
- [x] Privacy Policy vytvořena (`public/privacy.html`)
- [x] Terms of Service vytvořena (`public/terms.html`)
- [ ] Nahrané na veřejný web (URL potřebné pro Meta)

### 2. Web Hosting
**Potřebné URL:**
- Privacy Policy: `https://amitydrinks.cz/privacy.html`
- Terms of Service: `https://amitydrinks.cz/terms.html`

**Možnosti:**
1. **Vedos.cz** (pokud máš přístup k FTP/hosting)
2. **GitHub Pages** (zdarma, 5 min)
3. **Netlify** (zdarma, drag & drop)

### 3. Meta App Setup
- [ ] Vytvořena/zkontrolována Meta App
- [ ] App Name: "Amity Drinks Influencer Monitor"
- [ ] Business Account: Amity Drinks s.r.o. (2057935615056781)
- [ ] Instagram Product přidán
- [ ] Privacy Policy URL vyplněna
- [ ] Terms URL vyplněna

### 4. Demo Video
**Co ukázat (2-3 minuty):**
- [ ] Login do dashboardu
- [ ] Klik na "🔄 Synchronizovat Instagram"
- [ ] Zobrazení nalezených příspěvků
- [ ] Detail příspěvku s metrikami
- [ ] Excel export

**Kde nahrát:**
- YouTube (unlisted) - DOPORUČENO
- Loom.com
- Google Drive (public link)

### 5. Test User
- [ ] Vytvořen test user v Meta App
- [ ] Test user má přístup k dashboardu
- [ ] Připraveny login credentials pro Meta reviewera

### 6. App Review Formulář

**Potřebná oprávnění:**
- [ ] `instagram_basic` (Request Advanced Access)
- [ ] `instagram_manage_insights` (Request Advanced Access)
- [ ] `pages_read_engagement` (Request Advanced Access)

**Pro každé oprávnění vyplnit:**
- [ ] Use Case: "Influencer Performance Tracking"
- [ ] Detailed Description (viz níže)
- [ ] Screencast URL
- [ ] Test Instructions

---

## 📝 Use Case Description (Copy-Paste Ready)

### Use Case Name:
```
Influencer Performance Tracking
```

### Detailed Description:
```
Our application (Amity Drinks Influencer Monitor) is an internal business tool
that helps us track when influencers mention or tag our Instagram business
account (@amitydrinks.cz) in their posts and stories.

WHAT WE NEED:

1. instagram_basic
   - Access to our own Instagram Business Account (@amitydrinks.cz)
   - Read basic profile information and media

2. instagram_manage_insights
   - Access to insights/metrics for posts that tag our account
   - Measure reach, impressions, and engagement
   - Track campaign performance

3. pages_read_engagement
   - Detect when users tag our Facebook page
   - Read tagged posts on our Facebook page

HOW WE USE THIS DATA:

1. Track influencer marketing campaign performance
   - We partner with influencers who promote our drinks
   - Need to measure reach and engagement of their posts mentioning us

2. Calculate ROI on influencer partnerships
   - Determine which influencers drive the most engagement
   - Make data-driven decisions about future collaborations

3. Generate monthly performance reports
   - Provide reports to our marketing team
   - Track campaign effectiveness over time

4. Compensate influencers fairly
   - Pay influencers based on actual reach and engagement
   - Transparent performance-based compensation

WHAT WE DON'T DO:

- We do NOT publish content on behalf of users
- We do NOT access private user data
- We do NOT scrape or store unnecessary information
- We only track publicly available data related to our brand

This is an internal tool used exclusively by Amity Drinks employees
to manage our influencer marketing program.
```

### Test Instructions:
```
HOW TO TEST THE APP:

1. Login credentials are provided in the secure attachment
   Username: [will be provided]
   Password: [will be provided]

2. Navigate to: https://dashboard.amitydrinks.cz
   (or the URL where dashboard is hosted)

3. After login, you will see the Amity Drinks dashboard

4. In the left sidebar, click the "🔄 Synchronizovat Instagram" button
   - This triggers synchronization with Instagram API
   - The app will fetch tagged posts from @amitydrinks.cz

5. Wait for synchronization to complete (~10 seconds)
   - You'll see a summary of detected posts

6. View the "Příspěvky" (Posts) section
   - Shows influencer posts with metrics (likes, reach, comments)
   - Displays which influencer created each post

7. Click "📊 Excel Report" to download performance data
   - Generates Excel file with all influencer metrics

The app demonstrates how we use instagram_basic to access our account,
instagram_manage_insights to get engagement metrics, and
pages_read_engagement to detect tagged posts.
```

---

## 🎬 Demo Video Script

**Scénář (2-3 minuty):**

1. **Intro (10s)**
   - "This is Amity Drinks Influencer Monitor dashboard"
   - Show login screen

2. **Login (5s)**
   - Enter credentials
   - Click login

3. **Dashboard Overview (15s)**
   - Show main dashboard
   - Point out influencer list
   - Show current statistics

4. **Synchronization (30s)**
   - Click "🔄 Synchronizovat Instagram" button
   - Show loading/progress
   - Explain: "This fetches posts where influencers tagged @amitydrinks.cz"
   - Show results: "Found X posts from Y influencers"

5. **View Post Details (40s)**
   - Select an influencer
   - Show their posts
   - Point out metrics: likes, reach, comments, date
   - Explain: "We use this data to track campaign performance"

6. **Generate Report (20s)**
   - Click "📊 Excel Report"
   - Show downloaded file
   - Open Excel, show data columns

7. **Outro (10s)**
   - "This helps us measure influencer ROI and compensate fairly"
   - "Only uses publicly available data from our own account"

**Nástroje na nahrávání:**
- **Mac:** QuickTime (Cmd+Shift+5)
- **Windows:** Xbox Game Bar (Win+G)
- **Web:** Loom.com (zdarma)

---

## 🚀 Quick Start - Co Teď

### KROK 1: Upload Privacy & Terms na Web

**Nejrychlejší: GitHub Pages**

```bash
cd /home/mariobracho/influencer
git init
git add public/privacy.html public/terms.html
git commit -m "Add privacy and terms"

# Vytvoř repo na github.com/new
# Pojmenuj: amity-legal

git remote add origin https://github.com/[your-username]/amity-legal.git
git push -u origin main

# Zapni GitHub Pages v Settings → Pages
# URL bude: https://[your-username].github.io/amity-legal/privacy.html
```

**Alternativa: Netlify (Drag & Drop)**
1. Jdi na netlify.com
2. Drag & drop složku `public/`
3. Okamžitě dostaneš URL

### KROK 2: Nahraj Demo Video

1. Spusť dashboard:
```bash
./venv/bin/streamlit run dashboard.py
```

2. Nahraj screencast (2-3 min)
3. Upload na YouTube (unlisted)
4. Zkopíruj URL

### KROK 3: Meta App Review

1. Jdi na [developers.facebook.com](https://developers.facebook.com)
2. My Apps → [Your App] → App Review
3. Permissions and Features
4. Request Advanced Access pro:
   - instagram_basic
   - instagram_manage_insights
   - pages_read_engagement
5. Vyplň formuláře (použij texty výše)
6. Submit

---

## ⏱️ Časový Odhad

| Úkol | Čas |
|------|-----|
| Upload privacy/terms na web | 15 min |
| Nahrání demo video | 20 min |
| Vytvoření test user | 10 min |
| Vyplnění App Review formuláře | 30 min |
| **TOTAL** | **~75 minut** |
| **Meta Review čekání** | **3-7 dní** |

---

## 🎯 Po Schválení

Meta pošle email s výsledkem:

**✅ APPROVED:**
- Access token automaticky získá nová oprávnění
- Restartuj dashboard
- Testuj `/tags` endpoint
- Odstranit manuální @mention workaround

**❌ REJECTED:**
- Přečti feedback od Meta
- Uprav podle požadavků
- Re-submit (neomezené pokusy)

---

## 📞 Potřebuješ Pomoc?

Jsem tady! Stačí říct na kterém kroku jsi a pomohu ti.

**Běžné problémy:**
- Privacy policy nenahraná → použij GitHub Pages nebo Netlify
- Demo video špatná kvalita → nahraj znovu v HD
- Test user nefunguje → zkontroluj permissions

---

**Ready to start?** 🚀

Začni uploadem privacy.html a terms.html na web!
