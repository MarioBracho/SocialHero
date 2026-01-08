# 🔄 Automatizace po schválení Meta API

## 📋 Aktuální stav

**Datum:** 29.12.2025
**Status:** ⏳ Čeká se na schválení Meta App Review

### Co je připraveno:

✅ Dashboard funkční s manuálním zadáváním
✅ API klient připraven (`src/api/meta_api.py`)
✅ Monitoring logika implementována (`src/monitoring/monitor.py`)
✅ Scheduler pro automatické spouštění (`src/monitoring/scheduler.py`)
✅ Access token aktuální a funkční

### Co čeká na schválení:

⏳ Meta App Review pro `instagram_manage_comments` permission
⏳ Aktivace `/tags` endpointu

## 🚀 Kroky k aktivaci automatizace (po schválení)

### KROK 1: Ověření oprávnění

Po schválení od Meta ověřte, že máte následující permissions:

```bash
./venv/bin/python3 -c "
from src.api.meta_api import MetaAPIClient
api = MetaAPIClient()

# Test permissions
print('Testuji /tags endpoint...')
tags = api.get_instagram_tags(limit=5)
if tags:
    print(f'✅ /tags funguje! Nalezeno {len(tags)} tagů')
else:
    print('❌ /tags stále nefunguje - zkontrolujte permissions')
"
```

### KROK 2: Test manuálního spuštění

Otestujte monitoring manuálně:

```bash
cd /home/mariobracho/influencer
./venv/bin/python3 main.py --mode check --hours 168
```

**Očekávaný výstup:**
```
🔍 Kontroluji Instagram tagy (posledních 168h)...
✅ Nalezeno X Instagram tagů
🎯 Nalezeno Y nových příspěvků
```

### KROK 3: Aktivace automatického scheduleru

Spusťte scheduler, který bude kontrolovat tagy 2x denně:

```bash
# Spuštění na pozadí
nohup ./venv/bin/python3 main.py --mode auto > logs/scheduler.log 2>&1 &

# Nebo pomocí systemd služby (doporučeno)
sudo systemctl start amity-monitor
sudo systemctl enable amity-monitor
```

### KROK 4: Odebrání manuálního formuláře (volitelné)

Pokud chcete odstranit manuální formulář z dashboardu:

**Soubor:** `dashboard.py`
**Řádky:** 321-393

Zakomentujte nebo smažte sekci:
```python
# Rychlé přidání příspěvku
st.markdown("### ➕ Přidat Příspěvek")
...
```

**NEBO** nechte formulář jako backup pro ruční zadávání.

## 📊 Automatický monitoring - Jak to bude fungovat

### Schedule (default):

```
09:00 - První denní kontrola
17:00 - Druhá denní kontrola
18:00 - Denní souhrn (email)
1. den v měsíci, 08:00 - Měsíční report
```

### Co se bude dít automaticky:

1. **Kontrola Instagram tagů** (`/tags` endpoint)
   - Najde příspěvky, kde byl @amitydrinks označen
   - Identifikuje autora (influencer)
   - Přidá do databáze

2. **Kontrola Facebook tagů** (`/tagged` endpoint)
   - Stejný proces pro Facebook

3. **Aktualizace statistik**
   - Automatický přepočet měsíčních metrik
   - Kontrola plnění cílů

4. **Email notifikace**
   - Nové příspěvky
   - Denní souhrn
   - Měsíční report

### Konfigurace:

**Soubor:** `.env`

```bash
# Časování kontrol
FIRST_CHECK_TIME=09:00
SECOND_CHECK_TIME=17:00
CHECK_INTERVAL_HOURS=12

# Email notifikace
EMAIL_ENABLED=true
EMAIL_TO=marketing@amitydrinks.cz
```

## 🔧 Kód připravený k aktivaci

### Metoda pro Instagram tagy (již implementována):

**Soubor:** `src/api/meta_api.py:138-165`

```python
def get_instagram_tags(self, limit: int = 50) -> List[Dict]:
    """
    Získá příspěvky, ve kterých byl účet označen (tagged)
    """
    url = f"{self.base_url}/{self.ig_account_id}/tags"
    # ... kód připraven, čeká na permissions
```

### Monitoring check (již implementován):

**Soubor:** `src/monitoring/monitor.py:22-110`

```python
def check_instagram_tags(self, since_hours: int = 12) -> List[Dict]:
    """
    Zkontroluje Instagram tagy za posledních X hodin
    """
    # Získání tagů z API
    tags = self.api.get_instagram_tags(limit=50)
    # Filtrování podle influencerů
    # Přidání do databáze
    # ... vše připraveno
```

### Scheduler (již implementován):

**Soubor:** `src/monitoring/scheduler.py:19-134`

```python
class MonitorScheduler:
    def monitoring_job(self):
        # Automatický monitoring 2x denně
        results = self.monitor.run_check(since_hours=12)
        # Email notifikace
        # ... vše připraveno
```

## ✅ Checklist pro přechod na automatizaci

- [ ] Meta App Review schválena
- [ ] Permissions ověřeny (test `/tags` endpoint)
- [ ] Manuální test monitoringu proběhl úspěšně
- [ ] Email notifikace nakonfigurovány
- [ ] Scheduler spuštěn a testován
- [ ] Dashboard funguje bez manuálního formuláře (volitelné)
- [ ] Team proškolen o automatickém systému
- [ ] Dokumentace aktualizována

## 📞 Jak požádat o Meta App Review

### 1. Přejděte do Meta for Developers

URL: https://developers.facebook.com/apps/2035208633880002/app-review/permissions/

### 2. Vyžádejte permissions:

- `instagram_manage_comments` ← KLÍČOVÉ pro /tags endpoint
- `instagram_manage_insights`
- `pages_read_engagement`

### 3. Vyplňte formulář:

**Účel použití:**
```
Monitoring značkování (tagging) Instagram účtu @amitydrinks.cz
influencery pro marketingové reporty. Potřebujeme automaticky
detekovat, kdy influencer označil náš brand v příspěvku nebo
story, abychom mohli sledovat spolupráce a měřit dosah kampaní.
```

**Detaily:**
- Screenshot dashboardu
- Vysvětlení business use case
- Bezpečnostní opatření

### 4. Připravte screencapture/video:

Meta vyžaduje demo, jak používáte permissions:
- Ukázka dashboardu
- Ukázka monitoringu
- Ukázka reportů

### 5. Čekací doba:

⏰ Typicky 2-4 týdny
📧 Meta vás kontaktuje emailem

## 💡 Pro-tipy

### Tip 1: Kombinace auto + manuální

I po aktivaci automatizace můžete nechat manuální formulář:
- Automatizace běží na pozadí
- Manuální formulář pro okamžité doplnění
- Best of both worlds

### Tip 2: Monitoring logů

```bash
# Sledování scheduler logů
tail -f logs/amity_monitor.log

# Kontrola posledních příspěvků
./venv/bin/python3 main.py --mode stats
```

### Tip 3: Test s dummy daty

Před aktivací otestujte celý flow s testovacími daty:
```bash
# Přidání testovacího příspěvku
./venv/bin/python3 add_post_manual.py
```

## 📝 Poznámky pro vývojáře

### Změny potřebné po schválení:

**ŽÁDNÉ!**

Všechen kód je připraven. Stačí:
1. Ověřit, že `/tags` endpoint funguje
2. Spustit scheduler

### Fallback strategie:

Pokud `/tags` stále nefunguje:
1. Použít `/mentioned_media` endpoint (alternativa)
2. Použít hashtag monitoring
3. Pokračovat s manuálním zadáváním

### Monitoring endpointu:

Přidejte do `src/api/meta_api.py` tracking:

```python
def get_instagram_tags(self, limit: int = 50) -> List[Dict]:
    api_logger.info(f"Calling /tags endpoint...")

    data = self._make_request(url, params)

    if data is None:
        api_logger.error("TAGS ENDPOINT FAILED - check permissions")
        # Fallback na manuální nebo alternativní metodu

    return data.get('data', []) if data else []
```

---

**Připravil:** Claude Sonnet 4.5
**Datum:** 29.12.2025
**Status:** Připraveno k aktivaci po Meta approval
