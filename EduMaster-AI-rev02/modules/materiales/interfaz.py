"""
EduMaster AI — Interfaz del Generador de Materiales Didácticos

Permite configurar, estructurar y redactar situaciones de aprendizaje, unidades y recursos de aula.
"""

import streamlit as st

from core.ai_engine import is_configured
from core.document_writer import create_docx, create_pdf
from .generador import (
    cargar_plantilla_unidad,
    generar_material_didactico,
)


def render():
    st.header("📚 Generador de Materiales y Recursos Didácticos")
    st.caption(
        "Diseña situaciones de aprendizaje, unidades didácticas y recursos pedagógicos adaptados "
        "a tu materia y nivel educativo, con enfoque competencial y DUA."
    )

    if not is_configured():
        st.error("Falta la clave GEMINI_API_KEY en la configuración (.env o st.secrets).")
        st.info("Configura la variable GEMINI_API_KEY para habilitar la generación de recursos didácticos.")
        return

    # 1. Tipo de material pedagógico
    opciones_recurso = [
        "Situación de Aprendizaje (LOMLOE)",
        "Guía de Trabajo y Recursos para el Alumnado",
        "Propuesta Didáctica DUA (Atención a la Diversidad)",
        "Unidad Didáctica Personalizada",
    ]
    tipo_recurso = st.selectbox("Tipo de recurso didáctico", opciones_recurso, key="mat_tipo_recurso")

    mapa_plantillas = {
        "Situación de Aprendizaje (LOMLOE)": "situacion_aprendizaje_lomloe",
        "Guía de Trabajo y Recursos para el Alumnado": "guia_alumnado",
        "Propuesta Didáctica DUA (Atención a la Diversidad)": "adaptacion_dua",
    }

    # 2. Configuración curricular y contexto
    col1, col2 = st.columns(2)
    with col1:
        titulo = st.text_input(
            "Título o reto de la situación / unidad",
            placeholder="Ej.: 'Guardianes del Clima: Misión Sostenibilidad'",
            key="mat_titulo",
        )
        materia = st.text_input(
            "Materia, Área o Módulo formativo",
            placeholder="Ej.: Biología y Geología / Geografía e Historia / Lengua",
            key="mat_materia",
        )

    with col2:
        nivel = st.selectbox(
            "Nivel educativo y curso",
            [
                "1º ESO", "2º ESO", "3º ESO", "4º ESO",
                "1º Bachillerato", "2º Bachillerato",
                "FP Grado Básico", "FP Grado Medio", "FP Grado Superior",
                "Educación Primaria (5º - 6º)",
                "Universidad / Grado",
            ],
            key="mat_nivel",
        )
        duracion = st.selectbox(
            "Temporalización estimada",
            [
                "3 a 4 sesiones (1 semana aprox.)",
                "6 a 8 sesiones (Unidad estándar de 2-3 semanas)",
                "10 a 12 sesiones (Proyecto trimestral extenso)",
                "1 sesión puntual (Taller / Actividad intensiva)",
            ],
            key="mat_duracion",
        )

    col_met, col_obj = st.columns(2)
    with col_met:
        metodologia = st.selectbox(
            "Metodología activa predominante",
            [
                "Aprendizaje Basado en Proyectos (ABP)",
                "Aprendizaje Cooperativo (estructuras Kagan/Johnson)",
                "Flipped Classroom (Clase invertida)",
                "Aprendizaje-Servicio (ApS)",
                "Gamificación y retos pedagógicos",
                "Indagación y método científico",
                "Enseñanza multinivel y DUA",
            ],
            key="mat_metodologia",
        )

    with col_obj:
        consigna = st.text_area(
            "Objetivos clave, saberes básicos o retos específicos",
            placeholder="Ej.: Vinculado al ODS 13, elaboración de un pódcast divulgativo, trabajo en equipos heterogéneos...",
            height=85,
            key="mat_consigna",
        )

    # 3. Estructura y esquema
    st.subheader("📑 Estructura de la unidad didáctica")
    if st.button("Cargar estructura recomendada", key="btn_cargar_plantilla_mat"):
        p_id = mapa_plantillas.get(tipo_recurso)
        if p_id:
            p_data = cargar_plantilla_unidad(p_id)
            if p_data and "secciones" in p_data:
                st.session_state["mat_esquema_actual"] = "\n".join(p_data["secciones"])
                st.success("Estructura curricular cargada.")
        else:
            st.session_state["mat_esquema_actual"] = (
                "1. Justificación y contexto\n"
                "2. Competencias y saberes básicos\n"
                "3. Secuencia de actividades por sesiones\n"
                "4. Metodología y recursos\n"
                "5. Evaluación competencial"
            )

    esquema_inicial = st.session_state.get("mat_esquema_actual", "")
    esquema_usuario = st.text_area(
        "Esquema curricular a desarrollar (editable)",
        value=esquema_inicial,
        height=180,
        key="mat_area_esquema",
        placeholder="1. Datos identificativos...\n2. Conexión curricular...\n3. Secuencia de sesiones...",
    )

    st.divider()

    # 4. Generación
    if st.button("🚀 Elaborar recurso didáctico", type="primary", key="btn_generar_material"):
        if not titulo.strip():
            st.warning("Introduce el título o reto central del recurso.")
            return
        if not materia.strip():
            st.warning("Especifica la materia o área formativa.")
            return
        if not esquema_usuario.strip():
            st.warning("Carga o escribe el esquema curricular a desarrollar.")
            return

        with st.spinner("Diseñando material didáctico con enfoque competencial..."):
            resultado = generar_material_didactico(
                tipo_recurso=tipo_recurso,
                titulo=titulo,
                materia=materia,
                nivel_etapa=nivel,
                duracion_sesiones=duracion,
                metodologia=metodologia,
                objetivos_consigna=consigna,
                esquema=esquema_usuario,
            )

        if not resultado.success:
            st.error(f"Error al generar material didáctico: {resultado.error or resultado.content}")
            return

        st.session_state["material_resultado"] = resultado.content
        st.session_state["material_titulo"] = titulo

    # 5. Visualización, edición y exportación
    if "material_resultado" in st.session_state:
        st.subheader("📋 Recurso Didáctico Elaborado")
        st.markdown(st.session_state["material_resultado"])

        st.divider()
        st.subheader("✏️ Editor para personalización docente")
        texto_editado = st.text_area(
            "Ajusta los detalles de las sesiones, actividades o recursos según tu centro:",
            value=st.session_state["material_resultado"],
            height=340,
            key="mat_area_edicion_final",
        )

        st.subheader("💾 Exportar recurso")
        col_d1, col_d2, col_d3 = st.columns(3)

        col_d1.download_button(
            "Descargar en Markdown (.md)",
            data=texto_editado,
            file_name=f"unidad_{titulo[:25].strip().replace(' ', '_')}.md",
            mime="text/markdown",
            key="btn_descarga_md_mat",
        )

        try:
            docx_data = create_docx(
                content=texto_editado,
                title=st.session_state.get("material_titulo", "Unidad Didáctica"),
                subtitle=f"{tipo_recurso} — {materia} ({nivel})",
            )
            col_d2.download_button(
                "Descargar en Word (.docx)",
                data=docx_data,
                file_name=f"unidad_{titulo[:25].strip().replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="btn_descarga_docx_mat",
            )
        except Exception as e:
            col_d2.info(f"DOCX no disponible: {e}")

        try:
            pdf_data = create_pdf(
                content=texto_editado,
                title=st.session_state.get("material_titulo", "Unidad Didáctica"),
                subtitle=f"{tipo_recurso} — {materia} ({nivel})",
            )
            col_d3.download_button(
                "Descargar en PDF (.pdf)",
                data=pdf_data,
                file_name=f"unidad_{titulo[:25].strip().replace(' ', '_')}.pdf",
                mime="application/pdf",
                key="btn_descarga_pdf_mat",
            )
        except Exception as e:
            col_d3.info(f"PDF no disponible: {e}")
