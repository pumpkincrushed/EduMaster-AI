"""
EduMaster AI — Motor central de Inteligencia Artificial

Único punto de conexión con la API de Google Gemini (SDK google-genai).
Todos los módulos deben llamar a este motor; ninguno conecta directamente con Gemini.
"""

import os
from typing import Optional, Generator

import streamlit as st
api_key = st.secrets["GEMINI_API_KEY"]

from config.settings import GEMINI_MODEL_DEFAULT, MAX_OUTPUT_TOKENS, DEFAULT_TEMPERATURE
from config.prompts import SYSTEM_BASE, PROMPT_NO_API_KEY, PROMPT_API_ERROR
from config.models import AIResponse


def _get_api_key() -> str:
    """
    Obtiene la clave de la API de Gemini.
    Prioridad: st.secrets (Streamlit Cloud) → variable de entorno → cadena vacía.
    """
    # 1. Streamlit Cloud secrets
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError, Exception):
        pass

    # 2. Variable de entorno (local con .env)
    return os.getenv("GEMINI_API_KEY", "")


def is_configured() -> bool:
    """Comprueba si hay una clave de API configurada."""
    return bool(_get_api_key())


def _get_client():
    """Crea y devuelve un cliente de Gemini configurado."""
    from google import genai
    api_key = _get_api_key()
    return genai.Client(api_key=api_key)


def generate(
    prompt: str,
    system_instruction: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = DEFAULT_TEMPERATURE,
    max_output_tokens: int = MAX_OUTPUT_TOKENS,
) -> AIResponse:
    """
    Genera una respuesta de Gemini.

    Args:
        prompt: El prompt del usuario.
        system_instruction: Instrucción de sistema específica del módulo.
                            Si es None, se usa SYSTEM_BASE.
        model: Modelo de Gemini. Si es None, se usa el modelo por defecto.
        temperature: Creatividad (0.0 determinista — 1.0 máxima creatividad).
        max_output_tokens: Tokens máximos de la respuesta.

    Returns:
        AIResponse con el contenido generado o información de error.
    """
    api_key = _get_api_key()
    if not api_key:
        return AIResponse(
            content=PROMPT_NO_API_KEY,
            model="none",
            success=False,
            error="api_key_missing",
        )

    model_name = model or GEMINI_MODEL_DEFAULT
    system = system_instruction or SYSTEM_BASE

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            ),
        )

        content = response.text if response.text else ""

        # Métricas de uso
        try:
            prompt_tokens = response.usage_metadata.prompt_token_count or 0
            output_tokens = response.usage_metadata.candidates_token_count or 0
        except AttributeError:
            prompt_tokens = 0
            output_tokens = 0

        return AIResponse(
            content=content,
            model=model_name,
            prompt_tokens=prompt_tokens,
            output_tokens=output_tokens,
            success=True,
        )

    except Exception as e:
        error_msg = str(e)
        return AIResponse(
            content=PROMPT_API_ERROR,
            model=model_name,
            success=False,
            error=error_msg,
        )


def generate_streaming(
    prompt: str,
    system_instruction: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = DEFAULT_TEMPERATURE,
) -> Generator[str, None, None]:
    """
    Generador que produce chunks de texto en streaming.
    Útil para respuestas largas que se muestran progresivamente en Streamlit.

    Usage:
        for chunk in generate_streaming(prompt):
            st.write(chunk)
    """
    api_key = _get_api_key()
    if not api_key:
        yield PROMPT_NO_API_KEY
        return

    model_name = model or GEMINI_MODEL_DEFAULT
    system = system_instruction or SYSTEM_BASE

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        for chunk in client.models.generate_content_stream(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=temperature,
                max_output_tokens=MAX_OUTPUT_TOKENS,
            ),
        ):
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"\n\n Error al conectar con Gemini: {e}"
