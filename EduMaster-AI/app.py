import streamlit as st
from modules import revision
from modules.humanizador import interfaz as humanizador

st.set_page_config(page_title="EduMaster AI", page_icon="🎓", layout="wide")

st.sidebar.title("🎓 EduMaster AI")
seccion = st.sidebar.radio(
    "Herramientas",
    ["Laboratorio de escritura", "Revisión de redacción"],
)

if seccion == "Laboratorio de escritura":
    humanizador.render()
elif seccion == "Revisión de redacción":
    revision.render()

st.sidebar.divider()
st.sidebar.caption("EduMaster AI · Herramientas de apoyo académico")
