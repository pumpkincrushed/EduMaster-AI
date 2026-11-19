"""
EduMaster AI — Analizador de Similitud Documental

Compara borradores contra documentos de referencia o fuentes disponibles para
detectar coincidencias textuales, solapamiento léxico y prevenir el plagio directo.
"""

import streamlit as st
from core.source_validator import calculate_text_similarity
from core.document_reader import read_uploaded_file


def render_analizador_similitud():
    st.subheader("⚖️ Analizador de Similitud Documental")
    st.caption(
        "Compara tu borrador contra una fuente o documento de referencia para detectar "
        "coincidencias léxicas exactas, n-gramas idénticos y verificar el parafraseo correcto."
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**1. Tu Borrador**")
        modo_b = st.radio("Entrada borrador", ["Pegar texto", "Subir archivo"], horizontal=True, key="sim_modo_b")
        draft_text = ""
        if modo_b == "Subir archivo":
            f_b = st.file_uploader("Borrador (.docx, .pdf, .txt)", type=["docx", "pdf", "txt"], key="sim_up_b")
            if f_b:
                draft_text = read_uploaded_file(f_b) or ""
                st.caption(f"Cargado: {f_b.name} ({len(draft_text.split())} palabras)")
        else:
            draft_text = st.text_area("Pega tu borrador", height=220, key="sim_text_b", placeholder="Pega aquí tu texto...")

    with c2:
        st.markdown("**2. Documento o Fuente de Referencia**")
        modo_s = st.radio("Entrada fuente", ["Pegar texto", "Subir archivo"], horizontal=True, key="sim_modo_s")
        source_text = ""
        if modo_s == "Subir archivo":
            f_s = st.file_uploader("Fuente (.docx, .pdf, .txt)", type=["docx", "pdf", "txt"], key="sim_up_s")
            if f_s:
                source_text = read_uploaded_file(f_s) or ""
                st.caption(f"Cargado: {f_s.name} ({len(source_text.split())} palabras)")
        else:
            source_text = st.text_area("Pega la fuente de referencia", height=220, key="sim_text_s", placeholder="Pega aquí el texto original a comparar...")

    n_gram_size = st.slider("Sensibilidad de coincidencia de frase (longitud mínima en palabras)", 3, 7, 4, key="sim_ngram_slider")

    if st.button("Comparar similitud textual", type="primary", key="btn_calcular_similitud"):
        if not draft_text.strip() or not source_text.strip():
            st.warning("Debes introducir tanto el borrador como el texto fuente de comparación.")
        else:
            with st.spinner("Analizando solapamiento de n-gramas y vocabulario..."):
                res = calculate_text_similarity(draft_text, source_text, n_gram_size=n_gram_size)

            st.divider()
            st.subheader("📊 Resultados de Similitud")

            m1, m2, m3 = st.columns(3)
            sim_pct = res["similarity_percentage"]
            jaccard = res["jaccard_similarity"]
            count = res["matching_count"]

            m1.metric("Similitud de frases continuas", f"{sim_pct}%")
            m2.metric("Vocabulario compartido (Jaccard)", f"{jaccard}%")
            m3.metric("Bloques idénticos detectados", count)

            if sim_pct > 30.0:
                st.error(
                    f"⚠️ **Alto índice de coincidencia textual ({sim_pct}%):** Hay múltiples fragmentos de {n_gram_size} o más palabras "
                    "idénticas a la fuente. Si corresponden a citas textuales, asegúrate de colocarlas entre comillas con su cita correspondiente."
                )
            elif sim_pct > 10.0:
                st.warning(
                    f"⚠️ **Coincidencia moderada ({sim_pct}%):** Revisa las frases coincidentes para asegurar que haya una reelaboración personal "
                    "y una cita de autor adecuada."
                )
            else:
                st.success(
                    f"✅ **Baja coincidencia textual ({sim_pct}%):** La redacción muestra autonomía léxica respecto a la fuente proporcionada."
                )

            if res["matching_samples"]:
                with st.expander(f"🔍 Ver secuencias idénticas detectadas ({count} en total)"):
                    for idx, sample in enumerate(res["matching_samples"], start=1):
                        st.markdown(f"{idx}. `\"{sample}\"`")

            st.info(
                "💡 **Criterio metodológico:** La similitud léxica no equivale automáticamente a plagio. "
                "Las citas textuales encomilladas y con autor son completamente legítimas. "
                "El plagio se produce cuando se copian estructuras, ideas o fragmentos sin atribuir la fuente original."
            )
