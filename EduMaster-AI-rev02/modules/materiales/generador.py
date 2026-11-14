"""
EduMaster AI — Generador de Materiales y Recursos Didácticos

Lógica para la elaboración de situaciones de aprendizaje, unidades didácticas y recursos educativos
alineados con el marco curricular contemporáneo (LOMLOE, DUA y metodologías activas).
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from config.settings import TEMPLATES_DIR
from core.ai_engine import generate, AIResponse

SYSTEM_MATERIALES = """Eres un especialista en diseño curricular, pedagogía activa y didáctica específica en español.
Tu función es elaborar materiales, situaciones de aprendizaje y recursos educativos de alta calidad profesional para docentes y opositores del Máster de Formación del Profesorado.

Criterios pedagógicos indispensables:
1. Enfoque competencial alineado con el marco curricular vigente (LOMLOE): competencias clave, competencias específicas y criterios de evaluación.
2. Inclusión y Diseño Universal para el Aprendizaje (DUA): ofrece múltiples formas de representación, expresión e implicación para atender a la diversidad del aula.
3. Metodologías activas: promueve el aprendizaje significativo, retos contextualizados (ABP, aprendizaje basado en problemas, proyectos, pensamiento visible).
4. Rigor organizativo: estructura las secuencias didácticas detallando fases claras (motivación/activación, investigación/desarrollo, síntesis/aplicación, evaluación y difusión).
5. Claridad y aplicabilidad directa: proporciona consignas realistas, recursos concretos y tablas organizativas en Markdown cuando faciliten la lectura."""


def listar_plantillas_unidades() -> Dict[str, Path]:
    """Devuelve las plantillas disponibles en templates/unidades/."""
    dir_plantillas = TEMPLATES_DIR / "unidades"
    if not dir_plantillas.exists():
        return {}
    return {f.stem: f for f in dir_plantillas.glob("*.json")}


def cargar_plantilla_unidad(identificador: str) -> Optional[Dict[str, Any]]:
    """Carga los datos de una plantilla de unidades didácticas."""
    dir_plantillas = TEMPLATES_DIR / "unidades"
    archivo = dir_plantillas / f"{identificador}.json"
    if not archivo.exists():
        return None
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def generar_material_didactico(
    tipo_recurso: str,
    titulo: str,
    materia: str,
    nivel_etapa: str,
    duracion_sesiones: str,
    metodologia: str,
    objetivos_consigna: str,
    esquema: str,
) -> AIResponse:
    """Genera el recurso o material didáctico completo en Markdown."""
    prompt = f"""Diseña un recurso didáctico profesional con las siguientes especificaciones:

- **Tipo de recurso:** {tipo_recurso}
- **Título o Tema:** {titulo}
- **Materia o Área:** {materia}
- **Etapa / Curso:** {nivel_etapa}
- **Temporalización:** {duracion_sesiones}
- **Metodología pedagógica principal:** {metodologia}
- **Objetivos, retos o directrices particulares del docente:**
\"\"\"
{objetivos_consigna or 'Sin consignas adicionales'}
\"\"\"

- **Estructura obligatoria a desarrollar:**
\"\"\"
{esquema}
\"\"\"

Pautas de entrega:
- Desarrolla cada apartado de forma minuciosa, práctica y lista para implementar en el aula.
- En la secuencia de actividades, desglosa las sesiones indicando qué hace el docente, qué hace el alumnado y los agrupamientos.
- Si incluye instrumentos de evaluación, redacta indicadores claros y observables.
- Utiliza formato Markdown profesional con títulos, listas y tablas donde proceda."""

    return generate(prompt, system_instruction=SYSTEM_MATERIALES, temperature=0.4)
