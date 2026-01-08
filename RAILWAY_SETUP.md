# 🚂 Railway.app Setup - Krok po kroku

## ✅ Co je připraveno:
- ✅ Kód je ready pro Railway
- ✅ PostgreSQL podpora přidána
- ✅ Konfigurace vytvořena
- ✅ Admin panel pro správu influencerů

---

## 🚀 CO MUSÍTE UDĚLAT (10 minut):

### KROK 1: Vytvořte Railway účet (2 minuty)

1. **Jděte na:** https://railway.app
2. **Klikněte:** "Start a New Project"
3. **Přihlaste se přes GitHub** (tlačítko "Login with GitHub")
4. **Autorizujte Railway**

---

### KROK 2: Přidejte platební metodu ($5/měs)

1. **Klikněte na** váš profil (pravý horní roh)
2. **Account Settings** → **Billing**
3. **Add Payment Method**
4. **Přidejte kartu**

Railway nabízí **$5 free credit** na zkušení!

---

### KROK 3: Vytvořte nový projekt (3 minuty)

1. **Klikněte:** "New Project"

2. **Vyberte:** "Deploy from GitHub repo"

3. **Autorizujte Railway** přístup k vašim repozitářům

4. **Vyberte repozitář:** `MarioBracho/SocialHero`

5. **Railway automaticky detekuje** Streamlit aplikaci!

6. **Klikněte:** "Deploy Now"

---

### KROK 4: Přidejte PostgreSQL databázi (2 minuty)

1. **V projektu klikněte:** "New" → "Database" → "Add PostgreSQL"

2. **Railway automaticky vytvoří** databázi a propojí ji s aplikací

3. **Database proměnné** se automaticky nastaví!

---

### KROK 5: Nastavte Environment Variables (3 minuty)

1. **Klikněte na vaši aplikaci** (ne databázi)

2. **Najděte:** "Variables" tab

3. **Přidejte tyto proměnné** (klikněte "+ New Variable"):

```bash
# Přihlášení do dashboardu
DASHBOARD_USERNAME=amity
DASHBOARD_PASSWORD=Socialherobracho

# Meta API
META_APP_ID=2035208633880002
META_APP_SECRET=b01381154ce058d2b3e318c1a2507ce6
META_ACCESS_TOKEN=EAAc7AuZBqjcIBQXZBM8Y23w44TTHvpGXcm9tFTf4RpsJZAGRxC2LuKX7xubnwTjZA1kJHJy1JsYxaK5IRiELbNy8ZCXWPAZAF4G3G8AINNkaZC2ZAlNskMon0ViYbdr7lZBNwMZASVH4LzwzLrOnhP8lVUOPHoZAo003Dxz9tiY24Vva3SOpvRlSK0SYGTZCDnhP
FACEBOOK_PAGE_ACCESS_TOKEN=EAAc7AuZBqjcIBQSmLLtg5P8qXJWNQA5SGeHvDMychZCdZB1gws5ubCUZCCpWJ8hsT3DdhBslbIlHcuYgfRB0vkzUFmkBOfJ3VQ00oewQOdZCNvEEEZBDEZBvvxQABUsW2T1PobZBJaOP9jf1XJacL7qokGXoppQxDZAaVZBk4etuDFerxqJu8bZBLJ0PMCxyfQHWEZCmj4pr
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841401076549915
INSTAGRAM_USERNAME=amitydrinks.cz
FACEBOOK_PAGE_ID=965137150187108
META_BUSINESS_ID=2057935615056781

# Email
EMAIL_TO=marian@amitydrinks.cz
```

**Railway automaticky nastaví DATABASE_URL!** (nepotřebujete to přidávat)

---

### KROK 6: Nasaďte aplikaci!

1. **Railway automaticky** začne buildovat aplikaci

2. **Počkejte 3-5 minut** (první build trvá déle)

3. **Sledujte progress** v "Deployments" tabu

---

### KROK 7: Otevřete aplikaci! 🎉

1. **Klikněte na:** "Settings" tab

2. **V sekci "Domains"** klikněte **"Generate Domain"**

3. **Railway vygeneruje URL** jako: `socialhero-production-xxxx.up.railway.app`

4. **Klikněte na URL** → Dashboard se otevře!

---

## 🎯 Přihlašovací údaje:

```
Username: amity
Password: Socialherobracho
```

---

## 🎨 CO MÁ DASHBOARD NOVĚ:

### ⭐ **Admin Panel pro správu influencerů**

V sidebaru najdete sekci **"⚙️ Admin Panel"** kde můžete:

- ➕ **Přidat nového influencera**
- ✏️ **Editovat existující** (jméno, Instagram handle, cíle)
- 🗑️ **Smazat influencera**
- 📊 **Zobrazit všechny influencery**

**Veškeré změny jsou okamžitě viditelné!**

---

## 💾 Import stávajících dat:

### Jak nahrát vaše influencery:

1. **V Admin Panelu** najdete sekci "📥 Import z Excelu"

2. **Nahrajte** váš `influencers_master.xlsx`

3. **Klikněte "Import"**

4. **Hotovo!** Všichni influenceři jsou v databázi

---

## 🔄 Auto-deploy z GitHubu:

**Railway je propojený s GitHubem!**

Když pushne něco na GitHub:
```bash
git push
```

Railway **automaticky redeployuje** aplikaci! 🎉

---

## 💰 Cena:

- **Starter:** $5/měsíc
  - 500 hodin runtime
  - PostgreSQL databáze
  - Dostatečné pro váš dashboard

---

## 🆘 Problémy?

### "Application failed to start"
- Zkontrolujte Logs v Railway (tab "Deployments")
- Ověřte že všechny Environment Variables jsou nastavené

### "Database connection error"
- Ujistěte se že PostgreSQL služba běží
- Railway automaticky nastaví DATABASE_URL

### "Cannot find module"
- Railway automaticky instaluje dependencies z `requirements.txt`

---

## 🎯 Po úspěšném nasazení:

✅ Dashboard běží 24/7
✅ Persistentní PostgreSQL databáze
✅ Admin panel pro správu influencerů
✅ Auto-backup databáze (Railway)
✅ Vlastní URL
✅ Auto-deploy z GitHubu

---

## 📱 Další kroky (volitelné):

### Vlastní doména:
1. Railway Settings → Domains
2. Add Custom Domain
3. Nastavte DNS (např. `dashboard.amitydrinks.cz`)

### SSL Certifikát:
- Railway automaticky poskytuje **free SSL**!

### Monitoring:
- Railway poskytuje metriky v "Observability" tabu

---

## 🎉 HOTOVO!

Váš Amity Social Hero dashboard je nyní na vlastním serveru s persistentní databází!

**URL:** `https://socialhero-production-xxxx.up.railway.app`

---

**Potřebujete pomoct? Napište mi!** 🚀
