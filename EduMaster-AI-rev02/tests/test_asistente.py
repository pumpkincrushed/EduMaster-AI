"""
Tests para el módulo de Asistente IA y Router Pedagógico — EduMaster AI
"""

from unittest.mock import patch
from modules.asistente import render
from modules.asistente.tutor import responder_asistente
from config.models import AIResponse


def test_asistente_render_callable():
    assert callable(render)


@patch("modules.asistente.tutor.generate")
def test_responder_asistente(mock_generate):
    mock_generate.return_value = AIResponse(
        content="Te recomiendo utilizar la herramienta de Trabajos en la barra lateral.",
        model="gemini-2.0-flash",
        success=True,
    )
    res = responder_asistente("¿Dónde puedo escribir mi ensayo de TFM?")
    assert res.success is True
    assert "Trabajos" in res.content
