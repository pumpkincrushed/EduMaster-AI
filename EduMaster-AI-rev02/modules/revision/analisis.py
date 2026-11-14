"""
EduMaster AI — Módulo de Diagnóstico y Análisis de Textos Académicos

Permite diagnosticar textos académicos sin modificarlos: evalúa métricas objetivas,
calidad de redacción, cohesión, argumentación y detecta afirmaciones que requieren citas.
"""

import re
import statistics
import streamlit as st

from core.ai_engine import generate, is_configured
from core.document_reader import read_uploaded_file
from core.document_writer import create_docx, create_pdf

SYSTEM_ANALISIS = """Eres un asesor experto en evaluación lingüística y académica en español para el ámbito universitario y del profesorado.
Tu objetivo es diagnosticar el texto de forma analítica, constructiva y descriptiva sin modificarlo.

Reglas estrictas:
- No afirmes ni intentes deducir si el texto ha sido escrito por una persona o por una IA: no es científicamente concluyente basándose únicamente en el estilo.
- No inventes fuentes, citas, datos ni autores.
- Si una afirmación, dato estadístico o teoría carece de respaldo bibliográfico, señálala expresamente con la etiqueta [Cita requerida].
- Sé preciso, constructivo y fundamenta cada señalamiento citando brevemente fragmentos del texto original."""

PROMPT_ANALISIS = """Realiza un diagnóstico riguroso del siguiente texto académico y genera un informe estructurado en formato Markdown:

## 1. Resumen ejecutivo del diagnóstico
Una síntesis de 3-4 líneas sobre las fortalezas principales y los aspectos críticos a mejorar.

## 2. Claridad, precisión y registro académico
- Identifica formulaciones ambiguas, coloquiales o excesivamente genéricas.
- Evalúa el tono y la adecuación terminológica.

## 3. Cohesión y coherencia estructural
- Conexión entre ideas y progresión temática entre párrafos.
- Uso de conectores lógicos discursivos.

## 4. Repeticiones y riqueza léxica
- Detección de muletillas, redundancias o pobreza de vocabulario con ejemplos textuales.

## 5. Estructura sintáctica y ritmo
- Variedad de construcciones sintácticas (oraciones compuestas, subordinación, equilibrio de extensión).

## 6. Detección de citas ausentes y rigor científico
- **Muy importante para prevención de plagio y rigor:** Enumera aquellas afirmaciones, datos o posturas teóricas que necesitan obligatoriamente una referencia o fuente contrastada [Cita requerida].

## 7. Plan de mejora recomendado
- 4 a 5 recomendaciones prácticas y priorizadas para que el propio autor perfeccione su borrador.

TEXTO A ANALIZAR:
\"\"\"
{texto}
\"\"\""""


def calcular_metricas(texto: str) -> dict:
    """Calcula métricas estadísticas objetivas del texto."""
    palabras = re.findall(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ'-]+\b", texto, flags=re.UNICODE)
    frases = [s.strip() for s in re.split(r"(?<=[.!?])\s+", texto.strip()) if s.strip()]
    parrafos = [p for p in re.split(r"\n\s*\n", texto.strip()) if p.strip()]
    longitudes = [len(re.findall(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ'-]+\b", f)) for f in frases]
    vocabulario = len({p.lower() for p in palabras})
    total_palabras = len(palabras)
    diversidad = round(vocabulario / total_palabras, 3) if total_palabras else 0

    return {
        "Palabras": total_palabras,
        "Frases": len(frases),
        "Párrafos": len(parrafos),
        "Media palabras/frase": round(statistics.mean(longitudes), 1) if longitudes else 0,
        "Palabras únicas": vocabulario,
        "Diversidad léxica (TTR)": diversidad,
    }


def render():
    st.header("🔍 Diagnóstico y Análisis de Texto")
    st.caption(
        "Diagnostica la calidad estructural, cohesión, argumentación y detección de citas ausentes "
        "sin modificar tu texto ni atribuir autoría artificial."
    )

    if not is_configured():
        st.error("Falta la clave GEMINI_API_KEY en la configuración (.env o st.secrets).")
        st.info("Configura la variable GEMINI_API_KEY para activar las capacidades analíticas de IA.")
        return

    # Método de entrada: Texto directo o subida de archivo
    modo_entrada = st.radio(
        "Modo de entrada",
        ["Escribir o pegar texto", "Subir archivo (.docx, .pdf, .txt)"],
        horizontal=True,
        key="analisis_modo_entrada",
    )

    texto_analizar = ""
    if modo_entrada == "Subir archivo (.docx, .pdf, .txt)":
        archivo = st.file_uploader(
            "Selecciona un documento para analizar",
            type=["docx", "pdf", "txt"],
            key="analisis_uploader",
        )
        if archivo is not None:
            try:
                with st.spinner("Extrayendo texto del archivo..."):
                    texto_analizar = read_uploaded_file(archivo) or ""
                st.success(f"Archivo cargado: **{archivo.name}** ({len(texto_analizar.split())} palabras)")
            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")
    else:
        texto_analizar = st.text_area(
            "Pega aquí el borrador a diagnosticar",
            height=280,
            key="analisis_texto_area",
            placeholder="Introduce tu texto académico (mínimo 50 caracteres)...",
        )

    if texto_analizar.strip():
        # Panel de métricas estadísticas objetivas
        metricas = calcular_metricas(texto_analizar)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Palabras", metricas["Palabras"])
        c2.metric("Frases", metricas["Frases"])
        c3.metric("Media Palabras/Frase", metricas["Media palabras/frase"])
        c4.metric("Diversidad Léxica", f"{metricas['Diversidad léxica (TTR)'] * 100:.1f}%")

        with st.expander("📊 Ver detalle completo de métricas lingüísticas"):
            st.json(metricas)

    if st.button("Diagnosticar borrador", type="primary", key="btn_ejecutar_diagnostico"):
        if len(texto_analizar.strip()) < 50:
            st.warning("El texto debe contener al menos 50 caracteres para un diagnóstico significativo.")
            return

        with st.spinner("Realizando diagnóstico lingüístico y académico..."):
            prompt = PROMPT_ANALISIS.format(texto=texto_analizar)
            respuesta = generate(prompt, system_instruction=SYSTEM_ANALISIS, temperature=0.2)

        if not respuesta.success:
            st.error(f"No se pudo completar el diagnóstico: {respuesta.error or respuesta.content}")
            return

        st.session_state["ultimo_diagnostico"] = respuesta.content
        st.session_state["ultimo_texto_analizado"] = texto_analizar

    if "ultimo_diagnostico" in st.session_state:
        st.subheader("📋 Informe de Diagnóstico")
        st.markdown(st.session_state["ultimo_diagnostico"])

        # Opciones de descarga
        st.divider()
        st.subheader("💾 Exportar informe")
        d_col1, d_col2, d_col3 = st.columns(3)

        d_col1.download_button(
            "Descargar en Markdown (.md)",
            data=st.session_state["ultimo_diagnostico"],
            file_name="diagnostico_academico_edumaster.md",
            mime="text/markdown",
            key="btn_descarga_md_diagnostico",
        )

        try:
            docx_data = create_docx(
                content=st.session_state["ultimo_diagnostico"],
                title="Informe de Diagnóstico Académico",
                subtitle="EduMaster AI — Diagnóstico Lingüístico y Estructural",
            )
            d_col2.download_button(
                "Descargar en Word (.docx)",
                data=docx_data,
                file_name="diagnostico_academico_edumaster.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="btn_descarga_docx_diagnostico",
            )
        except Exception as e:
            d_col2.info(f"Exportación DOCX no disponible: {e}")

        try:
            pdf_data = create_pdf(
                content=st.session_state["ultimo_diagnostico"],
                title="Informe de Diagnóstico Académico",
                subtitle="EduMaster AI — Diagnóstico Lingüístico y Estructural",
            )
            d_col3.download_button(
                "Descargar en PDF (.pdf)",
                data=pdf_data,
                file_name="diagnostico_academico_edumaster.pdf",
                mime="application/pdf",
                key="btn_descarga_pdf_diagnostico",
            )
        except Exception as e:
            d_col3.info(f"Exportación PDF no disponible: {e}")

    with st.expander("ℹ️ Transparencia y rigor ante detectores de IA"):
        st.markdown(
            """
            - **No certificación de autoría:** La lingüística computacional no permite determinar fehacientemente si un texto es de autoría humana o artificial únicamente por estilo o perplejidad.
            - **Prevención de plagio:** El diagnóstico señala dónde faltan referencias explícitas para evitar plagio involuntario y asegurar la trazabilidad científica.
            - **Supervisión humana:** El autor conserva en todo momento la responsabilidad intelectual sobre su manuscrito.
            """
        )
