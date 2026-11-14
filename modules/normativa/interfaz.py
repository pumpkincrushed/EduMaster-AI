"""
EduMaster AI — Interfaz del Consultor de Normativa Educativa

Permite consultar dudas legales sobre currículo y generar la fundamentación jurídica para TFM y programaciones.
"""

import streamlit as st

from core.ai_engine import is_configured
from core.document_writer import create_docx, create_pdf
from .consultor import consultar_normativa, generar_fundamentacion_juridica


def render():
    st.header("⚖️ Normativa Educativa y Marco Curricular")
    st.caption(
        "Consulta de legislación educativa (LOMLOE, Reales Decretos y decretos autonómicos) "
        "y redacción asistida de la justificación legal para tu TFM o programación didáctica."
    )

    if not is_configured():
        st.error("Falta la clave GEMINI_API_KEY en la configuración (.env o st.secrets).")
        st.info("Configura la variable GEMINI_API_KEY para habilitar la asesoría normativa.")
        return

    tab_consulta, tab_fundamentacion = st.tabs([
        "📖 Consultor de Dudas Normativas",
        "⚖️ Redactor de Fundamentación Legal (TFM / Programación)",
    ])

    ccaa_lista = [
        "Galicia", "Andalucía", "Cataluña", "Comunidad de Madrid",
        "Comunitat Valenciana", "Castilla y León", "Castilla-La Mancha",
        "País Vasco", "Canarias", "Región de Murcia", "Aragón",
        "Islas Baleares", "Extremadura", "Asturias", "Navarra",
        "Cantabria", "La Rioja", "Ceuta y Melilla", "Marco Estatal General",
    ]

    with tab_consulta:
        st.subheader("Asesoría Jurídico-Curricular")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            etapa_c = st.selectbox(
                "Etapa educativa",
                ["Educación Secundaria Obligatoria (ESO)", "Bachillerato", "Formación Profesional (FP)", "Primaria"],
                key="norm_cons_etapa",
            )
        with col_c2:
            ccaa_c = st.selectbox("Comunidad Autónoma", ccaa_lista, index=0, key="norm_cons_ccaa")

        duda = st.text_area(
            "Escribe tu duda sobre legislación o currículo",
            placeholder="Ej.: ¿Cuáles son los criterios de promoción en 4º de ESO según la LOMLOE en Galicia? / ¿Cómo se justifican las situaciones de aprendizaje?",
            height=120,
            key="norm_cons_duda",
        )

        if st.button("Consultar normativa", type="primary", key="btn_consultar_norm"):
            if not duda.strip():
                st.warning("Introduce tu consulta.")
            else:
                with st.spinner("Analizando marco legislativo y decretos aplicables..."):
                    res = consultar_normativa(duda, etapa=etapa_c, comunidad_autonoma=ccaa_c)
                if res.success:
                    st.markdown(res.content)
                else:
                    st.error(f"Error al consultar: {res.error or res.content}")

    with tab_fundamentacion:
        st.subheader("Redacción de Fundamentación Jurídica para TFM / Programación")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            materia_f = st.text_input("Materia o Especialidad", placeholder="Ej.: Lengua y Literatura / Matemáticas", key="norm_f_materia")
            curso_f = st.text_input("Curso y Etapa", placeholder="Ej.: 3º de ESO / 1º de Bachillerato", key="norm_f_curso")
        with col_f2:
            ccaa_f = st.selectbox("Comunidad Autónoma", ccaa_lista, index=0, key="norm_f_ccaa")
            tema_f = st.text_input("Tema o Propuesta de innovación", placeholder="Ej.: Situaciones de aprendizaje basadas en ABP", key="norm_f_tema")

        if st.button("Redactar apartado de Fundamentación Legal", type="primary", key="btn_redactar_fundamentacion"):
            if not materia_f.strip() or not curso_f.strip():
                st.warning("Indica al menos la materia y el curso.")
            else:
                with st.spinner("Redactando fundamentación jurídica rigurosa..."):
                    res_f = generar_fundamentacion_juridica(
                        materia=materia_f,
                        curso_etapa=curso_f,
                        tema_proyecto=tema_f or "Programación Docente Anual",
                        comunidad_autonoma=ccaa_f,
                    )
                if res_f.success:
                    st.session_state["norm_fundamentacion_res"] = res_f.content
                else:
                    st.error(f"Error al redactar: {res_f.error or res_f.content}")

        if "norm_fundamentacion_res" in st.session_state:
            st.divider()
            st.markdown(st.session_state["norm_fundamentacion_res"])

            st.subheader("💾 Exportar apartado legal")
            d1, d2, d3 = st.columns(3)
            d1.download_button(
                "Descargar en Markdown (.md)",
                data=st.session_state["norm_fundamentacion_res"],
                file_name="fundamentacion_legal_edumaster.md",
                mime="text/markdown",
                key="btn_descarga_md_norm",
            )
            try:
                docx_b = create_docx(
                    content=st.session_state["norm_fundamentacion_res"],
                    title="Fundamentación Jurídica y Curricular",
                    subtitle=f"{materia_f} ({curso_f}) — {ccaa_f}",
                )
                d2.download_button(
                    "Descargar en Word (.docx)",
                    data=docx_b,
                    file_name="fundamentacion_legal_edumaster.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key="btn_descarga_docx_norm",
                )
            except Exception as e:
                d2.info(f"DOCX no disponible: {e}")

            try:
                pdf_b = create_pdf(
                    content=st.session_state["norm_fundamentacion_res"],
                    title="Fundamentación Jurídica y Curricular",
                    subtitle=f"{materia_f} ({curso_f}) — {ccaa_f}",
                )
                d3.download_button(
                    "Descargar en PDF (.pdf)",
                    data=pdf_b,
                    file_name="fundamentacion_legal_edumaster.pdf",
                    mime="application/pdf",
                    key="btn_descarga_pdf_norm",
                )
            except Exception as e:
                d3.info(f"PDF no disponible: {e}")
