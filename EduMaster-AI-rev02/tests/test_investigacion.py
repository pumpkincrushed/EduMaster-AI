"""
Tests para el módulo de Investigación, APA 7 y Verificación de Fuentes — EduMaster AI
"""

from modules.investigacion import render
from core.source_validator import (
    calculate_text_similarity,
    verify_url,
    search_crossref,
)
from config.models import BibliographyEntry


def test_investigacion_render_callable():
    assert callable(render)


def test_in_text_citations_one_author():
    entry = BibliographyEntry(
        authors=["Dewey, J."],
        year=1938,
        title="Experience and Education",
        source="Kappa Delta Pi",
    )
    assert entry.to_in_text_parenthetical() == "(Dewey, 1938)"
    assert entry.to_in_text_narrative() == "Dewey (1938)"


def test_in_text_citations_two_authors():
    entry = BibliographyEntry(
        authors=["Vygotsky, L.", "Luria, A."],
        year=1930,
        title="Estudios sobre la historia de la conducta",
        source="Editorial Pedagógica",
    )
    assert entry.to_in_text_parenthetical() == "(Vygotsky & Luria, 1930)"
    assert entry.to_in_text_narrative() == "Vygotsky y Luria (1930)"


def test_in_text_citations_three_plus_authors():
    entry = BibliographyEntry(
        authors=["García, A.", "Martínez, B.", "López, C."],
        year=2024,
        title="Innovación educativa",
        source="Revista Científica",
    )
    assert entry.to_in_text_parenthetical() == "(García et al., 2024)"
    assert entry.to_in_text_narrative() == "García et al. (2024)"


def test_calculate_text_similarity_identical():
    texto = "El aprendizaje basado en proyectos fomenta la motivación intrínseca del alumnado en educación secundaria."
    res = calculate_text_similarity(texto, texto, n_gram_size=4)
    assert res["similarity_percentage"] == 100.0
    assert res["jaccard_similarity"] == 100.0
    assert res["matching_count"] > 0


def test_calculate_text_similarity_different():
    texto_a = "La fotosíntesis es el proceso químico mediante el cual las plantas producen oxígeno."
    texto_b = "El feudalismo fue un sistema de organización política y social en la Edad Media europea."
    res = calculate_text_similarity(texto_a, texto_b, n_gram_size=4)
    assert res["similarity_percentage"] == 0.0
    assert res["matching_count"] == 0


def test_verify_url_invalid():
    res = verify_url("not-a-valid-url")
    assert res["valid"] is False
    assert "inválida" in res["error"].lower()


def test_search_crossref_empty():
    res = search_crossref("")
    assert res == []
