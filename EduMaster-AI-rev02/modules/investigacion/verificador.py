"""
EduMaster AI — Verificador de Fuentes y DOIs Reales

Comprueba la existencia fehaciente de artículos y publicaciones en bases científicas reales (Crossref)
y verifica el estado de enlaces para erradicar citas alucinadas o fraudulentas.
"""

import streamlit as st
from core.source_validator import verify_doi, search_crossref, verify_url
from config.models import BibliographyEntry


def render_verificador_fuentes():
    st.subheader("🌐 Verificador de Fuentes Científicas y DOIs")
    st.caption(
        "Garantía contra citas alucinadas: conecta en vivo con la base oficial de Crossref "
        "para certificar autores, año, revista y existencia real del documento."
    )

    tab_doi, tab_busqueda, tab_url = st.tabs([
        "🔍 Comprobar DOI concreto",
        "📚 Buscar artículos reales por título / tema",
        "🔗 Verificar enlace o URL",
    ])

    with tab_doi:
        doi_input = st.text_input(
            "Introduce el DOI a comprobar",
            placeholder="Ej.: 10.1016/j.learninstruc.2021.101434 o https://doi.org/...",
            key="verif_doi_input",
        )
        if st.button("Verificar existencia en Crossref", type="primary", key="btn_check_doi"):
            if not doi_input.strip():
                st.warning("Introduce un DOI válido.")
            else:
                with st.spinner("Consultando servidores de Crossref..."):
                    resultado = verify_doi(doi_input)

                if resultado.get("valid"):
                    st.success("✅ **DOI Oficial verificado con éxito en Crossref.**")
                    st.markdown(f"**Título:** {resultado.get('title')}")
                    st.markdown(f"**Autores:** {', '.join(resultado.get('authors', [])) or 'No especificados'}")
                    st.markdown(f"**Año:** {resultado.get('year') or 'Desconocido'}")
                    st.markdown(f"**Revista / Fuente:** {resultado.get('journal') or 'No especificada'}")
                    st.markdown(f"**Enlace oficial:** [https://doi.org/{resultado.get('doi')}](https://doi.org/{resultado.get('doi')})")

                    entry = BibliographyEntry(
                        authors=resultado.get("authors", []),
                        year=resultado.get("year") or 2024,
                        title=resultado.get("title", ""),
                        source=resultado.get("journal", ""),
                        doi=resultado.get("doi"),
                        verified=True,
                    )
                    st.info(f"**Formato APA 7 automático:**\n> {entry.to_apa7()}")
                else:
                    st.error(f"❌ **Verificación fallida:** {resultado.get('error')}")
                    st.warning("Advertencia: No utilices esta cita en tu trabajo académico sin comprobar que el artículo existe realmente.")

    with tab_busqueda:
        query = st.text_input(
            "Buscar publicaciones en la base científica de Crossref",
            placeholder="Ej.: flipped classroom secondary education mathematics",
            key="verif_query_busqueda",
        )
        filas = st.slider("Resultados máximos", min_value=3, max_value=10, value=5, key="verif_filas_busqueda")
        if st.button("Buscar en Crossref", type="primary", key="btn_buscar_crossref"):
            if not query.strip():
                st.warning("Introduce un término de búsqueda.")
            else:
                with st.spinner("Buscando en millones de publicaciones académicas..."):
                    articulos = search_crossref(query, rows=filas)

                if articulos:
                    st.success(f"Se han localizado {len(articulos)} publicaciones reales:")
                    for idx, art in enumerate(articulos, start=1):
                        with st.expander(f"{idx}. {art['title']} ({art['year'] or 's.f.'})"):
                            st.write(f"**Autores:** {', '.join(art['authors']) or 'No especificados'}")
                            st.write(f"**Revista / Editorial:** {art['journal'] or 'No especificada'}")
                            if art['doi']:
                                st.write(f"**DOI:** `{art['doi']}`")
                                st.markdown(f"[Abrir publicación](https://doi.org/{art['doi']})")
                            entry = BibliographyEntry(
                                authors=art["authors"],
                                year=art["year"] or 2024,
                                title=art["title"],
                                source=art["journal"],
                                doi=art["doi"] or None,
                                verified=True,
                            )
                            st.code(entry.to_apa7(), language="text")
                else:
                    st.info("No se encontraron publicaciones que coincidan con la búsqueda.")

    with tab_url:
        url_input = st.text_input(
            "Introduce un enlace web o repositorio a verificar",
            placeholder="https://dialnet.unirioja.es/...",
            key="verif_url_input",
        )
        if st.button("Comprobar estado del enlace", key="btn_check_url"):
            if not url_input.strip():
                st.warning("Introduce una URL completa.")
            else:
                with st.spinner("Verificando disponibilidad de la URL..."):
                    estado = verify_url(url_input)
                if estado.get("valid"):
                    st.success(f"✅ Enlace activo y accesible (HTTP {estado.get('status_code')}).")
                else:
                    st.error(f"❌ Error al conectar con el enlace: {estado.get('error')}")
