"""
EduMaster AI — Validador de fuentes bibliográficas

Esqueleto para validación de DOIs y referencias. Implementación completa en Fase 5.
"""

import re
import requests
from typing import Optional


CROSSREF_API = "https://api.crossref.org/works"
OPENALEX_API = "https://api.openalex.org/works"


def is_valid_doi_format(doi: str) -> bool:
    """Verifica que el formato del DOI sea válido (no que exista)."""
    doi_pattern = r'^10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+$'
    cleaned = doi.replace("https://doi.org/", "").replace("http://dx.doi.org/", "").strip()
    return bool(re.match(doi_pattern, cleaned))


def verify_doi(doi: str, timeout: int = 5) -> dict:
    """
    Verifica que un DOI existe y devuelve metadatos básicos via Crossref.

    Returns:
        dict con 'valid', 'title', 'authors', 'year', 'journal', 'error'
    """
    if not is_valid_doi_format(doi):
        return {"valid": False, "error": "Formato de DOI inválido"}

    cleaned_doi = doi.replace("https://doi.org/", "").replace("http://dx.doi.org/", "").strip()

    try:
        response = requests.get(
            f"{CROSSREF_API}/{cleaned_doi}",
            timeout=timeout,
            headers={"User-Agent": "EduMasterAI/1.0 (mailto:contact@edumaster.ai)"}
        )

        if response.status_code == 200:
            data = response.json().get("message", {})
            authors = []
            for author in data.get("author", []):
                family = author.get("family", "")
                given = author.get("given", "")
                if family:
                    authors.append(f"{family}, {given}" if given else family)

            year = None
            if "published" in data:
                date_parts = data["published"].get("date-parts", [[]])
                if date_parts and date_parts[0]:
                    year = date_parts[0][0]

            return {
                "valid": True,
                "title": data.get("title", [""])[0],
                "authors": authors,
                "year": year,
                "journal": data.get("container-title", [""])[0],
                "doi": cleaned_doi,
                "error": None,
            }
        else:
            return {"valid": False, "error": f"DOI no encontrado (HTTP {response.status_code})"}

    except requests.Timeout:
        return {"valid": False, "error": "Timeout al verificar el DOI"}
    except Exception as e:
        return {"valid": False, "error": f"Error al verificar: {e}"}
