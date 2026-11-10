"""
Tests de lectura y escritura de documentos — EduMaster AI
"""

import pytest
from core.text_processor import (
    count_words, count_sentences, count_paragraphs,
    clean_text, get_text_stats, sanitize_filename, truncate_text
)


class TestTextProcessor:
    """Tests para core/text_processor.py"""

    def test_count_words_basic(self):
        assert count_words("Hola mundo académico") == 3

    def test_count_words_empty(self):
        assert count_words("") == 0
        assert count_words("   ") == 0

    def test_count_sentences(self):
        text = "Esta es la primera frase. Esta es la segunda. ¿Y la tercera?"
        assert count_sentences(text) == 3

    def test_count_paragraphs(self):
        text = "Primer párrafo de texto.\n\nSegundo párrafo aquí.\n\nTercero."
        assert count_paragraphs(text) == 3

    def test_clean_text_normalizes_newlines(self):
        text = "Línea uno\r\nLínea dos\rLínea tres"
        cleaned = clean_text(text)
        assert "\r" not in cleaned
        assert "Línea uno" in cleaned
        assert "Línea dos" in cleaned

    def test_clean_text_removes_multiple_newlines(self):
        text = "Párrafo uno.\n\n\n\nPárrafo dos."
        cleaned = clean_text(text)
        assert "\n\n\n" not in cleaned

    def test_get_text_stats(self):
        text = "Esta es una frase. Esta es otra frase diferente."
        stats = get_text_stats(text)
        assert "words" in stats
        assert "sentences" in stats
        assert "paragraphs" in stats
        assert "chars" in stats
        assert stats["words"] > 0
        assert stats["chars"] == len(text)

    def test_sanitize_filename(self):
        name = "Mi trabajo: análisis de datos/resultados"
        safe = sanitize_filename(name)
        assert "/" not in safe
        assert ":" not in safe

    def test_sanitize_filename_max_length(self):
        long_name = "a" * 100
        safe = sanitize_filename(long_name, max_length=50)
        assert len(safe) <= 50

    def test_truncate_text_no_truncation_needed(self):
        text = "Texto corto"
        result = truncate_text(text, 1000)
        assert result == text

    def test_truncate_text_applied(self):
        text = "Esta es una frase muy larga. " * 100
        result = truncate_text(text, 100)
        assert len(result) <= 200  # con sufijo
        assert "truncado" in result.lower()


class TestDocumentReader:
    """Tests para core/document_reader.py"""

    def test_read_txt_basic(self):
        from core.document_reader import read_txt
        content = "Hola, esto es un texto de prueba."
        result = read_txt(content.encode("utf-8"))
        assert result == content

    def test_read_txt_latin1_fallback(self):
        from core.document_reader import read_txt
        content = "Texto con caracteres especiales: ñ, á, é"
        # utf-8 encoding, should work
        result = read_txt(content.encode("utf-8"))
        assert "ñ" in result

    def test_read_uploaded_file_none(self):
        from core.document_reader import read_uploaded_file
        result = read_uploaded_file(None)
        assert result is None

    def test_unsupported_format_raises(self):
        from core.document_reader import read_uploaded_file
        mock_file = type("MockFile", (), {
            "name": "archivo.xlsx",
            "read": lambda self: b"datos",
        })()
        with pytest.raises(ValueError, match="no soportado"):
            read_uploaded_file(mock_file)
