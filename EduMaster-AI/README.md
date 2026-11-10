# EduMaster AI

**Plataforma académica y pedagógica con Inteligencia Artificial**

EduMaster AI es una aplicación web construida con Streamlit y la API de Google Gemini, diseñada para apoyar la producción académica, la creación de materiales docentes y la gestión documental en el ámbito educativo.

---

## Módulos disponibles

| # | Módulo | Estado |
|---|--------|--------|
| 01 | 🖊️ Humanizador y editor académico | ✅ Fase 1 |
| 02 | 📄 Generador de trabajos académicos | 🔄 Fase 3 |
| 03 | 📚 Generador de materiales docentes | 🔄 Fase 4 |
| 04 | 🔍 Investigación y bibliografía | 🔄 Fase 5 |
| 05 | 📊 Evaluación y atención a la diversidad | 🔄 Fase 6 |
| 06 | 📁 Gestión de documentos | 🔄 Fase 7 |
| 07 | ⚖️ Normativa educativa de Galicia | 🔄 Fase 6 |
| 08 | 🤖 Asistente académico general | 🔄 Fase 7 |

---

## Requisitos

- Python 3.10 o superior
- Clave de API de Google Gemini ([obtener aquí](https://aistudio.google.com/app/apikey))

---

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

# 4. Configura las variables de entorno
copy .env.example .env
# Edita .env y añade tu GEMINI_API_KEY

# 5. Ejecuta la aplicación
streamlit run app.py
```

---

## Despliegue en Streamlit Community Cloud

1. Haz fork o push de este repositorio a tu cuenta de GitHub.
2. Ve a [share.streamlit.io](https://share.streamlit.io) e inicia sesión con GitHub.
3. Crea una nueva app apuntando a `app.py`.
4. En **Settings → Secrets**, añade:

```toml
GEMINI_API_KEY = "tu_clave_aqui"
```

---

## Estructura del proyecto

```
EduMaster-AI/
├── app.py                  # Punto de entrada Streamlit
├── requirements.txt
├── .env.example
│
├── config/
│   ├── settings.py         # Configuración global
│   ├── models.py           # Tipos y dataclasses
│   └── prompts.py          # Prompts base del sistema
│
├── core/
│   ├── ai_engine.py        # Motor central de Gemini
│   ├── document_reader.py  # Lectura DOCX/PDF/TXT
│   ├── document_writer.py  # Generación DOCX/PDF
│   ├── text_processor.py   # Utilidades de texto
│   └── source_validator.py # Validación de fuentes
│
├── modules/
│   ├── humanizador/        # ✅ Módulo completo
│   ├── trabajos/           # 🔄 Esqueleto
│   ├── materiales/         # 🔄 Esqueleto
│   ├── investigacion/      # 🔄 Esqueleto
│   ├── evaluacion/         # 🔄 Esqueleto
│   ├── documentos/         # 🔄 Esqueleto
│   ├── normativa/          # 🔄 Esqueleto
│   └── asistente/          # 🔄 Esqueleto
│
├── database/               # Historial (fase posterior)
├── templates/              # Plantillas DOCX
└── tests/                  # Tests automatizados
```

---

## Restricciones y ética

- **Privacidad**: Los documentos se procesan en memoria y no se almacenan permanentemente.
- **API**: Las claves de Gemini nunca se suben al repositorio.
- **Referencias**: El módulo de investigación valida DOIs externos; no inventa fuentes.
- **IA**: Los resultados generados deben revisarse antes de usarse en contextos académicos reales.
- **Detectores**: El humanizador mejora la calidad académica del texto; no garantiza resultados frente a detectores de IA.

---

## Tecnologías

| Tecnología | Uso |
|------------|-----|
| Python 3.10+ | Motor principal |
| Streamlit | Interfaz web |
| Google Gemini 2.0 Flash | IA generativa |
| python-docx | Documentos Word |
| ReportLab | Documentos PDF |
| PyMuPDF | Lectura de PDFs |
| OpenAlex / Crossref | Fuentes científicas |
| GitHub Actions | CI/CD |

---

## Licencia

Proyecto de desarrollo personal. Consulta el archivo LICENSE para más detalles.
