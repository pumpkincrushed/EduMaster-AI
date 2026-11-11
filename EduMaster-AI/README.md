# EduMaster AI

**Plataforma académica y pedagógica con Inteligencia Artificial**

EduMaster AI es una aplicación web construida con Streamlit y la API de Google Gemini, pensada para apoyar la producción académica y la creación de materiales docentes en el ámbito educativo.

El proyecto está en desarrollo. Hoy funciona la revisión de redacción; el resto de módulos están planificados.

---

## Estado actual

| Módulo | Estado |
|--------|--------|
| ✍️ Revisión de redacción | ✅ Disponible |
| 📄 Generador de trabajos académicos | 🗂️ Carpeta creada, sin implementar |
| 📚 Materiales docentes | 🗂️ Carpeta creada, sin implementar |
| 🔍 Investigación y bibliografía | 🗂️ Carpeta creada, sin implementar |
| 📊 Evaluación y atención a la diversidad | 🗂️ Carpeta creada, sin implementar |
| 📁 Gestión de documentos | 🗂️ Carpeta creada, sin implementar |
| ⚖️ Normativa educativa de Galicia | 🗂️ Carpeta creada, sin implementar |
| 🤖 Asistente académico general | 🗂️ Carpeta creada, sin implementar |

### Revisión de redacción

El usuario pega un borrador escrito por él mismo y la aplicación:

- Señala repeticiones, problemas de cohesión, registro poco académico y errores.
- Explica cada sugerencia para que el autor aprenda de ella.
- Opcionalmente propone una versión revisada, que se muestra junto al original y se puede editar.

No cambia el significado, los datos ni las citas, y no inventa fuentes.

---

## Requisitos

- Python 3.10 o superior
- Clave de API de Google Gemini ([obtener aquí](https://aistudio.google.com/app/apikey))

## Instalación local

```bash
# 1. Clona el repositorio
git clone https://github.com/pumpkincrushed/EduMaster-AI.git
cd EduMaster-AI

# 2. Crea un entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Configura la clave de API
# Crea un archivo .env en la raíz con esta línea:
# GEMINI_API_KEY=tu_clave_aqui

# 5. Ejecuta la aplicación
streamlit run app.py
```

## Despliegue en Streamlit Community Cloud

1. Sube el repositorio a tu cuenta de GitHub.
2. Entra en [share.streamlit.io](https://share.streamlit.io) con GitHub.
3. Crea una nueva app con `app.py` como archivo principal.
4. En **Settings → Secrets**, añade:

```toml
GEMINI_API_KEY = "tu_clave_aqui"
```

La app se actualiza sola con cada commit en la rama principal.

---

## Estructura del proyecto

```
EduMaster-AI/
├── app.py                  # Punto de entrada Streamlit
├── requirements.txt
├── .gitignore
│
├── config/
│   ├── settings.py         # Configuración global
│   ├── models.py           # AIResponse (resultado del motor de IA)
│   └── prompts.py          # Prompts base y mensajes de error
│
├── core/
│   ├── ai_engine.py        # Motor central de Gemini
│   ├── document_reader.py  # Lectura DOCX/PDF/TXT
│   ├── document_writer.py  # Generación DOCX/PDF
│   ├── text_processor.py   # Utilidades de texto
│   └── source_validator.py # Validación de fuentes
│
├── modules/
│   ├── revision.py         # ✅ Revisión de redacción
│   └── (trabajos, materiales, investigacion, evaluacion,
│        documentos, normativa, asistente, humanizador)/
│                           # Carpetas reservadas, sin código todavía
│
├── database/               # Conexión SQLite e historial (sin conectar a la app)
├── templates/              # Plantillas (vacías)
└── tests/                  # Tests de IA, documentos y fuentes
```

Todos los módulos llaman a `core/ai_engine.py`; ninguno se conecta directamente con Gemini.

---

## Tecnologías

| Tecnología | Uso |
|------------|-----|
| Python 3.10+ | Lenguaje principal |
| Streamlit | Interfaz web |
| Google Gemini (`gemini-2.5-flash` por defecto) | IA generativa, mediante `google-genai` |
| python-dotenv | Variables de entorno en local |

Las dependencias de `core/document_reader.py` y `core/document_writer.py` (python-docx, ReportLab, PyMuPDF) no están en `requirements.txt` todavía; se añadirán al activar esos módulos.

---

## Privacidad y buenas prácticas

- **Claves:** la clave de Gemini va en los Secrets de Streamlit o en `.env`, que está en `.gitignore`. Nunca se sube al repositorio.
- **Datos:** los textos se procesan en memoria. No se deben introducir datos identificativos de menores ni información sensible del alumnado.
- **Revisión humana:** los resultados generados por IA deben revisarse antes de usarlos en contextos académicos reales.
- **Autoría:** la herramienta ayuda a mejorar textos propios. No está pensada para eludir detectores de IA ni para entregar como propio un texto generado.

---


Proyecto de desarrollo personal.
