"""
EduMaster AI — Interfaz del Generador de Trabajos Académicos

Permite configurar, estructurar y generar borradores originales para ensayos, TFM y actividades.
"""

import streamlit as st

from core.ai_engine import is_configured
from core.document_writer import create_docx, create_pdf
from .generador import (
    cargar_plantilla,
    sugerir_esquema,
    generar_contenido_trabajo,
)


def render():
    st.header("📝 Generador de Trabajos Académicos Originales")
    st.caption(
        "Elabora borradores originales para ensayos, TFM y tareas académicas a partir de tus propias "
        "consignas y esquemas, garantizando rigor ético y prevención de citas falsas."
    )

    if not is_configured():
        st.error("Falta la clave GEMINI_API_KEY en la configuración (.env o st.secrets).")
        st.info("Configura la variable GEMINI_API_KEY para activar la generación con IA.")
        return

    # Selección del tipo de trabajo
    opciones_tipo = [
        "Ensayo Académico",
        "Propuesta de Innovación Educativa (TFM)",
        "Actividad Académica / Tarea Competencial",
        "Trabajo Académico Personalizado",
    ]
    tipo_trabajo = st.selectbox("Tipo de trabajo académico", opciones_tipo, key="trabajos_tipo")

    # Mapeo a plantilla JSON si corresponde
    mapa_plantillas = {
        "Ensayo Académico": "ensayo",
        "Propuesta de Innovación Educativa (TFM)": "tfm_innovacion",
        "Actividad Académica / Tarea Competencial": "actividad",
    }

    # Datos básicos del encargo
    col1, col2 = st.columns([2, 1])
    with col1:
        tema = st.text_input(
            "Título o tema central del trabajo",
            placeholder="Ej.: El Aprendizaje Basado en Proyectos para la enseñanza de la Historia en Secundaria",
            key="trabajos_tema",
        )
    with col2:
        etapa = st.selectbox(
            "Etapa educativa / Contexto",
            [
                "Educación Secundaria Obligatoria (ESO)",
                "Bachillerato",
                "Formación Profesional (FP)",
                "Universidad / Máster",
                "Educación Primaria",
                "General / Teórico",
            ],
            key="trabajos_etapa",
        )

    consigna = st.text_area(
        "Consignas específicas, hipótesis u objetivos docentes (opcional)",
        placeholder="Ej.: Enfocar en la motivación del alumnado de 3º de ESO, incluir evaluación formativa y TIC...",
        height=100,
        key="trabajos_consigna",
    )

    # Configuración del esquema
    st.subheader("📑 Esquema y apartados del trabajo")
    st.caption("Puedes cargar la estructura recomendada, pedirle a la IA que te proponga una o escribir tu propio esquema.")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Cargar estructura estándar", key="btn_cargar_plantilla_trabajos"):
            p_id = mapa_plantillas.get(tipo_trabajo)
            if p_id:
                plantilla = cargar_plantilla(p_id)
                if plantilla and "secciones" in plantilla:
                    st.session_state["trabajos_esquema_actual"] = "\n".join(plantilla["secciones"])
                    st.success("Estructura estándar cargada.")
            else:
                st.session_state["trabajos_esquema_actual"] = (
                    "1. Introducción y Justificación\n"
                    "2. Marco Teórico y Conceptual\n"
                    "3. Desarrollo Principal\n"
                    "4. Conclusiones y Discusión\n"
                    "5. Referencias Bibliográficas"
                )

    with col_btn2:
        if st.button("Sugerir esquema personalizado con IA", key="btn_sugerir_esquema_trabajos"):
            if not tema.strip():
                st.warning("Escribe primero el título o tema central para poder sugerir un esquema adaptado.")
            else:
                with st.spinner("Diseñando esquema académico..."):
                    res_esquema = sugerir_esquema(tipo_trabajo, tema, consigna)
                    if res_esquema.success:
                        st.session_state["trabajos_esquema_actual"] = res_esquema.content
                        st.success("Esquema sugerido con éxito.")
                    else:
                        st.error(f"Error al generar esquema: {res_esquema.error or res_esquema.content}")

    esquema_inicial = st.session_state.get("trabajos_esquema_actual", "")
    esquema_usuario = st.text_area(
        "Esquema que se desarrollará (editable)",
        value=esquema_inicial,
        height=180,
        key="trabajos_area_esquema",
        placeholder="1. Introducción...\n2. Marco teórico...\n3. Metodología...",
    )

    col_ext, col_esp = st.columns([1, 1])
    with col_ext:
        extension = st.select_slider(
            "Extensión orientativa",
            options=[
                "Breve (600 - 900 palabras)",
                "Media (1000 - 1600 palabras)",
                "Extensa (2000 - 3000 palabras)",
            ],
            value="Media (1000 - 1600 palabras)",
            key="trabajos_extension",
        )

    st.divider()

    # Botón de generación
    if st.button("🚀 Generar borrador del trabajo", type="primary", key="btn_generar_trabajo"):
        if not tema.strip():
            st.warning("Por favor, introduce el título o tema del trabajo.")
            return
        if not esquema_usuario.strip():
            st.warning("Por favor, define o carga el esquema de apartados a desarrollar.")
            return

        with st.spinner("Redactando borrador académico original..."):
            resultado = generar_contenido_trabajo(
                tipo=tipo_trabajo,
                tema=tema,
                nivel_etapa=etapa,
                esquema=esquema_usuario,
                consigna=consigna,
                extension_orientativa=extension,
            )

        if not resultado.success:
            st.error(f"No se pudo generar el trabajo: {resultado.error or resultado.content}")
            return

        st.session_state["trabajo_generado_resultado"] = resultado.content
        st.session_state["trabajo_generado_titulo"] = tema

    # Mostrar resultado y opciones de edición y exportación
    if "trabajo_generado_resultado" in st.session_state:
        st.subheader("📄 Borrador Generado")
        
        st.warning(
            "⚠️ **Verificación de fuentes requerida:** Las afirmaciones teóricas que necesitan fundamentación "
            "incluyen la etiqueta `[Cita requerida]`. Puedes localizarlas y validarlas con el módulo **Investigar**."
        )

        st.markdown(st.session_state["trabajo_generado_resultado"])

        st.divider()
        st.subheader("✏️ Editor y revisión del borrador")
        texto_editado = st.text_area(
            "Puedes editar el texto final aquí antes de descargarlo:",
            value=st.session_state["trabajo_generado_resultado"],
            height=350,
            key="trabajos_area_edicion_final",
        )

        st.subheader("💾 Exportar trabajo")
        col_d1, col_d2, col_d3 = st.columns(3)

        col_d1.download_button(
            "Descargar en Markdown (.md)",
            data=texto_editado,
            file_name=f"{tema[:30].strip().replace(' ', '_')}.md",
            mime="text/markdown",
            key="btn_descarga_md_trabajos",
        )

        try:
            docx_data = create_docx(
                content=texto_editado,
                title=st.session_state.get("trabajo_generado_titulo", "Trabajo Académico"),
                subtitle=f"{tipo_trabajo} — EduMaster AI",
            )
            col_d2.download_button(
                "Descargar en Word (.docx)",
                data=docx_data,
                file_name=f"{tema[:30].strip().replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="btn_descarga_docx_trabajos",
            )
        except Exception as e:
            col_d2.info(f"DOCX no disponible: {e}")

        try:
            pdf_data = create_pdf(
                content=texto_editado,
                title=st.session_state.get("trabajo_generado_titulo", "Trabajo Académico"),
                subtitle=f"{tipo_trabajo} — EduMaster AI",
            )
            col_d3.download_button(
                "Descargar en PDF (.pdf)",
                data=pdf_data,
                file_name=f"{tema[:30].strip().replace(' ', '_')}.pdf",
                mime="application/pdf",
                key="btn_descarga_pdf_trabajos",
            )
        except Exception as e:
            col_d3.info(f"PDF no disponible: {e}")
