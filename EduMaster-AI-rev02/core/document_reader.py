"""
EduMaster AI — Lector de documentos

Extrae texto de archivos DOCX, PDF y TXT subidos por el usuario.
"""

import io
from typing import Optional


def read_docx(file_bytes: bytes) -> str:
    """Extrae texto de un archivo DOCX."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)
    except ImportError:
        raise RuntimeError("python-docx no está instalado. Ejecuta: pip install python-docx")
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo DOCX: {e}")


def read_pdf(file_bytes: bytes) -> str:
    """Extrae texto de un archivo PDF usando PyMuPDF."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_parts = []
        for page in doc:
            text = page.get_text("text")
            if text.strip():
                text_parts.append(text)
        doc.close()
        return "\n\n".join(text_parts)
    except ImportError:
        raise RuntimeError("PyMuPDF no está instalado. Ejecuta: pip install pymupdf")
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo PDF: {e}")


def read_txt(file_bytes: bytes, encoding: str = "utf-8") -> str:
    """Lee el texto de un archivo TXT."""
    try:
        return file_bytes.decode(encoding)
    except UnicodeDecodeError:
        try:
            return file_bytes.decode("latin-1")
        except Exception as e:
            raise RuntimeError(f"Error al leer el archivo TXT: {e}")


def read_uploaded_file(uploaded_file) -> Optional[str]:
    """
    Lee el contenido de un archivo subido mediante st.file_uploader.

    Args:
        uploaded_file: Objeto UploadedFile de Streamlit.

    Returns:
        Texto extraído del archivo, o None si falla.

    Raises:
        ValueError: Si el tipo de archivo no está soportado.
        RuntimeError: Si hay un error al procesar el archivo.
    """
    if uploaded_file is None:
        return None

    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".docx"):
        return read_docx(file_bytes)
    elif file_name.endswith(".pdf"):
        return read_pdf(file_bytes)
    elif file_name.endswith(".txt"):
        return read_txt(file_bytes)
    else:
        extension = file_name.split(".")[-1] if "." in file_name else "desconocido"
        raise ValueError(
            f"Formato '{extension}' no soportado. "
            f"Formatos permitidos: TXT, DOCX, PDF."
        )
