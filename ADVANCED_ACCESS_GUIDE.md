# 🔐 NÁVOD: Meta Advanced Access & Business Verification

---

## 📋 CO POTŘEBUJETE

Důvod: **Automatická detekce tagů od influencerů vyžaduje Advanced Access**

Bez Advanced Access:
- ❌ Nemůžete číst tagy od jiných uživatelů
- ❌ API vrací chybu: "(#10) Application does not have permission"
- ✅ Můžete pouze číst vlastní příspěvky

S Advanced Access:
- ✅ Automatická detekce všech tagů
- ✅ Plně funkční monitoring systém
- ✅ Žádné manuální přidávání

---

## 🚀 KROK 1: META BUSINESS VERIFICATION

### 1.1 Otevřete Meta App Dashboard

```
https://developers.facebook.com/apps/2035208633880002/dashboard/
```

### 1.2 Přejděte na App Settings

1. V levém menu klikněte na **"Settings"** → **"Basic"**
2. Scrollujte dolů k sekci **"Business Verification"**

### 1.3 Spusťte Business Verification

Klikněte na **"Start Verification"** nebo **"Get Verified"**

### 1.4 Vyplňte informace o firmě

Budete potřebovat:

**Základní informace:**
- ✅ Oficiální název firmy: **Amity Drinks s.r.o.** (nebo jak je registrována)
- ✅ Adresa firmy (úplná)
- ✅ Telefonní číslo firmy
- ✅ Email firmy
- ✅ Webové stránky: **https://amitydrinks.cz** (pokud máte)

**Dokumenty (potřebujete JEDEN z těchto):**
- 📄 Výpis z obchodního rejstříku (nejlepší varianta pro ČR)
- 📄 IČO dokumentace
- 📄 Daňové doklady
- 📄 Živnostenský list

**Kde získat výpis z obchodního rejstříku:**
```
https://or.justice.cz/ias/ui/rejstrik
```
1. Vyhledejte "Amity Drinks"
2. Stáhněte si aktuální výpis jako PDF
3. Nahrajte do Meta

### 1.5 Počkejte na schválení

⏰ **Obvykle trvá: 1-3 pracovní dny**

Dostanete email na adresu spojenou s Meta účtem.

---

## 🔑 KROK 2: POŽÁDAT O ADVANCED ACCESS

### 2.1 Přejděte na App Review

```
https://developers.facebook.com/apps/2035208633880002/app-review/
```

Nebo v levém menu: **"App Review"** → **"Permissions and Features"**

### 2.2 Najděte Instagram Permissions

Vyhledejte nebo scrollujte k:
- **`instagram_basic`** (už máte)
- **`instagram_manage_insights`** (už máte nebo potřebujete)
- **`instagram_content_publish`** (možná potřebujete)

### 2.3 Klíčová oprávnění pro tagging

Potřebujete požádat o:

#### A) **instagram_basic** - Advanced Access
- **Co to umožňuje:** Číst tagy od jiných uživatelů
- **Status:** Pravděpodobně máte jen Basic
- **Potřeba:** Advanced Access

#### B) **instagram_manage_insights** - Advanced Access
- **Co to umožňuje:** Číst metriky (likes, comments, reach)
- **Potřeba:** Advanced Access

### 2.4 Klikněte na "Request Advanced Access"

Pro každé oprávnění:

1. Klikněte na tlačítko **"Request Advanced Access"** nebo **"Get Advanced Access"**

2. **Vyplňte formulář:**

**Použití aplikace (App Use Case):**
```
Monitoring influencer marketing campaigns for Amity Drinks.
The app monitors Instagram posts where @amitydrinks is tagged
by our influencer partners to track campaign performance and
engagement metrics.
```

**Důvod pro data (Why do you need this data?):**
```
We need to automatically detect when influencers tag our brand
(@amitydrinks) in their Instagram stories and posts. This data
is used to:
- Track influencer campaign deliverables
- Monitor brand mentions and reach
- Measure engagement metrics (likes, comments, reach)
- Generate monthly performance reports
```

**Jak budete data používat (How will you use this data?):**
```
The data will be used internally by Amity Drinks marketing team to:
1. Verify influencer contract fulfillment (number of posts/stories)
2. Analyze campaign performance metrics
3. Generate automated reports for stakeholders
4. Monitor brand awareness and engagement

Data is NOT shared with third parties and is only used for
internal marketing analytics.
```

### 2.5 Screencasts nebo Screenshots

Meta může požadovat **video nebo screencasts** ukazující, jak aplikaci používáte.

**Připravte:**

1. **Screenshot dashboardu** (dashboard.py běžící)
   - Ukažte tabulku influencerů
   - Ukažte grafy a metriky

2. **Screenshot Excel reportu**
   - Ukažte vygenerovaný měsíční report
   - Zvýrazněte, jak tracujete příspěvky

3. **Video (volitelné, ale doporučené):**
   - 30-60 sekund
   - Ukažte spuštění `python main.py --mode check`
   - Ukažte dashboard s příspěvky
   - Ukažte Excel report

**Nástroj na nahrávání:**
- Windows: Xbox Game Bar (Win + G)
- Linux: SimpleScreenRecorder, OBS Studio
- Mac: QuickTime Player

### 2.6 Odeslat žádost

Klikněte **"Submit"** nebo **"Send"**

---

## ⏰ KROK 3: ČEKÁNÍ NA SCHVÁLENÍ

### Časová osa:

```
📅 Den 0:  Odeslání žádosti
📅 Den 1-2: Meta může požádat o další informace
📅 Den 3-5: Obvyklá doba schválení
📅 Den 7:  Pokud stále čekáte, kontaktujte support
```

### Co dělat během čekání:

✅ **Pokračujte v manuálním přidávání:**
```bash
./venv/bin/python3 add_post_manual.py
```

✅ **Používejte dashboard:**
```bash
streamlit run dashboard.py
```

✅ **Generujte reporty:**
```bash
python main.py --mode report
```

---

## 📧 KROK 4: PO SCHVÁLENÍ

Jakmile dostanete email **"Your request for Advanced Access has been approved"**:

### 4.1 Ověřte nová oprávnění

```bash
./venv/bin/python3 main.py --mode test
```

Mělo by vypsat:
```
✅ API připojení funguje!
✅ Advanced Access aktivní
```

### 4.2 Spusťte první automatický check

```bash
./venv/bin/python3 main.py --mode check --hours 168
```
(168 hodin = 7 dní - zkontroluje všechny tagy za poslední týden)

### 4.3 Spusťte automatický scheduler

```bash
./venv/bin/python3 main.py --mode auto
```

Od této chvíle bude systém automaticky:
- ✅ Detekovat nové tagy 2x denně (9:00 a 17:00)
- ✅ Odesílat denní souhrny (18:00)
- ✅ Generovat měsíční reporty (1. den v měsíci)

---

## ❓ TROUBLESHOOTING

### "Business Verification zamítnuta"

**Možné důvody:**
- ❌ Neplatné nebo neúplné dokumenty
- ❌ Nesoulad mezi názvem firmy a dokumenty
- ❌ Chybějící informace

**Řešení:**
1. Zkontrolujte všechny dokumenty
2. Ujistěte se, že jsou aktuální (ne starší než 1 rok)
3. Odešlete znovu s kompletními informacemi

### "Advanced Access zamítnuto"

**Možné důvody:**
- ❌ Nedostatečné vysvětlení použití
- ❌ Chybějící screencasts
- ❌ Aplikace nevypadá legitimně

**Řešení:**
1. Poskytněte podrobnější vysvětlení use case
2. Nahrajte screencasts/video
3. Ukažte fungující dashboard a reporty
4. Odešlete novou žádost (můžete zkusit znovu)

### "Chci to urychlit"

Meta nepodporuje urychlenou review, ale můžete:
1. Ujistit se, že všechny informace jsou kompletní
2. Přidat video ukázku fungující aplikace
3. V komentářích zmínit, že je to pro business marketing monitoring

---

## 📝 RYCHLÝ CHECKLIST

Před odesláním žádosti zkontrolujte:

```
☐ Business Verification spuštěna
☐ Výpis z obchodního rejstříku nahrán
☐ Všechny firemní údaje vyplněny
☐ Advanced Access žádost odeslána pro:
  ☐ instagram_basic
  ☐ instagram_manage_insights
☐ Use case detailně popsán
☐ Screenshots dashboardu přiloženy
☐ Screenshots Excel reportu přiloženy
☐ (Volitelné) Video screencast nahrán
```

---

## 🆘 KONTAKT NA META SUPPORT

Pokud máte problémy:

1. **Meta Developer Support:**
   ```
   https://developers.facebook.com/support/
   ```

2. **Community Forum:**
   ```
   https://developers.facebook.com/community/
   ```

3. **Bug Report:**
   ```
   https://developers.facebook.com/support/bugs/
   ```

---

## ✅ SHRNUTÍ

1. **Business Verification** (1-3 dny)
   - Nahrajte výpis z OR
   - Vyplňte firemní údaje

2. **Advanced Access Request** (3-5 dní)
   - Popište use case (influencer monitoring)
   - Nahrajte screenshots/video
   - Odešlete žádost

3. **Po schválení**
   - Test API
   - Spusťte automatický monitoring
   - Užívejte si plně automatický systém!

---

**Odhadovaná celková doba: 5-8 pracovních dní**

*Během čekání používejte `add_post_manual.py` pro ruční přidávání příspěvků.*

---

📅 **Verze:** 1.0
📆 **Datum:** 29.12.2025
🍹 **Amity Drinks Influencer Monitor**
