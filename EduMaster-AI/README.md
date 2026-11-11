# 🎓 EduMaster AI

**Asistente académico basado en inteligencia artificial para el Máster de Formación del Profesorado.**

EduMaster AI es una aplicación web desarrollada con Python y Streamlit que utiliza Google Gemini para ayudar en la redacción, revisión y mejora de textos académicos.

El proyecto busca facilitar el trabajo académico y educativo mediante herramientas de inteligencia artificial, manteniendo el criterio, la autoría y la responsabilidad del usuario sobre los contenidos generados.

## 🚀 Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python | Lenguaje principal |
| Streamlit | Interfaz web |
| Google Gemini | Motor de inteligencia artificial |
| Google Gen AI SDK | Conexión con Gemini |
| python-dotenv | Gestión de variables de entorno |

## 🧰 Funcionalidades implementadas

Actualmente, la aplicación dispone de dos herramientas principales.

### 1. Revisión de redacción

Permite analizar borradores académicos y obtener sugerencias de mejora mediante inteligencia artificial.

**Características:**
- Análisis de gramática y redacción.
- Identificación de repeticiones.
- Mejora de cohesión y coherencia.
- Detección de ambigüedades.
- Recomendaciones sobre registro académico.
- Generación de una versión revisada del texto.
- Comparación entre el documento original y el revisado.

Dispone de dos modalidades:
- Solo comentarios.
- Comentarios y versión revisada.

### 2. Laboratorio de escritura académica (AI Text Lab)

Nuevo módulo incorporado para analizar las características lingüísticas de textos académicos y mejorar su calidad de escritura.

Se organiza en dos apartados:

**A. Análisis del texto**

Permite estudiar diferentes características del documento:

- Número de palabras.
- Número de frases.
- Número de párrafos.
- Longitud media de las frases.
- Número de palabras diferentes.
- Diversidad léxica.
- Análisis de claridad y precisión.
- Análisis de cohesión y coherencia.
- Identificación de repeticiones y problemas de vocabulario.
- Evaluación de la estructura sintáctica.
- Revisión de la argumentación y las citas.

**B. Revisión académica**

Permite mejorar un texto a partir de diferentes enfoques:

- Claridad y precisión.
- Cohesión y estructura.
- Registro académico.
- Revisión integral.

También permite introducir instrucciones adicionales para personalizar la revisión.

La herramienta genera:
- Una versión revisada del texto.
- Una explicación de los cambios realizados.
- Aspectos que el autor debe comprobar.
- Descarga del resultado en formato Markdown (.md).

**Nota metodológica:** este módulo no determina si un texto ha sido escrito por una persona o por una IA. Los detectores de inteligencia artificial pueden producir falsos positivos y falsos negativos. El análisis lingüístico no constituye una prueba de autoría ni garantiza resultados ante detectores externos.

## 🧠 Arquitectura del proyecto

La aplicación utiliza una arquitectura modular que separa la interfaz, los módulos funcionales y los servicios centrales.

```text
EduMaster-AI/
│
├── app.py
│
├── config/
│   ├── settings.py
│   ├── prompts.py
│   └── models.py
│
├── core/
│   ├── ai_engine.py
│   ├── document_reader.py
│   ├── document_writer.py
│   ├── source_validator.py
│   └── text_processor.py
│
├── modules/
│   ├── revision.py
│   │
│   └── humanizador/
│       ├── __init__.py
│       └── interfaz.py
│
├── requirements.txt
└── README.md
```

### Motor central de inteligencia artificial

El archivo `core/ai_engine.py` centraliza las conexiones con Google Gemini.

Sus responsabilidades son:
- Obtener la clave API.
- Configurar el cliente de Gemini.
- Gestionar las peticiones.
- Controlar errores de conexión.
- Devolver las respuestas del modelo.
- Gestionar la generación de contenido.

Los módulos funcionales utilizan este motor común para comunicarse con Gemini.

## ⚙️ Instalación y configuración

### Requisitos

- Python 3.10 o superior.
- Una clave API de Google Gemini.
- Git (opcional, para clonar el repositorio).

### 1. Clonar el repositorio

```bash
git clone https://github.com/pumpkincrushed/EduMaster-AI.git
```

### 2. Entrar en la carpeta de la aplicación

```bash
cd EduMaster-AI/EduMaster-AI
```

### 3. Crear un entorno virtual

```bash
python -m venv venv
```

Activación en Windows:

```bash
venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar Gemini

Crear un archivo `.env` en la carpeta de la aplicación:

```env
GEMINI_API_KEY=tu_clave_api
```

La clave puede obtenerse desde Google AI Studio:

https://aistudio.google.com/apikey

No subir nunca el archivo `.env` ni la clave API al repositorio público.

### 6. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá normalmente en:

```text
http://localhost:8501
```

## ☁️ Despliegue en Streamlit Community Cloud

La aplicación puede alojarse gratuitamente en Streamlit Community Cloud, sujeto a sus condiciones de uso y disponibilidad.

Configuración del despliegue:

| Parámetro | Valor |
|---|---|
| Repositorio | pumpkincrushed/EduMaster-AI |
| Rama | EduMaster-AI-rev01 |
| Archivo principal | EduMaster-AI/app.py |

La clave `GEMINI_API_KEY` debe configurarse en los Secrets de Streamlit Cloud.

https://share.streamlit.io/

## 🔒 Privacidad y uso responsable

- No introducir información personal o sensible innecesaria.
- Revisar las respuestas generadas por Gemini.
- Comprobar la veracidad de los datos y las referencias.
- No utilizar las respuestas de IA como sustituto del criterio académico.
- Mantener la responsabilidad sobre los documentos entregados.
- Declarar el uso de inteligencia artificial cuando lo exijan las normas académicas correspondientes.

## 🛠️ Desarrollo futuro

El proyecto está preparado para incorporar nuevas herramientas.

Entre las funcionalidades previstas se encuentran:

- Generación de trabajos académicos.
- Creación de materiales didácticos.
- Análisis de similitud textual y prevención del plagio.
- Comprobación de citas y referencias bibliográficas.
- Comparación experimental de detectores de textos generados por IA.
- Exportación de informes académicos a Word y PDF.
- Ampliación de las herramientas de investigación educativa.

Estas funcionalidades no deben considerarse implementadas hasta que se incorporen al código.

## 📌 Estado del proyecto

**Versión:** 0.2 – Laboratorio de escritura académica.

**Estado:** En desarrollo.

**Repositorio:** https://github.com/pumpkincrushed/EduMaster-AI

**Aplicación web:** https://edumaster-ai-rsnewqkq96ak3j93veqnoh.streamlit.app/

---

*EduMaster AI es un proyecto académico y experimental orientado a la aplicación de la inteligencia artificial en el ámbito educativo.*
