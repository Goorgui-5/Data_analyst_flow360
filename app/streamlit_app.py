import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64

# Configuration de la page
st.set_page_config(
    page_title="Lions de la Téranga - Dashboard Analytique",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🇸🇳"
)

# Couleurs du thème Sénégal (exactes) avec palette professionnelle
PRIMARY = "#00853F"    # Vert Sénégal
ACCENT = "#FCD116"     # Jaune Sénégal
SECONDARY = "#E31B23"  # Rouge Sénégal
BG_WHITE = "#FFFFFF"   # Fond blanc
CARD_BG = "#F9FAFB"    # Couleur des cartes
TEXT_DARK = "#1F2937"  # Texte sombre
TEXT_GRAY = "#6B7280"  # Texte gris
SIDEBAR_BG = "#F8F9FA" # Fond sidebar professionnel
SIDEBAR_ACCENT = "#00853F" # Accent sidebar

# Fonction pour charger les images en base64
@st.cache_data
def get_image_base64(image_path):
    """Convertit une image en base64"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Charger les images
logo_b64 = get_image_base64("app/assets/Drapeau_senegal.jpg")
drapeau_b64 = get_image_base64("app/assets/Logo.png")

# CSS personnalisé pour design professionnel épuré
# CSS personnalisé pour design professionnel épuré
st.markdown(f"""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* ===== FOND GLOBAL ===== */
    .main {{
        background-color: {BG_WHITE} !important;
        font-family: 'Inter', sans-serif !important;
    }}
    .block-container {{
        background-color: {BG_WHITE} !important;
        padding-top: 1rem !important;
        max-width: 1400px !important;
        border: none !important;
        box-shadow: none !important;
    }}
    
    /* ===== SUPPRESSION DU CADRE NOIR ===== */
    .stApp {{
        background-color: {BG_WHITE} !important;
        border: none !important;
    }}
    .main .block-container {{
        border: none !important;
        box-shadow: none !important;
    }}
    
    /* ===== SIDEBAR PROFESSIONNELLE ===== */
    [data-testid="stSidebar"] {{
        background: {SIDEBAR_BG} !important;
        border-right: 1px solid #E5E7EB;
    }}
    [data-testid="stSidebar"] .sidebar-content {{
        background: transparent !important;
    }}

    /* ===== HEADER PROFESSIONNEL ===== */
    .header-professional {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem 0 2rem 0;
        border-bottom: 3px solid {PRIMARY};
        margin-bottom: 2.5rem;
        background: {BG_WHITE};
    }}
    .header-left {{
        display: flex;
        align-items: center;
        gap: 1.2rem;
    }}
    .header-title {{
        font-size: 2.2rem;
        font-weight: 800;
        color: {TEXT_DARK} !important;
        margin: 0;
        margin-bottom: 0.1rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
    }}
    .header-subtitle {{
        color: {TEXT_GRAY} !important;
        font-size: 0.95rem;
        margin-top: 0;
        font-weight: 500;
        letter-spacing: 0.01em;
    }}

    /* ===== KPI CARDS PROFESSIONNELLES ===== */
    .kpi-card-professional {{
        background: linear-gradient(135deg, {BG_WHITE} 0%, {CARD_BG} 100%);
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 1.8rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        border-left: 4px solid {PRIMARY};
        overflow: hidden;
    }}
    .kpi-card-professional::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, {PRIMARY}08 0%, transparent 70%);
        border-radius: 50%;
    }}
    .kpi-card-professional:hover {{
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        transform: translateY(-4px);
        border-left-width: 6px;
    }}
    .kpi-label-professional {{
        font-size: 0.82rem;
        color: {TEXT_GRAY} !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.9rem;
        position: relative;
        z-index: 1;
    }}
    .kpi-value-professional {{
        font-size: 2.5rem;
        font-weight: 800;
        color: {TEXT_DARK};
        margin: 0;
        line-height: 1;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.03em;
        position: relative;
        z-index: 1;
    }}

    /* ===== TITRES DE SECTION ===== */
    .section-title {{
        font-size: 1.6rem;
        font-weight: 800;
        color: {TEXT_DARK} !important;
        margin: 2.5rem 0 1.8rem 0;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid {PRIMARY};
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
        position: relative;
    }}
    .section-title::after {{
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 80px;
        height: 3px;
        background: {ACCENT};
    }}

    /* ===== BADGES AMÉLIORÉS ===== */
    .badge {{
        padding: 7px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        display: inline-block;
        text-transform: capitalize;
        border: 1px solid transparent;
        letter-spacing: 0.02em;
    }}
    .badge-attaquant {{ 
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%); 
        color: #991B1B; 
        border-color: #F87171; 
    }}
    .badge-defenseur {{ 
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); 
        color: #065F46; 
        border-color: #34D399; 
    }}
    .badge-milieu {{ 
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); 
        color: #92400E; 
        border-color: #FBBF24; 
    }}
    .badge-gardien {{ 
        background: linear-gradient(135deg, #FFE4E6 0%, #FECDD3 100%); 
        color: #9F1239; 
        border-color: #FB7185; 
    }}
    .badge-arriere {{ 
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%); 
        color: #1E40AF; 
        border-color: #60A5FA; 
    }}

    /* ===== CHARTS PROFESSIONNELS ===== */
    .chart-container {{
        background: {BG_WHITE};
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 2rem 1.8rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }}
    .chart-container:hover {{
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    }}
    .chart-title {{
        font-size: 1.3rem;
        font-weight: 700;
        color: {TEXT_DARK} !important;
        margin-bottom: 1.5rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.01em;
    }}

    /* ===== TABLES AMÉLIORÉES ===== */
    .dataframe {{
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}
    .dataframe th {{
        background: linear-gradient(180deg, {CARD_BG} 0%, {BG_WHITE} 100%) !important;
        color: {TEXT_DARK} !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.08em !important;
        border-bottom: 2px solid {PRIMARY} !important;
        padding: 1rem 0.75rem !important;
    }}
    .dataframe td {{
        color: {TEXT_DARK} !important;
        border-bottom: 1px solid #F3F4F6 !important;
        padding: 0.9rem 0.75rem !important;
        font-size: 0.9rem !important;
    }}
    .dataframe tr:hover {{
        background-color: {PRIMARY}08 !important;
        transition: all 0.2s ease;
    }}

    /* ===== SIDEBAR PROFESSIONNELLE ===== */
    .sidebar-content {{
        padding: 1rem;
    }}
    .sidebar-section {{
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #E5E7EB;
    }}
    .sidebar-title {{
        font-size: 1.05rem;
        font-weight: 800;
        color: {SIDEBAR_ACCENT} !important; 
        margin-bottom: 0.8rem;
        letter-spacing: -0.01em;
    }}
    
    /* ===== ÉLÉMENTS DE LA SIDEBAR ===== */
    [data-testid="stSidebarNav"] {{
        background: transparent !important;
    }}
    .stSidebar .stRadio > div {{
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        color: {TEXT_DARK} !important;
    }}
    
    /* Style pour les éléments de formulaire dans la sidebar */
    [data-testid="stSidebar"] .stSelectbox, 
    [data-testid="stSidebar"] .stSlider,
    [data-testid="stSidebar"] .stRadio {{
        background: white;
        padding: 0.5rem;
        border-radius: 8px;
    }}

    /* ===== PLOTS VISIBLES ===== */
    .js-plotly-plot .plotly .main-svg {{
        background: transparent !important;
    }}
    .js-plotly-plot text {{
        fill: {TEXT_DARK} !important;
        font-family: 'Inter', sans-serif !important;
    }}
    .plotly-graph-div .svg-container {{
        background: transparent !important;
    }}

    /* ===== STATS VISIBLES SUR GRAPHIQUES ===== */
    .stat-annotation {{
        font-size: 14px !important;
        font-weight: 700 !important;
        fill: {TEXT_DARK} !important;
    }}
    .hovertext {{
        background-color: white !important;
        border: 1px solid #E5E7EB !important;
        color: {TEXT_DARK} !important;
        font-weight: 600 !important;
    }}

    /* ===== BOUTONS ET FILTRES ===== */
    .stButton>button {{
        border-radius: 10px;
        border: 2px solid {PRIMARY};
        background: linear-gradient(135deg, {PRIMARY} 0%, #007a38 100%);
        color: white;
        font-weight: 700;
        padding: 0.6rem 1.5rem;
        font-size: 0.9rem;
        letter-spacing: 0.02em;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,133,63,0.3);
    }}

    /* ===== SELECTBOX VISIBLES - COULEURS SÉNÉGAL ===== */
    .stSelectbox > div > div {{
        border-radius: 10px;
        border: 2px solid #00853F !important;
        background: white !important;
        transition: all 0.3s ease;
    }}
    .stSelectbox label {{
        color: #00853F !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }}
    .stSelectbox [data-baseweb="select"] > div {{
        color: #1F2937 !important;
        font-weight: 600 !important;
    }}
    .stSelectbox > div > div:hover {{
        border-color: #FCD116 !important;
        box-shadow: 0 0 0 3px rgba(0, 133, 63, 0.1);
    }}
    .stSelectbox [data-baseweb="popover"] {{
        border: 2px solid #00853F !important;
    }}
    .stSelectbox [role="option"]:hover {{
        background-color: #00853F15 !important;
        color: #00853F !important;
    }}

    /* ===== SLIDER VISIBLE - COULEURS SÉNÉGAL ===== */
    .stSlider label {{
        color: #00853F !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.8rem !important;
    }}
    .stSlider [data-baseweb="slider"] {{
        padding: 1rem 0;
    }}
    /* Poignées du slider */
    .stSlider [role="slider"] {{
        background-color: #E31B23 !important;
        border: 3px solid white !important;
        box-shadow: 0 2px 8px rgba(227, 27, 35, 0.3) !important;
        width: 20px !important;
        height: 20px !important;
    }}
    .stSlider [role="slider"]:hover {{
        background-color: #FCD116 !important;
        box-shadow: 0 4px 12px rgba(252, 209, 22, 0.5) !important;
        transform: scale(1.1);
    }}
    /* Barre du slider */
    .stSlider [data-baseweb="slider"] > div > div {{
        background: linear-gradient(90deg, #00853F 0%, #FCD116 100%) !important;
        height: 6px !important;
        border-radius: 3px !important;
    }}
    /* Valeurs affichées */
    .stSlider [data-baseweb="slider"] + div {{
        color: #1F2937 !important;
        font-weight: 700 !important;
    }}
    /* ===== RADIO BUTTONS - TEXTES ULTRA VISIBLES ===== */

    /* Le label principal "Navigation" */
    .stRadio > label {{
        font-weight: 700 !important;
        color: #00853F !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.8rem !important;
    }}

    /* TOUS les textes des options radio - APPROCHE 1 */
    [data-testid="stSidebar"] .stRadio label span {{
        color: #00813c !important;  /* NOIR PUR */
        font-weight: 700 !important;
        font-size: 1rem !important;
    }}

    /* TOUS les textes des options radio - APPROCHE 2 */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        color: #00813c !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.8rem 1.2rem !important;
    }}

    /* TOUS les textes des options radio - APPROCHE 3 (Plus spécifique) */
    [data-testid="stSidebar"] .stRadio div[data-baseweb="radio"] label {{
        color: #00813c !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }}

    /* Le texte à l'intérieur du label */
    [data-testid="stSidebar"] .stRadio label > div {{
        color: #00813c !important;
        font-weight: 700 !important;
    }}

    /* Option sélectionnée */
    [data-testid="stSidebar"] .stRadio input[type="radio"]:checked + label {{
        color: #00853F !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #00853F15, #00853F25) !important;
        border-left: 4px solid #00853F !important;
        padding: 0.8rem 1.2rem !important;
        border-radius: 8px;
    }}

    /* Forcer TOUT le texte dans la sidebar radio */
    [data-testid="stSidebar"] .stRadio * {{
        color: #00813c !important;
    }}

    /* Exception pour l'option sélectionnée */
    [data-testid="stSidebar"] .stRadio input[type="radio"]:checked ~ * {{
        color: #00853F !important;
    }}
    /* ===== METRICS ===== */
    [data-testid="stMetricValue"] {{
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: {PRIMARY} !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: {TEXT_GRAY} !important;
    }}

    /* ===== CACHER LE BRANDING STREAMLIT ===== */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    .st-emotion-cache-1dp5vir {{display: none;}}
    
    /* ===== SCROLLBAR PERSONNALISÉE ===== */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: {CARD_BG};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {PRIMARY};
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: #007a38;
    }}
    
    /* ===== SUPPRESSION DES BORDURES NOIRES ===== */
    .element-container {{
        border: none !important;
    }}
    div[data-testid="stVerticalBlock"] {{
        background: transparent !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# Chargement des données
@st.cache_data
def load_data():
    """Charge les données depuis les fichiers CSV"""
    try:
        players = pd.read_csv("data/players_clean.csv")
        kpis = pd.read_csv("data/processed/players_kpis.csv")
        performances = pd.read_csv("data/performances_clean.csv")
        
        df = players.merge(kpis, on="player_id", how="left")
        df = df.fillna(0)
        
        if "birth_date" in df.columns:
            df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce")
            df["age"] = (datetime.now() - df["birth_date"]).dt.days // 365
        
        return df, performances
    except FileNotFoundError as e:
        st.error(f"❌ Fichier manquant : {e}")
        st.stop()

# Header professionnel
def create_header_professional():
    """Header avec design professionnel"""
    if drapeau_b64 and logo_b64:
        st.markdown(f"""
        <div class="header-professional">
            <div class="header-left">
                <img src="data:image/jpeg;base64,{drapeau_b64}" width="75" style="border-radius: 8px; border: 2px solid #E5E7EB; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div>
                    <h1 class="header-title" style="line-height: 0.7;">Lions de la Téranga <br>
                    <span class="header-subtitle" style="margin-top: -5px; display: inline-block;">Équipe Nationale du Sénégal • DataAnalystFlow360</span>
                    </h1>
                </div>
            </div>
            <img src="data:image/png;base64,{logo_b64}" width="55" style="border-radius: 8px; border: 2px solid #E5E7EB; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-top: 2px;">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="header-professional">
            <div class="header-left">
                <div>
                    <h1 class="header-title">Lions de la Téranga</h1>
                    <p class="header-subtitle">Équipe Nationale du Sénégal • DataAnalystFlow360</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# KPI Card professionnelle
def kpi_card_professional(label, value, border_color=PRIMARY):
    """Crée une carte KPI épurée et professionnelle sans icônes"""
    st.markdown(f"""
    <div class="kpi-card-professional" style="border-left-color: {border_color};">
        <div class="kpi-label-professional">{label}</div>
        <div class="kpi-value-professional">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# Fonction pour obtenir le badge de position
def get_position_badge_html(position):
    """Retourne le HTML du badge de position avec couleurs professionnelles"""
    position_lower = str(position).lower()
    
    if "attaquant" in position_lower or "avant" in position_lower:
        classe = "badge-attaquant"
        display = "Attaquant"
    elif "défenseur" in position_lower or "défense" in position_lower:
        classe = "badge-defenseur"
        display = "Défenseur"
    elif "milieu" in position_lower:
        if "offensif" in position_lower:
            classe = "badge-milieu"
            display = "Milieu Offensif"
        elif "défensif" in position_lower:
            classe = "badge-milieu"
            display = "Milieu Défensif"
        else:
            classe = "badge-milieu"
            display = "Milieu Central"
    elif "gardien" in position_lower:
        classe = "badge-gardien"
        display = "Gardien"
    elif "arrière" in position_lower:
        classe = "badge-arriere"
        display = "Arrière"
    else:
        classe = "badge-milieu"
        display = position_lower.capitalize()
    
    return f'<span class="badge {classe}">{display}</span>'

# Fonction pour créer des graphiques avec statistiques visibles
def create_visible_bar_chart(data, x_col, y_col, title, color, orientation='v'):
    """Crée un graphique à barres avec des statistiques bien visibles"""
    if orientation == 'h':
        fig = px.bar(data, x=x_col, y=y_col, orientation='h', color_discrete_sequence=[color])
    else:
        fig = px.bar(data, x=x_col, y=y_col, color_discrete_sequence=[color])
    
    # Ajouter les valeurs sur les barres
    if orientation == 'h':
        fig.update_traces(
            texttemplate='<b>%{x}</b>',
            textposition='outside',
            textfont=dict(size=13, color=TEXT_DARK, family="Inter", weight=700)
        )
    else:
        fig.update_traces(
            texttemplate='<b>%{y}</b>',
            textposition='outside',
            textfont=dict(size=13, color=TEXT_DARK, family="Inter", weight=700)
        )
    
    fig.update_layout(
        height=420,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20),
        font=dict(family="Inter", color=TEXT_DARK),
        title=dict(
            text=f"<b>{title}</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=19, color=TEXT_DARK, family="Inter")
        ),
        xaxis=dict(
            gridcolor="#F3F4F6",
            title_font=dict(size=13, family="Inter", weight=600),
            tickfont=dict(size=12, family="Inter")
        ),
        yaxis=dict(
            gridcolor="#F3F4F6",
            title_font=dict(size=13, family="Inter", weight=600),
            tickfont=dict(size=12, family="Inter")
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Inter",
            bordercolor="#E5E7EB"
        )
    )
    return fig

# Navigation
def main():
    df, performances = load_data()
    
    create_header_professional()
    
    # Sidebar professionnelle
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        # Navigation
        # st.markdown('<div class="sidebar-section">Navigation', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section" style="text-align:center; color:#1c884f; font-weight:bold; font-size:16px;">Navigation</div>',unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title"></div>', unsafe_allow_html=True)
        page = st.radio("", 
                       ["Tableau de Bord", "Analyses Avancées", "Gestion des Joueurs"], 
                       label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Filtres
        # st.markdown('<div class="sidebar-section">Filtres Avancés', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section" style="text-align:center; color:#1c884f; font-weight:bold; font-size:16px;">Filtres Avancés</div>',unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title"></div>', unsafe_allow_html=True)
        
        clubs = ["Tous"] + sorted(df["current_club"].dropna().unique().tolist())
        selected_club = st.selectbox("Club Actuel", clubs)
        
        positions = ["Toutes"] + sorted(df["position"].dropna().unique().tolist())
        selected_position = st.selectbox("Position", positions)
        
        # Filtre par âge
        if "age" in df.columns:
            min_age = int(df["age"].min()) if not df.empty else 18
            max_age = int(df["age"].max()) if not df.empty else 40
            age_range = st.slider(" Tranche d'âge", min_age, max_age, (min_age, max_age))
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Appliquer les filtres
    filtered_df = df.copy()
    if selected_club != "Tous":
        filtered_df = filtered_df[filtered_df["current_club"] == selected_club]
    if selected_position != "Toutes":
        filtered_df = filtered_df[filtered_df["position"] == selected_position]
    if "age" in df.columns:
        filtered_df = filtered_df[
            (filtered_df["age"] >= age_range[0]) & 
            (filtered_df["age"] <= age_range[1])
        ]
    
    if page == "Tableau de Bord":
        show_dashboard(filtered_df)
    elif page == "Analyses Avancées":
        show_analyses(filtered_df)
    elif page == "Gestion des Joueurs":
        show_players_table(filtered_df)

# PAGE 1: DASHBOARD PROFESSIONNEL
def show_dashboard(df):
    # Section Statistiques Clés
    st.markdown('<div class="section-title"> Statistiques Clés de l\'Équipe</div>', unsafe_allow_html=True)
    
    # Première ligne de KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        kpi_card_professional("Joueurs Totaux", len(df), PRIMARY)
    
    with col2:
        total_buts = int(df["goals"].sum())
        kpi_card_professional("Buts Marqués", f"{total_buts:,}", SECONDARY)
    
    with col3:
        total_passes = int(df["assists"].sum())
        kpi_card_professional("Passes Décisives", f"{total_passes:,}", ACCENT)
    
    with col4:
        avg_eff = round(df["efficiency"].replace([np.inf, -np.inf], 0).mean(), 1)
        kpi_card_professional("Efficacité Moy.", f"{avg_eff}%", "#4ECDC4")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Deuxième ligne de KPIs
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        nb_clubs = df["current_club"].nunique()
        kpi_card_professional("Clubs Représentés", nb_clubs, "#FF6B35")
    
    with col6:
        nb_competitions = df["current_competition"].nunique()
        kpi_card_professional("Compétitions", nb_competitions, "#95E1D3")
    
    with col7:
        nb_pays = df["current_pays_de_competition"].nunique()
        kpi_card_professional("Pays", nb_pays, "#A8DADC")
    
    with col8:
        # age moyens convertie en entier
        if "age" in df.columns and not df.empty:
            avg_age = int(df["age"].mean())
            kpi_card_professional("Âge Moyen", f"{avg_age} ans", "#F4A261")
        
        # total_matches = int(df["nb_matches"].sum())
        # kpi_card_professional("Matchs Joués", f"{total_matches:,}", "#457B9D")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Top Performers
    st.markdown('<div class="section-title"> Top Performers</div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        # st.markdown('<div class="chart-container" >Top 10 Meilleurs Buteurs', unsafe_allow_html=True)
        st.markdown('<div class="chart-container" style="text-align:center; color:#004d00; font-weight:bold; font-size:22px;">Top 10 Meilleurs Buteurs</div>',unsafe_allow_html=True)
        
        top_scorers = df.nlargest(10, "goals")[["name", "goals"]].reset_index(drop=True)
        
        if not top_scorers.empty:
            fig = create_visible_bar_chart(
                top_scorers.iloc[::-1], 
                "goals", "name", 
                "", 
                PRIMARY, 
                'h'
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        # st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-container" style="text-align:center; color:#d4ae0b; font-weight:bold; font-size:22px;">Top 10 Meilleurs Passeurs</div>',unsafe_allow_html=True)
        
        top_passers = df.nlargest(10, "assists")[["name", "assists"]].reset_index(drop=True)
        
        if not top_passers.empty:
            fig = create_visible_bar_chart(
                top_passers.iloc[::-1], 
                "assists", "name", 
                "", 
                ACCENT, 
                'h'
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# PAGE 2: ANALYSES AVANCÉES
def show_analyses(df):
    st.markdown('<div class="section-title"> Analyses Avancées</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-container" style="text-align:center; color:#004d00; font-weight:bold; font-size:22px;">TRépartition par Position</div>',unsafe_allow_html=True)
        
        position_counts = df["position"].value_counts()
        
        fig = px.pie(
            values=position_counts.values,
            names=position_counts.index,
            color_discrete_sequence=[PRIMARY, ACCENT, SECONDARY, "#4ECDC4", "#FF6B35", "#95E1D3"]
        )
        fig.update_traces(
            textposition='inside',
            textinfo='percent',
            textfont=dict(size=13, color="white", family="Inter", weight=700),
            hovertemplate="<b>%{label}</b><br>Joueurs: %{value}<br>Pourcentage: %{percent}<extra></extra>",
            marker=dict(line=dict(color='white', width=3))
        )
        fig.update_layout(
            height=420,
            showlegend=True,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=60, b=20),
            font=dict(family="Inter", color=TEXT_DARK),
            title=dict(
                text="<b> </b>",
                x=0.5,
                xanchor='center',
                font=dict(size=19, color=TEXT_DARK, family="Inter")
            ),
            legend=dict(
                font=dict(size=12, family="Inter"),
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-container" style="text-align:center; color:#e31b23; font-weight:bold; font-size:22px;">Top 10 Compétitions</div>',unsafe_allow_html=True)
        
        comp_counts = df["current_competition"].value_counts().head(10)
        comp_data = pd.DataFrame({
            'Competition': comp_counts.index,
            'Joueurs': comp_counts.values
        })
        
        fig = create_visible_bar_chart(
            comp_data,
            'Competition', 'Joueurs',
            '',
            SECONDARY,
            'v'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Distribution géographique
    # st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-container" style="text-align:center; color:#004d00; font-weight:bold; font-size:22px;">Répartition Géographique - Top 15 Pays</div>',unsafe_allow_html=True)
    
    pays_counts = df["current_pays_de_competition"].value_counts().head(15)
    pays_data = pd.DataFrame({
        'Pays': pays_counts.index,
        'Joueurs': pays_counts.values
    })
    
    fig = create_visible_bar_chart(
        pays_data,
        'Pays', 'Joueurs',
        '',
        PRIMARY,
        'v'
    )
    fig.update_layout(xaxis_tickangle=-45, height=450)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analyse par âge
    if "age" in df.columns and not df.empty:
        st.markdown('<div class="section-title"> Analyse Démographique</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-container" style="text-align:center; color:#00853f; font-weight:bold; font-size:22px;">Distribution par Tranche d\'Âge</div>',unsafe_allow_html=True)
            
            # Créer des tranches d'âge
            bins = [18, 23, 27, 31, 35, 40]
            labels = ['18-22', '23-26', '27-30', '31-34', '35+']
            df_age = df[df["age"] > 0].copy()
            df_age['age_group'] = pd.cut(df_age['age'], bins=bins, labels=labels, include_lowest=True)
            
            age_counts = df_age['age_group'].value_counts().sort_index()
            age_data = pd.DataFrame({
                'Tranche d\'âge': age_counts.index.astype(str),
                'Nombre de joueurs': age_counts.values
            })
            
            fig = create_visible_bar_chart(
                age_data,
                'Tranche d\'âge', 'Nombre de joueurs',
                '',
                "#00853f",
                'v'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-container" style="text-align:center; color:#00853f; font-weight:bold; font-size:22px;">Statistiques d\'Âge</div>',unsafe_allow_html=True)
            
            # Statistiques d'âge converties en entier
            avg_age = int(round(df_age["age"].mean()))     # arrondi à l'entier le plus proche
            median_age = int(df_age["age"].median())      # tronque la valeur si décimale
            min_age = int(df_age["age"].min())
            max_age = int(df_age["age"].max())

            
            st.markdown(f"""
            <div style="padding: 2rem 0;">
                <h3 style="color: {TEXT_DARK}; font-size: 1.3rem; font-weight: 700; margin-bottom: 2rem;">
                    ....
                </h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                    <div style="background: {CARD_BG}; padding: 1.2rem; border-radius: 12px; border-left: 4px solid {PRIMARY};">
                        <div style="color: {TEXT_GRAY}; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;">ÂGE MOYEN</div>
                        <div style="color: {TEXT_DARK}; font-size: 2rem; font-weight: 800;">{avg_age:.1f} ans</div>
                    </div>
                    <div style="background: {CARD_BG}; padding: 1.2rem; border-radius: 12px; border-left: 4px solid {ACCENT};">
                        <div style="color: {TEXT_GRAY}; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;">ÂGE MÉDIAN</div>
                        <div style="color: {TEXT_DARK}; font-size: 2rem; font-weight: 800;">{median_age:.0f} ans</div>
                    </div>
                    <div style="background: {CARD_BG}; padding: 1.2rem; border-radius: 12px; border-left: 4px solid {SECONDARY};">
                        <div style="color: {TEXT_GRAY}; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;">PLUS JEUNE</div>
                        <div style="color: {TEXT_DARK}; font-size: 2rem; font-weight: 800;">{min_age:.0f} ans</div>
                    </div>
                    <div style="background: {CARD_BG}; padding: 1.2rem; border-radius: 12px; border-left: 4px solid #4ECDC4;">
                        <div style="color: {TEXT_GRAY}; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;">PLUS ÂGÉ</div>
                        <div style="color: {TEXT_DARK}; font-size: 2rem; font-weight: 800;">{max_age:.0f} ans</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# PAGE 3: TABLE DES JOUEURS PROFESSIONNELLE
def show_players_table(df):
    st.markdown('<div class="section-title"> Gestion des Joueurs</div>', unsafe_allow_html=True)
    
    # Barre de recherche et filtres avancés
    col_search, col_filter, col_export = st.columns([2, 1, 1])
    
    with col_search:
        search = st.text_input(" Rechercher un joueur", "", 
                             placeholder="Entrez le nom d'un joueur...")
    
    with col_filter:
        sort_by = st.selectbox(" Trier par", 
                              ["Nom", "Buts", "Passes", "Matchs", "Efficacité"])
    
    with col_export:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(" Exporter CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Télécharger",
                data=csv,
                file_name="lions_teranga_joueurs.csv",
                mime="text/csv"
            )
    
    # Appliquer la recherche
    if search:
        df = df[df["name"].str.contains(search, case=False, na=False)]
    
    # Appliquer le tri
    sort_columns = {
        "Nom": "name",
        "Buts": "goals", 
        "Passes": "assists",
        "Matchs": "nb_matches",
        "Efficacité": "efficiency"
    }
    if sort_by in sort_columns:
        df = df.sort_values(sort_columns[sort_by], ascending=sort_by == "Nom")
    
    # Préparer les données pour l'affichage
    display_df = df[[
        "name", "age", "position", "current_club", 
        "goals", "assists", "nb_matches", "efficiency"
    ]].copy()
    
    display_df.columns = [
        "Nom", "Âge", "Position", "Club", 
        "Buts", "Passes", "Matchs", "Efficacité"
    ]
    
    # Appliquer le formatage de position avec badges
    display_df["Position"] = display_df["Position"].apply(lambda x: get_position_badge_html(x))
    
    # Formater l'efficacité avec badge coloré
    def format_efficiency(val):
        try:
            val_float = float(val)
            if val_float >= 30:
                color = "#10B981"  # Vert
                label = "Excellent"
            elif val_float >= 20:
                color = "#F59E0B"  # Orange
                label = "Bon"
            elif val_float >= 10:
                color = "#6B7280"  # Gris
                label = "Moyen"
            else:
                color = "#EF4444"  # Rouge
                label = "Faible"
            return f'<span style="background: linear-gradient(135deg, {color}15, {color}25); color: {color}; padding: 8px 14px; border-radius: 16px; font-weight: 700; border: 1px solid {color}40; font-size: 0.85rem;">{val_float:.1f}%</span>'
        except:
            return f'<span style="background: #6B728015; color: #6B7280; padding: 8px 14px; border-radius: 16px; font-weight: 700;">N/A</span>'
    
    display_df["Efficacité"] = display_df["Efficacité"].apply(format_efficiency)
    
    # Formater les nombres
    display_df["Buts"] = display_df["Buts"].apply(lambda x: f'<span style="font-weight: 600; color: {SECONDARY};">{int(x)}</span>')
    display_df["Passes"] = display_df["Passes"].apply(lambda x: f'<span style="font-weight: 600; color: {ACCENT};">{int(x)}</span>')
    display_df["Matchs"] = display_df["Matchs"].apply(lambda x: f'<span style="font-weight: 600;">{int(x)}</span>')
    
    # Afficher le tableau avec des informations
    st.markdown(f"""
    <div style="background: {CARD_BG}; padding: 1rem 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid {PRIMARY};">
        <span style="font-size: 1.1rem; font-weight: 700; color: {TEXT_DARK};">
             {len(display_df)} joueur(s) trouvé(s)
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Utiliser un container pour le tableau
    with st.container():
        st.markdown(
            display_df.to_html(escape=False, index=False), 
            unsafe_allow_html=True
        )
    

if __name__ == "__main__":
    main()
