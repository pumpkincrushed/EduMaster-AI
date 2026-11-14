"""
EduMaster AI — Módulo de Exportación y Maquetación de Documentos

Espacio centralizado para componer, maquetar y exportar documentos académicos a formatos
Word (.docx) y PDF (.pdf) con formato estándar universitario y APA 7.
"""

import streamlit as st
from core.document_writer import create_docx, create_pdf
from core.document_reader import read_uploaded_file


def render():
    st.header("📄 Exportación y Maquetación de Documentos")
    st.caption(
        "Convierte cualquier borrador, memoria de TFM, unidad didáctica o informe en documentos "
        "formales en Word (.docx) y PDF (.pdf) con maquetación académica profesional."
    )

    modo_entrada = st.radio(
        "Origen del contenido",
        ["Escribir o pegar texto / Markdown", "Cargar archivo (.docx, .pdf, .txt)"],
        horizontal=True,
        key="doc_modo_entrada",
    )

    contenido_doc = ""
    if modo_entrada == "Cargar archivo (.docx, .pdf, .txt)":
        archivo_cargado = st.file_uploader(
            "Selecciona un archivo",
            type=["docx", "pdf", "txt", "md"],
            key="doc_uploader",
        )
        if archivo_cargado:
            try:
                if archivo_cargado.name.lower().endswith(".md"):
                    contenido_doc = archivo_cargado.read().decode("utf-8")
                else:
                    contenido_doc = read_uploaded_file(archivo_cargado) or ""
                st.success(f"Archivo cargado: **{archivo_cargado.name}** ({len(contenido_doc.split())} palabras)")
            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")
    else:
        contenido_doc = st.text_area(
            "Contenido del documento (admite encabezados #, ## y listas)",
            height=280,
            placeholder="# 1. Introducción\nEscribe aquí el texto que deseas maquetar y exportar...",
            key="doc_texto_area",
        )

    # Metadatos para la portada y encabezados
    st.subheader("📑 Metadatos y maquetación académica")
    c1, c2 = st.columns(2)
    with c1:
        titulo = st.text_input("Título del documento", value="Trabajo Académico", key="doc_titulo")
        subtitulo = st.text_input(
            "Subtítulo o tipología",
            value="Máster de Formación del Profesorado",
            key="doc_subtitulo",
        )
    with c2:
        autor = st.text_input("Nombre del autor/a", placeholder="Ej.: Nombre Apellido", key="doc_autor")
        institucion = st.text_input(
            "Universidad o Centro Educativo",
            placeholder="Ej.: Universidad — Facultad de Educación",
            key="doc_institucion",
        )

    if contenido_doc.strip():
        palabras = len(contenido_doc.split())
        st.caption(f"📊 Extensión actual: **{palabras} palabras** | Formatos listos para generar:")

        st.divider()
        st.subheader("💾 Generar y descargar documento")

        col_d1, col_d2, col_d3 = st.columns(3)

        # 1. DOCX
        try:
            docx_bytes = create_docx(
                content=contenido_doc,
                title=titulo,
                subtitle=subtitulo,
                author=autor.strip() if autor.strip() else None,
                institution=institucion.strip() if institucion.strip() else None,
            )
            col_d1.download_button(
                "📥 Descargar Word (.docx)",
                data=docx_bytes,
                file_name=f"{titulo[:30].strip().replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="btn_descarga_docx_docmod",
            )
        except Exception as e:
            col_d1.error(f"Error DOCX: {e}")

        # 2. PDF
        try:
            pdf_bytes = create_pdf(
                content=contenido_doc,
                title=titulo,
                subtitle=subtitulo,
                author=autor.strip() if autor.strip() else None,
                institution=institucion.strip() if institucion.strip() else None,
            )
            col_d2.download_button(
                "📥 Descargar PDF (.pdf)",
                data=pdf_bytes,
                file_name=f"{titulo[:30].strip().replace(' ', '_')}.pdf",
                mime="application/pdf",
                key="btn_descarga_pdf_docmod",
            )
        except Exception as e:
            col_d2.error(f"Error PDF: {e}")

        # 3. Markdown
        col_d3.download_button(
            "📥 Descargar Markdown (.md)",
            data=contenido_doc,
            file_name=f"{titulo[:30].strip().replace(' ', '_')}.md",
            mime="text/markdown",
            key="btn_descarga_md_docmod",
        )

        with st.expander("👁️ Vista previa del contenido a exportar"):
            st.markdown(f"**{titulo}**")
            if subtitulo:
                st.caption(subtitulo)
            if autor or institucion:
                st.caption(f"{autor} | {institucion}")
            st.markdown(contenido_doc)
    else:
        st.info("Pega texto o sube un documento para habilitar las opciones de descarga en Word y PDF.")
