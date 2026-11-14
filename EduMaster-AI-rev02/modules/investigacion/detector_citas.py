"""
EduMaster AI — Detector de Citas Ausentes

Localiza afirmaciones fácticas, estadísticas, citas veladas y asertos teóricos
que carecen de referencia explícita, previniendo el plagio involuntario y el déficit de rigor.
"""

import streamlit as st
from core.ai_engine import generate, is_configured
from core.document_reader import read_uploaded_file

SYSTEM_DETECTOR_CITAS = """Eres un revisor de integridad académica y metodología de la investigación.
Tu misión es auditar un texto para identificar pasajes que requieren obligatoriamente una cita bibliográfica y que actualmente carecen de ella.

Categorías a detectar:
1. Afirmaciones empíricas o estadísticas específicas (porcentajes, cifras, resultados de estudios).
2. Conceptos teóricos acuñados por autores específicos sin atribución (ej. 'zona de desarrollo próximo', 'inteligencias múltiples').
3. Sentencias categóricas de causa-efecto en el ámbito educativo o científico.
4. Citas indirectas o paráfrasis donde no se indica la fuente original.

Reglas:
- No inventes citas falsas.
- Indica claramente qué tipo de fuente necesita el autor buscar para respaldar cada punto."""


def render_detector_citas():
    st.subheader("⚠️ Detector de Citas Ausentes")
    st.caption("Identifica pasajes que afirman datos o teorías sin respaldo bibliográfico para evitar el plagio involuntario.")

    if not is_configured():
        st.error("Falta GEMINI_API_KEY para utilizar el detector con IA.")
        return

    modo_in = st.radio(
        "Modo de entrada para auditar citas",
        ["Pegar texto", "Subir documento (.docx, .pdf, .txt)"],
        horizontal=True,
        key="det_citas_modo",
    )

    texto_borrador = ""
    if modo_in == "Subir documento (.docx, .pdf, .txt)":
        f = st.file_uploader("Documento a auditar", type=["docx", "pdf", "txt"], key="det_citas_uploader")
        if f:
            try:
                texto_borrador = read_uploaded_file(f) or ""
                st.success(f"Archivo cargado: **{f.name}**")
            except Exception as e:
                st.error(f"Error al leer: {e}")
    else:
        texto_borrador = st.text_area(
            "Pega el texto a auditar",
            height=240,
            placeholder="Pega aquí el capítulo, sección o ensayo a revisar...",
            key="det_citas_text_area",
        )

    if st.button("Auditar citas y afirmaciones", type="primary", key="btn_auditar_citas"):
        if len(texto_borrador.strip()) < 50:
            st.warning("Introduce un texto de al menos 50 caracteres.")
        else:
            with st.spinner("Analizando afirmaciones y necesidades de fundamentación..."):
                prompt = f"""Audita el siguiente texto académico e identifica exhaustivamente todas las afirmaciones que carecen de cita y que la necesitan.

Devuelve en Markdown:
## 1. Nivel de necesidad bibliográfica
Indica si el texto tiene un riesgo Alto, Medio o Bajo de afirmaciones no fundamentadas.

## 2. Afirmaciones detectadas que requieren cita
Lista numerada. Para cada una:
- **Fragmento original:** \"...\"
- **Motivo por el que requiere cita:** (Dato estadístico, teoría específica, afirmación categórica, etc.)
- **Tipo de fuente recomendada:** (Artículo científico, informe institucional, autor clásico, etc.)

## 3. Recomendaciones para el autor
Cómo integrar las citas respetando las normas APA 7 sin alterar el discurso propio.

TEXTO A AUDITAR:
\"\"\"
{texto_borrador}
\"\"\""""
                res = generate(prompt, system_instruction=SYSTEM_DETECTOR_CITAS, temperature=0.2)

            if res.success:
                st.markdown(res.content)
            else:
                st.error(f"Error en la auditoría: {res.error or res.content}")
