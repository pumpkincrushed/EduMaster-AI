"""
EduMaster AI — Generador de Rúbricas e Instrumentos de Evaluación

Lógica para el diseño de rúbricas analíticas, listas de cotejo, escalas de valoración
y evaluación formativa competencial con principios DUA.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from config.settings import TEMPLATES_DIR
from core.ai_engine import generate, AIResponse

SYSTEM_EVALUACION = """Eres un asesor pedagógico especialista en evaluación formativa, continua y competencial en español.
Tu función es diseñar instrumentos de evaluación educativa de alta precisión pedagógica (rúbricas analíticas, listas de cotejo, dianas de evaluación).

Criterios indispensables:
1. Enfoque competencial: los criterios de evaluación deben centrarse en desempeños observables y capacidades del alumnado, no en mera memorización.
2. Descriptores cualitativos claros: cada nivel de logro debe describir con precisión qué sabe, comprende o es capaz de hacer el estudiante.
3. Gradación coherente: cuatro niveles de logro progresivos (Insuficiente, Suficiente, Notable, Sobresaliente).
4. Principios DUA: alternativas de evaluación inclusiva para no evaluar barreras de acceso sino competencias reales.
5. Formato: entrega matrices de rúbricas obligatoriamente en formato tabla Markdown para facilitar su lectura y exportación."""


def cargar_plantilla_rubrica() -> Optional[Dict[str, Any]]:
    """Carga la plantilla estándar de rúbrica."""
    archivo = TEMPLATES_DIR / "rubricas" / "rubrica_analitica.json"
    if not archivo.exists():
        return None
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def generar_instrumento_evaluacion(
    tipo_instrumento: str,
    tarea_evaluar: str,
    materia: str,
    nivel_etapa: str,
    criterios_especificos: str,
    ponderaciones: str,
    incluir_dua: bool = True,
) -> AIResponse:
    """Diseña la rúbrica o instrumento de evaluación formativa."""
    prompt = f"""Diseña un instrumento de evaluación competencial profesional con los siguientes parámetros:

- **Tipo de instrumento:** {tipo_instrumento}
- **Producto, tarea o desempeño a evaluar:** {tarea_evaluar}
- **Materia o Área:** {materia}
- **Etapa / Curso:** {nivel_etapa}
- **Ponderación o escala sugerida:** {ponderaciones or 'Equitativa entre dimensiones'}
- **Criterios o focos específicos indicados por el docente:**
\"\"\"
{criterios_especificos or 'Dimensiones estándar de calidad, rigor y comunicación'}
\"\"\"

Requisitos de diseño:
1. Si es Rúbrica Analítica, incluye una tabla Markdown completa con las columnas:
   | Criterio / Dimensión | Ponderación (%) | Insuficiente (1-4) | Suficiente/Bien (5-6) | Notable (7-8) | Sobresaliente (9-10) |
2. Si es Lista de Cotejo, incluye tabla con Criterio / Indicador observable, Sí/No/En proceso, y Espacio para retroalimentación formativa.
3. Si incluir_dua está activado ({incluir_dua}), añade un apartado final breve con medidas de evaluación inclusiva (flexibilidad en formatos de respuesta, tiempos o apoyos visuales).
4. Redacta descriptores claros, no ambiguos y en tono positivo y formativo."""

    return generate(prompt, system_instruction=SYSTEM_EVALUACION, temperature=0.3)
