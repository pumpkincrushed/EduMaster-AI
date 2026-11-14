# 🎓 EduMaster AI

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Google%20Gen%20AI-v1beta-4285F4.svg)](https://ai.google.dev/)
[![Crossref API](https://img.shields.io/badge/Crossref-DOI%20Live%20API-orange.svg)](https://www.crossref.org/)
[![Tests](https://img.shields.io/badge/Tests-56%20Passing-brightgreen.svg)](tests/)
[![License](https://img.shields.io/badge/License-MIT%20Academic-green.svg)](LICENSE)

**EduMaster AI** es una plataforma integral de asistencia académica y pedagógica basada en Inteligencia Artificial, diseñada específicamente para estudiantes del **Máster de Formación del Profesorado**, docentes de Educación Secundaria, Bachillerato y Formación Profesional, y el ámbito universitario general.

La aplicación combina el potencial generativo y analítico de los modelos **Google Gemini** con bases de datos científicas reales (**Crossref API**) y motores de maquetación documental (**Word `.docx` y PDF `.pdf`**), bajo un principio irrenunciable: **el rigor, la autoría intelectual honesta y la prevención activa del plagio**.

---

## 🧭 Principios de Integridad Académica y Ética Pedagógica

EduMaster AI no es una herramienta para eludir el trabajo reflexivo ni para engañar detectores de texto. Su filosofía se asienta sobre cuatro pilares:

1. **Autoría en manos del usuario:** La IA orienta, estructura, diagnostica y sugiere mejoras; el estudiante o docente toma todas las decisiones conceptuales y conserva la autoría exclusiva de su obra.
2. **Tolerancia cero a las citas inventadas (*Anti-Hallucination*):** Cuando el modelo identifica que una afirmación teórica o dato requiere respaldo, inserta explícitamente etiquetas `[Cita requerida]`. Nunca genera referencias falsas ni enlaces ficticios.
3. **Verificación contra fuentes reales:** Integra conexión en vivo con la base oficial de **Crossref** para validar DOIs existentes y extraer metadatos contrastados.
4. **Rechazo a la certificación arbitraria de autoría:** La lingüística computacional demuestra que los detectores opacos de texto artificial ofrecen falsos positivos y falsos negativos. EduMaster AI diagnostica calidad lingüística y similitud léxica real sin emitir juicios probabilísticos sesgados sobre la condición humana o artificial del autor.

---

## 🏛️ Organización Funcional de la Aplicación

La aplicación se estructura en **3 grandes áreas de trabajo** y **9 herramientas operativas**:

```
                              🎓 EDUMASTER AI
                                     │
     ┌───────────────────────────────┼───────────────────────────────┐
     ▼                               ▼                               ▼
✍️ CREACIÓN ORIGINAL          🔍 REVISIÓN Y RIGOR             📦 ENTREGA Y APOYO
  ├─ Trabajos académicos         ├─ Analizar borrador            ├─ Exportar documentos
  ├─ Material docente            ├─ Revisar redacción            ├─ Normativa educativa
  └─ Evaluación formativa        └─ Investigar y APA 7           └─ Asistente orientador
```

### 1. ✍️ Creación de contenido original
* **📝 Trabajos académicos (`modules/trabajos/`):**
  * Asistente estructurado para **Ensayos académicos**, **Propuestas de TFM** (proyectos de innovación o investigaciones educativas) y **Actividades formativas**.
  * Permite trabajar a partir de consignas del profesor o esquemas propios, con carga de plantillas curriculares estándar (`templates/trabajos/`).
  * Inyección obligatoria de marcas `[Cita requerida]` para evitar citas alucinadas.
* **📚 Material docente (`modules/materiales/`):**
  * Diseñador de **Situaciones de Aprendizaje (LOMLOE)** alineadas con competencias clave, competencias específicas, saberes básicos y criterios de evaluación.
  * Generador de **Guías de Trabajo y Fichas para el Alumnado** y adaptaciones inclusivas con **Diseño Universal para el Aprendizaje (DUA)**.
  * Planificación pormenorizada por sesiones y metodologías activas (ABP, cooperativo, flipped classroom).
* **📊 Evaluación educativa (`modules/evaluacion/`):**
  * Generador de **Rúbricas analíticas en tabla** con 4 niveles de logro (*Insuficiente, Suficiente, Notable, Sobresaliente*) y descriptores cualitativos claros.
  * Elaboración de **Listas de cotejo (*checklists*)** para autoevaluación y coevaluación del alumnado, con enfoque formativo y DUA.

### 2. 🔍 Revisión y prevención del plagio
* **🔍 Analizar borrador (`modules/revision/analisis.py`):**
  * Diagnóstico descriptivo y objetivo **sin alterar el texto original**.
  * Conteo y cálculo de **métricas estadísticas cuantitativas:** palabras, frases, párrafos, longitud media por frase y diversidad léxica (*Type-Token Ratio*).
  * Informe cualitativo: claridad, registro formal, cohesión, repeticiones y **detección preventiva de citas ausentes**.
* **✍️ Revisar redacción (`modules/revision/redaccion.py`):**
  * Tutor de estilo con enfoques configurables: *Claridad y precisión*, *Cohesión y conectores*, *Registro académico formal* o *Revisión integral*.
  * **Comparativa lado a lado:** Muestra el borrador original y la propuesta revisada en un editor editable en vivo.
  * Preservación escrupulosa de todas las citas y datos originales del autor.
* **🔬 Investigación y fuentes (`modules/investigacion/`):**
  * **Gestor APA 7:** Generación precisa de referencias bibliográficas completas, citas parentéticas `(Autor, Año)` y narrativas `Autor (Año)` según la 7.ª edición.
  * **Verificador de DOIs y Fuentes Reales:** Conexión en vivo con servidores de **Crossref** para contrastar si un artículo o DOI existe verdaderamente.
  * **Detector de Citas Ausentes:** Auditoría orientada a identificar afirmaciones estadísticas o teóricas huérfanas de fuente.
  * **Analizador de Similitud Documental:** Algoritmo determinista de n-gramas continuos y coeficiente de Jaccard para comparar borradores contra textos o fuentes de referencia.

### 3. 📦 Entrega y acompañamiento
* **📄 Exportación y maquetación (`modules/documentos/`):**
  * Centro unificado de descarga a **Word (`.docx`)** y **PDF (`.pdf`)** mediante `python-docx` y `reportlab`.
  * Portada académica configurada con título, subtítulo, autor e institución (universidad o centro escolar).
* **⚖️ Normativa educativa (`modules/normativa/`):**
  * Consultor del marco estatal (**LOMLOE - Ley Orgánica 3/2020**, RD 217/2022 de ESO, RD 243/2022 de Bachillerato, RD 659/2023 de FP) y autonómico (**Galicia y demás CCAA**).
  * Generador de apartados formales de **Fundamentación Jurídica y Curricular** listos para insertar en programaciones docentes o memorias de TFM.
* **🤖 Asistente orientador pedagógico (`modules/asistente/`):**
  * Chatbot conversacional que responde dudas del máster y orienta al usuario hacia la herramienta adecuada del menú.

---

## 🗂️ Estructura del Proyecto

```text
EduMaster-AI/
├── app.py                         # Punto de entrada principal y menú lateral jerárquico
├── requirements.txt               # Dependencias de producción
├── task.md                        # Registro de tareas y fases de desarrollo
├── README.md                      # Documentación completa del proyecto
│
├── config/
│   ├── settings.py                # Configuración global, modelos y metadatos de módulos
│   ├── models.py                  # Dataclasses compartidos (AIResponse, BibliographyEntry)
│   └── prompts.py                 # Prompts de sistema base y plantillas comunes
│
├── core/                          # Servicios y motores centrales reutilizables
│   ├── ai_engine.py               # Conexión centralizada con Gemini API (google-genai v1beta)
│   ├── source_validator.py        # Validación de DOIs (Crossref), URLs y similitud n-gramas
│   ├── document_writer.py         # Generador de documentos Word (.docx) y PDF (.pdf)
│   ├── document_reader.py         # Extracción de texto desde DOCX, PDF y TXT
│   └── text_processor.py          # Utilidades lingüísticas y conteo de métricas
│
├── modules/                       # Módulos funcionales de la plataforma
│   ├── revision/                  # [Área 2] Diagnóstico y revisión de estilo
│   │   ├── analisis.py            # Diagnóstico de texto y métricas descriptivas
│   │   └── redaccion.py           # Tutor de estilo con editor comparativo
│   ├── trabajos/                  # [Área 1] Generador de trabajos originales y TFM
│   │   ├── generador.py           # Lógica y prompts con directivas anti-alucinación
│   │   └── interfaz.py            # Interfaz Streamlit de creación de trabajos
│   ├── materiales/                # [Área 1] Generador de recursos didácticos y SA
│   │   ├── generador.py           # Lógica curricular LOMLOE y adaptaciones DUA
│   │   └── interfaz.py            # Interfaz Streamlit de materiales
│   ├── evaluacion/                # [Área 1] Rúbricas analíticas e instrumentos
│   │   ├── generador.py           # Generador de matrices y tablas de evaluación
│   │   └── interfaz.py            # Interfaz Streamlit de evaluación
│   ├── investigacion/             # [Área 2] Gestión de citas y prevención de plagio
│   │   ├── citas_apa.py           # Formateador APA 7 (parentéticas y narrativas)
│   │   ├── verificador.py         # Consultor de Crossref en vivo y DOIs
│   │   ├── detector_citas.py      # Auditor de afirmaciones sin referencia
│   │   └── similitud.py           # Analizador de similitud documental
│   ├── documentos/                # [Área 3] Centro de exportación y maquetación
│   │   └── interfaz.py            # Interfaz de composición y descarga Word/PDF
│   ├── normativa/                 # [Área 3] Legislación y marco curricular
│   │   ├── consultor.py           # Asesor jurídico LOMLOE / Decretos autonómicos
│   │   └── interfaz.py            # Consultor y redactor de fundamentación legal
│   └── asistente/                 # [Área 3] Orientador interactivo y router
│       ├── tutor.py               # Lógica conversacional del tutor pedagógico
│       └── interfaz.py            # Chat interactivo con Streamlit
│
├── templates/                     # Esquemas y plantillas curriculares en JSON
│   ├── trabajos/                  # ensayo.json, tfm_innovacion.json, actividad.json
│   ├── unidades/                  # situacion_aprendizaje_lomloe.json, guia_alumnado.json, adaptacion_dua.json
│   └── rubricas/                  # rubrica_analitica.json
│
└── tests/                         # Suite completa de pruebas unitarias con pytest
    ├── test_ai.py                 # Tests del motor central de IA y llamadas mockeadas
    ├── test_documents.py          # Tests del lector de documentos y procesamiento de texto
    ├── test_documentos_modulo.py  # Tests del generador DOCX/PDF con metadatos
    ├── test_sources.py            # Tests de validación de formato DOI y dataclass APA 7
    ├── test_revision.py           # Tests del módulo unificado de revisión y métricas
    ├── test_trabajos.py           # Tests del generador de trabajos y carga de plantillas
    ├── test_materiales.py         # Tests de recursos didácticos y situaciones de aprendizaje
    ├── test_investigacion.py      # Tests de citas en el texto, similitud y validación web
    ├── test_evaluacion.py         # Tests de generación de rúbricas analíticas
    ├── test_normativa.py          # Tests del consultor legislativo y fundamentación jurídica
    └── test_asistente.py          # Tests del tutor interactivo
```

---

## 🛠️ Tecnologías y Librerías Utilizadas

| Componente | Paquete / Tecnología | Función en EduMaster AI |
|---|---|---|
| **Lenguaje** | Python 3.10+ | Lenguaje base del proyecto |
| **Frontend** | Streamlit (`>=1.40.0`) | Interfaz web reactiva y componentes interactivos |
| **Inteligencia Artificial** | `google-genai` | SDK oficial para conectar con Google Gemini |
| **Fuentes Científicas** | `requests` (Crossref REST API) | Consulta en vivo de DOIs y metadatos de artículos |
| **Exportación Word** | `python-docx` | Generación de archivos `.docx` con formato APA |
| **Exportación PDF** | `reportlab` | Maquetación y generación directa de archivos `.pdf` |
| **Lectura de Documentos** | `PyMuPDF` (`fitz`) | Extracción de texto de PDFs subidos por el usuario |
| **Variables de Entorno** | `python-dotenv` | Gestión segura de claves en desarrollo local |
| **Testing** | `pytest` | Ejecución automatizada de pruebas unitarias |

---

## 🚀 Instalación y Puesta en Marcha

### Requisitos previos
- Tener instalado **Python 3.10** o superior.
- Disponer de una clave de API de **Google Gemini** ([Google AI Studio](https://aistudio.google.com/apikey)).

### 1. Clonar el repositorio
```bash
git clone https://github.com/pumpkincrushed/EduMaster-AI.git
cd EduMaster-AI/EduMaster-AI-EduMaster-AI-rev01/EduMaster-AI
```

### 2. Crear y activar el entorno virtual
En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
En Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la clave de Gemini API
Crear un archivo llamado `.env` en la carpeta raíz del proyecto (`EduMaster-AI/`):
```env
GEMINI_API_KEY=tu_clave_api_aqui
GEMINI_MODEL=gemini-2.5-flash
```

> [!NOTE]
> En **Streamlit Cloud**, no es necesario crear el archivo `.env`. Puedes configurar la clave directamente desde el panel de control en **App Settings → Secrets**:
> ```toml
> GEMINI_API_KEY = "tu_clave_api_aqui"
> ```

### 5. Iniciar la aplicación web
```bash
streamlit run app.py
```
La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`.

---

## 🧪 Ejecución de Pruebas Unitarias

EduMaster AI cuenta con una batería completa de pruebas unitarias automatizadas que validan el comportamiento de todos los módulos, el motor de IA (con mocks), el cálculo determinista de similitud léxica, el formateador APA 7 y los generadores de documentos Word y PDF.

Para ejecutar los tests:

```bash
# Establecer PYTHONPATH al directorio de la aplicación
$env:PYTHONPATH="."
python -m pytest tests/
```

Salida esperada:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.2.0, pluggy-1.7.0
collected 56 items

tests/test_ai.py .....                                                   [  8%]
tests/test_asistente.py ..                                               [ 12%]
tests/test_documentos_modulo.py ...                                      [ 17%]
tests/test_documents.py ...............                                  [ 44%]
tests/test_evaluacion.py ...                                             [ 50%]
tests/test_investigacion.py ........                                     [ 64%]
tests/test_materiales.py ....                                            [ 71%]
tests/test_normativa.py ...                                              [ 76%]
tests/test_revision.py ..                                                [ 80%]
tests/test_sources.py ......                                             [ 91%]
tests/test_trabajos.py .....                                             [100%]

======================== 56 passed, 1 warning in 3.46s ========================
```

---

## 📖 Guía de Uso por Herramientas

| Herramienta | Cuándo usarla | Formatos de salida |
|:---|:---|:---|
| **📝 Trabajos** | Para estructurar y redactar borradores originales de TFM, ensayos o tareas docentes sin inventar fuentes. | `.docx`, `.pdf`, `.md` |
| **📚 Materiales** | Para diseñar unidades didácticas y Situaciones de Aprendizaje LOMLOE por competencias y con DUA. | `.docx`, `.pdf`, `.md` |
| **📊 Evaluación** | Para crear rúbricas analíticas en tabla, listas de cotejo o dianas de evaluación formativa. | `.docx`, `.pdf`, `.md` |
| **🔍 Analizar** | Para obtener un diagnóstico lingüístico de legibilidad, coherencia y detección de citas sin modificar el texto. | `.docx`, `.pdf`, `.md` |
| **✍️ Revisar** | Para pulir la redacción, variedad sintáctica y tono académico con una vista comparativa lado a lado. | `.docx`, `.pdf`, `.md` |
| **🔬 Investigar** | Para formatear referencias APA 7, auditar afirmaciones huérfanas de cita, comprobar DOIs en Crossref y medir similitud léxica. | Texto, `.json`, APA 7 |
| **📄 Documentos** | Para maquetar y exportar cualquier borrador o informe a Word y PDF con portada universitaria. | `.docx`, `.pdf`, `.md` |
| **⚖️ Normativa** | Para resolver dudas curriculares y generar la fundamentación legal para programaciones didácticas o TFM. | `.docx`, `.pdf`, `.md` |
| **🤖 Asistente** | Para consultar dudas pedagógicas o metodológicas y recibir orientación sobre la herramienta a utilizar. | Chat interactivo |

---

## 📄 Licencia

Este proyecto está distribuido bajo la licencia de uso académico y pedagógico **MIT License**. Consulta el archivo `LICENSE` para más detalles.
