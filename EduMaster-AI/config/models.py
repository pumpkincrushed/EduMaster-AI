"""
EduMaster AI — Tipos de datos compartidos entre módulos
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from enum import Enum


# ─── Enumeraciones ────────────────────────────────────────────────────────────

class RevisionLevel(str, Enum):
    """Nivel de intervención del humanizador."""
    SUAVE = "suave"
    ESTANDAR = "estandar"
    PROFUNDO = "profundo"


class AcademicRegister(str, Enum):
    """Registro lingüístico objetivo."""
    ACADEMICO = "academico"
    TECNICO = "tecnico"
    DIVULGATIVO = "divulgativo"


class DocumentFormat(str, Enum):
    """Formato de exportación."""
    DOCX = "docx"
    PDF = "pdf"
    TXT = "txt"


class ModuleStatus(str, Enum):
    """Estado de cada módulo de la plataforma."""
    ACTIVE = "active"
    COMING_SOON = "coming_soon"
    BETA = "beta"


# ─── Modelos de datos ─────────────────────────────────────────────────────────

@dataclass
class TextRevision:
    """Resultado de una revisión del humanizador."""
    original_text: str
    revised_text: str
    changes_summary: str
    word_count_original: int
    word_count_revised: int
    revision_level: RevisionLevel
    academic_register: AcademicRegister
    timestamp: datetime = field(default_factory=datetime.now)
    model_used: str = "gemini-2.0-flash"


@dataclass
class AcademicWork:
    """Trabajo académico generado."""
    title: str
    structure: list[str]
    content: dict[str, str]   # sección → contenido
    bibliography: list[str]
    word_count: int
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class BibliographyEntry:
    """Entrada bibliográfica en formato APA 7."""
    authors: list[str]
    year: int
    title: str
    source: str
    doi: Optional[str] = None
    url: Optional[str] = None
    verified: bool = False

    def to_apa7(self) -> str:
        """Formatea la entrada en APA 7."""
        authors_str = ", ".join(self.authors)
        doi_str = f" https://doi.org/{self.doi}" if self.doi else (f" {self.url}" if self.url else "")
        return f"{authors_str} ({self.year}). {self.title}. *{self.source}*.{doi_str}"


@dataclass
class DidacticUnit:
    """Unidad didáctica generada."""
    title: str
    subject: str
    grade_level: str
    objectives: list[str]
    contents: list[str]
    activities: list[dict]
    evaluation_criteria: list[str]
    competences: list[str]
    sessions: int
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class RubricCriterion:
    """Criterio individual de una rúbrica."""
    name: str
    weight: float           # Porcentaje del total
    levels: dict[str, str]  # nivel → descripción (Excelente, Bueno, etc.)


@dataclass
class Rubric:
    """Rúbrica de evaluación completa."""
    title: str
    task_description: str
    criteria: list[RubricCriterion]
    grade_levels: list[str]
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class AIResponse:
    """Respuesta genérica del motor de IA."""
    content: str
    model: str
    prompt_tokens: int = 0
    output_tokens: int = 0
    success: bool = True
    error: Optional[str] = None
