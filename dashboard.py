#!/usr/bin/env python3
"""
AMITY DRINKS - Streamlit Dashboard
Živý web dashboard pro monitoring influencerů
"""
import streamlit as st

# Konfigurace stránky - MUSÍ BÝT PRVNÍ!
st.set_page_config(
    page_title="Amity Drinks - Influencer Dashboard",
    page_icon="🍹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================
# AUTENTIZACE
# ===========================================

def check_password():
    """Kontrola přihlášení pomocí hesla"""

    # Zkontrolovat, jestli už je přihlášen
    if "authenticated" in st.session_state and st.session_state.authenticated:
        return True

    # Načtení credentials - podporuje Streamlit Cloud i Railway
    import os

    # Zkusit načíst z Railway environment variables (priorita)
    correct_username = os.getenv("DASHBOARD_USERNAME")
    correct_password = os.getenv("DASHBOARD_PASSWORD")

    # Pokud nejsou v ENV, zkusit Streamlit secrets
    if not correct_username or not correct_password:
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

# Kontrola přihlášení - pokud není přihlášen, zastaví aplikaci
if not check_password():
    st.stop()

# ===========================================
# HLAVNÍ APLIKACE
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

from src.database.postgres_manager import UniversalDatabaseManager
from src.utils.config import Config
from src.reporting.excel_report import ExcelReporter
import streamlit.components.v1 as components
import json

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

    /* Čisté bílé karty */
    .glass-card {
        background: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E8E8E8;
        padding: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    }

    /* Metriky */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: #000000;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        font-weight: 600;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 0.9rem;
        color: #C8A43B;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E8E8E8;
    }

    section[data-testid="stSidebar"] > div {
        background: transparent;
    }

    /* Tlačítka - zlatá barva Amity */
    .stButton > button {
        background: #C8A43B;
        color: #000000;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(200, 164, 59, 0.25);
    }

    .stButton > button:hover {
        background: #B39435;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(200, 164, 59, 0.35);
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid #E8E8E8;
    }

    /* Dataframe obsah - bílé pozadí, černý text */
    div[data-testid="stDataFrame"] table {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
    }

    div[data-testid="stDataFrame"] th,
    div[data-testid="stDataFrame"] td,
    div[data-testid="stDataFrame"] table th,
    div[data-testid="stDataFrame"] table td {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* Dataframe header */
    div[data-testid="stDataFrame"] thead th {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #C8A43B !important;
    }

    /* Dataframe řádky */
    div[data-testid="stDataFrame"] tbody tr,
    div[data-testid="stDataFrame"] tbody tr td {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    div[data-testid="stDataFrame"] tbody tr:hover,
    div[data-testid="stDataFrame"] tbody tr:hover td {
        background: #FAFAFA !important;
        background-color: #FAFAFA !important;
    }

    /* Všechny elementy uvnitř dataframe */
    div[data-testid="stDataFrame"] * {
        color: #000000 !important;
    }

    /* Dataframe container */
    div[data-testid="stDataFrame"] > div {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
    }

    /* Hover efekt na řádcích tabulky */
    div[data-testid="stDataFrame"] tbody tr {
        transition: background-color 0.2s ease !important;
    }

    div[data-testid="stDataFrame"] tbody tr:hover {
        background-color: #F5F0E8 !important;
    }

    div[data-testid="stDataFrame"] tbody tr:hover td {
        background-color: #F5F0E8 !important;
        cursor: pointer !important;
    }

    /* Headery */
    h1, h2, h3 {
        color: #000000;
        font-weight: 600;
    }

    h2 {
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #C8A43B;
    }

    /* Expander */
    div[data-testid="stExpander"] {
        background: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E8E8E8;
        margin-bottom: 0.5rem;
    }

    /* Text v expanderu - bílý/černý pro čitelnost */
    div[data-testid="stExpander"] label,
    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] span {
        color: #000000 !important;
    }

    /* Input fieldy v expanderu */
    div[data-testid="stExpander"] input,
    div[data-testid="stExpander"] textarea {
        color: #000000 !important;
        background: #FFFFFF !important;
    }

    /* Selectboxy - základní styling */
    div[data-baseweb="select"] {
        border-radius: 8px;
    }

    /* Selectbox - bílé pozadí, černý text */
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] input {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* Selectbox options dropdown */
    div[role="listbox"] {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
    }

    div[role="option"] {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    div[role="option"]:hover {
        background: #F5F0E8 !important;
        background-color: #F5F0E8 !important;
    }

    /* Horizontal line */
    hr {
        border: none;
        height: 1px;
        background: #E8E8E8;
        margin: 2rem 0;
    }

    /* Spinner */
    div[data-testid="stSpinner"] > div {
        border-color: #C8A43B;
    }

    /* Info/Warning/Success boxy */
    div[data-testid="stAlert"] {
        background: #FFFFFF;
        border-radius: 8px;
        border-left: 4px solid #C8A43B;
        color: #000000;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    /* Text */
    p, span, div {
        color: #333333;
    }

    /* Link tlačítka */
    .stLinkButton > a {
        background: #FFFFFF;
        border: 1px solid #E8E8E8;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        color: #000000;
        text-decoration: none;
        transition: all 0.3s ease;
    }

    .stLinkButton > a:hover {
        background: #C8A43B;
        color: #000000;
        transform: translateY(-2px);
        box-shadow: 0 2px 8px rgba(200, 164, 59, 0.25);
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #F5F0E8;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: #C8A43B;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #B39435;
    }

    /* Skrýt fullscreen tlačítko u obrázků */
    button[title="View fullscreen"] {
        display: none !important;
    }

    /* Skrýt horní Streamlit toolbar */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Upravit padding hlavního containeru bez headeru */
    .main .block-container {
        padding-top: 1rem !important;
    }

    /* Input pole - bílé pozadí, černý text, ohraničení */
    input[type="text"],
    input[type="number"],
    textarea,
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        background: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #E8E8E8 !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }

    /* Focus stav u input polí */
    input[type="text"]:focus,
    input[type="number"]:focus,
    textarea:focus,
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {
        border-color: #C8A43B !important;
        box-shadow: 0 0 0 1px #C8A43B !important;
    }

    /* Labely u input polí */
    .stTextInput label,
    .stTextArea label,
    .stNumberInput label {
        color: #000000 !important;
        font-weight: 500 !important;
    }
</style>""", unsafe_allow_html=True)

# Inicializace databáze
@st.cache_resource
def get_db():
    return UniversalDatabaseManager()

db = get_db()

# Hlavní nadpis - bez emoji, podle brandbooku
st.markdown('<div class="main-header">AMITY DRINKS</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">social hero</div>', unsafe_allow_html=True)

# Sidebar - s Amity logem
with st.sidebar:
    # Logo Amity - relativní cesta pro Streamlit Cloud
    logo_path = Path(__file__).parent / "printscreens" / "Amity Hlavní jpg.jpg"

    # Zobrazit logo jen pokud existuje
    if logo_path.exists():
        st.image(str(logo_path), use_column_width=True)
    else:
        # Fallback - ikona místo loga
        st.markdown('<div style="text-align: center; font-size: 4rem;">🍹</div>', unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: center; padding: 1rem 0 1rem 0; border-bottom: 1px solid #E8E8E8;'>
            <div style='font-size: 1.5rem; font-weight: 700; color: #000000; letter-spacing: -0.5px;'>AMITY DRINKS</div>
            <div style='font-size: 1.7rem; color: #666666; margin-top: 0.5rem; font-weight: 700;'>social hero</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Výběr období
    st.markdown("### 📅 Období")
    now = datetime.now()

    # Rok - rozbalovací menu
    with st.expander(f"📅 Rok: {now.year}", expanded=False):
        selected_year = st.radio(
            "Vyberte rok",
            options=[now.year - 1, now.year],
            index=1,
            label_visibility="collapsed",
            horizontal=False
        )

    month_names = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
                   "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]

    # Měsíc - rozbalovací menu
    with st.expander(f"📆 Měsíc: {month_names[now.month - 1]}", expanded=False):
        selected_month_name = st.radio(
            "Vyberte měsíc",
            options=month_names,
            index=now.month - 1,
            label_visibility="collapsed",
            horizontal=False
        )
    selected_month = month_names.index(selected_month_name) + 1

    st.markdown("---")

    # Akce
    st.markdown("### ⚙️ Akce")

    if st.button("🔄 Obnovit Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    if st.button("📊 Excel Report", use_container_width=True):
        with st.spinner("Generuji report..."):
            reporter = ExcelReporter()
            report_path = reporter.generate_monthly_report(selected_year, selected_month)
            st.success(f"✅ Report vygenerován!")
            st.info(f"📁 {report_path}")

    # Instagram Synchronizace
    if st.button("🔄 Synchronizovat Instagram", use_container_width=True):
        with st.spinner("Synchronizuji Instagram příspěvky..."):
            try:
                # Import sync managera
                import sys
                from pathlib import Path
                sys.path.append(str(Path(__file__).parent))
                from sync_instagram import InstagramSyncManager

                # Spuštění synchronizace
                sync_manager = InstagramSyncManager()
                stats = sync_manager.sync(days_back=90)

                # Zobrazení výsledků
                st.success("✅ Synchronizace dokončena!")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Zkontrolováno", stats['total_posts_checked'])
                with col2:
                    st.metric("Nových příspěvků", stats['new_posts_found'])
                with col3:
                    st.metric("Influencerů", stats['influencers_matched'])

                if stats['new_posts_found'] > 0:
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.info("ℹ️ Žádné nové příspěvky nenalezeny")

            except Exception as e:
                st.error(f"❌ Chyba při synchronizaci: {str(e)}")

    st.markdown("---")

    # Info box - jak repostovat
    st.info("""
**💡 Jak repostovat influencer stories:**

Když repostujete story influencera:
1. Přidejte @mention do textu
   (např. "Repost @dustyfeet23")
2. Nebo označte influencera
3. Klikněte "🔄 Synchronizovat Instagram"

Systém automaticky přiřadí příspěvek!
""")

    st.markdown("---")

    # Rychlé přidání příspěvku
    st.markdown("### ➕ Přidat Příspěvek")

    # Získání seznamu influencerů
    db.connect()
    influencers_list = db.get_all_influencers()
    db.close()

    influencer_options = {inf['jmeno']: inf['id'] for inf in influencers_list}

    with st.form("quick_add_post"):
        # Influencer - rozbalovací menu
        with st.expander("👤 Influencer: Vyberte...", expanded=False):
            selected_influencer = st.radio(
                "Vyberte influencera",
                options=list(influencer_options.keys()),
                label_visibility="collapsed",
                horizontal=False
            )

        # Typ příspěvku - rozbalovací menu s multi-select checkboxy
        with st.expander("📝 Typ příspěvku: Vyberte...", expanded=False):
            st.markdown("*Můžete vybrat více typů najednou*")
            post_types_selected = []
            if st.checkbox("Story", key="type_story"):
                post_types_selected.append("Story")
            if st.checkbox("Post", key="type_post"):
                post_types_selected.append("Post")
            if st.checkbox("Reel", key="type_reel"):
                post_types_selected.append("Reel")

        post_url = st.text_input(
            "URL příspěvku (volitelné)",
            placeholder="https://instagram.com/p/..."
        )

        caption = st.text_area(
            "Popis (volitelné)",
            placeholder="Krátký popis příspěvku...",
            height=60
        )

        col1, col2 = st.columns(2)
        with col1:
            reach = st.number_input("Reach", min_value=0, value=0, step=100)
        with col2:
            likes = st.number_input("Likes", min_value=0, value=0, step=10)

        submitted = st.form_submit_button("✅ Přidat", use_container_width=True)

        if submitted and selected_influencer:
            if not post_types_selected:
                st.error("⚠️ Vyberte alespoň jeden typ příspěvku!")
            else:
                influencer_id = influencer_options[selected_influencer]
                db.connect()

                added_count = 0
                for post_type in post_types_selected:
                    post_data = {
                        'influencer_id': influencer_id,
                        'platform': 'instagram',
                        'post_type': post_type.lower(),
                        'post_id': f'manual_{post_type.lower()}_{datetime.now().timestamp()}',
                        'post_url': post_url if post_url else '',
                        'caption': caption if caption else '',
                        'timestamp': datetime.now(),
                        'likes': likes,
                        'comments': 0,
                        'shares': 0,
                        'reach': reach,
                        'impressions': 0,
                        'engagement_rate': 0
                    }

                    post_id = db.add_post(post_data)
                    if post_id:
                        added_count += 1

                # Aktualizace měsíčních statistik
                db.update_monthly_stats(influencer_id, now.year, now.month)
                db.close()

                if added_count > 0:
                    types_str = ", ".join(post_types_selected)
                    st.success(f"✅ Přidáno {added_count} příspěvků: {selected_influencer} - {types_str}")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.warning("⚠️ Příspěvky již existují v databázi")

    st.markdown("---")

    # ==========================================
    # ADMIN PANEL - Správa Influencerů
    # ==========================================
    st.markdown("### ⚙️ Admin Panel")

    with st.expander("➕ Přidat Influencera", expanded=False):
        with st.form("add_influencer_form", clear_on_submit=True):
            st.markdown("**Nový influencer**")

            new_name = st.text_input("Jméno *", placeholder="Jana Nováková")
            new_instagram = st.text_input("Instagram handle", placeholder="@jana.novakova")

            col1, col2, col3 = st.columns(3)
            with col1:
                new_stories = st.number_input("Stories/měsíc", min_value=0, value=4, step=1)
            with col2:
                new_posts = st.number_input("Posty/měsíc", min_value=0, value=1, step=1)
            with col3:
                new_reels = st.number_input("Reels/měsíc", min_value=0, value=0, step=1)

            new_email = st.text_input("Email", placeholder="jana@email.cz")
            new_notes = st.text_area("Poznámky", placeholder="Volitelné poznámky...", height=60)

            add_submit = st.form_submit_button("✅ Přidat influencera", use_container_width=True)

            if add_submit and new_name:
                db.connect()
                influencer_data = {
                    'jmeno': new_name,
                    'instagram_handle': new_instagram if new_instagram else '',
                    'facebook_handle': '',
                    'tiktok_handle': '',
                    'stories_mesic': new_stories,
                    'prispevky_mesic': new_posts,
                    'reels_mesic': new_reels,
                    'email': new_email if new_email else '',
                    'datum_zacatku': datetime.now().strftime('%Y-%m-%d'),
                    'poznamky': new_notes if new_notes else '',
                    'aktivni': 'ano'
                }
                try:
                    influencer_id = db.add_influencer(influencer_data)
                    db.close()
                    st.success(f"✅ Influencer {new_name} přidán!")
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    db.close()
                    st.error(f"❌ Chyba: {str(e)}")
            elif add_submit:
                st.warning("⚠️ Vyplňte alespoň jméno!")

    with st.expander("✏️ Editovat Influencera", expanded=False):
        db.connect()
        all_influencers = db.get_all_influencers(active_only=False)
        db.close()

        if all_influencers:
            inf_names = {inf['jmeno']: inf for inf in all_influencers}
            selected_inf_name = st.selectbox(
                "Vyberte influencera",
                options=list(inf_names.keys()),
                key="edit_influencer_select"
            )

            if selected_inf_name:
                selected_inf = inf_names[selected_inf_name]

                with st.form("edit_influencer_form"):
                    edit_name = st.text_input("Jméno", value=selected_inf['jmeno'])
                    edit_instagram = st.text_input("Instagram handle", value=selected_inf.get('instagram_handle', ''))

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        edit_stories = st.number_input("Stories/měsíc", min_value=0, value=selected_inf.get('stories_mesic', 0), step=1)
                    with col2:
                        edit_posts = st.number_input("Posty/měsíc", min_value=0, value=selected_inf.get('prispevky_mesic', 0), step=1)
                    with col3:
                        edit_reels = st.number_input("Reels/měsíc", min_value=0, value=selected_inf.get('reels_mesic', 0), step=1)

                    edit_email = st.text_input("Email", value=selected_inf.get('email', ''))
                    edit_active = st.checkbox("Aktivní", value=selected_inf.get('aktivni', 'ano') == 'ano')

                    col_save, col_delete = st.columns(2)
                    with col_save:
                        save_submit = st.form_submit_button("💾 Uložit změny", use_container_width=True)
                    with col_delete:
                        delete_submit = st.form_submit_button("🗑️ Smazat", use_container_width=True, type="secondary")

                    if save_submit:
                        db.connect()
                        update_data = {
                            'jmeno': edit_name,
                            'instagram_handle': edit_instagram,
                            'stories_mesic': edit_stories,
                            'prispevky_mesic': edit_posts,
                            'reels_mesic': edit_reels,
                            'email': edit_email,
                            'aktivni': 'ano' if edit_active else 'ne'
                        }
                        try:
                            db.update_influencer(selected_inf['id'], update_data)
                            db.close()
                            st.success(f"✅ {edit_name} aktualizován!")
                            st.cache_data.clear()
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            db.close()
                            st.error(f"❌ Chyba: {str(e)}")

                    if delete_submit:
                        db.connect()
                        try:
                            # Soft delete - nastavíme jako neaktivního
                            db.update_influencer(selected_inf['id'], {'aktivni': 'ne'})
                            db.close()
                            st.success(f"✅ {selected_inf['jmeno']} deaktivován!")
                            st.cache_data.clear()
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            db.close()
                            st.error(f"❌ Chyba: {str(e)}")
        else:
            st.info("Zatím žádní influenceři v databázi")

    with st.expander("📋 Seznam Influencerů", expanded=False):
        db.connect()
        all_inf = db.get_all_influencers(active_only=False)
        db.close()

        if all_inf:
            for inf in all_inf:
                status_emoji = "✅" if inf.get('aktivni', 'ano') == 'ano' else "❌"
                st.markdown(f"""
                    **{status_emoji} {inf['jmeno']}**
                    Stories: {inf.get('stories_mesic', 0)} | Posts: {inf.get('prispevky_mesic', 0)} | Reels: {inf.get('reels_mesic', 0)}
                """)
                st.markdown("---")
            st.info(f"**Celkem:** {len(all_inf)} influencerů")
        else:
            st.info("Zatím žádní influenceři")

    with st.expander("🔌 Meta API & Synchronizace", expanded=False):
        st.markdown("**Testování a synchronizace Instagram/Facebook dat**")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🧪 Test Meta API", use_container_width=True):
                with st.spinner("Testuji připojení k Meta API..."):
                    try:
                        from src.api.meta_api import MetaAPIClient
                        client = MetaAPIClient()

                        # Test připojení
                        if client.test_connection():
                            st.success("✅ Meta API funguje správně!")

                            # Zobrazit info o tokenu
                            token_info = client.check_token_validity()
                            if token_info:
                                st.info(f"Token platný: {token_info.get('is_valid', False)}")
                        else:
                            st.error("❌ Meta API test selhal. Zkontrolujte credentials v Railway.")
                    except Exception as e:
                        st.error(f"❌ Chyba: {str(e)}")

        with col2:
            if st.button("🔄 Synchronizovat Instagram", use_container_width=True):
                with st.spinner("Stahuji data z Instagramu..."):
                    try:
                        from src.api.meta_api import MetaAPIClient
                        client = MetaAPIClient()

                        # Stáhnout media z posledního měsíce
                        from datetime import timedelta
                        since = datetime.now() - timedelta(days=30)
                        media = client.get_instagram_media(limit=50, since=since)

                        if media:
                            st.success(f"✅ Nalezeno {len(media)} příspěvků!")

                            # Zobrazit náhled
                            for post in media[:3]:
                                st.markdown(f"""
                                    **{post.get('media_type', 'POST')}** - {post.get('timestamp', '')[:10]}
                                    Likes: {post.get('like_count', 0)} | Comments: {post.get('comments_count', 0)}
                                """)
                                st.markdown("---")
                        else:
                            st.warning("⚠️ Žádná data nenalezena")
                    except Exception as e:
                        st.error(f"❌ Chyba: {str(e)}")

        st.markdown("---")
        st.info("💡 **Tip:** Test API zkontroluje připojení k Instagramu a Facebooku. Synchronizace stáhne poslední příspěvky.")

    st.markdown("---")

    # Logout tlačítko
    if st.button("🚪 Odhlásit se", use_container_width=True, key="logout_btn"):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown("---")

    # Info box - Amity style
    st.markdown("""
        <div style='background: #FFFFFF; padding: 1rem; border-radius: 8px; margin-top: 2rem; border: 1px solid #E8E8E8;'>
            <div style='font-size: 0.75rem; color: #666666; text-align: center;'>
                Dashboard v2.0<br>
                <span style='color: #C8A43B; font-weight: 600;'>Update: {}</span>
            </div>
        </div>
    """.format(now.strftime("%H:%M")), unsafe_allow_html=True)

# Načtení dat
db.connect()
influencers = db.get_all_influencers()
monthly_stats = db.get_monthly_stats(selected_year, selected_month)
posts = db.get_posts_by_month(selected_year, selected_month)
db.close()

# ===========================================
# PŘEHLEDOVÉ METRIKY
# ===========================================

st.header("📊 Celkový Přehled")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_influencers = len(influencers)
    st.metric("👥 Aktivní Influenceři", total_influencers)

with col2:
    met_target = sum(1 for s in monthly_stats if s.get('target_met'))
    st.metric("✅ Splnili Cíle", met_target,
             delta=f"{met_target/total_influencers*100:.0f}%" if total_influencers > 0 else "0%")

with col3:
    total_posts = len(posts)
    st.metric("📱 Celkem Příspěvků", total_posts)

with col4:
    total_reach = sum(s.get('total_reach', 0) for s in monthly_stats)
    st.metric("👁️ Celkový Reach", f"{total_reach:,}")

st.markdown("---")

# ===========================================
# STAV PLNĚNÍ
# ===========================================

st.header(f"🎯 Stav Plnění - {selected_month}/{selected_year}")

# Vždy zobrazit všechny influencery, i ty bez dat
if not monthly_stats:
    # Pokud nejsou žádná data, vytvoříme prázdnou tabulku se všemi influencery
    monthly_stats = []
    for inf in influencers:
        monthly_stats.append({
            'jmeno': inf['jmeno'],
            'stories_count': 0,
            'posts_count': 0,
            'reels_count': 0,
            'stories_mesic': inf.get('stories_mesic', 0),
            'prispevky_mesic': inf.get('prispevky_mesic', 0),
            'reels_mesic': inf.get('reels_mesic', 0),
            'total_reach': 0,
            'target_met': False
        })

# Přidáme influencery, kteří nejsou v monthly_stats (nemají žádná data)
existing_names = {stat['jmeno'] for stat in monthly_stats}
for inf in influencers:
    if inf['jmeno'] not in existing_names:
        monthly_stats.append({
            'jmeno': inf['jmeno'],
            'stories_count': 0,
            'posts_count': 0,
            'reels_count': 0,
            'stories_mesic': inf.get('stories_mesic', 0),
            'prispevky_mesic': inf.get('prispevky_mesic', 0),
            'reels_mesic': inf.get('reels_mesic', 0),
            'total_reach': 0,
            'target_met': False
        })

if monthly_stats:
    # Příprava dat pro tabulku
    df_stats = pd.DataFrame(monthly_stats)

    df_stats['stories_text'] = df_stats.apply(
        lambda x: f"{x['stories_count']}/{x['stories_mesic']}", axis=1
    )
    df_stats['posts_text'] = df_stats.apply(
        lambda x: f"{x['posts_count']}/{x['prispevky_mesic']}", axis=1
    )
    df_stats['reels_text'] = df_stats.apply(
        lambda x: f"{x['reels_count']}/{x['reels_mesic']}", axis=1
    )

    # Výpočet % plnění
    df_stats['total_actual'] = df_stats['stories_count'] + df_stats['posts_count'] + df_stats['reels_count']
    df_stats['total_target'] = df_stats['stories_mesic'] + df_stats['prispevky_mesic'] + df_stats['reels_mesic']
    df_stats['completion'] = (df_stats['total_actual'] / df_stats['total_target'] * 100).fillna(0).round(0)

    # Status
    def get_status(row):
        if row['target_met']:
            return '✅ Splněno'
        elif row['completion'] >= 50:
            return '⚠️ Riziko'
        else:
            return '❌ Nesplní'

    df_stats['status'] = df_stats.apply(get_status, axis=1)

    # Zobrazení tabulky
    display_df = df_stats[[
        'jmeno', 'stories_text', 'posts_text', 'reels_text',
        'total_actual', 'completion', 'status', 'total_reach'
    ]].copy()

    display_df.columns = [
        'Jméno', 'Stories', 'Posty', 'Reels',
        'Celkem', '% Plnění', 'Status', 'Reach'
    ]

    # Použití pandas Styler pro přímé stylování (obchází CSS cache)
    def style_dataframe(df):
        return df.style.set_properties(**{
            'background-color': '#FFFFFF',
            'color': '#000000',
            'border': '1px solid #E8E8E8'
        }).set_table_styles([
            {'selector': 'thead th', 'props': [
                ('background-color', '#FFFFFF'),
                ('color', '#000000'),
                ('font-weight', '600'),
                ('border-bottom', '2px solid #C8A43B'),
                ('text-align', 'left'),
                ('padding', '8px')
            ]},
            {'selector': 'tbody td', 'props': [
                ('background-color', '#FFFFFF'),
                ('color', '#000000'),
                ('padding', '8px'),
                ('transition', 'background-color 0.2s ease')
            ]},
            {'selector': 'tbody tr:hover td', 'props': [
                ('background-color', '#F5F0E8'),
                ('cursor', 'pointer')
            ]},
            {'selector': 'table', 'props': [
                ('background-color', '#FFFFFF'),
                ('border-collapse', 'collapse'),
                ('width', '100%')
            ]}
        ])

    # Formátování hodnot pro statickou tabulku
    display_df['% Plnění'] = display_df['% Plnění'].apply(lambda x: f"{int(x)}%")
    display_df['Reach'] = display_df['Reach'].apply(lambda x: f"{int(x):,}".replace(',', ' '))

    # Zobrazení stylované tabulky pomocí st.table (podporuje CSS hover)
    styled_df = style_dataframe(display_df)
    st.table(styled_df)

    # ===========================================
    # ŽEBŘÍČKY
    # ===========================================
    st.markdown("---")
    st.markdown("### 🏆 Žebříčky")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Nejvíce příspěvků")
        # Seřadit podle celkového počtu příspěvků
        top_posts = df_stats.nlargest(5, 'total_actual')[['jmeno', 'total_actual']].copy()
        top_posts.columns = ['Influencer', 'Počet příspěvků']
        top_posts.index = range(1, len(top_posts) + 1)

        # Stylování pro žebříček
        def style_leaderboard(df):
            return df.style.set_properties(**{
                'background-color': '#FFFFFF',
                'color': '#000000',
                'text-align': 'left',
                'padding': '8px'
            }).set_table_styles([
                {'selector': 'thead th', 'props': [
                    ('background-color', '#FFFFFF'),
                    ('color', '#000000'),
                    ('font-weight', '600'),
                    ('border-bottom', '2px solid #C8A43B'),
                    ('padding', '8px')
                ]},
                {'selector': 'tbody tr:nth-child(1) td', 'props': [
                    ('background-color', '#FFD700'),
                    ('font-weight', '700'),
                    ('color', '#000000')
                ]},
                {'selector': 'tbody tr:nth-child(2) td', 'props': [
                    ('background-color', '#C0C0C0'),
                    ('font-weight', '600'),
                    ('color', '#000000')
                ]},
                {'selector': 'tbody tr:nth-child(3) td', 'props': [
                    ('background-color', '#CD7F32'),
                    ('font-weight', '600'),
                    ('color', '#000000')
                ]},
                {'selector': 'tbody tr:hover td', 'props': [
                    ('background-color', '#F5F0E8'),
                    ('cursor', 'pointer')
                ]},
                {'selector': 'table', 'props': [
                    ('background-color', '#FFFFFF'),
                    ('width', '100%')
                ]}
            ])

        st.table(style_leaderboard(top_posts))

    with col2:
        st.markdown("#### 🎯 Největší dosah")
        # Seřadit podle celkového dosahu
        top_reach = df_stats.nlargest(5, 'total_reach')[['jmeno', 'total_reach']].copy()
        top_reach.columns = ['Influencer', 'Celkový reach']
        top_reach['Celkový reach'] = top_reach['Celkový reach'].apply(lambda x: f"{int(x):,}".replace(',', ' '))
        top_reach.index = range(1, len(top_reach) + 1)

        st.table(style_leaderboard(top_reach))


# ===========================================
# PŘÍSPĚVKY
# ===========================================

st.markdown("---")
st.header("📱 Příspěvky")

if posts:
    # Seskupení příspěvků podle influencerů
    posts_by_influencer = {}
    for post in posts:
        inf_name = post.get('influencer_name', 'Neznámý')
        if inf_name not in posts_by_influencer:
            posts_by_influencer[inf_name] = []
        posts_by_influencer[inf_name].append(post)

    # Seřazení příspěvků u každého influencera podle data
    for inf_name in posts_by_influencer:
        posts_by_influencer[inf_name] = sorted(
            posts_by_influencer[inf_name],
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )

    # Vyhledávací pole - moderní design s dropdown
    col1, col2 = st.columns([3, 1])
    with col1:
        # Vytvoření seznamu influencerů seřazených alfabeticky
        influencer_names = sorted(posts_by_influencer.keys())

        # Přidání možnosti "Všichni influenceři" na začátek
        select_options = ["Všichni influenceři"] + influencer_names

        selected_influencer = st.selectbox(
            "🔍 Vyberte influencera",
            options=select_options,
            index=0,
            label_visibility="collapsed",
            key="influencer_select"
        )

    with col2:
        total_influencers = len(posts_by_influencer)
        st.markdown(f"""
            <div style='padding: 0.65rem;
                        text-align: center;
                        background: linear-gradient(135deg, #C8A43B 0%, #B39435 100%);
                        border-radius: 8px;
                        color: #FFFFFF;
                        font-weight: 600;
                        margin-top: 0rem;'>
                👥 {total_influencers} influencerů
            </div>
        """, unsafe_allow_html=True)

    # Filtrování podle výběru
    if selected_influencer == "Všichni influenceři":
        filtered_influencers = posts_by_influencer
    else:
        filtered_influencers = {selected_influencer: posts_by_influencer[selected_influencer]}

    # Zobrazení informace o výběru
    if selected_influencer != "Všichni influenceři":
        post_count = len(filtered_influencers[selected_influencer])
        st.markdown(f"""
            <div style='padding: 0.75rem;
                        background: linear-gradient(135deg, #F0F8FF 0%, #E8F4FF 100%);
                        border-radius: 8px;
                        border-left: 4px solid #C8A43B;
                        margin-bottom: 1rem;
                        color: #000000;'>
                ✨ Zobrazuji: <strong>{selected_influencer}</strong> ({post_count} příspěvků)
            </div>
        """, unsafe_allow_html=True)

    # Zobrazení influencerů a jejich příspěvků
    for inf_name, inf_posts in filtered_influencers.items():
        # Počet příspěvků podle typu
        stories_count = sum(1 for p in inf_posts if p['post_type'] == 'story')
        posts_count = sum(1 for p in inf_posts if p['post_type'] == 'post')
        reels_count = sum(1 for p in inf_posts if p['post_type'] == 'reel')

        # Celkový reach
        total_reach = sum(p.get('reach', 0) for p in inf_posts)

        # Influencer karta - moderní Chakra UI styl
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
                        border-radius: 16px;
                        padding: 1.5rem;
                        margin-bottom: 1.5rem;
                        border: 2px solid #E8E8E8;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                        transition: all 0.3s ease;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                    <div style='display: flex; align-items: center; gap: 1rem;'>
                        <div style='width: 48px;
                                    height: 48px;
                                    border-radius: 50%;
                                    background: linear-gradient(135deg, #C8A43B 0%, #B39435 100%);
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    font-size: 1.5rem;
                                    font-weight: 700;
                                    color: #FFFFFF;
                                    box-shadow: 0 2px 8px rgba(200, 164, 59, 0.3);'>
                            {inf_name[0].upper()}
                        </div>
                        <div>
                            <div style='font-size: 1.3rem;
                                        font-weight: 700;
                                        color: #000000;
                                        margin-bottom: 0.25rem;'>
                                {inf_name}
                            </div>
                            <div style='font-size: 0.85rem; color: #666666;'>
                                {len(inf_posts)} příspěvků celkem
                            </div>
                        </div>
                    </div>
                    <div style='display: flex; gap: 1rem; align-items: center;'>
                        <div style='text-align: center; padding: 0.5rem 1rem; background: #FFFFFF; border-radius: 8px; border: 1px solid #E8E8E8;'>
                            <div style='font-size: 0.7rem; color: #666666; text-transform: uppercase; letter-spacing: 0.5px;'>Stories</div>
                            <div style='font-size: 1.2rem; font-weight: 700; color: #C8A43B;'>{stories_count}</div>
                        </div>
                        <div style='text-align: center; padding: 0.5rem 1rem; background: #FFFFFF; border-radius: 8px; border: 1px solid #E8E8E8;'>
                            <div style='font-size: 0.7rem; color: #666666; text-transform: uppercase; letter-spacing: 0.5px;'>Posts</div>
                            <div style='font-size: 1.2rem; font-weight: 700; color: #C8A43B;'>{posts_count}</div>
                        </div>
                        <div style='text-align: center; padding: 0.5rem 1rem; background: #FFFFFF; border-radius: 8px; border: 1px solid #E8E8E8;'>
                            <div style='font-size: 0.7rem; color: #666666; text-transform: uppercase; letter-spacing: 0.5px;'>Reels</div>
                            <div style='font-size: 1.2rem; font-weight: 700; color: #C8A43B;'>{reels_count}</div>
                        </div>
                        <div style='text-align: center; padding: 0.5rem 1rem; background: #FFFFFF; border-radius: 8px; border: 1px solid #E8E8E8;'>
                            <div style='font-size: 0.7rem; color: #666666; text-transform: uppercase; letter-spacing: 0.5px;'>Reach</div>
                            <div style='font-size: 1.2rem; font-weight: 700; color: #000000;'>{total_reach:,}</div>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Rozbalovací menu s příspěvky
        with st.expander(f"📂 Zobrazit příspěvky ({len(inf_posts)})", expanded=False):
            for idx, post in enumerate(inf_posts):
                # Post karta
                post_date = post.get('timestamp', 'N/A')[:10] if post.get('timestamp') else 'N/A'
                post_type_emoji = {
                    'story': '📸',
                    'post': '📷',
                    'reel': '🎬'
                }.get(post['post_type'], '📱')

                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                with col1:
                    st.markdown(f"""
                        <div style='padding: 0.75rem;
                                    background: #FFFFFF;
                                    border-radius: 8px;
                                    border-left: 4px solid #C8A43B;
                                    margin-bottom: 0.5rem;'>
                            <div style='font-weight: 600; color: #000000; margin-bottom: 0.25rem;'>
                                {post_type_emoji} {post['post_type'].title()} • {post_date}
                            </div>
                            <div style='font-size: 0.85rem; color: #666666;'>
                                {post.get('caption', 'Bez popisku')[:100]}{'...' if len(post.get('caption', '')) > 100 else ''}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.metric("❤️", post.get('likes', 0), label_visibility="visible")

                with col3:
                    st.metric("👁️", post.get('reach', 0), label_visibility="visible")

                with col4:
                    if post.get('post_url'):
                        st.link_button("🔗", post['post_url'], use_container_width=True)
                    else:
                        st.write("")

                if idx < len(inf_posts) - 1:
                    st.markdown("<hr style='margin: 0.5rem 0; border: none; height: 1px; background: #E8E8E8;'>", unsafe_allow_html=True)
else:
    st.info("Zatím žádné příspěvky v tomto měsíci")

# Footer - Amity minimalistický design
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 3rem 0 2rem 0;'>
        <div style='background: #FFFFFF;
                    border-radius: 12px;
                    padding: 2rem;
                    max-width: 600px;
                    margin: 0 auto;
                    border: 1px solid #E8E8E8;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);'>
            <div style='font-size: 1.2rem; font-weight: 700; color: #000000; margin-bottom: 0.5rem; letter-spacing: -0.5px;'>
                AMITY DRINKS
            </div>
            <div style='font-size: 1.8rem; color: #666666; margin-bottom: 0.5rem; font-weight: 700;'>
                social hero
            </div>
            <div style='font-size: 0.85rem; color: #C8A43B; font-weight: 600;'>
                v2.0
            </div>
            <div style='font-size: 0.75rem; color: #999999; margin-top: 1rem;'>
                {} • dobrota je uvnitř
            </div>
        </div>
    </div>
    """.format(datetime.now().strftime("%d.%m.%Y %H:%M")),
    unsafe_allow_html=True
)
