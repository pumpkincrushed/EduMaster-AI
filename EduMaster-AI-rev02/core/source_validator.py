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


def search_crossref(query: str, rows: int = 5, timeout: int = 5) -> list:
    """
    Busca publicaciones académicas en Crossref por título o palabras clave.

    Returns:
        Lista de diccionarios con metadatos de las obras encontradas.
    """
    if not query or not query.strip():
        return []

    try:
        response = requests.get(
            CROSSREF_API,
            params={"query": query.strip(), "rows": rows},
            timeout=timeout,
            headers={"User-Agent": "EduMasterAI/1.0 (mailto:contact@edumaster.ai)"}
        )

        if response.status_code == 200:
            items = response.json().get("message", {}).get("items", [])
            results = []
            for item in items:
                authors = []
                for author in item.get("author", []):
                    family = author.get("family", "")
                    given = author.get("given", "")
                    if family:
                        authors.append(f"{family}, {given}" if given else family)

                year = None
                if "published" in item:
                    date_parts = item["published"].get("date-parts", [[]])
                    if date_parts and date_parts[0]:
                        year = date_parts[0][0]

                titles = item.get("title", [""])
                title = titles[0] if titles else "Sin título"
                containers = item.get("container-title", [""])
                journal = containers[0] if containers else ""
                doi = item.get("DOI", "")

                results.append({
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "journal": journal,
                    "doi": doi,
                })
            return results
        return []
    except Exception:
        return []


def verify_url(url: str, timeout: int = 5) -> dict:
    """
    Comprueba si un enlace o URL responde con un estado HTTP válido.
    """
    if not url or not url.strip().startswith(("http://", "https://")):
        return {"valid": False, "error": "URL inválida (debe empezar con http:// o https://)"}

    try:
        res = requests.head(
            url.strip(),
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (EduMaster AI Source Validator)"}
        )
        if res.status_code < 400:
            return {"valid": True, "status_code": res.status_code, "error": None}
        return {"valid": False, "status_code": res.status_code, "error": f"HTTP {res.status_code}"}
    except Exception as e:
        return {"valid": False, "status_code": None, "error": str(e)}


def calculate_text_similarity(draft: str, source: str, n_gram_size: int = 4) -> dict:
    """
    Compara un borrador con un texto fuente mediante cálculo de n-gramas
    y coeficiente de Jaccard, detectando frases idénticas o muy similares.
    """
    def tokenize(text: str) -> list:
        return re.findall(r"\b[\wáéíóúüñÁÉÍÓÚÜÑ]+\b", text.lower())

    tokens_draft = tokenize(draft)
    tokens_source = tokenize(source)

    if not tokens_draft or not tokens_source:
        return {
            "similarity_percentage": 0.0,
            "jaccard_similarity": 0.0,
            "matching_count": 0,
            "matching_samples": [],
            "total_draft_words": len(tokens_draft),
            "total_source_words": len(tokens_source),
        }

    # Jaccard por palabras únicas
    set_draft = set(tokens_draft)
    set_source = set(tokens_source)
    intersection = set_draft.intersection(set_source)
    union = set_draft.union(set_source)
    jaccard = round((len(intersection) / len(union)) * 100, 2) if union else 0.0

    # N-gramas para detectar coincidencia de frases
    def get_ngrams(tokens: list, n: int) -> set:
        return {" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}

    ngrams_draft = get_ngrams(tokens_draft, n_gram_size)
    ngrams_source = get_ngrams(tokens_source, n_gram_size)

    matching_ngrams = ngrams_draft.intersection(ngrams_source)
    similarity = round((len(matching_ngrams) / len(ngrams_draft)) * 100, 2) if ngrams_draft else 0.0

    sample_matches = list(matching_ngrams)[:10]

    return {
        "similarity_percentage": similarity,
        "jaccard_similarity": jaccard,
        "matching_count": len(matching_ngrams),
        "matching_samples": sample_matches,
        "total_draft_words": len(tokens_draft),
        "total_source_words": len(tokens_source),
    }

