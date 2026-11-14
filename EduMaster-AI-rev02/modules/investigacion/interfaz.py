"""
EduMaster AI — Módulo Central de Investigación y Prevención del Plagio

Integra:
1. Gestor de Citas y Bibliografía APA 7.
2. Verificador de Fuentes Científicas y DOIs en vivo (Crossref).
3. Detector de Citas Ausentes y afirmaciones no fundamentadas.
4. Analizador de Similitud Documental y coincidencia de textos.
"""

import streamlit as st
from .citas_apa import render_gestor_apa
from .verificador import render_verificador_fuentes
from .detector_citas import render_detector_citas
from .similitud import render_analizador_similitud


def render():
    st.header("🔬 Investigación, Fuentes y Prevención del Plagio")
    st.caption(
        "Herramientas rigurosas para la verificación científica, gestión bibliográfica en APA 7, "
        "detección de citas ausentes y análisis de similitud textual."
    )

    t1, t2, t3, t4 = st.tabs([
        "📑 Gestor APA 7",
        "🌐 Verificador de Fuentes (DOIs)",
        "⚠️ Detector de Citas Ausentes",
        "⚖️ Analizador de Similitud",
    ])

    with t1:
        render_gestor_apa()

    with t2:
        render_verificador_fuentes()

    with t3:
        render_detector_citas()

    with t4:
        render_analizador_similitud()
