# ⚡ Rychlý start - Nasazení na web za 15 minut

## 📋 Rychlý checklist

### ✅ Co už máte připraveno:
- ✓ `.streamlit/secrets.toml` - přihlašovací údaje a API klíče
- ✓ `.streamlit/config.toml` - konfigurace Streamlit
- ✓ `requirements_web.txt` - závislosti pro web
- ✓ `Procfile` + `railway.json` - konfigurace pro hosting
- ✓ `.gitignore` - ochrana citlivých dat
- ✓ `dashboard_auth.py` - základ dashboardu s autentizací

### 🔧 Co musíte udělat (5 kroků):

#### 1. Přidejte autentizaci do dashboard.py (5 min)
```bash
# Následujte návod v souboru:
cat PRIDANI_AUTENTIZACE.md
```

**NEBO rychle:**
```bash
mv dashboard.py dashboard_original.py
mv dashboard_auth.py dashboard.py
# Pak zkopírujte obsah z dashboard_original.py do dashboard.py
```

#### 2. Změňte heslo (1 min)
Upravte `.streamlit/secrets.toml`:
```toml
[passwords]
username = "amity"
password = "VaseSilneHeslo2026!"  # ← ZMĚŇTE TOTO!
```

#### 3. Nahrajte na GitHub (3 min)
```bash
git init
git add .
git commit -m "Amity Social Hero Dashboard"

# Vytvořte PRIVATE repozitář na https://github.com/new
# Pak:
git remote add origin https://github.com/VASE_JMENO/amity-social-hero.git
git branch -M main
git push -u origin main
```

#### 4. Nasaďte na Streamlit Cloud (5 min)
1. Jděte na https://streamlit.io/cloud
2. Klikněte "New app"
3. Vyberte váš GitHub repozitář
4. Main file: `dashboard.py`
5. V "Advanced settings" → "Secrets": Zkopírujte CELÝ obsah `.streamlit/secrets.toml`
6. Deploy!

#### 5. Hotovo! (1 min)
- URL: `https://vas-nazev.streamlit.app`
- Login: `amity` / `VaseSilneHeslo2026!`

---

## 🎯 Přihlašovací údaje

**Výchozí nastavení:**
- Uživatelské jméno: `amity`
- Heslo: `AmityDrinks2026!` (ZMĚŇTE!)
- Email pro notifikace: `marian@amitydrinks.cz`

---

## 📖 Detailní návody

Pokud potřebujete více informací:

1. **NASAZENI_NA_WEB.md** - Kompletní návod krok po kroku
2. **PRIDANI_AUTENTIZACE.md** - Jak přidat přihlášení
3. **README.md** - Základní info o projektu

---

## ⚠️ DŮLEŽITÉ bezpečnostní poznámky

1. **GitHub repozitář MUSÍ být PRIVATE!**
2. **Nikdy necommitujte `.env` nebo `.streamlit/secrets.toml`**
3. **Změňte výchozí heslo na silné heslo**
4. **Meta API token vyprší za 60 dní** - obnovte přes `python auto_setup_api.py`

---

## 🆘 Problémy?

### Dashboard nejde spustit
```bash
# Nainstalujte závislosti:
pip install -r requirements_web.txt

# Spusťte lokálně:
streamlit run dashboard.py
```

### Přihlášení nefunguje
→ Zkontrolujte `.streamlit/secrets.toml`
→ Ujistěte se, že soubor existuje a obsahuje `[passwords]`

### GitHub odmítá push
→ Zkontrolujte, že jste vytvořili repozitář na GitHubu
→ Zkontrolujte URL: `git remote -v`

### Streamlit Cloud error
→ Zkontrolujte Logs v App Settings
→ Ověřte, že Secrets obsahují CELÝ `.streamlit/secrets.toml`

---

## 📞 Kontakt

Pro technickou podporu: marian@amitydrinks.cz

---

**Úspěšné nasazení!** 🎉

Váš Amity Social Hero dashboard je nyní živý na internetu a chráněný heslem.
