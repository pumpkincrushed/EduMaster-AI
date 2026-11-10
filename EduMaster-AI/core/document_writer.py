"""
EduMaster AI — Generador de documentos

Crea archivos DOCX y PDF descargables desde Streamlit.
"""

import io
from typing import Optional


# ─── DOCX ─────────────────────────────────────────────────────────────────────

def create_docx(
    content: str,
    title: str = "Documento",
    subtitle: Optional[str] = None,
) -> bytes:
    """
    Genera un archivo DOCX con el contenido proporcionado.

    Args:
        content: Texto del documento (soporta saltos de línea).
        title: Título del documento.
        subtitle: Subtítulo opcional.

    Returns:
        Bytes del archivo DOCX listo para descargar.
    """
    try:
        from docx import Document
        from docx.shared import Inches, Pt
        from docx.enum.text import WD_ALIGN_PARAGRAPH
    except ImportError:
        raise RuntimeError("python-docx no está instalado. Ejecuta: pip install python-docx")

    doc = Document()

    # Configurar márgenes
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.25)

    # Título
    title_para = doc.add_heading(title, level=0)
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Subtítulo
    if subtitle:
        sub_para = doc.add_paragraph(subtitle)
        sub_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sub_para.runs[0].font.size = Pt(12)
        sub_para.runs[0].bold = True

    doc.add_paragraph()  # Espacio

    # Contenido: procesar párrafos y posibles títulos
    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped:
            doc.add_paragraph()
            continue

        # Detectar títulos de sección (líneas que empiezan con #)
        if stripped.startswith("## "):
            doc.add_heading(stripped[3:], level=2)
        elif stripped.startswith("# "):
            doc.add_heading(stripped[2:], level=1)
        elif stripped.startswith("### "):
            doc.add_heading(stripped[4:], level=3)
        else:
            para = doc.add_paragraph(stripped)
            para.style.font.size = Pt(12)

    # Guardar en memoria
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


# ─── PDF ──────────────────────────────────────────────────────────────────────

def create_pdf(
    content: str,
    title: str = "Documento",
    subtitle: Optional[str] = None,
) -> bytes:
    """
    Genera un archivo PDF con el contenido proporcionado usando ReportLab.

    Args:
        content: Texto del documento.
        title: Título del documento.
        subtitle: Subtítulo opcional.

    Returns:
        Bytes del archivo PDF listo para descargar.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    except ImportError:
        raise RuntimeError("ReportLab no está instalado. Ejecuta: pip install reportlab")

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=3 * cm,
        leftMargin=3 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
    )

    styles = getSampleStyleSheet()
    story = []

    # Estilo título
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=18,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1a1a2e"),
    )

    # Estilo cuerpo
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=11,
        leading=18,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
    )

    # Estilo heading
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading1"],
        fontSize=13,
        spaceBefore=14,
        spaceAfter=6,
        textColor=colors.HexColor("#4f46e5"),
    )

    # Título
    story.append(Paragraph(title, title_style))

    if subtitle:
        story.append(Paragraph(subtitle, ParagraphStyle(
            "Subtitle", parent=body_style, alignment=TA_CENTER, fontSize=12
        )))

    story.append(Spacer(1, 0.5 * cm))

    # Contenido
    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 0.3 * cm))
            continue

        if stripped.startswith("## ") or stripped.startswith("# ") or stripped.startswith("### "):
            heading_text = stripped.lstrip("#").strip()
            story.append(Paragraph(heading_text, heading_style))
        else:
            story.append(Paragraph(stripped, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
