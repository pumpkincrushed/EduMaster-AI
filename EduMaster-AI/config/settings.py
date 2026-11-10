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
GEMINI_MODEL_DEFAULT = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

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
    {
        "id": "humanizador",
        "icon": "✍️",
        "name": "Humanizador",
        "description": "Mejora la calidad académica y la naturalidad de tus textos",
        "status": "active",   # active | coming_soon
    },
    {
        "id": "trabajos",
        "icon": "📄",
        "name": "Trabajos académicos",
        "description": "Genera y estructura ensayos, TFM y actividades del máster",
        "status": "coming_soon",
    },
    {
        "id": "materiales",
        "icon": "📚",
        "name": "Material docente",
        "description": "Crea unidades didácticas, situaciones de aprendizaje y actividades",
        "status": "coming_soon",
    },
    {
        "id": "investigacion",
        "icon": "🔍",
        "name": "Investigación",
        "description": "Busca fuentes científicas y genera bibliografía APA 7",
        "status": "coming_soon",
    },
    {
        "id": "evaluacion",
        "icon": "📊",
        "name": "Evaluación",
        "description": "Diseña rúbricas, listas de cotejo y atención a la diversidad",
        "status": "coming_soon",
    },
    {
        "id": "documentos",
        "icon": "📁",
        "name": "Documentos",
        "description": "Exporta a Word y PDF con plantillas universitarias",
        "status": "coming_soon",
    },
    {
        "id": "normativa",
        "icon": "⚖️",
        "name": "Normativa Galicia",
        "description": "Consulta LOMLOE, currículo gallego y normativa educativa vigente",
        "status": "coming_soon",
    },
    {
        "id": "asistente",
        "icon": "🤖",
        "name": "Asistente IA",
        "description": "Resuelve dudas del máster y coordina las herramientas",
        "status": "coming_soon",
    },
]
