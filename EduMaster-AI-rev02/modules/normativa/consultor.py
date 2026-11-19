"""
EduMaster AI — Consultor de Normativa y Legislación Educativa

Proporciona asesoramiento jurídico-curricular riguroso basado en el marco de la LOMLOE
(Ley Orgánica 3/2020), los Reales Decretos estatales y los Decretos autonómicos.
"""

from core.ai_engine import generate, AIResponse

SYSTEM_NORMATIVA = """Eres un jurista y asesor pedagógico especialista en Derecho Educativo y Legislación Curricular en España.
Tu función es orientar a docentes, opositores y estudiantes del Máster de Formación del Profesorado sobre el marco legal vigente.

Marco de referencia estatal:
- Ley Orgánica 3/2020 (LOMLOE), que modifica la LOE 2/2006.
- Real Decreto 217/2022 (Ordenación y enseñanzas mínimas de la Educación Secundaria Obligatoria).
- Real Decreto 243/2022 (Ordenación y enseñanzas mínimas del Bachillerato).
- Real Decreto 157/2022 (Ordenación y enseñanzas mínimas de la Educación Primaria).
- Real Decreto 659/2023 (Desarrollo de la ordenación del Sistema de Formación Profesional).
- Marco de Competencias Clave y Descriptores Operativos del Perfil de Salida.

Reglas indispensables:
1. Cita con precisión las normas jurídicas aplicables (ley, real decreto, decreto autonómico o decreto de evaluación).
2. Si se consulta por una Comunidad Autónoma específica (ej. Galicia, Madrid, Andalucía), señala la normativa autonómica que concreta el currículo.
3. No inventes artículos ni disposiciones falsas; cita de forma rigurosa y verificable."""


def consultar_normativa(
    duda: str,
    etapa: str,
    comunidad_autonoma: str = "Galicia",
) -> AIResponse:
    """Responde consultas sobre normativa y currículo educativo."""
    prompt = f"""Responde a la siguiente consulta sobre legislación educativa en España:

- **Etapa educativa:** {etapa}
- **Comunidad Autónoma:** {comunidad_autonoma}
- **Consulta concreta del usuario:**
\"\"\"
{duda}
\"\"\"

Estructura de respuesta:
1. **Resumen de la respuesta jurídica/pedagógica:** respuesta concisa y directa.
2. **Marco normativo estatal aplicable:** Leyes Orgánicas y Reales Decretos con artículos relevantes.
3. **Normativa autonómica de aplicación ({comunidad_autonoma}):** Decretos curriculares autonómicos y órdenes de evaluación.
4. **Implicaciones prácticas para la programación docente o el TFM.**"""

    return generate(prompt, system_instruction=SYSTEM_NORMATIVA, temperature=0.2)


def generar_fundamentacion_juridica(
    materia: str,
    curso_etapa: str,
    tema_proyecto: str,
    comunidad_autonoma: str = "Galicia",
) -> AIResponse:
    """Genera el apartado de fundamentación legal para una programación didáctica o TFM."""
    prompt = f"""Redacta el apartado formal de 'Fundamentación Jurídica y Curricular' para incluir en una Programación Didáctica o Memoria de TFM:

- **Materia o Área:** {materia}
- **Curso y Etapa:** {curso_etapa}
- **Tema o Propuesta didáctica:** {tema_proyecto}
- **Comunidad Autónoma:** {comunidad_autonoma}

Pautas de redacción:
- Redacta en tono formal y académico universitario en primera persona del plural o forma impersonal.
- Cita la jerarquía normativa completa: Constitución Española (art. 27), LOMLOE/LOE, Reales Decretos estatales de enseñanzas mínimas, Decretos curriculares autonómicos ({comunidad_autonoma}) y normativa de atención a la diversidad / evaluación.
- Justifica por qué la propuesta cumple estrictamente con el marco competencial vigente."""

    return generate(prompt, system_instruction=SYSTEM_NORMATIVA, temperature=0.25)
