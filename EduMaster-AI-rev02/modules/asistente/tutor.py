"""
EduMaster AI — Tutor Inteligente y Router Pedagógico

Guía al usuario en sus tareas del Máster de Formación del Profesorado y lo orienta
hacia la herramienta idónea dentro del ecosistema EduMaster AI.
"""

from typing import List, Dict, Optional
from core.ai_engine import generate, AIResponse

SYSTEM_ASISTENTE = """Eres el Asistente y Orientador Pedagógico de EduMaster AI para estudiantes del Máster de Formación del Profesorado y docentes universitarios.

Tus dos misiones principales son:
1. Responder con rigor pedagógico, claridad y calidez a cualquier duda sobre redacción académica, diseño de situaciones de aprendizaje, evaluación formativa, normas APA 7 o estructura de TFM.
2. **Canalizar al usuario hacia la herramienta específica de EduMaster AI que mejor resuelve su necesidad actual:**
   - **Creación de contenido original:**
     * `Trabajos`: para redactar ensayos, propuestas de TFM y actividades a partir de esquemas propios.
     * `Materiales`: para diseñar situaciones de aprendizaje LOMLOE y recursos didácticos por nivel.
     * `Evaluación`: para generar rúbricas analíticas en tabla y listas de cotejo con DUA.
   - **Revisión y prevención del plagio:**
     * `Analizar`: para diagnosticar calidad, cohesión y métricas de un borrador sin alterarlo.
     * `Revisar`: para reescribir con mayor fluidez y rigor preservando citas.
     * `Investigar`: para generar citas APA 7, verificar DOIs en Crossref y analizar similitud documental.
   - **Entrega y acompañamiento:**
     * `Documentos`: para exportar trabajos en Word (.docx) y PDF (.pdf) maquetados.
     * `Normativa`: para consultar artículos de la LOMLOE y decretos autonómicos.

En tus respuestas:
- Sé conciso, empático y constructivo.
- Indica siempre de forma destacada qué herramienta de la barra lateral debe usar el usuario para continuar su trabajo."""


def responder_asistente(
    mensaje: str,
    historial: Optional[List[Dict[str, str]]] = None,
) -> AIResponse:
    """Procesa el mensaje del usuario considerando el contexto de la conversación."""
    contexto = ""
    if historial:
        for turno in historial[-4:]:  # Últimos turnos para mantener foco
            rol = "Usuario" if turno.get("role") == "user" else "Asistente"
            contexto += f"{rol}: {turno.get('content', '')}\n"

    prompt = f"""Historial reciente de la consulta:
{contexto}

Nuevo mensaje del usuario:
\"{mensaje}\"

Responde de forma clara y añade una recomendación explícita sobre qué herramienta de EduMaster AI utilizar."""

    return generate(prompt, system_instruction=SYSTEM_ASISTENTE, temperature=0.35)
