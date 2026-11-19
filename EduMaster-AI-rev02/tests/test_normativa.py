"""
Tests para el módulo de Normativa Educativa — EduMaster AI
"""

from unittest.mock import patch
from modules.normativa import render
from modules.normativa.consultor import consultar_normativa, generar_fundamentacion_juridica
from config.models import AIResponse


def test_normativa_render_callable():
    assert callable(render)


@patch("modules.normativa.consultor.generate")
def test_consultar_normativa(mock_generate):
    mock_generate.return_value = AIResponse(
        content="Según el Real Decreto 217/2022 de la ESO...",
        model="gemini-2.0-flash",
        success=True,
    )
    res = consultar_normativa("Duda sobre evaluación", etapa="ESO", comunidad_autonoma="Galicia")
    assert res.success is True
    assert "217/2022" in res.content


@patch("modules.normativa.consultor.generate")
def test_generar_fundamentacion_juridica(mock_generate):
    mock_generate.return_value = AIResponse(
        content="## Fundamentación Jurídica\nConforme a la Ley Orgánica 3/2020...",
        model="gemini-2.0-flash",
        success=True,
    )
    res = generar_fundamentacion_juridica("Historia", "3º ESO", "ABP en el aula", "Galicia")
    assert res.success is True
    assert "Fundamentación Jurídica" in res.content
