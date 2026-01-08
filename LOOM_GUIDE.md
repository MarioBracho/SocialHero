# 📹 Loom.com - Průvodce Nahráváním Demo Videa

---

## 🎯 Proč Používáme Loom.com?

### Výhody Loom pro Meta App Review:

✅ **Nejjednodušší setup** (3 minuty instalace)
- Žádný stažený software
- Funguje jako Chrome extension
- Okamžitý start nahrávání

✅ **Automatický upload**
- Nahrává rovnou do cloudu
- Během nahrávání není potřeba nic stahovat
- Okamžitě dostaneš URL odkaz

✅ **Perfektní kvalita**
- HD kvalita (1080p)
- Nahrává celou obrazovku nebo vybranou záložku
- Zachycuje i zvuk mikrofonu

✅ **Sdílení jedním klikem**
- Po dokončení automaticky vytvoří URL
- URL můžeš rovnou zkopírovat do Meta App Review
- Nemusíš nahrávat na YouTube nebo jinam

✅ **Zdarma pro naše účely**
- Free plan umožňuje neomezená videa
- Max 5 minut per video (náš je 2-3 min ✅)
- Žádná kreditní karta potřeba

✅ **Meta ho akceptuje**
- Meta App Review tým běžně dostává Loom linky
- Podporuje přímé přehrávání v prohlížeči
- Žádné přihlášení potřeba pro viewery

---

## 🚀 Jak na Loom.com - Krok za Krokem

### KROK 1: Registrace (2 minuty)

1. **Otevři:** https://www.loom.com/signup
2. **Zaregistruj se:**
   - Email: mario@amitydrinks.cz (nebo tvůj email)
   - Nebo: "Sign up with Google"
3. **Vyber plan:** FREE (zdarma)
4. **Skip** všechny onboarding kroky

---

### KROK 2: Instalace Chrome Extension (1 minuta)

Po registraci Loom automaticky nabídne instalaci extension:

1. **Klikni:** "Add Loom to Chrome"
2. **Chrome Web Store** se otevře
3. **Klikni:** "Add to Chrome"
4. **Klikni:** "Add extension"
5. **Ikonka Loom** se objeví v Chrome toolbar (vpravo nahoře)

**Alternativa:**
Pokud se nenabídne automaticky, jdi na:
https://chrome.google.com/webstore/detail/loom/liecbddmkiiihnedobmlmillhodjkdmb

---

### KROK 3: Nastavení Loom (1 minuta)

Po instalaci:

1. **Klikni na Loom ikonu** v Chrome toolbar
2. **Sign in** (automaticky přihlášen)
3. **Povolit přístup:**
   - Camera (volitelné - můžeš vypnout)
   - Microphone (pokud chceš mluvit)
   - Screen recording (POVINNÉ)

---

### KROK 4: Příprava před Nahráváním

#### A) Dashboard Ready
```bash
# Spustím dashboard za chvíli (bod 3 tvé žádosti)
./venv/bin/streamlit run dashboard.py
```

#### B) Windows Nastavení
1. **Vypni notifikace:**
   - Windows: `Settings → System → Focus Assist → Priority only`
   - Nebo: `Win + A` → zapni "Focus assist"

2. **Zavři nepotřebné aplikace:**
   - Email klienty
   - Chat aplikace (Slack, Teams, atd.)
   - Zbytečné browser tabs

3. **Připrav script:**
   - Otevři `DEMO_VIDEO_SCRIPT.md`
   - Dej ho na druhý monitor NEBO
   - Vytiskni si ho

#### C) Browser Nastavení
1. **Fullscreen mód:**
   - Chrome: `F11`
2. **Zoom na 100%:**
   - `Ctrl + 0`
3. **Jen potřebné tabs:**
   - Dashboard tab
   - Zavři všechny ostatní

---

### KROK 5: Nahrávání Videa

#### Spuštění Nahrávání:

1. **Otevři dashboard** v Chrome
   - URL: http://localhost:8501

2. **Klikni na Loom ikonu** v Chrome toolbar

3. **Vyber nastavení:**
   - **Screen + Camera:** Vypni (nechceme tvou tvář ve videu)
   - **Screen Only:** ✅ ZAPNI
   - **Microphone:** Zapni (pokud chceš mluvit) nebo Vypni (jen screen)

4. **Vyber co nahrávat:**
   - **Current Tab** (DOPORUČENO) ← Vyberte tuto možnost
   - Nebo: **Full Desktop** (pokud chceš ukazovat víc tabs)

5. **Klikni:** "Start Recording"

6. **Loom ukáže odpočet:** 3... 2... 1...

7. **Začni nahrávat!** 🎬
   - Postupuj podle `DEMO_VIDEO_SCRIPT.md`
   - Nemůžeš pauzovat, takže chystej všechno předem

#### Během Nahrávání:

- **Malá Loom toolbar** bude viditelná v levém dolním rohu
- **Ukazuje čas** - sleduj, ať nepřesáhneš 3 minuty
- **Pause button** - můžeš pauzovat, ale lepší je nahrát celé najednou

#### Ukončení Nahrávání:

1. **Klikni na Loom toolbar** (levý dolní roh)
2. **Klikni:** "Finish"
3. **Loom automaticky uploaduje video** (10-30 sekund)
4. **Otevře se nová stránka** s tvým videem

---

### KROK 6: Po Nahrání

#### Automaticky se otevře Loom video stránka:

**Co vidíš:**
- Náhled videa
- URL link (např. `https://www.loom.com/share/abc123def456`)
- Sharing tlačítka

**Co dělat:**

1. **Přehraj video** - zkontroluj, že všechno vypadá dobře
   - Kvalita OK?
   - Zvuk OK? (pokud jsi mluvil)
   - Všechny kroky jsou tam?

2. **Pokud je video špatné:**
   - Klikni "Delete" (vpravo nahoře)
   - Nahraj znovu

3. **Pokud je video OK:**
   - Klikni "Copy Link" (vpravo nahoře)
   - **Pošli mi URL!** ✅

---

### KROK 7: Optimalizace Videa (Volitelné)

Loom umožňuje **základní úpravy**:

#### Změna Privacy Nastavení:
1. Klikni **"Share"** (vpravo nahoře)
2. Vyber: **"Anyone with the link"** ✅
   - Meta revieweři potřebují přístup bez přihlášení

#### Přidání Titulku:
1. Klikni na titulek (nahoře)
2. Napiš: `Amity Drinks Influencer Monitor - Meta App Review Demo`

#### Trim Video (Odstranit začátek/konec):
1. Klikni **"Edit video"**
2. Klikni **"Trim"**
3. Přesuň slidery na začátek a konec
4. **Save**

---

## 🎬 Alternativní Scénář - "Screen + Webcam"

Pokud chceš vypadat profesionálněji:

1. **Zapni Camera v Loom nastavení**
2. **Tvoje tvář** bude v malém kruhu v rohu videa
3. **Výhoda:** Působí důvěryhodněji pro reviewery
4. **Nevýhoda:** Musíš vypadat prezentovatelně 😄

**Doporučení:** První video nahraj bez webcam. Pokud Meta bude chtít víc info, můžeš nahrát nové s webcam.

---

## 📋 Checklist před "Record"

### Technické:
- [ ] Dashboard běží na http://localhost:8501
- [ ] Dashboard funguje (zkusil jsi sync tlačítko)
- [ ] Loom extension nainstalovaný
- [ ] Loom přihlášen
- [ ] Chrome v fullscreen módu (F11)
- [ ] Zoom 100% (Ctrl+0)

### Obsah:
- [ ] Script připravený (`DEMO_VIDEO_SCRIPT.md`)
- [ ] Víš co říkat / co ukazovat
- [ ] V databázi jsou nějaká data k ukázání
- [ ] Login credentials připravené

### Prostředí:
- [ ] Notifikace vypnuté (Focus Assist)
- [ ] Nepotřebné apps zavřené
- [ ] Stabilní internet
- [ ] Tichý prostor (pokud nahráváš zvuk)

---

## ⚠️ Časté Problémy a Řešení

### "Loom nejde nainstalovat"
**Řešení:** Používáš Chrome/Brave/Edge (Chromium)? Loom nefunguje na Firefoxu.

### "Video se neuploaded"
**Řešení:** Zkontroluj internet. Loom potřebuje stabilní připojení.

### "Nahrál jsem špatně"
**Řešení:** Klidně nahraj znovu! Můžeš nahrát kolikrát chceš (free plan).

### "Video je moc dlouhé (víc než 5 min)"
**Řešení:**
- Free Loom limit je 5 min
- Náš script je 2-3 min, takže OK
- Pokud přesáhneš: nahraj znovu, mluv rychleji

### "Meta nepřijímá Loom link"
**Řešení:**
- Zkontroluj, že video je nastavené na "Anyone with link"
- Otevři link v incognito módu - funguje bez přihlášení?

---

## 🎯 Co Teď?

**Já (Claude) udělám:**
- ✅ Spustím dashboard (tvůj požadavek #3)

**Ty uděláš:**
1. Otevři https://www.loom.com/signup a zaregistruj se
2. Nainstaluj Loom Chrome extension
3. Řekni mi "ready" až budeš mít Loom nainstalovaný

**Pak:**
- Projdeme si dashboard společně
- Nahraješ video podle scriptu
- Pošleš mi Loom URL
- Pokračujeme na KROK 3 (Meta App Review submission)

---

## 📊 Proč Loom vs. Ostatní?

| Nástroj | Pros | Cons | Verdict |
|---------|------|------|---------|
| **Loom** | ✅ Nejjednodušší<br>✅ Okamžitý URL<br>✅ HD kvalita | ⚠️ 5 min limit (OK pro nás) | **WINNER** |
| Xbox Game Bar | ✅ Built-in Windows<br>✅ Zdarma | ❌ Musíš stahovat soubor<br>❌ Upload na YouTube ruční | Složitější |
| OBS Studio | ✅ Profesionální<br>✅ No limits | ❌ Složité nastavení<br>❌ Velká learning curve | Overkill |
| Zoom | ✅ Možná už máš<br>✅ Recording funkce | ❌ Musíš mít Zoom meeting<br>❌ Větší soubory | Komplikovanější |

**Závěr:** Loom je pro naše účely nejlepší volba! ✅

---

**Otázky? Jsem tady!** 🚀
