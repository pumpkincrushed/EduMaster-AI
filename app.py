"""
EduMaster AI — Aplicación Web Principal

Asistente académico basado en Inteligencia Artificial para el Máster de Formación del Profesorado
y el ámbito universitario. Organizado en tres áreas fundamentales:
1. Creación de contenido original
2. Revisión y prevención del plagio
3. Entrega y acompañamiento
"""

import streamlit as st
from modules.revision import render_analisis, render_redaccion
from modules.trabajos import render as render_trabajos
from modules.materiales import render as render_materiales
from modules.investigacion import render as render_investigacion
from modules.documentos import render as render_documentos
from modules.evaluacion import render as render_evaluacion
from modules.normativa import render as render_normativa
from modules.asistente import render as render_asistente

# Configuración general de la página
st.set_page_config(
    page_title="EduMaster AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── BARRA LATERAL: NAVEGACIÓN JERÁRQUICA ──────────────────────────────────────
st.sidebar.title("🎓 EduMaster AI")
st.sidebar.caption("Plataforma académica con rigor pedagógico e IA")

# 1. Selector de categoría principal
CATEGORIAS = [
    "🔍 Revisión y prevención del plagio",
    "✍️ Creación de contenido original",
    "📦 Entrega y acompañamiento",
]

categoria_seleccionada = st.sidebar.selectbox(
    "Área de trabajo",
    CATEGORIAS,
    index=0,
)

# 2. Selector de herramienta según categoría
HERRAMIENTAS = {
    "✍️ Creación de contenido original": [
        ("Trabajos", "Ensayos, TFM y actividades"),
        ("Materiales", "Unidades y recursos didácticos"),
        ("Evaluación", "Rúbricas e instrumentos de evaluación"),
    ],
    "🔍 Revisión y prevención del plagio": [
        ("Analizar", "Diagnosticar textos sin modificarlos"),
        ("Revisar", "Mejorar la redacción y el rigor académico"),
        ("Investigar", "Localizar y verificar fuentes en APA 7"),
    ],
    "📦 Entrega y acompañamiento": [
        ("Documentos", "Exportar resultados a Word y PDF"),
        ("Normativa", "Consultar legislación educativa"),
        ("Asistente", "Orientar al usuario a la herramienta adecuada"),
    ],
}

opciones_sub = [f"{nombre}: {desc}" for nombre, desc in HERRAMIENTAS[categoria_seleccionada]]
sub_seleccion = st.sidebar.radio("Herramienta", opciones_sub)
herramienta_actual = sub_seleccion.split(":")[0].strip()

st.sidebar.divider()
st.sidebar.info(
    "💡 **Rigor Académico:** EduMaster AI fomenta la autoría honesta. "
    "Las herramientas analizan y sugieren; tú conservas la autoría final."
)
st.sidebar.caption("EduMaster AI · Versión 1.1")

# ─── ENRUTAMIENTO DE MÓDULOS ───────────────────────────────────────────────────

if herramienta_actual == "Analizar":
    render_analisis()

elif herramienta_actual == "Revisar":
    render_redaccion()

elif herramienta_actual == "Investigar":
    render_investigacion()

elif herramienta_actual == "Trabajos":
    render_trabajos()

elif herramienta_actual == "Materiales":
    render_materiales()

elif herramienta_actual == "Evaluación":
    render_evaluacion()

elif herramienta_actual == "Documentos":
    render_documentos()

elif herramienta_actual == "Normativa":
    render_normativa()

elif herramienta_actual == "Asistente":
    render_asistente()
