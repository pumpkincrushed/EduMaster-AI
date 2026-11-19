"""
Tests de validación de fuentes — EduMaster AI
"""

import pytest
from core.source_validator import is_valid_doi_format
from config.models import BibliographyEntry


class TestDOIValidation:
    """Tests para core/source_validator.py"""

    def test_valid_doi_format(self):
        valid_dois = [
            "10.1038/nature12373",
            "10.1016/j.learninstruc.2021.101434",
            "10.3389/feduc.2022.800360",
        ]
        for doi in valid_dois:
            assert is_valid_doi_format(doi), f"DOI válido rechazado: {doi}"

    def test_invalid_doi_format(self):
        invalid_dois = [
            "not-a-doi",
            "9.1234/something",   # Prefijo incorrecto
            "",
            "10/nodot",
        ]
        for doi in invalid_dois:
            assert not is_valid_doi_format(doi), f"DOI inválido aceptado: {doi}"

    def test_doi_with_url_prefix(self):
        """DOIs con prefijo https://doi.org/ también son válidos."""
        doi = "https://doi.org/10.1038/nature12373"
        assert is_valid_doi_format(doi)


class TestBibliographyEntry:
    """Tests para el dataclass BibliographyEntry y su formato APA 7."""

    def test_apa7_with_doi(self):
        entry = BibliographyEntry(
            authors=["García, J.", "Martínez, A."],
            year=2023,
            title="Innovación pedagógica en la era digital",
            source="Revista de Educación",
            doi="10.4438/educacion.v1i1.001",
        )
        apa = entry.to_apa7()
        assert "García, J." in apa
        assert "2023" in apa
        assert "Innovación pedagógica" in apa
        assert "10.4438" in apa

    def test_apa7_without_doi(self):
        entry = BibliographyEntry(
            authors=["Pérez, M."],
            year=2022,
            title="Metodologías activas",
            source="Cuadernos de Pedagogía",
        )
        apa = entry.to_apa7()
        assert "Pérez, M." in apa
        assert "2022" in apa
        assert "doi" not in apa.lower()

    def test_bibliography_verified_flag(self):
        entry = BibliographyEntry(
            authors=["Autor, A."],
            year=2024,
            title="Estudio experimental",
            source="Journal of Education",
            verified=True,
        )
        assert entry.verified is True
