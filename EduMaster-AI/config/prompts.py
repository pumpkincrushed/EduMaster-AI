"""
EduMaster AI — Prompts base del sistema

Los prompts de cada módulo específico están en sus propios archivos prompts.py.
Aquí se definen las instrucciones de sistema compartidas.
"""

# ─── Instrucción de sistema base ─────────────────────────────────────────────

SYSTEM_BASE = """Eres EduMaster AI, un asistente académico y pedagógico de alto nivel.

PRINCIPIOS FUNDAMENTALES:
1. Precisión académica: Nunca inventas datos, referencias, autores ni resultados de investigaciones.
2. Transparencia: Cuando no estás seguro, lo indicas explícitamente.
3. Fidelidad al original: No alteras el significado del texto del usuario.
4. Registro apropiado: Adaptas tu lenguaje al nivel académico requerido.
5. Respeto a la normativa: Cuando citas normativa educativa, referencias fuentes oficiales verificables.

RESTRICCIONES ABSOLUTAS:
- No fabricar DOIs, ISBNs, autores ni publicaciones.
- No realizar diagnósticos clínicos ni psicológicos.
- No garantizar resultados frente a detectores de IA.
- No sustituir la revisión humana final de documentos académicos.

Responde siempre en español, con rigor académico y claridad pedagógica."""


# ─── Prompts de error y fallback ─────────────────────────────────────────────

PROMPT_NO_API_KEY = """
No se ha configurado la clave de la API de Gemini.

Para usar EduMaster AI necesitas:
1. Obtener una clave gratuita en https://aistudio.google.com/app/apikey
2. Crear un archivo `.env` en la raíz del proyecto con:
   GEMINI_API_KEY=tu_clave_aqui

O en Streamlit Cloud: Settings → Secrets → añadir GEMINI_API_KEY
"""

PROMPT_API_ERROR = """
Se ha producido un error al conectar con la API de Gemini.

Posibles causas:
- Clave de API inválida o expirada
- Límite de cuota alcanzado
- Error temporal del servicio

Por favor, verifica tu clave de API y vuelve a intentarlo.
"""
