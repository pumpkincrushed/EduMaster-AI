"""
EduMaster AI — Motor central de Inteligencia Artificial

Único punto de conexión con la API de Google Gemini (SDK google-genai).
Todos los módulos deben llamar a este motor; ninguno conecta directamente con Gemini.
"""

import os
from typing import Optional, Generator

import streamlit as st

from config.settings import GEMINI_MODEL_DEFAULT, MAX_OUTPUT_TOKENS, DEFAULT_TEMPERATURE
from config.prompts import SYSTEM_BASE, PROMPT_NO_API_KEY, PROMPT_API_ERROR
from config.models import AIResponse


def _get_api_key() -> str:
    """
    Obtiene la clave de la API de Gemini.
    Prioridad: st.secrets (Streamlit Cloud) → variable de entorno → cadena vacía.
    """
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY", "")


def is_configured() -> bool:
    """Comprueba si hay una clave de API configurada."""
    return bool(_get_api_key())


def _get_client():
    """Crea el cliente de Gemini forzando la versión v1beta de la API."""
    from google import genai
    from google.genai import types

    return genai.Client(
        api_key=_get_api_key(),
        http_options=types.HttpOptions(api_version="v1beta"),
    )


def generate(
    prompt: str,
    system_instruction: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = DEFAULT_TEMPERATURE,
    max_output_tokens: int = MAX_OUTPUT_TOKENS,
) -> AIResponse:
    """Genera una respuesta de Gemini y devuelve un AIResponse."""
    if not _get_api_key():
        return AIResponse(
            content=PROMPT_NO_API_KEY,
            model="none",
            success=False,
            error="api_key_missing",
        )

    model_name = model or GEMINI_MODEL_DEFAULT
    system = system_instruction or SYSTEM_BASE

    try:
        from google.genai import types

        client = _get_client()
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
        return AIResponse(
            content=PROMPT_API_ERROR,
            model=model_name,
            success=False,
            error=str(e),
        )


def generate_streaming(
    prompt: str,
    system_instruction: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = DEFAULT_TEMPERATURE,
) -> Generator[str, None, None]:
    """Genera la respuesta en streaming, por trozos de texto."""
    if not _get_api_key():
        yield PROMPT_NO_API_KEY
        return

    model_name = model or GEMINI_MODEL_DEFAULT
    system = system_instruction or SYSTEM_BASE

    try:
        from google.genai import types

        client = _get_client()
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
        yield f"\n\nError al conectar con Gemini: {e}"
