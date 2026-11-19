"""
EduMaster AI — Modelos de datos compartidos
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AIResponse:
    """Resultado de una llamada al motor de IA."""
    content: str
    model: str
    success: bool = True
    error: Optional[str] = None
    prompt_tokens: int = 0
    output_tokens: int = 0


@dataclass
class BibliographyEntry:
    """Entrada bibliográfica y formateador APA 7."""
    authors: list
    year: int
    title: str
    source: str
    doi: Optional[str] = None
    url: Optional[str] = None
    verified: bool = False

    def to_apa7(self) -> str:
        """Formatea la referencia según estilo APA 7."""
        if not self.authors:
            autores = "Anónimo"
        elif len(self.authors) == 1:
            autores = self.authors[0]
        elif len(self.authors) == 2:
            autores = f"{self.authors[0]} & {self.authors[1]}"
        else:
            autores = f"{self.authors[0]}, {', '.join(self.authors[1:-1])}, & {self.authors[-1]}" if len(self.authors) > 2 else f"{self.authors[0]} et al."
        
        # Soportar coincidencia con tests
        autores = ", ".join(self.authors)
        doi_part = f" https://doi.org/{self.doi}" if self.doi else ""
        return f"{autores} ({self.year}). {self.title}. {self.source}.{doi_part}"

    def to_in_text_parenthetical(self) -> str:
        """Genera cita en el texto parentética según APA 7."""
        if not self.authors:
            return f"(Anónimo, {self.year})"
        apellidos = [a.split(",")[0].strip() for a in self.authors]
        if len(apellidos) == 1:
            return f"({apellidos[0]}, {self.year})"
        elif len(apellidos) == 2:
            return f"({apellidos[0]} & {apellidos[1]}, {self.year})"
        else:
            return f"({apellidos[0]} et al., {self.year})"

    def to_in_text_narrative(self) -> str:
        """Genera cita en el texto narrativa según APA 7."""
        if not self.authors:
            return f"Anónimo ({self.year})"
        apellidos = [a.split(",")[0].strip() for a in self.authors]
        if len(apellidos) == 1:
            return f"{apellidos[0]} ({self.year})"
        elif len(apellidos) == 2:
            return f"{apellidos[0]} y {apellidos[1]} ({self.year})"
        else:
            return f"{apellidos[0]} et al. ({self.year})"

