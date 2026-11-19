"""
Tests para el módulo de Documentos y Generador DOCX/PDF — EduMaster AI
"""

from modules.documentos import render
from core.document_writer import create_docx, create_pdf


def test_documentos_render_callable():
    assert callable(render)


def test_create_docx_with_metadata():
    content = "# Introducción\nEste es un párrafo de prueba.\n\n## Metodología\nSegundo apartado."
    docx_bytes = create_docx(
        content=content,
        title="TFM Innovación",
        subtitle="Máster de Profesorado",
        author="María García",
        institution="Universidad Complutense",
    )
    assert isinstance(docx_bytes, bytes)
    assert len(docx_bytes) > 1000


def test_create_pdf_with_metadata():
    content = "# Introducción\nEste es un párrafo de prueba.\n\n## Metodología\nSegundo apartado."
    pdf_bytes = create_pdf(
        content=content,
        title="TFM Innovación",
        subtitle="Máster de Profesorado",
        author="María García",
        institution="Universidad Complutense",
    )
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF")
