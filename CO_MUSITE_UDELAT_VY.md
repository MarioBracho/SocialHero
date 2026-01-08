# 🎯 CO MUSÍTE UDĚLAT VY - Finální kroky

Udělal jsem za vás maximum! Teď zbývá jen několik kroků, které vyžadují VAŠE účty.

---

## ✅ Co je UŽ HOTOVO (udělal jsem za vás):

- ✅ Přidána autentizace s přihlášením do dashboardu
- ✅ Dashboard připraven pro nasazení na web
- ✅ Config upravený pro Streamlit Cloud
- ✅ Git repozitář inicializován a připraven
- ✅ První commit vytvořen
- ✅ Všechny konfigurační soubory připraveny
- ✅ Dokumentace napsána
- ✅ Citlivé soubory zabezpečeny (.gitignore)

---

## 📋 CO MUSÍTE UDĚLAT VY (5-10 minut):

### KROK 1: Změňte heslo (30 sekund)

Otevřete: `.streamlit/secrets.toml`

Změňte řádek:
```toml
password = "AmityDrinks2026!"  # ← ZMĚŇTE na vaše heslo
```

Na něco jako:
```toml
password = "VaseSilneHeslo123!"
```

**Výchozí přihlašovací údaje:**
- Username: `amity`
- Password: (co jste si nastavili)

---

### KROK 2: Vytvořte GitHub repozitář (2 minuty)

1. **Jděte na:** https://github.com/new

2. **Nastavení repozitáře:**
   - Repository name: `amity-social-hero`
   - Description: "Amity Drinks Social Hero Dashboard"
   - **DŮLEŽITÉ: Vyberte PRIVATE!** ⚠️
   - **NEVYBÍREJTE** "Add README" ani nic jiného

3. **Klikněte:** "Create repository"

4. **Zkopírujte URL** vašeho nového repozitáře:
   ```
   https://github.com/VASE_JMENO/amity-social-hero.git
   ```

---

### KROK 3: Nahrajte kód na GitHub (1 minuta)

Spusťte v terminálu:

```bash
# Přidání vzdáleného repozitáře
git remote add origin https://github.com/VASE_JMENO/amity-social-hero.git

# Push na GitHub
git push -u origin main
```

**Pokud vás to vyzve k přihlášení:**
- Zadejte vaše GitHub username
- Pro heslo použijte **Personal Access Token** (ne vaše GitHub heslo!)
  - Vytvořte token zde: https://github.com/settings/tokens
  - Vyberte "Generate new token (classic)"
  - Dejte mu práva: `repo`
  - Zkopírujte token a použijte místo hesla

---

### KROK 4: Nasaďte na Streamlit Cloud (3 minuty)

1. **Jděte na:** https://streamlit.io/cloud

2. **Přihlaste se:**
   - Klikněte "Sign in with GitHub"
   - Autorizujte Streamlit

3. **Vytvořte aplikaci:**
   - Klikněte "New app"
   - Repository: `VASE_JMENO/amity-social-hero`
   - Branch: `main`
   - Main file path: `dashboard.py`

4. **DŮLEŽITÉ - Nastavte Secrets:**
   - Klikněte "Advanced settings"
   - Najděte sekci "Secrets"
   - Otevřete na vašem počítači: `.streamlit/secrets.toml`
   - **ZKOPÍRUJTE CELÝ OBSAH** tohoto souboru
   - **VLOŽTE** do pole "Secrets" v Streamlit Cloud
   - Klikněte "Save"

5. **Deploy!**
   - Klikněte "Deploy"
   - Počkejte 2-5 minut

---

### KROK 5: Přihlaste se! (10 sekund)

Váš dashboard bude živý na:
```
https://NAZEV-APLIKACE.streamlit.app
```

**Přihlašovací údaje:**
- Username: `amity`
- Password: (co jste nastavili v kroku 1)

---

## 🎉 HOTOVO!

Váš Amity Social Hero dashboard je živý na internetu!

---

## 🔄 Co dál?

### Přidání Meta API (když ji dostanete):

1. Otevřete Streamlit Cloud
2. Jděte na vaši aplikaci → Settings → Secrets
3. Aktualizujte tyto řádky:
   ```toml
   META_APP_ID = "your_real_app_id"
   META_APP_SECRET = "your_real_secret"
   META_ACCESS_TOKEN = "your_real_token"
   FACEBOOK_PAGE_ACCESS_TOKEN = "your_real_page_token"
   INSTAGRAM_BUSINESS_ACCOUNT_ID = "your_real_ig_id"
   FACEBOOK_PAGE_ID = "your_real_fb_page_id"
   ```
4. Klikněte "Save"
5. Aplikace se automaticky restartuje s novými údaji!

**Poznámka:** Dashboard funguje i BEZ Meta API - zobrazí prázdná data nebo demo režim.

---

## 📊 Sdílení s týmem

URL můžete sdílet s kýmkoli:
```
https://vas-nazev.streamlit.app
```

Všichni budou potřebovat:
- Username: `amity`
- Password: (vaše heslo)

### Pokud chcete více uživatelů s různými hesly:

V Streamlit Cloud Secrets přidejte:
```toml
[passwords]
# Hlavní přístup
username = "amity"
password = "hlavni_heslo"

# Další uživatelé
username_marian = "marian"
password_marian = "marianovo_heslo"

username_team = "team"
password_team = "teamove_heslo"
```

(Pak musíte upravit autentizaci v `dashboard.py` - napište mi pokud to budete potřebovat)

---

## 🔒 Bezpečnost - DŮLEŽITÉ!

- ✅ GitHub repo je PRIVATE - nikdy ho nezveřejňujte
- ✅ Nikdy necommitujte `.env` nebo `secrets.toml`
- ✅ Měňte heslo pravidelně
- ✅ Meta API token vyprší za 60 dní - pak ho obnovte

---

## 🆘 Pomoc?

### Problémy s GitHub push:
```bash
# Zkontrolujte remote:
git remote -v

# Změňte URL pokud je špatně:
git remote set-url origin https://github.com/VASE_JMENO/amity-social-hero.git
```

### Problémy se Streamlit Cloud:
- Zkontrolujte Logs v App Settings
- Ověřte že Secrets obsahují CELÝ obsah `secrets.toml`
- Klikněte "Reboot app"

### Přihlášení nefunguje:
- Zkontrolujte heslo v Streamlit Cloud → Settings → Secrets
- Ujistěte se že je sekce `[passwords]` správně

---

## 📞 Kontakt

Email: marian@amitydrinks.cz

---

## 📝 Rychlý checklist:

- [ ] Změnit heslo v `.streamlit/secrets.toml`
- [ ] Vytvořit GitHub repozitář (PRIVATE!)
- [ ] Push kódu na GitHub
- [ ] Registrovat se na Streamlit Cloud
- [ ] Vytvořit novou aplikaci
- [ ] Zkopírovat secrets do Streamlit Cloud
- [ ] Deploy
- [ ] Přihlásit se a otestovat
- [ ] Sdílet URL s týmem

---

**Trvání:** 5-10 minut celkem

**Náročnost:** ⭐⭐☆☆☆ (Snadné - jen copy-paste a klikání)

---

Držím palce! 🍀

Pokud budete mít JAKÝKOLI problém, napište mi na marian@amitydrinks.cz nebo se prostě zeptejte.

---

<div align="center">

**🍹 AMITY DRINKS • social hero • v2.0**

*dobrota je uvnitř*

</div>
