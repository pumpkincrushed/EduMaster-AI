"""
EduMaster AI — Interfaz del Asistente Orientador Pedagógico

Proporciona un chat interactivo para orientar al usuario y canalizarlo a la herramienta idónea.
"""

import streamlit as st
from core.ai_engine import is_configured
from .tutor import responder_asistente


def render():
    st.header("🤖 Asistente Orientador Pedagógico")
    st.caption(
        "Tu tutor virtual para el Máster de Profesorado. Cuéntale qué necesitas hacer "
        "y te orientará pedagógicamente y te indicará la herramienta exacta de EduMaster AI a utilizar."
    )

    if not is_configured():
        st.error("Falta la clave GEMINI_API_KEY en la configuración (.env o st.secrets).")
        st.info("Configura la variable GEMINI_API_KEY para activar el asistente.")
        return

    # Inicializar historial de chat en session_state
    if "asistente_historial" not in st.session_state:
        st.session_state["asistente_historial"] = [
            {
                "role": "assistant",
                "content": (
                    "¡Hola! Soy tu asistente pedagógico en EduMaster AI. 🎓\n\n"
                    "Puedo orientarte con las dudas de tu TFM, diseño de situaciones de aprendizaje, "
                    "normas APA 7 o canalizarte directamente a la herramienta adecuada del menú lateral.\n\n"
                    "¿En qué estás trabajando hoy?"
                ),
            }
        ]

    # Botones de consulta rápida
    st.caption("Sugerencias rápidas de consulta:")
    c1, c2, c3 = st.columns(3)
    pregunta_rapida = None
    if c1.button("📑 ¿Cómo estructuro mi TFM?", key="btn_rapido_1"):
        pregunta_rapida = "¿Cómo estructuro la propuesta de mi Trabajo de Fin de Máster y qué herramienta me ayuda a redactarlo?"
    if c2.button("🔍 ¿Cómo verificar si mis citas son reales?", key="btn_rapido_2"):
        pregunta_rapida = "¿Cómo compruebo si una cita científica existe en bases oficiales para evitar el plagio?"
    if c3.button("📚 ¿Cómo diseñar una Situación de Aprendizaje?", key="btn_rapido_3"):
        pregunta_rapida = "¿Qué pasos debo seguir para diseñar una situación de aprendizaje LOMLOE con DUA?"

    # Mostrar mensajes del chat
    for msg in st.session_state["asistente_historial"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Entrada del usuario por chat_input o botón rápido
    prompt_usuario = st.chat_input("Escribe tu consulta o duda pedagógica aquí...") or pregunta_rapida

    if prompt_usuario:
        st.session_state["asistente_historial"].append({"role": "user", "content": prompt_usuario})
        with st.chat_message("user"):
            st.markdown(prompt_usuario)

        with st.chat_message("assistant"):
            with st.spinner("Analizando y consultando orientación pedagógica..."):
                respuesta = responder_asistente(
                    mensaje=prompt_usuario,
                    historial=st.session_state["asistente_historial"][:-1],
                )
            if respuesta.success:
                st.markdown(respuesta.content)
                st.session_state["asistente_historial"].append(
                    {"role": "assistant", "content": respuesta.content}
                )
            else:
                err_msg = f"No pude procesar la consulta: {respuesta.error or respuesta.content}"
                st.error(err_msg)

    # Botón para reiniciar chat
    st.divider()
    if st.button("🗑️ Reiniciar conversación", key="btn_reiniciar_chat"):
        st.session_state["asistente_historial"] = []
        st.rerun()
