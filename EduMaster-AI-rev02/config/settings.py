"""
EduMaster AI — Configuración global de la aplicación
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (desarrollo local)
load_dotenv()

# ─── Rutas base ─────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
DATABASE_DIR = BASE_DIR / "database"

# ─── Nombre y versión ────────────────────────────────────────────────────────
APP_NAME = "EduMaster AI"
APP_VERSION = "1.0.0"
APP_SUBTITLE = "Plataforma académica y pedagógica con Inteligencia Artificial"
APP_ICON = "🎓"

# ─── API de Gemini ───────────────────────────────────────────────────────────
# En Streamlit Cloud, las secrets se leen desde st.secrets
# En local, se leen desde el archivo .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL_DEFAULT = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Modelos disponibles
GEMINI_MODELS = {
    "gemini-2.0-flash": "Gemini 2.0 Flash — Rápido y eficiente",
    "gemini-2.5-flash": "Gemini 2.5 Flash — Balance calidad/velocidad",
    "gemini-2.5-pro": "Gemini 2.5 Pro — Máxima capacidad",
}

# ─── Límites de la aplicación ────────────────────────────────────────────────
MAX_UPLOAD_SIZE_MB = int(os.getenv("APP_MAX_UPLOAD_MB", "10"))
MAX_INPUT_CHARS = 50_000       # Caracteres máximos de texto de entrada
MAX_OUTPUT_TOKENS = 8_192      # Tokens máximos de respuesta
DEFAULT_TEMPERATURE = 0.7      # Creatividad de Gemini (0.0 — 1.0)

# ─── Tipos de archivo permitidos ─────────────────────────────────────────────
ALLOWED_UPLOAD_TYPES = ["txt", "docx", "pdf"]

# ─── Configuración de debug ──────────────────────────────────────────────────
DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"

# ─── Módulos de la aplicación ────────────────────────────────────────────────
MODULES = [
    # 1. Creación de contenido original
    {
        "id": "trabajos",
        "category": "creacion",
        "icon": "📝",
        "name": "Trabajos académicos",
        "description": "Generador estructurado de ensayos, TFM y actividades a partir de esquemas propios",
        "status": "active",
    },
    {
        "id": "materiales",
        "category": "creacion",
        "icon": "📚",
        "name": "Material docente",
        "description": "Elabora unidades didácticas y recursos adaptados al nivel educativo",
        "status": "active",
    },
    {
        "id": "evaluacion",
        "category": "creacion",
        "icon": "📊",
        "name": "Evaluación",
        "description": "Diseña rúbricas e instrumentos de evaluación competencial",
        "status": "active",
    },
    # 2. Revisión y prevención del plagio
    {
        "id": "analizar",
        "category": "revision",
        "icon": "🔍",
        "name": "Analizar borrador",
        "description": "Diagnóstico de textos sin modificarlos ni juzgar autoría artificial",
        "status": "active",
    },
    {
        "id": "revisar",
        "category": "revision",
        "icon": "✍️",
        "name": "Revisar redacción",
        "description": "Mejora fluidez, cohesión y rigor académico respetando citas",
        "status": "active",
    },
    {
        "id": "investigacion",
        "category": "revision",
        "icon": "🔬",
        "name": "Investigación y APA 7",
        "description": "Verificación de DOIs reales en Crossref/OpenAlex y citas ausentes",
        "status": "active",
    },
    # 3. Entrega y acompañamiento
    {
        "id": "documentos",
        "category": "entrega",
        "icon": "📄",
        "name": "Documentos",
        "description": "Exportación a Word y PDF con maquetación académica profesional",
        "status": "active",
    },
    {
        "id": "normativa",
        "category": "entrega",
        "icon": "⚖️",
        "name": "Normativa",
        "description": "Consulta de legislación educativa (LOMLOE y decretos autonómicos)",
        "status": "active",
    },
    {
        "id": "asistente",
        "category": "entrega",
        "icon": "🤖",
        "name": "Asistente IA",
        "description": "Tutor inteligente y router para orientar hacia la herramienta adecuada",
        "status": "active",
    },
]
