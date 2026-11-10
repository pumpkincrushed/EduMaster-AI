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
