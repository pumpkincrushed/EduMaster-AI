"""Interfaz del laboratorio de escritura académica.

El módulo ayuda a analizar y mejorar textos. No intenta engañar detectores
ni presenta sus resultados como prueba de autoría humana o artificial.
"""

import re
import statistics
import streamlit as st

from core.ai_engine import generate, is_configured

SYSTEM_ANALISIS = """Eres un asistente de escritura académica en español para estudiantes
 del Máster de Formación del Profesorado. Analiza el texto de forma descriptiva.
 No intentes determinar si lo ha escrito una persona o una IA: no es posible
 establecerlo con fiabilidad solo por el estilo. No inventes fuentes, datos,
 citas ni experiencias. Señala las limitaciones y explica tus observaciones
 con ejemplos concretos del texto."""

SYSTEM_REVISION = """Eres un tutor de escritura académica en español. Ayudas al autor a
expresar mejor sus propias ideas. Conserva el significado, los datos, las citas
 y la voz del autor. No añadas experiencias personales ni referencias que no
 estén en el original. No optimices el texto para superar detectores de IA.
 Devuelve un texto claro, preciso, coherente y natural, y explica los cambios."""


def _metricas(texto: str) -> dict:
    palabras = re.findall(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ'-]+\b", texto, flags=re.UNICODE)
    frases = [s.strip() for s in re.split(r"(?<=[.!?])\s+", texto.strip()) if s.strip()]
    parrafos = [p for p in re.split(r"\n\s*\n", texto.strip()) if p.strip()]
    longitudes = [len(re.findall(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ'-]+\b", f)) for f in frases]
    vocabulario = len({p.lower() for p in palabras})
    return {
        "Palabras": len(palabras),
        "Frases": len(frases),
        "Párrafos": len(parrafos),
        "Media de palabras por frase": round(statistics.mean(longitudes), 1) if longitudes else 0,
        "Palabras distintas": vocabulario,
        "Diversidad léxica": round(vocabulario / len(palabras), 2) if palabras else 0,
    }


def _prompt_analisis(texto: str) -> str:
    return f"""Analiza el siguiente texto académico y entrega un informe en Markdown:

1. **Claridad y precisión:** identifica frases confusas o demasiado generales.
2. **Cohesión y coherencia:** analiza la conexión entre ideas y párrafos.
3. **Repeticiones y vocabulario:** señala repeticiones reales con ejemplos.
4. **Estructura sintáctica:** comenta variedad y legibilidad sin asumir autoría.
5. **Voz y argumentación:** indica dónde falta desarrollar una idea o justificar una afirmación.
6. **Citas y fuentes:** señala afirmaciones que podrían necesitar referencia; no inventes referencias.
7. **Propuestas concretas:** ofrece hasta cinco mejoras explicadas.

No asignes un porcentaje de probabilidad de IA ni afirmes que el texto es humano o artificial.

TEXTO:
---
{texto}
---"""


def render():
    st.header("✍️ Laboratorio de escritura académica")
    st.caption(
        "Analiza la calidad lingüística y mejora tus propios textos. "
        "Los detectores de IA pueden equivocarse: este módulo no certifica autoría ni garantiza resultados ante detectores."
    )

    if not is_configured():
        st.error("Falta GEMINI_API_KEY en los Secrets de Streamlit.")
        st.info('En Streamlit Cloud, configura GEMINI_API_KEY en Settings → Secrets.')
        return

    tab_analisis, tab_revision = st.tabs(["Análisis del texto", "Revisión académica"])

    with tab_analisis:
        texto = st.text_area(
            "Pega el texto que quieres analizar",
            height=260,
            key="lab_texto_analisis",
            placeholder="Introduce aquí un texto académico (mínimo 50 caracteres)...",
        )
        if texto.strip():
            datos = _metricas(texto)
            cols = st.columns(3)
            cols[0].metric("Palabras", datos["Palabras"])
            cols[1].metric("Frases", datos["Frases"])
            cols[2].metric("Párrafos", datos["Párrafos"])
            with st.expander("Ver otras métricas descriptivas"):
                st.json(datos)
        if st.button("Analizar calidad de escritura", type="primary", key="btn_analizar_lab"):
            if len(texto.strip()) < 50:
                st.warning("Introduce un texto de al menos 50 caracteres.")
            else:
                with st.spinner("Analizando claridad, cohesión y estilo..."):
                    resultado = generate(_prompt_analisis(texto), system_instruction=SYSTEM_ANALISIS, temperature=0.2)
                if resultado.success:
                    st.markdown(resultado.content)
                    st.caption(f"Modelo utilizado: {resultado.model}")
                else:
                    st.error(f"No se pudo completar el análisis: {resultado.error or resultado.content}")

    with tab_revision:
        original = st.text_area(
            "Tu borrador",
            height=260,
            key="lab_texto_revision",
            placeholder="Pega el borrador que has escrito y quieres mejorar...",
        )
        enfoque = st.selectbox(
            "Enfoque de la revisión",
            ["Claridad y precisión", "Cohesión y estructura", "Registro académico", "Revisión integral"],
        )
        instrucciones = st.text_input(
            "Instrucciones adicionales (opcional)",
            placeholder="Ej.: conserva la terminología de didáctica y no cambies las citas.",
        )
        if st.button("Revisar mi texto", type="primary", key="btn_revision_lab"):
            if len(original.strip()) < 50:
                st.warning("Introduce un texto de al menos 50 caracteres.")
            else:
                prompt = f"""Revisa el texto según este enfoque: {enfoque}.
Instrucciones adicionales del autor: {instrucciones or 'Ninguna'}.

Devuelve:
- **Versión revisada**: el texto completo, manteniendo ideas, datos y citas.
- **Cambios realizados**: lista breve de cambios y su justificación.
- **Aspectos que debe comprobar el autor**: datos, fuentes o afirmaciones que requieren revisión.

TEXTO ORIGINAL:
---
{original}
---"""
                with st.spinner("Revisando el texto..."):
                    resultado = generate(prompt, system_instruction=SYSTEM_REVISION, temperature=0.35)
                if resultado.success:
                    st.markdown(resultado.content)
                    st.download_button(
                        "Descargar revisión (.md)",
                        data=resultado.content,
                        file_name="revision_academica_edumaster.md",
                        mime="text/markdown",
                    )
                else:
                    st.error(f"No se pudo completar la revisión: {resultado.error or resultado.content}")

    with st.expander("Nota metodológica: detectores de IA"):
        st.write(
            "Los detectores de texto generado por IA ofrecen estimaciones y pueden producir falsos positivos "
            "o falsos negativos, especialmente con textos breves, textos editados o autores no nativos. "
            "No deben utilizarse como única prueba de mala conducta académica. Para una evaluación justa, "
            "conviene valorar borradores, fuentes, proceso de elaboración y defensa oral del trabajo."
        )
