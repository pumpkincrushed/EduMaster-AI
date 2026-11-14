"""
EduMaster AI — Generador de Trabajos Académicos Originales

Lógica de generación de borradores estructurados para ensayos, TFM y actividades.
Aplica principios estrictos de rigor académico y prevención de plagio / alucinaciones.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from config.settings import TEMPLATES_DIR
from core.ai_engine import generate, AIResponse

SYSTEM_TRABAJOS = """Eres un asistente de redacción académica y pedagógica universitaria en español.
Tu función es ayudar al estudiante o docente a generar un borrador estructurado, coherente, original y de alta calidad para sus trabajos académicos (ensayos, TFM, actividades pedagógicas) a partir de sus propias consignas y esquemas.

Reglas deontológicas y anti-plagio indispensables:
1. NO inventes autores, citas, títulos de libros/artículos ni enlaces falsos.
2. Cada vez que el texto requiera fundamentación teórica, evidencia empírica o referencia normativa, inserta explícitamente:
   '[Cita requerida: Autor, año o concepto clave]'
3. Desarrolla los argumentos con rigor conceptual, variedad sintáctica y registro formal universitario.
4. Ajusta la terminología al contexto educativo (currículo, competencias, metodologías activas, DUA, evaluación formativa).
5. Respeta escrupulosamente la estructura y apartados indicados en el esquema."""


def listar_plantillas_disponibles() -> Dict[str, Path]:
    """Devuelve las plantillas JSON disponibles en templates/trabajos/."""
    dir_plantillas = TEMPLATES_DIR / "trabajos"
    if not dir_plantillas.exists():
        return {}
    return {f.stem: f for f in dir_plantillas.glob("*.json")}


def cargar_plantilla(identificador: str) -> Optional[Dict[str, Any]]:
    """Carga los datos de una plantilla por su nombre o identificador."""
    dir_plantillas = TEMPLATES_DIR / "trabajos"
    archivo = dir_plantillas / f"{identificador}.json"
    if not archivo.exists():
        return None
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def sugerir_esquema(tipo: str, tema: str, consigna: str) -> AIResponse:
    """Genera una propuesta de esquema detallado para un trabajo académico."""
    prompt = f"""Propón un esquema detallado y numerado para un trabajo académico de tipo '{tipo}'.
Tema principal: {tema}
Consigna u objetivos del autor: {consigna or 'Estándar para el Máster de Profesorado'}

Devuelve únicamente la lista numerada de apartados y subapartados con una breve descripción de lo que debe contener cada uno."""
    return generate(prompt, system_instruction=SYSTEM_TRABAJOS, temperature=0.3)


def generar_contenido_trabajo(
    tipo: str,
    tema: str,
    nivel_etapa: str,
    esquema: str,
    consigna: str,
    extension_orientativa: str = "Media (1000 - 1500 palabras)",
) -> AIResponse:
    """Genera la redacción original del trabajo siguiendo el esquema y consignas."""
    prompt = f"""Redacta un borrador original y completo para el siguiente trabajo académico:

- **Tipo de trabajo:** {tipo}
- **Título o Tema:** {tema}
- **Etapa educativa / Contexto:** {nivel_etapa}
- **Extensión orientativa:** {extension_orientativa}
- **Consignas específicas del autor:**
\"\"\"
{consigna or 'Sin consignas adicionales'}
\"\"\"

- **Esquema obligatorio a desarrollar:**
\"\"\"
{esquema}
\"\"\"

Requisitos de redacción:
- Desarrolla cada apartado del esquema de manera sustantiva y profunda.
- No omitas secciones ni te limites a enumeraciones breves: redacta párrafos completos y argumentados.
- Recuerda: si hace falta una referencia bibliográfica, inserta '[Cita requerida: indicar concepto/autor]'; NO inventes citas bibliográficas falsas.
- Formatea la salida en Markdown con encabezados `#` y `##` según los apartados."""

    return generate(prompt, system_instruction=SYSTEM_TRABAJOS, temperature=0.45)
