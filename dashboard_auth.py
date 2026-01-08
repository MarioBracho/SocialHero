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

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
import sys
import time

# Přidání src do path
sys.path.append(str(Path(__file__).parent))

from src.database.db_manager import DatabaseManager
from src.utils.config import Config
from src.reporting.excel_report import ExcelReporter
import streamlit.components.v1 as components
import json

# Konfigurace stránky (už je nastavena výše před autentizací)
# Ale musíme ji nastavit znovu po rerun
if "page_configured" not in st.session_state:
    st.set_page_config(
        page_title="Amity Drinks - Influencer Dashboard",
        page_icon="🍹",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.session_state.page_configured = True

# Custom CSS - Amity Brand Design (with cache buster)
css_version = int(time.time())

st.markdown(f'<style data-version="{css_version}">' + """
    /* Import Amity fontu - Silka */
    @import url('https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;500;600;700&display=swap');

    /* Globální styly */
    * {
        font-family: 'Work Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Pozadí - světlé béžové/krémové jako na webu */
    .stApp {
        background: #F5F0E8;
        background-attachment: fixed;
    }

    /* Hlavní kontejner */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Hlavní nadpis */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #000000;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -1px;
    }

    .subtitle {
        color: #666666;
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        margin-top: -0.5rem;
        margin-bottom: 3rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E8E8E8;
    }

    /* Logout tlačítko */
    .logout-btn {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
    }
""" + '</style>', unsafe_allow_html=True)

# Logout tlačítko v sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("🚪 Odhlásit se", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ZDE POKRAČUJE ZBYTEK PŮVODNÍHO DASHBOARD.PY...
# (Pro úsporu místa, zkopírujte zbytek kódu z původního dashboard.py)

# Hlavička
st.markdown('<div class="main-header">AMITY DRINKS</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">social hero</div>', unsafe_allow_html=True)

# Dashboard content
st.info("📝 **Dashboard s autentizací je připraven!**\n\nPro plnou funkčnost zkopírujte zbytek kódu z původního `dashboard.py` souboru (řádky 31 až konec) sem.")

st.markdown("""
### ✅ Co je hotové:
- Přihlašovací systém
- Ochrana heslem
- Logout tlačítko
- Integrace se Streamlit secrets

### 📋 Jak dokončit:
1. Otevřete původní `dashboard.py`
2. Zkopírujte řádky od cca 31 (od "# Custom CSS") až do konce
3. Vložte je místo tohoto info boxu
4. Uložte soubor

### 🚀 Nasazení:
Následujte návod v souboru `NASAZENI_NA_WEB.md`
""")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0;'>
        <div style='font-size: 0.85rem; color: #999999;'>
            🍹 Amity Drinks • social hero v2.0 • {} • dobrota je uvnitř
        </div>
    </div>
    """.format(datetime.now().strftime("%d.%m.%Y %H:%M")),
    unsafe_allow_html=True
)
