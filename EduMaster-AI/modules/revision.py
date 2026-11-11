import streamlit as st
from core.ai_engine import generate, is_configured

SYSTEM = """Eres un revisor de redacción académica en español para estudiantes
de un máster de profesorado. El texto que recibes lo ha escrito el propio
estudiante y tú lo ayudas a mejorarlo.

Reglas:
- No cambies el significado, los datos ni las citas. No elimines citas.
- No inventes argumentos, referencias, datos ni experiencias.
- Si falta algo (una fuente, un dato), avísalo en lugar de rellenarlo.
- Explica cada sugerencia de forma breve para que el estudiante aprenda."""

PROMPT_COMENTARIOS = """Revisa este borrador y devuelve, en Markdown:

## Resumen
Dos o tres frases sobre los puntos fuertes y los principales problemas.

## Sugerencias
Lista numerada. Para cada una: fragmento original entre comillas,
problema (repetición, cohesión, registro, ambigüedad, gramática, etc.)
y cómo mejorarlo.

Borrador:
\"\"\"
{texto}
\"\"\""""

PROMPT_REESCRITURA = """Reescribe este borrador mejorando fluidez, cohesión,
variedad sintáctica y registro académico, sin cambiar su contenido, sus
datos ni sus citas. Devuelve únicamente el texto revisado.

Borrador:
\"\"\"
{texto}
\"\"\""""


def render():
    st.header("Revisión de redacción")
    st.caption("Pega un borrador escrito por ti. La IA te señala qué mejorar y por qué.")

    if not is_configured():
        st.error("Falta GEMINI_API_KEY en los Secrets de Streamlit.")
        return

    texto = st.text_area("Tu borrador", height=280)
    modo = st.radio(
        "Qué quieres obtener",
        ["Solo comentarios", "Comentarios y versión revisada"],
        horizontal=True,
    )

    if st.button("Revisar", type="primary"):
        if len(texto.strip()) < 50:
            st.warning("Pega un texto algo más largo.")
            return

        with st.spinner("Revisando..."):
            r1 = generate(PROMPT_COMENTARIOS.format(texto=texto),
                          system_instruction=SYSTEM)
            if not r1.success:
                st.error(f"{r1.content}\n\nDetalle: {r1.error}")
                return

            revisado = None
            if modo == "Comentarios y versión revisada":
                r2 = generate(PROMPT_REESCRITURA.format(texto=texto),
                              system_instruction=SYSTEM, temperature=0.5)
                if not r2.success:
                    st.error(f"{r2.content}\n\nDetalle: {r2.error}")
                    return
                revisado = r2.content

        st.markdown(r1.content)
        if revisado:
            st.subheader("Original y revisado")
            c1, c2 = st.columns(2)
            c1.text_area("Original", texto, height=300, disabled=True)
            c2.text_area("Revisado (editable)", revisado, height=300)
            st.info("Léelo con atención y quédate solo con lo que te convenza: "
                    "el texto final es tuyo.")
