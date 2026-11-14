"""
EduMaster AI — Módulo de Revisión y Diagnóstico de Textos Académicos
"""

import streamlit as st
from .analisis import render as render_analisis
from .redaccion import render as render_redaccion

__all__ = ["render_analisis", "render_redaccion", "render"]


def render():
    """Vista integrada que agrupa Diagnóstico y Revisión en pestañas."""
    tab_analisis, tab_revision = st.tabs([
        "🔍 Diagnóstico sin modificar",
        "✍️ Revisión de redacción y rigor",
    ])
    with tab_analisis:
        render_analisis()
    with tab_revision:
        render_redaccion()
