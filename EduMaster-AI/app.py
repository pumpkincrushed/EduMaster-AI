"""
EduMaster AI — Punto de entrada principal de Streamlit

Configura la página, aplica el estilo visual personalizado,
renderiza el menú lateral y enruta a cada módulo.
"""

import streamlit as st

from config.settings import APP_NAME, APP_SUBTITLE, APP_ICON, MODULES
from core.ai_engine import is_configured

# ─── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": f"**{APP_NAME}** — Plataforma académica y pedagógica con IA\n\nDesarrollada con Streamlit y Google Gemini.",
    },
)

# ─── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Importar fuente ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Variables de color ── */
:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --primary-light: #818cf8;
    --accent: #a855f7;
    --bg-dark: #0f0f1a;
    --bg-card: #1a1a2e;
    --bg-panel: #16213e;
    --border: rgba(99, 102, 241, 0.2);
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
}

/* ── Fondo global ── */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #0f1629 100%);
    font-family: 'Inter', sans-serif;
}

/* ── Ocultar elementos por defecto de Streamlit ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #1a1a2e 100%);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-primary);
}

/* ── Logo en sidebar ── */
.sidebar-logo {
    text-align: center;
    padding: 1.5rem 0 1rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}

.sidebar-logo-icon {
    font-size: 2.5rem;
    display: block;
    margin-bottom: 0.5rem;
}

.sidebar-logo-title {
    font-size: 1.3rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary-light), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}

.sidebar-logo-sub {
    font-size: 0.7rem;
    color: var(--text-secondary);
    margin-top: 0.25rem;
}

/* ── Botones del menú lateral ── */
.nav-btn {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 0.25rem;
    color: var(--text-secondary);
    text-decoration: none;
    width: 100%;
    border: none;
    background: transparent;
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
}

.nav-btn:hover {
    background: rgba(99, 102, 241, 0.1);
    color: var(--text-primary);
}

.nav-btn.active {
    background: rgba(99, 102, 241, 0.2);
    color: var(--primary-light);
    border-left: 3px solid var(--primary);
}

.nav-btn-icon { font-size: 1.1rem; min-width: 1.5rem; }
.nav-btn-text { flex: 1; text-align: left; }
.nav-btn-badge {
    font-size: 0.65rem;
    padding: 0.1rem 0.5rem;
    border-radius: 20px;
    background: rgba(99, 102, 241, 0.3);
    color: var(--primary-light);
}

/* ── Cabecera de módulo ── */
.module-header {
    display: flex;
    align-items: flex-start;
    gap: 1.25rem;
    padding: 1.75rem 2rem;
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.08));
    border: 1px solid var(--border);
    border-radius: 16px;
    margin-bottom: 1.75rem;
    backdrop-filter: blur(10px);
}

.module-icon {
    font-size: 2.5rem;
    line-height: 1;
    min-width: 3rem;
}

.module-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 0.25rem 0;
    background: linear-gradient(135deg, #fff, var(--primary-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.module-desc {
    color: var(--text-secondary);
    margin: 0;
    font-size: 0.95rem;
    line-height: 1.5;
}

/* ── Cards de próximamente ── */
.coming-soon-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    max-width: 700px;
    margin: 2rem auto;
}

.coming-soon-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.coming-soon-card h3 {
    color: var(--primary-light);
    font-size: 1.4rem;
    margin-bottom: 0.75rem;
}

.coming-soon-card p {
    color: var(--text-secondary);
    margin-bottom: 2rem;
}

.feature-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    text-align: left;
}

.feature-item {
    background: rgba(99,102,241,0.08);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    color: var(--text-secondary);
    font-size: 0.875rem;
}

/* ── Paneles de texto comparativo ── */
.text-panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem;
    min-height: 300px;
    max-height: 500px;
    overflow-y: auto;
    font-size: 0.9rem;
    line-height: 1.7;
    color: var(--text-secondary);
    white-space: pre-wrap;
}

.text-panel.original {
    border-left: 3px solid rgba(148, 163, 184, 0.4);
}

.text-panel.revised {
    border-left: 3px solid var(--success);
    color: var(--text-primary);
}

/* ── Info de texto ── */
.text-info {
    color: var(--text-secondary);
    font-size: 0.85rem;
    padding: 0.6rem 1rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-top: 0.4rem;
}

/* ── Métricas ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.8rem;
}

[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
}

/* ── Botones primarios ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--primary), var(--accent));
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: 600;
    padding: 0.6rem 1.5rem;
    transition: all 0.2s ease;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}

/* ── Inputs ── */
.stTextArea textarea,
.stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* ── Expanders ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-secondary) !important;
}

/* ── Alertas ── */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
}

/* ── Dividers ── */
hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0;
}

/* ── Home cards ── */
.home-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.5rem;
    transition: all 0.2s ease;
    cursor: default;
    height: 100%;
}

.home-card:hover {
    border-color: rgba(99, 102, 241, 0.4);
    background: rgba(99, 102, 241, 0.05);
    transform: translateY(-2px);
}

.home-card-icon { font-size: 2rem; margin-bottom: 0.75rem; }
.home-card-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.4rem;
}
.home-card-desc {
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.5;
}
.home-card-badge {
    display: inline-block;
    margin-top: 0.75rem;
    font-size: 0.7rem;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.3);
}
.home-card-badge.soon {
    background: rgba(99, 102, 241, 0.12);
    color: var(--primary-light);
    border-color: var(--border);
}

/* ── Status badge API ── */
.api-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
    font-size: 0.8rem;
    margin-top: 1rem;
}
.api-status.ok {
    background: rgba(16,185,129,0.1);
    color: #10b981;
    border: 1px solid rgba(16,185,129,0.2);
}
.api-status.error {
    background: rgba(239,68,68,0.1);
    color: #ef4444;
    border: 1px solid rgba(239,68,68,0.2);
}
</style>
""", unsafe_allow_html=True)


# ─── Estado de sesión ─────────────────────────────────────────────────────────
if "active_module" not in st.session_state:
    st.session_state.active_module = "home"


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="sidebar-logo">
        <span class="sidebar-logo-icon">🎓</span>
        <div class="sidebar-logo-title">EduMaster AI</div>
        <div class="sidebar-logo-sub">Plataforma académica con IA</div>
    </div>
    """, unsafe_allow_html=True)

    # Botón de Inicio
    if st.button(
        "🏠  Inicio",
        use_container_width=True,
        type="secondary" if st.session_state.active_module != "home" else "primary",
        key="nav_home",
    ):
        st.session_state.active_module = "home"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;"
        "color:rgba(148,163,184,0.5);padding:0 0.5rem;margin-bottom:0.5rem;'>Módulos</div>",
        unsafe_allow_html=True,
    )

    # Módulos
    for module in MODULES:
        label = f"{module['icon']}  {module['name']}"
        badge = "🟢 Activo" if module["status"] == "active" else "Próximamente"
        is_active = st.session_state.active_module == module["id"]

        if st.button(
            label,
            use_container_width=True,
            type="primary" if is_active else "secondary",
            key=f"nav_{module['id']}",
        ):
            st.session_state.active_module = module["id"]
            st.rerun()

    # Estado API en sidebar
    st.markdown("<br>", unsafe_allow_html=True)
    if is_configured():
        st.markdown("""
        <div class="api-status ok">
            <span>●</span> API Gemini conectada
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="api-status error">
            <span>●</span> API no configurada
        </div>
        """, unsafe_allow_html=True)


# ─── Enrutador principal ──────────────────────────────────────────────────────
active = st.session_state.active_module

if active == "home":
    # ── Página de inicio ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding: 3rem 0 2rem 0;">
        <div style="font-size:3.5rem; margin-bottom:1rem;">🎓</div>
        <h1 style="font-size:2.5rem; font-weight:800;
            background: linear-gradient(135deg, #818cf8, #a855f7);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text; margin-bottom:0.5rem;">
            EduMaster AI
        </h1>
        <p style="color:#94a3b8; font-size:1.1rem; max-width:600px; margin:0 auto;">
            Plataforma académica y pedagógica con Inteligencia Artificial.<br>
            Escoge un módulo del menú lateral para comenzar.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Cards de módulos
    cols = st.columns(4)
    for i, module in enumerate(MODULES):
        with cols[i % 4]:
            badge_class = "" if module["status"] == "active" else "soon"
            badge_text = "✅ Disponible" if module["status"] == "active" else "🔄 Próximamente"
            st.markdown(f"""
            <div class="home-card">
                <div class="home-card-icon">{module['icon']}</div>
                <div class="home-card-title">{module['name']}</div>
                <div class="home-card-desc">{module['description']}</div>
                <span class="home-card-badge {badge_class}">{badge_text}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

elif active == "humanizador":
    from modules.humanizador.interface import render
    render()

elif active == "trabajos":
    from modules.trabajos.interface import render
    render()

elif active == "materiales":
    from modules.materiales.interface import render
    render()

elif active == "investigacion":
    from modules.investigacion.interface import render
    render()

elif active == "evaluacion":
    from modules.evaluacion.interface import render
    render()

elif active == "documentos":
    from modules.documentos.interface import render
    render()

elif active == "normativa":
    from modules.normativa.interface import render
    render()

elif active == "asistente":
    from modules.asistente.interface import render
    render()
