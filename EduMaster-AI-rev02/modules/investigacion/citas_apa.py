"""
EduMaster AI — Gestor de Referencias y Citas APA 7

Genera y valida citas parentéticas, narrativas y bibliografías completas
conforme a la 7.ª edición de las normas APA.
"""

import streamlit as st
from config.models import BibliographyEntry
from core.ai_engine import generate, is_configured

SYSTEM_APA = """Eres un bibliotecario y documentalista universitario especializado en normas APA 7.ª edición.
Tu función es extraer metadatos bibliográficos a partir de referencias informales, enlaces o textos,
y devolver los datos estructurados en formato JSON sin inventar campos que no figuren en la fuente."""


def render_gestor_apa():
    st.subheader("📑 Gestor de Referencias y Citas APA 7")
    st.caption("Genera citas en el texto (parentéticas y narrativas) y referencias bibliográficas según APA 7.")

    modo = st.radio(
        "Modo de creación de referencia",
        ["Formulario manual guiado", "Asistente inteligente (pegar texto o datos sueltos)"],
        horizontal=True,
        key="apa_modo",
    )

    if modo == "Formulario manual guiado":
        c1, c2 = st.columns(2)
        with c1:
            autores_input = st.text_input(
                "Autores (separados por coma, formato Apellido, Inicial)",
                placeholder="Ej.: García, J., Martínez, A.",
                key="apa_autores",
            )
            anio = st.number_input("Año de publicación", min_value=1800, max_value=2030, value=2023, key="apa_anio")
            titulo = st.text_input(
                "Título de la obra o artículo",
                placeholder="Ej.: Innovación pedagógica en la era digital",
                key="apa_titulo",
            )
        with c2:
            fuente = st.text_input(
                "Revista, Editorial o Sitio Web",
                placeholder="Ej.: Revista de Educación / Editorial Graó",
                key="apa_fuente",
            )
            doi = st.text_input(
                "DOI (opcional)",
                placeholder="Ej.: 10.4438/educacion.v1i1.001",
                key="apa_doi",
            )
            url = st.text_input("URL (opcional)", placeholder="https://...", key="apa_url")

        if st.button("Generar formato APA 7", type="primary", key="btn_generar_apa_manual"):
            if not autores_input.strip() or not titulo.strip():
                st.warning("Debes introducir al menos el autor y el título.")
            else:
                autores = [a.strip() for a in autores_input.split(",") if a.strip()]
                # Reagrupar si vinieron en pares Apellido, Inicial
                autores_limpios = []
                temp = ""
                for parte in autores_input.split(","):
                    p = parte.strip()
                    if not p:
                        continue
                    if not temp:
                        temp = p
                    else:
                        autores_limpios.append(f"{temp}, {p}")
                        temp = ""
                if temp:
                    autores_limpios.append(temp)

                entry = BibliographyEntry(
                    authors=autores_limpios if autores_limpios else [autores_input.strip()],
                    year=int(anio),
                    title=titulo.strip(),
                    source=fuente.strip() if fuente.strip() else "s.e.",
                    doi=doi.strip() if doi.strip() else None,
                    url=url.strip() if url.strip() else None,
                    verified=bool(doi.strip()),
                )

                st.session_state["ultima_entrada_apa"] = entry

    else:
        st.caption("Pega cualquier referencia incompleta, enlace o texto copiado de un artículo:")
        texto_crudo = st.text_area(
            "Texto con datos de la fuente",
            placeholder="Ej.: John Dewey 1938 Experience and Education Kappa Delta Pi...",
            height=120,
            key="apa_texto_crudo",
        )
        if st.button("Estructurar y formatear en APA 7 con IA", type="primary", key="btn_ia_apa"):
            if not is_configured():
                st.error("Falta GEMINI_API_KEY para usar el asistente.")
            elif not texto_crudo.strip():
                st.warning("Introduce algún dato de la publicación.")
            else:
                with st.spinner("Analizando metadatos y aplicando normas APA 7..."):
                    prompt = f"""Analiza estos datos bibliográficos y genera:
1. Referencia completa en formato APA 7.
2. Cita en el texto parentética (ej. (Autor, Año)).
3. Cita en el texto narrativa (ej. Autor (Año)).
4. Metadatos desglosados (Autores, Año, Título, Fuente, DOI/URL).

Datos:
\"\"\"
{texto_crudo}
\"\"\""""
                    res = generate(prompt, system_instruction=SYSTEM_APA, temperature=0.1)
                if res.success:
                    st.markdown(res.content)
                else:
                    st.error(f"Error al procesar: {res.error or res.content}")

    if "ultima_entrada_apa" in st.session_state:
        entry: BibliographyEntry = st.session_state["ultima_entrada_apa"]
        st.divider()
        st.subheader("📋 Resultados APA 7")
        st.markdown(f"**Referencia bibliográfica final:**\n> {entry.to_apa7()}")
        c_c1, c_c2 = st.columns(2)
        c_c1.info(f"**Cita parentética en el texto:**\n`{entry.to_in_text_parenthetical()}`")
        c_c2.info(f"**Cita narrativa en el texto:**\n`{entry.to_in_text_narrative()}`")
