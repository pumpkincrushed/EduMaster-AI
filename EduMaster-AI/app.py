import streamlit as st
from modules import revision

st.set_page_config(page_title="EduMaster AI", page_icon="🎓", layout="wide")

st.sidebar.title("🎓 EduMaster AI")
seccion = st.sidebar.radio("Herramientas", ["Revisión de redacción"])

if seccion == "Revisión de redacción":
    revision.render()
