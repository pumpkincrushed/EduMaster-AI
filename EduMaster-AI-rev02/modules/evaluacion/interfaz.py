"""
EduMaster AI — Interfaz del Módulo de Evaluación Educativa

Permite configurar, generar y descargar rúbricas analíticas, listas de cotejo
e instrumentos de evaluación formativa y competencial.
"""

import streamlit as st

from core.ai_engine import is_configured
from core.document_writer import create_docx, create_pdf
from .generador import (
    cargar_plantilla_rubrica,
    generar_instrumento_evaluacion,
)


def render():
    st.header("📊 Evaluación Educativa e Instrumentos")
    st.caption(
        "Diseña rúbricas analíticas en tabla, listas de cotejo e instrumentos de evaluación "
        "formativa alineados con el marco competencial y el Diseño Universal para el Aprendizaje (DUA)."
    )

    if not is_configured():
        st.error("Falta la clave GEMINI_API_KEY en la configuración (.env o st.secrets).")
        st.info("Configura la variable GEMINI_API_KEY para habilitar la generación de instrumentos.")
        return

    opciones_inst = [
        "Rúbrica Analítica Competencial (Matriz)",
        "Lista de Cotejo (Checklist formativo)",
        "Diana de Autoevaluación y Coevaluación",
        "Escala de Valoración Graduada",
    ]
    tipo_inst = st.selectbox("Tipo de instrumento", opciones_inst, key="eval_tipo")

    col1, col2 = st.columns(2)
    with col1:
        tarea = st.text_input(
            "Tarea, producto final o desempeño a evaluar",
            placeholder="Ej.: Exposición oral de un proyecto / Informe de investigación / Debate",
            key="eval_tarea",
        )
        materia = st.text_input(
            "Materia o Ámbito",
            placeholder="Ej.: Lengua Castellana / Geografía e Historia / Física y Química",
            key="eval_materia",
        )
    with col2:
        nivel = st.selectbox(
            "Etapa y nivel educativo",
            [
                "Educación Secundaria Obligatoria (ESO)",
                "Bachillerato",
                "Formación Profesional (FP)",
                "Universidad / Máster",
                "Educación Primaria",
            ],
            key="eval_nivel",
        )
        ponderacion = st.text_input(
            "Ponderación o pesos (opcional)",
            placeholder="Ej.: Contenido 40%, Comunicación 30%, Originalidad 30%",
            key="eval_ponderacion",
        )

    criterios = st.text_area(
        "Dimensiones o criterios específicos a priorizar (opcional)",
        placeholder="Ej.: Calidad de las fuentes, adecuación léxica, capacidad de síntesis, trabajo en equipo...",
        height=100,
        key="eval_criterios",
    )

    incluir_dua = st.checkbox(
        "Incluir adaptaciones DUA (evaluación inclusiva y multinivel)",
        value=True,
        key="eval_dua",
    )

    if st.button("🚀 Diseñar instrumento de evaluación", type="primary", key="btn_generar_eval"):
        if not tarea.strip():
            st.warning("Introduce la tarea o producto a evaluar.")
            return

        with st.spinner("Construyendo matriz e indicadores de evaluación..."):
            resultado = generar_instrumento_evaluacion(
                tipo_instrumento=tipo_inst,
                tarea_evaluar=tarea,
                materia=materia or "General",
                nivel_etapa=nivel,
                criterios_especificos=criterios,
                ponderaciones=ponderacion,
                incluir_dua=incluir_dua,
            )

        if not resultado.success:
            st.error(f"Error al generar instrumento: {resultado.error or resultado.content}")
            return

        st.session_state["eval_resultado"] = resultado.content
        st.session_state["eval_titulo"] = f"Rúbrica: {tarea}"

    if "eval_resultado" in st.session_state:
        st.subheader("📋 Instrumento de Evaluación Generado")
        st.markdown(st.session_state["eval_resultado"])

        st.divider()
        st.subheader("✏️ Editor para ajustes de ponderaciones o descriptores")
        texto_editado = st.text_area(
            "Puedes retocar los descriptores antes de exportar:",
            value=st.session_state["eval_resultado"],
            height=320,
            key="eval_area_edicion",
        )

        st.subheader("💾 Exportar instrumento")
        c_d1, c_d2, c_d3 = st.columns(3)

        c_d1.download_button(
            "Descargar en Markdown (.md)",
            data=texto_editado,
            file_name=f"evaluacion_{tarea[:20].strip().replace(' ', '_')}.md",
            mime="text/markdown",
            key="btn_descarga_md_eval",
        )

        try:
            docx_data = create_docx(
                content=texto_editado,
                title=st.session_state.get("eval_titulo", "Instrumento de Evaluación"),
                subtitle=f"{tipo_inst} — {materia} ({nivel})",
            )
            c_d2.download_button(
                "Descargar en Word (.docx)",
                data=docx_data,
                file_name=f"evaluacion_{tarea[:20].strip().replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="btn_descarga_docx_eval",
            )
        except Exception as e:
            c_d2.info(f"DOCX no disponible: {e}")

        try:
            pdf_data = create_pdf(
                content=texto_editado,
                title=st.session_state.get("eval_titulo", "Instrumento de Evaluación"),
                subtitle=f"{tipo_inst} — {materia} ({nivel})",
            )
            c_d3.download_button(
                "Descargar en PDF (.pdf)",
                data=pdf_data,
                file_name=f"evaluacion_{tarea[:20].strip().replace(' ', '_')}.pdf",
                mime="application/pdf",
                key="btn_descarga_pdf_eval",
            )
        except Exception as e:
            c_d3.info(f"PDF no disponible: {e}")
