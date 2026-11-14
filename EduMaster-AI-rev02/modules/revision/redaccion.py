"""
EduMaster AI — Módulo de Revisión y Rigor Académico

Ayuda al autor a perfeccionar la redacción, cohesión, tono y rigor académico de su texto,
preservando fielmente su significado, citas y autoría original sin inventar fuentes.
"""

import streamlit as st

from core.ai_engine import generate, is_configured
from core.document_reader import read_uploaded_file
from core.document_writer import create_docx, create_pdf

SYSTEM_REVISION = """Eres un tutor experto de redacción y rigor académico en español para el ámbito pedagógico y universitario.
El texto que recibes pertenece al propio estudiante o docente, y tu misión es ayudarle a elevar la calidad, fluidez y rigor de su manuscrito.

Reglas deontológicas y metodológicas indispensables:
- NO cambies el significado, los datos empíricos ni las posturas del autor.
- NO elimines citas existentes bajo ninguna circunstancia.
- NO inventes citas, fuentes, bibliografía, datos numéricos ni experiencias personales.
- Si detectas una afirmación que carece de respaldo, añade la advertencia '[Nota: Requiere cita bibliográfica]' sin inventarte una referencia falsa.
- Explica de forma concisa cada corrección pedagógicamente para fomentar el aprendizaje del usuario.
- Entrega una redacción natural, coherente y ajustada a las convenciones del registro académico en español."""

PROMPT_COMENTARIOS = """Revisa este borrador académico según el enfoque '{enfoque}'.
Instrucciones particulares del autor: {instrucciones}.

Devuelve en formato Markdown estructurado:

## 1. Valoración general
Puntos fuertes del texto y principales aspectos sintácticos, de cohesión o de registro a pulir (3-4 líneas).

## 2. Sugerencias detalladas de mejora
Lista numerada donde para cada propuesta indiques:
- **Fragmento original:** \"...\"
- **Dificultad detectada:** (ambigüedad, redundancia, registro informal, salto lógico, etc.)
- **Propuesta de mejora y justificación pedagógica:** cómo reescribirlo y por qué.

## 3. Verificación de rigor y citas
Señala si hay afirmaciones categóricas o datos que requieren soporte bibliográfico explícito antes de la entrega final.

BORRADOR:
\"\"\"
{texto}
\"\"\""""

PROMPT_REESCRITURA_COMPLETA = """Reescribe este borrador mejorando su fluidez, variedad sintáctica, precisión léxica y registro académico según el enfoque '{enfoque}'.
Instrucciones adicionales del autor: {instrucciones}.

Criterios obligatorios:
1. Mantén intactos el significado, las ideas de fondo y TODAS las citas existentes.
2. Si una afirmación no tiene referencia y lo requiere, añade '[Nota: Requiere cita bibliográfica]'.
3. No inventes referencias falsas.
4. Devuelve el texto revisado y pulido de forma íntegra.

BORRADOR:
\"\"\"
{texto}
\"\"\""""


def render():
    st.header("✍️ Revisión de Redacción y Rigor Académico")
    st.caption(
        "Eleva la claridad, cohesión y precisión académica de tus borradores. "
        "Mantiene siempre intactas tus ideas y citas originales."
    )

    if not is_configured():
        st.error("Falta la clave GEMINI_API_KEY en la configuración (.env o st.secrets).")
        st.info("Configura la variable GEMINI_API_KEY para activar las funciones de revisión asistida.")
        return

    # Método de entrada
    modo_entrada = st.radio(
        "Modo de entrada del borrador",
        ["Escribir o pegar texto", "Subir archivo (.docx, .pdf, .txt)"],
        horizontal=True,
        key="revision_modo_entrada",
    )

    texto_original = ""
    if modo_entrada == "Subir archivo (.docx, .pdf, .txt)":
        archivo = st.file_uploader(
            "Selecciona el borrador a revisar",
            type=["docx", "pdf", "txt"],
            key="revision_uploader",
        )
        if archivo is not None:
            try:
                with st.spinner("Leyendo documento..."):
                    texto_original = read_uploaded_file(archivo) or ""
                st.success(f"Borrador cargado: **{archivo.name}** ({len(texto_original.split())} palabras)")
            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")
    else:
        texto_original = st.text_area(
            "Tu borrador",
            height=260,
            key="revision_texto_area",
            placeholder="Pega aquí el borrador que deseas pulir...",
        )

    # Parámetros de revisión
    col_enf, col_modo = st.columns(2)
    with col_enf:
        enfoque = st.selectbox(
            "Enfoque prioritario",
            [
                "Revisión integral (estilo, sintaxis y rigor)",
                "Claridad y precisión conceptual",
                "Cohesión textual y conectores",
                "Registro académico formal (tono científico)",
            ],
            key="revision_enfoque",
        )
    with col_modo:
        modo_salida = st.radio(
            "Modalidad de trabajo",
            ["Comentarios y versión revisada", "Solo comentarios y sugerencias"],
            horizontal=True,
            key="revision_modo_salida",
        )

    instrucciones = st.text_input(
        "Instrucciones complementarias (opcional)",
        placeholder="Ej.: 'mantener terminología de ABP', 'revisar especialmente el párrafo 2'...",
        key="revision_instrucciones",
    )

    if st.button("Iniciar revisión", type="primary", key="btn_iniciar_revision"):
        if len(texto_original.strip()) < 50:
            st.warning("El texto debe contener al menos 50 caracteres para poder revisarlo con rigor.")
            return

        inst_texto = instrucciones.strip() if instrucciones.strip() else "Ninguna especificada"

        with st.spinner("Analizando y elaborando recomendaciones..."):
            # Generar comentarios
            p_comentarios = PROMPT_COMENTARIOS.format(
                enfoque=enfoque,
                instrucciones=inst_texto,
                texto=texto_original,
            )
            r_comentarios = generate(p_comentarios, system_instruction=SYSTEM_REVISION, temperature=0.3)

            if not r_comentarios.success:
                st.error(f"Error al generar comentarios: {r_comentarios.error or r_comentarios.content}")
                return

            texto_revisado = None
            if modo_salida == "Comentarios y versión revisada":
                with st.spinner("Generando versión revisada y refinada..."):
                    p_reescritura = PROMPT_REESCRITURA_COMPLETA.format(
                        enfoque=enfoque,
                        instrucciones=inst_texto,
                        texto=texto_original,
                    )
                    r_reescritura = generate(p_reescritura, system_instruction=SYSTEM_REVISION, temperature=0.35)
                    if not r_reescritura.success:
                        st.error(f"Error al generar texto revisado: {r_reescritura.error or r_reescritura.content}")
                        return
                    texto_revisado = r_reescritura.content

            st.session_state["revision_comentarios"] = r_comentarios.content
            st.session_state["revision_texto_revisado"] = texto_revisado
            st.session_state["revision_original"] = texto_original

    # Mostrar resultados
    if "revision_comentarios" in st.session_state:
        st.divider()
        st.subheader("💡 Sugerencias y comentarios de mejora")
        st.markdown(st.session_state["revision_comentarios"])

        if st.session_state.get("revision_texto_revisado"):
            st.divider()
            st.subheader("⚖️ Comparación lado a lado")
            st.caption(
                "Puedes editar el texto revisado en la columna derecha para adaptarlo a tu criterio final."
            )

            col_orig, col_rev = st.columns(2)
            with col_orig:
                st.markdown("**Borrador original:**")
                st.text_area(
                    "Original",
                    value=st.session_state["revision_original"],
                    height=360,
                    disabled=True,
                    key="area_orig_view",
                )
            with col_rev:
                st.markdown("**Versión revisada (editable):**")
                texto_final_editado = st.text_area(
                    "Revisado",
                    value=st.session_state["revision_texto_revisado"],
                    height=360,
                    key="area_rev_edit",
                )

            # Exportación de la versión revisada
            st.subheader("💾 Exportar texto revisado")
            e1, e2, e3 = st.columns(3)

            e1.download_button(
                "Descargar en Markdown (.md)",
                data=texto_final_editado,
                file_name="texto_revisado_edumaster.md",
                mime="text/markdown",
                key="btn_descarga_md_revision",
            )

            try:
                docx_rev = create_docx(
                    content=texto_final_editado,
                    title="Documento Académico Revisado",
                    subtitle="EduMaster AI — Revisión de Rigor y Estilo",
                )
                e2.download_button(
                    "Descargar en Word (.docx)",
                    data=docx_rev,
                    file_name="texto_revisado_edumaster.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key="btn_descarga_docx_revision",
                )
            except Exception as e:
                e2.info(f"DOCX no disponible: {e}")

            try:
                pdf_rev = create_pdf(
                    content=texto_final_editado,
                    title="Documento Académico Revisado",
                    subtitle="EduMaster AI — Revisión de Rigor y Estilo",
                )
                e3.download_button(
                    "Descargar en PDF (.pdf)",
                    data=pdf_rev,
                    file_name="texto_revisado_edumaster.pdf",
                    mime="application/pdf",
                    key="btn_descarga_pdf_revision",
                )
            except Exception as e:
                e3.info(f"PDF no disponible: {e}")

        st.info("📌 Recordatorio: el manuscrito final es de tu entera responsabilidad y autoría. Revisa y aprueba cada cambio antes de su uso definitivo.")
