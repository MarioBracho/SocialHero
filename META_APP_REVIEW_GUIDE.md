# 🚀 Meta App Review - Kompletní Průvodce

**Datum aktualizace:** 12.01.2026
**Cíl:** Získat oprávnění pro `tagged_users` field → 100% automatická detekce influencer příspěvků

---

## 📊 SOUČASNÝ STAV

### ✅ Co už máme:
- [x] Business verification (Amity Drinks s.r.o.)
- [x] Meta App vytvořena
- [x] Access Token (long-lived)
- [x] Database schema s creator tracking fields
- [x] Webhook handler implementován (čeká na aktivaci)
- [x] 3-tier detection strategy (tagged posts → stories → regex)
- [x] Dashboard na Railway

### ⚠️ Co POTŘEBUJEME od Meta:
- [ ] **instagram_basic** s přístupem k `tagged_users` field
- [ ] **instagram_manage_insights** (insights metriky)
- [ ] **pages_read_engagement** (Facebook tagged posts)

**Proč potřebujeme:** Bez `tagged_users` fieldu nemůžeme identifikovat, KDO vytvořil příspěvek s tagem @amitydrinks.cz

---

## 🎯 PROCES APP REVIEW (Krok za Krokem)

### FÁZE 1: PŘÍPRAVA DOKUMENTACE

#### 1.1 Privacy Policy (POVINNÉ)

Meta vyžaduje veřejně dostupnou Privacy Policy.

**Co musí obsahovat:**
```markdown
# Privacy Policy - Amity Drinks Social Hero Dashboard

Last Updated: [DNEŠNÍ DATUM]

## 1. Overview
This application is an internal marketing analytics tool for Amity Drinks s.r.o.
We use Meta's Instagram Graph API to track performance of influencer collaborations.

## 2. Data We Collect
- Instagram usernames of our 30+ partner influencers
- Public posts/stories where @amitydrinks.cz is tagged
- Public engagement metrics (likes, comments, reach, impressions)
- Post type (story/post/reel)

## 3. How We Use This Data
- Track influencer marketing campaign performance
- Generate monthly performance reports for our marketing team
- Monitor brand mention compliance
- Calculate campaign ROI

## 4. Data We DO NOT Collect
- Private direct messages
- Personal information of Instagram users
- Data from non-partner accounts
- Any data beyond what's publicly visible

## 5. Data Storage & Security
- Data stored in secure PostgreSQL database on Railway (EU servers)
- Access restricted to authorized Amity Drinks staff only
- HTTPS encryption for all data transmission
- Regular security audits
- No third-party data sharing

## 6. Data Retention
- Campaign data retained for 12 months for reporting purposes
- Data can be deleted upon request
- Automatic cleanup of old posts after retention period

## 7. Instagram API Usage
We request the following Meta API permissions:

**instagram_basic (with tagged_users field):**
- Purpose: Identify which influencer tagged @amitydrinks.cz
- Data accessed: Username of post creator, post content, timestamp
- Why needed: Cannot track influencer performance without creator identification

**instagram_manage_insights:**
- Purpose: Retrieve engagement metrics
- Data accessed: Reach, impressions, engagement rate
- Why needed: Measure campaign performance and ROI

**pages_read_engagement:**
- Purpose: Monitor Facebook Page interactions
- Data accessed: Tagged posts on Facebook
- Why needed: Cross-platform influencer tracking

## 8. User Rights
This is an internal business tool for tracking our partner influencers.
All tracked influencers have contractual agreements with Amity Drinks.

Public Instagram data is collected in accordance with Instagram's Terms of Service.
Influencers who tag @amitydrinks.cz consent to public data collection per Instagram's ToS.

For data deletion requests or questions:
- Email: [YOUR EMAIL]
- Instagram: @amitydrinks.cz

## 9. Compliance
We comply with:
- Meta Platform Terms of Service
- GDPR (EU data protection)
- Czech data protection laws
- Instagram Community Guidelines

## 10. Changes to This Policy
We may update this policy as needed.
Last update date is shown at the top of this document.
Significant changes will be communicated to users.

## 11. Contact
For questions or concerns:
- Business: Amity Drinks s.r.o.
- Email: [YOUR EMAIL]
- Instagram: @amitydrinks.cz
```

**Kde vytvořit Privacy Policy:**

**Možnost A - Na vašem webu (ideální):**
```
https://amitydrinks.cz/privacy-policy
```

**Možnost B - GitHub Pages (zdarma, 5 minut):**
1. Vytvořte nový repo `amitydrinks-privacy`
2. Vytvořte `index.html` s Privacy Policy
3. Settings → Pages → Enable
4. URL: `https://[username].github.io/amitydrinks-privacy/`

**Možnost C - Notion/Google Sites (nejrychlejší):**
1. Vytvořte veřejnou stránku na Notion
2. Zkopírujte text Privacy Policy
3. "Share" → "Publish" → Získejte public link

---

#### 1.2 Screen Recording (POVINNÉ)

Meta chce vidět aplikaci v akci. Vytvořte video 3-5 minut.

**CO UKÁZAT ve videu:**

**00:00-00:30 - Intro & Login**
```
1. Otevřít Railway URL dashboardu
2. Ukázat login page
3. Přihlásit se
4. Mluvit: "This is Amity Drinks Social Hero Dashboard -
           an internal tool for tracking our 30+ influencer partners"
```

**00:30-01:30 - Influencer Database**
```
5. Otevřít Admin Panel
6. Ukázat "Seznam Influencerů" (30+ influencerů v databázi)
7. Ukázat sloupce: Jméno, Instagram handle, Měsíční cíle
8. Mluvit: "We collaborate with 30+ Instagram influencers.
           They tag @amitydrinks.cz in their stories and posts.
           Our challenge: automatically identify WHICH influencer
           created each tagged post."
```

**01:30-03:00 - Tagged Posts Detection (KLÍČOVÁ ČÁST!)**
```
9. Přejít na "🔌 Meta API & Synchronizace"
10. Kliknout "🔄 Synchronizovat Instagram"
11. Ukázat log output:
    - "Zkouším stáhnout tagged posts..."
    - "Nalezeno X tagged posts"
    - Ideálně: "✅ Saved post from @dustyfeet_23"

12. DŮLEŽITÉ - Vysvětlit business need:
    "When an influencer tags @amitydrinks.cz, we need to know:
     - WHO created that content (influencer username)
     - What was the reach and engagement
     - Did they meet their monthly targets

     This is why we need the `tagged_users` field from Instagram API.
     Without the creator's username, we cannot track individual
     influencer performance or calculate campaign ROI.

     Stories disappear after 24 hours, so automatic detection
     is critical - manual tracking is impossible at our scale."

13. Přejít na "Stav plnění" tabulku
14. Ukázat příklad influencera s příspěvky:
    - Mario (@dustyfeet_23): 3 stories, 5 posts, 2 reels
    - Reach, engagement metrics
15. Mluvit: "Here we can see individual performance -
            but this only works if we can identify the creator"
```

**03:00-04:00 - Reporting & Analytics**
```
16. Ukázat grafy (Reach over time, Engagement by influencer)
17. Kliknout "📊 Stáhnout Excel Report"
18. Otevřít stažený soubor, ukázat data
19. Mluvit: "We generate monthly reports for management
            showing ROI of each influencer partnership"
```

**04:00-05:00 - Webhook (Budoucnost)**
```
20. (Volitelné) Ukázat webhook_handler.py kód
21. Mluvit: "Once approved, we'll enable real-time webhooks
            for instant notifications when someone tags us"
22. Ukázat webhook endpoint URL
```

**JAK NAHRÁT VIDEO:**

**Software (vyberte jeden):**
- **Loom.com** (nejjednodušší, zdarma) ← DOPORUČENO
- **OBS Studio** (Windows/Mac, free)
- **QuickTime** (Mac: Cmd+Shift+5)
- **Xbox Game Bar** (Windows: Win+G)

**Tips pro nahrávání:**
- ✅ Mluvte ANGLICKY (Meta revieweři jsou mezinárodní)
- ✅ Mluvte pomalu a jasně
- ✅ Ukažte celý flow od začátku do konce
- ✅ Zdůrazněte "tagged_users" potřebu
- ✅ Max 5 minut (ideálně 3-4)
- ✅ HD kvalita (1080p)
- ❌ NEUKAZUJTE: hesla, tokeny, citlivá data

**Kam nahrát:**
- **Loom.com** → automaticky generuje link (nejlepší)
- **YouTube** → Upload jako "Unlisted" video
- **Google Drive** → Nastavte "Anyone with link can view"

---

#### 1.3 Business Use Case (Text pro Meta)

Toto napíšete do formuláře App Review.

**ŠABLONA - Zkopírujte a upravte:**

```
====================================
APP NAME: Amity Drinks Social Hero Dashboard

BUSINESS PURPOSE:
We are Amity Drinks s.r.o., a Czech beverage brand with 30+ active
Instagram influencer partnerships. Our influencers regularly tag
@amitydrinks.cz in their Instagram stories and posts as part of
marketing campaigns.

PROBLEM WE'RE SOLVING:
Instagram stories disappear after 24 hours, making manual tracking
impossible. Currently, we cannot automatically identify WHICH influencer
created a post that tagged us, preventing us from:
- Tracking individual influencer performance
- Calculating campaign ROI
- Verifying contractual obligations (monthly post targets)
- Generating accurate performance reports

REQUESTED PERMISSIONS:
1. instagram_basic (with tagged_users field access)
2. instagram_manage_insights
3. pages_read_engagement

WHY WE NEED tagged_users FIELD:
The `tagged_users` field provides the username of the post creator.
This is ESSENTIAL for our use case because:

1. When someone tags @amitydrinks.cz, we need to match the creator
   username against our database of 30+ partner influencers
2. We automatically record the post with metrics (reach, likes, comments)
3. We calculate if influencer met their monthly targets (e.g., 3 stories/month)
4. We generate monthly performance reports showing ROI per influencer

Without the creator's username from tagged_users, we cannot:
- Distinguish between posts from different influencers
- Track individual performance
- Fulfill our contractual reporting requirements
- Measure campaign effectiveness

DATA USAGE:
- Only track posts where @amitydrinks.cz is tagged
- Only store data from our 30+ verified partner influencers in database
- Only access publicly available Instagram data
- No third-party data sharing
- Full compliance with GDPR and Meta Platform Policies

PRIVACY & SECURITY:
- Secure PostgreSQL database on EU servers (Railway)
- Access restricted to authorized Amity Drinks marketing team only
- HTTPS encryption for all data transmission
- Privacy Policy: [YOUR PRIVACY POLICY URL]
- Compliance with Czech data protection laws

USER CONSENT:
All 30+ influencers have signed partnership agreements with Amity Drinks
that explicitly permit tracking of their @amitydrinks.cz mentions.
We only collect publicly visible Instagram data in accordance with
Instagram's Terms of Service.

====================================
```

---

#### 1.4 Test Instructions (Pro Meta Reviewery)

Meta revieweři potřebují otestovat vaši aplikaci.

**Text do formuláře:**

```
====================================
TEST INSTRUCTIONS FOR META REVIEWERS

DASHBOARD ACCESS:
URL: [YOUR RAILWAY URL - např. https://socialhero-production-xxxx.up.railway.app]
Login Email: admin@amitydrinks.cz
Password: Socialherobracho

TESTING STEPS:

1. LOGIN
   - Go to the URL above
   - Enter credentials
   - You'll see the main dashboard with graphs

2. VIEW INFLUENCER DATABASE
   - Click "👤 Admin Panel" in the left sidebar
   - Expand "📋 Seznam Influencerů"
   - You'll see 30+ influencers with their Instagram handles
   - Note: These are our real partner influencers

3. TEST INSTAGRAM SYNC
   - In Admin Panel, expand "🔌 Meta API & Synchronizace"
   - Click "🔄 Synchronizovat Instagram" button
   - Wait 5-10 seconds
   - System will attempt to fetch tagged posts from Instagram API
   - You'll see log output showing results

4. VIEW RESULTS
   - Scroll to "📊 Stav plnění" table on main page
   - Each row shows an influencer's monthly performance
   - Columns: Stories, Posts, Reels, Reach, Engagement
   - This data comes from tagged posts where @amitydrinks.cz was mentioned

5. EXPORT REPORT
   - Click "📊 Stáhnout Excel Report" button in sidebar
   - Excel file will download with detailed metrics

WHAT YOU'LL SEE:
- Currently, some data may show "žádná data" because we need
  tagged_users field approval to identify post creators
- Once approved, system will automatically detect and track all
  posts where influencers tag @amitydrinks.cz

TECHNICAL NOTE:
- Dashboard is hosted on Railway (EU servers)
- PostgreSQL database with 30+ influencers pre-loaded
- Webhook endpoint ready at /webhook/instagram (will activate post-approval)

For any issues during testing, please contact: [YOUR EMAIL]
====================================
```

---

### FÁZE 2: SUBMITOVÁNÍ APP REVIEW

#### Krok 1: Přístup do Meta Console

1. Jděte na: https://developers.facebook.com/apps/
2. Vyberte vaši aplikaci (Amity Drinks)
3. V levém menu: **App Review** → **Permissions and Features**

#### Krok 2: Request Advanced Access

**Pro každé permission:**

**A) instagram_basic (s tagged_users):**
```
1. Najděte "instagram_basic" v seznamu
2. Klikněte "Request Advanced Access"
3. Vyplňte formulář:

Permission: instagram_basic
Feature: tagged_users field access

Tell us how you'll use this:
[ZKOPÍRUJTE TEXT Z BODU 1.3 - Business Use Case]

Specifically, explain why you need tagged_users:
"The tagged_users field is critical because it provides the
username of the post creator. We need this to match posts
against our database of 30+ partner influencers and track
individual performance. Without this field, we cannot
distinguish between different influencers' posts."

Privacy Policy URL:
[YOUR PRIVACY POLICY URL]

Screencast demonstrating feature usage:
[YOUR LOOM/YOUTUBE VIDEO URL]

Test user instructions:
[ZKOPÍRUJTE TEXT Z BODU 1.4]
```

**B) instagram_manage_insights:**
```
Permission: instagram_manage_insights

Tell us how you'll use this:
"We need access to insights (reach, impressions, engagement)
to measure the performance of tagged posts and calculate
campaign ROI. This data is displayed in our dashboard and
included in monthly reports for management."

[SAME Privacy Policy, Screencast, Test Instructions]
```

**C) pages_read_engagement:**
```
Permission: pages_read_engagement

Tell us how you'll use this:
"We need to track tagged posts on our Facebook Page
(@amitydrinks.cz) for cross-platform influencer tracking.
Some influencers mention us on both Instagram and Facebook."

[SAME Privacy Policy, Screencast, Test Instructions]
```

#### Krok 3: Submit

1. Zkontrolujte všechny vyplněné údaje
2. Klikněte **"Submit for Review"**
3. Obdržíte potvrzení emailem

---

### FÁZE 3: ČEKÁNÍ NA SCHVÁLENÍ (3-7 dní)

**Co Meta kontroluje:**
- ✅ Je aplikace funkční a stabilní?
- ✅ Používáme data jen pro stated purpose?
- ✅ Máme platnou Privacy Policy?
- ✅ Je video jasné a ukazuje use case?
- ✅ Můžou testeři přistoupit k aplikaci?

**Během čekání můžete:**
- ✅ Přidat více influencerů do databáze
- ✅ Testovat manuální přidávání příspěvků
- ✅ Připravit dokumentaci pro tým
- ❌ NEMŮŽETE testovat tagged_users API (vyžaduje schválení)

**Možné výsledky:**
- ✅ **Approved** - Můžete aktivovat API + webhook
- ⚠️ **Needs More Info** - Meta chce upřesnění, odpovězte na otázky
- ❌ **Rejected** - Přečtěte důvod, opravte, re-submitujte

---

### FÁZE 4: PO SCHVÁLENÍ 🎉

**Meta pošle email: "Your permissions have been approved"**

#### Okamžité kroky:

**1. Ověření Permissions**
```
Meta Developer Console → App Dashboard → Permissions
Zkontrolujte:
- instagram_basic: "Advanced Access" ✅
- instagram_manage_insights: "Advanced Access" ✅
- pages_read_engagement: "Advanced Access" ✅
```

**2. Aktivace Webhook**

**A) Vygenerujte Verify Token:**
```bash
# Lokálně nebo na Railway SSH
openssl rand -hex 32
# Zkopírujte výsledek
```

**B) Přidejte do Railway Environment Variables:**
```
Railway Dashboard → Your Project → Variables → New Variable:

Name: WEBHOOK_VERIFY_TOKEN
Value: [TOKEN Z KROKU A]

Deploy changes
```

**C) Konfigurace v Meta Console:**
```
Meta Developer Console → Your App → Products → Webhooks → Instagram

Callback URL: https://socialhero-production-xxxx.up.railway.app/webhook/instagram
Verify Token: [STEJNÝ TOKEN JAKO V RAILWAY]

Klikněte "Verify and Save"

Subscribe to fields:
☑ mentions
☑ media

Klikněte "Subscribe"
```

**D) Test Webhook:**
```bash
# V terminálu otestujte:
curl "https://socialhero-production-xxxx.up.railway.app/webhook/instagram?hub.mode=subscribe&hub.verify_token=YOUR_TOKEN&hub.challenge=test123"

# Mělo by vrátit: test123
```

**3. Update Railway Deployment**

**Upravte startovní příkaz (Railway Settings → Deploy):**

```bash
# STARÝ (současný):
streamlit run dashboard.py --server.port=$PORT

# NOVÝ (s webhookem):
python webhook_server.py & streamlit run dashboard.py --server.port=$PORT
```

Nebo update `railway.toml`:
```toml
[deploy]
startCommand = "python webhook_server.py & streamlit run dashboard.py --server.port=$PORT"
```

**4. Test Tagged Posts API**

```
Dashboard → Admin Panel → 🔄 Synchronizovat Instagram

Měli byste nyní vidět:
✅ "Nalezeno X tagged posts" (NOVĚ FUNKČNÍ!)
✅ "✅ Saved post from @dustyfeet_23 (method: api_tags)"

Check Railway logs:
railway logs --tail
```

**5. Test Real-time Webhook (KRITICKÝ TEST)**

**A) Vytvořte testovací story:**
```
1. Na vašem osobním IG účtu (nebo influencer účtu)
2. Vytvořte story
3. Označte @amitydrinks.cz (použijte @ sticker nebo text)
4. Publikujte
```

**B) Sledujte Railway logs:**
```bash
railway logs --tail

Během 1-2 minut by se mělo objevit:
📨 Webhook received: {...}
🏷️ Tagged by @[username] in media [media_id]
✅ Webhook mention processed: @[username]
```

**C) Ověřte v dashboardu:**
```
Refresh dashboard
→ Měl by se objevit nový příspěvek
→ detection_method: webhook
→ creator_username: váš handle
→ Pokud jste v databázi jako influencer, měly by se aktualizovat stats
```

---

## 🔍 MONITORING PO AKTIVACI

### Den 1-7: Intenzivní monitoring

**Dashboard Metriky:**
- [ ] Nové příspěvky se ukládají s `detection_method: api_tags` nebo `webhook`
- [ ] Creator username správně mapován na influencer ID
- [ ] Měsíční stats se aktualizují automaticky
- [ ] Webhook endpoint responds 200 OK

**Railway Logs (denně):**
```bash
railway logs --tail

Hledejte:
✅ "🔄 Spouštím Instagram sync"
✅ "Nalezeno X tagged posts"
✅ "✅ Saved post from @username (method: api_tags)"
✅ "📨 Webhook received"
✅ "✅ Webhook mention processed"

Varování:
⚠️ "ℹ️ Přeskakuji @username (není v databázi)" - OK, očekávané
❌ "Invalid webhook signature" - PROBLÉM: Check WEBHOOK_VERIFY_TOKEN
❌ "403 Forbidden" - PROBLÉM: Check permissions v Meta Console
❌ "Could not fetch media" - PROBLÉM: Check Access Token validity
```

**Test Checklist (každý den prvních 7 dní):**
- [ ] Ranní sync (Dashboard → Synchronizovat Instagram)
- [ ] Check počet nových příspěvků za 24h
- [ ] Verify že všechny známé influenceři byli detekováni
- [ ] Check Railway logs pro errors
- [ ] Test webhook s reálnou story (každé 2-3 dny)

---

## ❌ CO DĚLAT PŘI ODMÍTNUTÍ

Meta může žádost odmítnout. Nejčastější důvody:

### Důvod 1: Neúplná nebo obecná Privacy Policy
**Řešení:**
- Přidejte konkrétnější sekce o data retention (12 měsíců)
- Přidejte sekci o user rights (data deletion request process)
- Přidejte contact info
- Ujistěte se že URL je veřejně dostupný (ne za loginem)

### Důvod 2: Nejasný business use case
**Řešení:**
- Přepište s KONKRÉTNÍMI čísly (30+ influencers)
- Zdůrazněte proč NEMŮŽETE fungovat bez tagged_users
- Vysvětlete business impact (ROI tracking, contractual compliance)
- Přidejte "Without this field, we cannot..." sekci

### Důvod 3: Video neukazuje použití tagged_users
**Řešení:**
- Nahrajte nové video
- Explicitně ukažte:
  - Kliknutí na sync button
  - Log output s "username" fieldem
  - Tabulku s creator_username sloupcem
- Slovně vysvětlete: "This username comes from the tagged_users field"

### Důvod 4: App není production-ready nebo nefunguje
**Řešení:**
- Ujistěte se že Railway deployment je stabilní
- Test login credentials fungují
- Dashboard se načte bez errors
- Sync button funguje (i když bez tagged_users nevrátí plná data)

### Důvod 5: Chybějící nebo nefunkční test user
**Řešení:**
- V Meta Console: App → Roles → Test Users
- Create new test user
- Přidejte test user credentials do formuláře
- Verify že test user může přistoupit k dashboardu

### Re-submit Process:
```
1. Meta Console → App Review → View Feedback
2. Přečtěte důvod odmítnutí (může být několik)
3. Opravte každý zmíněný problém
4. Update formulář s vylepšeními
5. Klikněte "Re-submit for Review"
6. Čekejte dalších 3-7 dní
```

**Neomezeně můžete re-submitovat!** Meta nepenalizuje za opakované žádosti.

---

## 🔄 FALLBACK PLÁNY (Pokud Meta trvale odmítá)

### Plan B: Hashtag-Based Detection

**Koncept:**
Influenceři používají specifický hashtag: `#AmityPartner` nebo `#AmityDrinks`

**Implementace:**
```python
# V meta_api.py
def search_hashtag(self, hashtag: str):
    url = f"{self.base_url}/ig_hashtag_search"
    params = {
        'user_id': self.ig_account_id,
        'q': hashtag
    }
    # Vrací posts s tímto hashtagem
    # Stále obsahuje username!
```

**Výhody:**
- Nevyžaduje tagged_users permission
- Funguje okamžitě
- Stále vrací creator username

**Nevýhody:**
- Vyžaduje spolupráci influencerů (musí používat hashtag)
- Méně spolehlivé než tagged posts

### Plan C: Stories Mentions Polling

**Koncept:**
Stahovat stories každé 2 hodiny, hledat @amitydrinks.cz mentions

**Implementace:**
```python
# Už částečně implementováno v sync_instagram.py
def _sync_stories(self):
    stories = self.api.get_instagram_stories()
    # Hledat @amitydrinks.cz v caption nebo mentions
```

**Výhody:**
- Funguje s basic permissions
- Žádné extra requirements

**Nevýhody:**
- Pouze 80% spolehlivost
- Musí běžet každé 2h (stories mizí po 24h)
- Rate limit concerns

### Plan D: Hybrid Approach (80/20 řešení)

**Koncept:**
Kombinace všech dostupných metod:
1. Caption regex (@mentions)
2. Hashtag search
3. Stories polling
4. Manuální doplnění zbylých 20%

**Výhody:**
- Realistické pro začátek
- Funguje okamžitě
- Postupně se zlepšuje

**Nevýhody:**
- Není 100% automatické
- Více komplexní logika

---

## 📋 FINAL CHECKLIST PŘED SUBMITOVÁNÍM

### Dokumentace:
- [ ] Privacy Policy vytvořena
- [ ] Privacy Policy URL je veřejně dostupný
- [ ] Screen recording nahráno (3-5 min, anglicky)
- [ ] Video URL funguje (není privátní)
- [ ] Business use case napsán (zdůrazňuje tagged_users potřebu)
- [ ] Test instructions připraveny

### Aplikace:
- [ ] Dashboard na Railway běží stabilně
- [ ] Login credentials fungují
- [ ] Admin panel zobrazuje 30+ influencerů
- [ ] Sync button funguje (i když bez plných dat před schválením)
- [ ] Žádné crash errors v dashboardu

### Meta App:
- [ ] App vytvořena v Meta Console
- [ ] Instagram Graph API přidána jako Product
- [ ] Basic permissions už máte (instagram_basic, atd.)
- [ ] Access Token je long-lived a platný
- [ ] Test v dashboardu: "🧪 Test Meta API" = zelená ✅

### Webhook (připravený, čeká na aktivaci):
- [ ] webhook_handler.py existuje
- [ ] webhook_server.py existuje
- [ ] Flask v requirements.txt

**Když máte všechny checkboxy ✅, můžete submitovat!**

---

## ⏱️ TIMELINE

| Fáze | Akce | Čas |
|------|------|-----|
| **Den 1** | Vytvoření Privacy Policy | 30 min |
| **Den 1** | Upload Privacy Policy na web | 15 min |
| **Den 1** | Nahrání screen recording | 45 min |
| **Den 1** | Vyplnění App Review formuláře | 30 min |
| **Den 1** | Submit for Review | 5 min |
| **Den 2-8** | **Čekání na Meta Review** | 3-7 dní |
| **Den 9** | Schválení → Aktivace webhook | 30 min |
| **Den 9** | Testing & verification | 1 hod |
| **Den 10+** | Production monitoring | ongoing |

**TOTAL čas na přípravu: ~2 hodiny**
**TOTAL čas čekání: 3-7 dní**
**TOTAL od startu k 100% automatizaci: ~1-2 týdny**

---

## 🎯 CO ZÍSKÁME PO SCHVÁLENÍ

### ✅ 100% Automatická Detekce:
- Influencer označí @amitydrinks.cz → **okamžitě detekováno** (webhook)
- System automaticky identifikuje **KDO** vytvořil příspěvek
- Automatické přiřazení k správnému influencerovi v databázi
- **Žádné manuální zadávání** @mentions

### ✅ Real-time Tracking:
- Webhook notifikace během **1-2 minut** po publikování
- Stories zachyceny **před 24h expirací**
- Okamžitá aktualizace dashboardu

### ✅ Kompletní Insights:
- Reach a impressions pro každý příspěvek
- Engagement rate kalkulace
- Demografické data (pokud dostupné)
- Best performing posts analytics

### ✅ Reporty & Analytics:
- Automatické měsíční reporty
- Export do Excelu jedním kliknutím
- ROI tracking per influencer
- Compliance verification (splnění měsíčních cílů)

---

## 📞 PODPORA & RESOURCES

**Meta Developer Support:**
- Community: https://developers.facebook.com/community/
- Bug Reports: https://developers.facebook.com/support/bugs/
- Live Chat: https://developers.facebook.com/support/ (business hours)

**Dokumentace:**
- Instagram Graph API: https://developers.facebook.com/docs/instagram-api
- App Review Guidelines: https://developers.facebook.com/docs/app-review
- Webhooks Setup: https://developers.facebook.com/docs/graph-api/webhooks
- Platform Policies: https://developers.facebook.com/docs/development/release/policies

**Užitečné Odkazy:**
- Graph API Explorer: https://developers.facebook.com/tools/explorer/
- Access Token Debugger: https://developers.facebook.com/tools/debug/accesstoken/

---

## 🚀 READY TO START?

### Immediate Next Steps:

**1. Vytvořte Privacy Policy** (30 min)
```
Zkopírujte template z sekce 1.1
Upravte [YOUR EMAIL] a další placeholdery
Vytvořte HTML stránku
Nahrajte na web (GitHub Pages / Notion / váš web)
```

**2. Nahrajte Demo Video** (45 min)
```
Otevřete Loom.com (nebo OBS Studio)
Nahrajte 3-5 min screencast podle sekce 1.2
Upload a získejte public link
```

**3. Submitujte App Review** (30 min)
```
Meta Console → App Review → Permissions
Vyplňte formulář podle sekce FÁZE 2
Zkopírujte business use case ze sekce 1.3
Vložte Privacy Policy URL a Video URL
Submit!
```

**4. Čekejte 3-7 dní** ⏳

**5. Po schválení: Aktivujte webhook** (30 min)
```
Následujte sekci FÁZE 4
Test všechny funkce
Začněte monitoring
```

---

**Success! Po schválení budete mít plně automatizovaný influencer tracking system. 🎉**

Pokud máte otázky během procesu, Meta Developer Support obvykle odpovídá do 24 hodin.

Hodně štěstí! 🍀
