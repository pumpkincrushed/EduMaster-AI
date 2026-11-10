"""
EduMaster AI — Utilidades de procesamiento de texto
"""

import re
from typing import Optional


def count_words(text: str) -> int:
    """Cuenta palabras en un texto."""
    if not text or not text.strip():
        return 0
    return len(text.split())


def count_sentences(text: str) -> int:
    """Cuenta frases en un texto."""
    if not text or not text.strip():
        return 0
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])


def count_paragraphs(text: str) -> int:
    """Cuenta párrafos en un texto."""
    if not text or not text.strip():
        return 0
    paragraphs = text.split('\n\n')
    return len([p for p in paragraphs if p.strip()])


def truncate_text(text: str, max_chars: int) -> str:
    """
    Trunca texto al límite de caracteres indicado,
    intentando cortar en un límite de frase.
    """
    if len(text) <= max_chars:
        return text

    truncated = text[:max_chars]
    # Intentar cortar en el último punto
    last_period = truncated.rfind('.')
    if last_period > max_chars * 0.8:
        return truncated[:last_period + 1] + "\n\n[Texto truncado por límite de longitud]"

    return truncated + "...\n\n[Texto truncado por límite de longitud]"


def clean_text(text: str) -> str:
    """
    Limpieza básica de texto:
    - Elimina caracteres de control extraños.
    - Normaliza saltos de línea.
    - Elimina espacios múltiples.
    """
    if not text:
        return ""

    # Normalizar saltos de línea
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Eliminar espacios múltiples en líneas
    lines = []
    for line in text.split('\n'):
        lines.append(' '.join(line.split()))
    text = '\n'.join(lines)

    # Eliminar más de dos saltos de línea consecutivos
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def get_text_stats(text: str) -> dict:
    """
    Calcula estadísticas básicas de un texto.

    Returns:
        dict con words, sentences, paragraphs, chars, avg_words_per_sentence.
    """
    words = count_words(text)
    sentences = count_sentences(text)
    paragraphs = count_paragraphs(text)

    avg_words_per_sentence = round(words / sentences, 1) if sentences > 0 else 0

    return {
        "words": words,
        "sentences": sentences,
        "paragraphs": paragraphs,
        "chars": len(text),
        "avg_words_per_sentence": avg_words_per_sentence,
    }


def sanitize_filename(name: str, max_length: int = 50) -> str:
    """
    Convierte una cadena en un nombre de archivo seguro.
    """
    # Eliminar caracteres no permitidos
    safe = re.sub(r'[<>:"/\\|?*]', '', name)
    safe = re.sub(r'\s+', '_', safe.strip())
    # Limitar longitud
    return safe[:max_length] if len(safe) > max_length else safe
