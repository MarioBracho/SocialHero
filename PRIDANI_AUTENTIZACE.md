# 🔐 Přidání autentizace do dashboard.py

## Rychlý návod

Máte 2 možnosti:

### Možnost 1: Použít připravený dashboard_auth.py (JEDNODUŠŠÍ)

1. **Přejmenujte soubory:**
   ```bash
   mv dashboard.py dashboard_original.py
   mv dashboard_auth.py dashboard.py
   ```

2. **Zkopírujte obsah z originálu:**
   - Otevřete `dashboard_original.py`
   - Zkopírujte **CELÝ CSS kód a zbytek aplikace** (od řádku 35 do konce)
   - Vložte ho do `dashboard.py` **MÍSTO info boxu** (nahraďte řádky od "st.info" až po konec)

3. **Hotovo!** Dashboard má nyní autentizaci.

---

### Možnost 2: Upravit původní dashboard.py ručně

#### Krok 1: Přidejte autentizaci na ZAČÁTEK souboru

Otevřete `dashboard.py` a **před všechny importy** přidejte:

```python
#!/usr/bin/env python3
"""
AMITY DRINKS - Streamlit Dashboard s autentizací
Živý web dashboard pro monitoring influencerů
"""
import streamlit as st

# ===========================================
# AUTENTIZACE - MUSÍ BÝT NA ZAČÁTKU!
# ===========================================

def check_password():
    """Kontrola přihlášení"""

    # Zkontrolovat, jestli už je přihlášen
    if "authenticated" in st.session_state and st.session_state.authenticated:
        return True

    # Načtení credentials ze secrets
    try:
        correct_username = st.secrets["passwords"]["username"]
        correct_password = st.secrets["passwords"]["password"]
    except:
        # Fallback pro lokální development
        correct_username = "amity"
        correct_password = "demo123"

    # Přihlašovací formulář
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #F5F0E8 0%, #E8DCC8 100%);
            }
        </style>
    """, unsafe_allow_html=True)

    # Centered login box
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)

        st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <div style='font-size: 4rem; margin-bottom: 1rem;'>🍹</div>
                <h1 style='color: #C8A43B; margin: 0; font-size: 2.5rem;'>AMITY DRINKS</h1>
                <p style='color: #666; font-size: 1.8rem; font-weight: 700; margin-top: 0.5rem;'>social hero</p>
                <p style='color: #999; font-size: 0.9rem;'>Přihlaste se pro přístup k dashboardu</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("👤 Uživatelské jméno", key="username_input")
            password = st.text_input("🔒 Heslo", type="password", key="password_input")
            submit = st.form_submit_button("🚀 Přihlásit se", use_container_width=True)

            if submit:
                if username == correct_username and password == correct_password:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Nesprávné přihlašovací údaje")

        st.markdown("""
            <div style='text-align: center; margin-top: 3rem; color: #999; font-size: 0.8rem;'>
                <p>© 2026 Amity Drinks s.r.o.</p>
            </div>
        """, unsafe_allow_html=True)

    return False

# Kontrola přihlášení - pokud není přihlášen, zobrazí login a zastaví se
if not check_password():
    st.stop()

# ===========================================
# HLAVNÍ APLIKACE (pokračuje normálně...)
# ===========================================

# ZDE POKRAČUJÍ VAŠE PŮVODNÍ IMPORTY A ZBYTEK KÓDU...
```

#### Krok 2: Přidejte logout tlačítko

V části kde vytváříte sidebar (obvykle po `st.set_page_config`), přidejte:

```python
# Logout tlačítko v sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("🚪 Odhlásit se", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
```

#### Krok 3: Otestujte lokálně

```bash
streamlit run dashboard.py
```

- Uživatelské jméno: `amity`
- Heslo: `demo123` (nebo co jste nastavili v `.streamlit/secrets.toml`)

---

## ✅ Kontrola

Po přidání autentizace:

- [ ] Dashboard se spustí s přihlašovací obrazovkou
- [ ] Po zadání správných údajů se zobrazí hlavní dashboard
- [ ] Tlačítko "Odhlásit se" funguje
- [ ] Při špatném heslu se zobrazí chybová hláška

---

## 🚀 Nasazení na web

Po úspěšném otestování lokálně:

1. Commitněte změny do gitu
2. Pushněte na GitHub
3. Nasaďte na Streamlit Cloud
4. Nastavte `secrets.toml` v Streamlit Cloud Settings

**Detailní návod:** viz `NASAZENI_NA_WEB.md`

---

## 🔧 Troubleshooting

### "KeyError: 'passwords'"
→ Vytvořte `.streamlit/secrets.toml` s credentials

### "This app has encountered an error"
→ Zkontrolujte, že autentizace je PŘED `st.set_page_config()`

### Přihlášení nefunguje
→ Zkontrolujte heslo v `.streamlit/secrets.toml`

### "st.rerun() not found"
→ Použijte `st.experimental_rerun()` pro starší verze Streamlit

---

**Vytvořeno:** 8.1.2026
**Pro:** Amity Drinks Marketing Team
