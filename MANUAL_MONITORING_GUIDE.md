# 📋 AMITY DRINKS - Průvodce Monitoringem Influencerů

## ✅ Co bylo vyřešeno (29.12.2025)

### 1. Opravené chyby
- ✅ **Dashboard error** - Opravena chyba s `cornerradius` v plotly grafech
- ✅ **Access token** - Aktualizován na nový, funkční token
- ✅ **API připojení** - Ověřeno, že Meta API funguje

### 2. Zjištěné omezení Instagram API

**PROBLÉM:** Instagram Graph API neumožňuje automatickou detekci tagů bez schválení aplikace od Meta.

**Endpointy, které NEFUNGUJÍ bez schválení:**
- `/tags` - Vyžaduje `instagram_manage_comments` permission + app review
- `/mentioned_media` - Vyžaduje speciální oprávnění
- Hashtag search - Vyžaduje Business Discovery API access

**Co FUNGUJE:**
- ✅ Základní API připojení
- ✅ Business account media (naše vlastní příspěvky)
- ✅ Manuální zadávání příspěvků

## 🎯 ŘEŠENÍ: Rychlé ruční zadávání v dashboardu

### Jak přidat příspěvek influencera:

1. **Otevřete dashboard**
   ```bash
   http://172.23.45.107:8501
   ```

2. **V levém sidebaru najděte sekci "➕ Přidat Příspěvek"**

3. **Klikněte na "Rychlé zadání"** (rozbalí se formulář)

4. **Vyplňte údaje:**
   - **Influencer** - Vyberte ze seznamu
   - **Typ příspěvku** - Story / Post / Reel
   - **URL** (volitelné) - Link na Instagram příspěvek
   - **Popis** (volitelné) - Krátký popis
   - **Reach** - Dosah příspěvku (z Instagram Insights)
   - **Likes** - Počet lajků

5. **Klikněte "✅ Přidat"**

6. **Dashboard se automaticky aktualizuje** a příspěvek se započítá do statistik

### Výhody tohoto řešení:

✅ **Rychlé** - Zadání příspěvku trvá 10-15 sekund
✅ **Jednoduché** - Všechno v jednom formuláři
✅ **Okamžité** - Statistiky se aktualizují ihned
✅ **Přesné** - Máte kontrolu nad daty
✅ **Flexibilní** - Můžete přidat i starší příspěvky

## 🔄 Workflow pro monitoring

### Denní rutina (doporučeno):

1. **Ráno:** Projděte Instagram účet @amitydrinks.cz
2. **Zkontrolujte notifikace** o označení
3. **Pro každé označení od influencera:**
   - Otevřete jeho profil
   - Zkopírujte URL příspěvku
   - V dashboardu použijte "Rychlé zadání"
   - Zadejte reach a likes (pokud máte přístup k insights)

### Jednou týdně:

1. **Vygenerujte Excel report** pomocí tlačítka "📊 Excel Report"
2. **Zkontrolujte, kdo plní cíle** (zelené checkmarky)
3. **Kontaktujte influencery**, kteří jsou pozadu

## 📊 Přístup k dashboardu

```bash
# Spuštění dashboardu (pokud neběží)
cd /home/mariobracho/influencer
./venv/bin/streamlit run dashboard.py
```

**URL:**
- Local: http://172.23.45.107:8501
- External: http://175.157.53.188:8501

## 🔧 Další možnosti

### Pokud chcete PLNĚ automatický monitoring:

**Možnost 1: App Review od Meta (komplikované)**
- Přihlaste aplikaci k review na Meta Developers
- Vysvětlete, proč potřebujete `instagram_manage_comments`
- Čekejte 2-4 týdny na schválení
- ❌ Složité, časově náročné

**Možnost 2: Third-party nástroje**
- Brand24 - https://brand24.com
- Mention - https://mention.com
- Hootsuite Insights
- ✅ Profesionální monitoring
- ❌ Placené služby ($99-$299/měsíc)

**Možnost 3: Influenceři vám pošlou screenshots**
- Domluvte s influencery, že vám pošlou screenshots insights
- Vy to pak rychle zadáte do dashboardu
- ✅ Jednoduché, přesné data
- ✅ Rychlé (s naším formulářem)

## 📝 Tips & Tricks

### Rychlé zadávání více příspěvků:

1. Otevřete Instagram na PC/telefonu
2. Projděte notifikace označení
3. Pro každé označení:
   - Vpravo: Instagram příspěvek
   - Vlevo: Dashboard s formulářem
   - Kopírujte URL a zadávejte

### Odhad Reach (pokud nemáte přesná čísla):

- **Story:** ~500-2000 (podle velikosti influencera)
- **Post:** ~1000-5000
- **Reel:** ~2000-10000

### Kontrola, zda jste nezapomněli:

1. Dashboard zobrazuje **VŠECHNY influencery** i bez dat
2. Pokud někdo má 0/4 stories → zkontrolujte jeho profil
3. Pokud tam příspěvky jsou → přidejte je

## ❓ FAQ

**Q: Proč automatizace nefunguje?**
A: Instagram API vyžaduje schválení od Meta pro automatickou detekci tagů. Bez tohoto schválení musíme zadávat ručně.

**Q: Jak dlouho trvá zadat jeden příspěvek?**
A: 10-15 sekund s naším rychlým formulářem

**Q: Můžu přidat i starší příspěvky?**
A: Ano! Formulář používá aktuální datum, ale příspěvek se započítá do měsíčních statistik.

**Q: Co když zadám duplicitní příspěvek?**
A: Dashboard zobrazí varování "⚠️ Příspěvek již existuje v databázi"

**Q: Kde najdu reach a likes?**
A: Ideálně se domluvte s influencery, že vám pošlou screenshot Insights. Pokud ne, použijte odhad nebo zadejte 0.

## 🎉 Závěr

I když automatizace přes API není možná bez schválení od Meta, náš rychlý formulář v dashboardu dělá ruční zadávání velmi efektivním. Zadání příspěvku trvá jen pár sekund a máte plnou kontrolu nad daty.

**Doporučený workflow:**
1. Kontrolujte Instagram 1x denně (ráno)
2. Zadávejte příspěvky průběžně (5 minut denně)
3. Generujte reporty 1x týdně

**Potřebujete pomoc?** Otevřete issue na GitHubu nebo kontaktujte tech support.

---

*Last updated: 29.12.2025*
*Dashboard version: 2.0*
