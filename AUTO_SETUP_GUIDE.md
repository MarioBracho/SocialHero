# 🚀 RYCHLÝ NÁVOD - Auto Setup Script

## Co tento script udělá za vás:

✅ Prodlouží váš token z 1 hodiny na **60 dní**  
✅ Automaticky najde váš **Instagram Business Account ID**  
✅ Automaticky najde váš **Facebook Page ID**  
✅ Vytvoří finální **`.env` soubor** s všemi údaji  
✅ Otestuje připojení k API  

---

## 📋 CO BUDETE POTŘEBOVAT:

Tyto 3 věci, které už máte z Meta Developer Console:

```
1. App ID: 2035208633880002
2. App Secret: [ten co jste zkopírovali]
3. Short-Lived Access Token: [ten co jste právě získali v Graph API Explorer]
```

---

## 🏃 JAK SPUSTIT SCRIPT:

### Krok 1: Uložte script

Stáhněte si soubor `auto_setup_api.py` a uložte ho do složky vašeho projektu.

### Krok 2: Otevřete terminál

```bash
# Windows: PowerShell nebo CMD
# Mac/Linux: Terminal
```

### Krok 3: Přejděte do složky projektu

```bash
cd cesta/k/amity-influencer-monitor
```

### Krok 4: Spusťte script

```bash
python auto_setup_api.py
```

### Krok 5: Zadejte údaje

Script se vás postupně zeptá na:

```
App ID: 2035208633880002
App Secret: [vložte váš secret]
Short-Lived Access Token: [vložte token z Graph API Explorer]
```

### Krok 6: Vyberte stránku

Pokud máte více Facebook stránek, vyberte tu správnou (Amity Drinks).

### Krok 7: Hotovo! 🎉

Script automaticky:
- ✅ Prodlouží token na 60 dní
- ✅ Najde Instagram účet
- ✅ Vytvoří `.env` soubor
- ✅ Otestuje vše

---

## 📄 VÝSTUP

Po dokončení budete mít soubor `.env` s tímto obsahem:

```env
META_APP_ID=2035208633880002
META_APP_SECRET=váš_secret
META_ACCESS_TOKEN=váš_60_denní_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000000
INSTAGRAM_USERNAME=amitydrinks
FACEBOOK_PAGE_ID=123456789012345
...
```

---

## ⚠️ POKUD NĚCO NEJDE:

### Chyba: "Module not found: requests"

```bash
pip install requests
```

### Chyba: "Instagram účet není propojen"

**Řešení:**
1. Jděte na Facebook.com
2. Otevřete stránku Amity Drinks
3. Nastavení → Instagram
4. Připojte Instagram Business účet
5. Spusťte script znovu

### Chyba: "Invalid OAuth access token"

**Řešení:**
- Token možná vypršel
- Vygenerujte nový v Graph API Explorer
- Spusťte script znovu ihned

---

## ✅ CO PO DOKONČENÍ:

1. **Zkontrolujte `.env` soubor** - měl by obsahovat všechny údaje
2. **Doplňte EMAIL_PASSWORD** (volitelné, pro notifikace)
3. **Spusťte aplikaci:**

```bash
# Test připojení
python scripts/test_connection.py

# Monitoring
python main.py --mode check

# Dashboard
streamlit run dashboard.py
```

---

## 💡 TIPY:

- Script můžete spustit vícekrát bez problémů
- Token bude automaticky obnovován každých 60 dní
- `.env` soubor NIKDY nesdílejte a nepřidávejte do gitu!

---

**Hotovo! Nyní máte plně nakonfigurované Meta API a můžete začít používat aplikaci.** 🚀
