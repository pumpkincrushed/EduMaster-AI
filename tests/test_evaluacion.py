"""
Tests para el módulo de Evaluación Educativa — EduMaster AI
"""

from unittest.mock import patch
from modules.evaluacion import render
from modules.evaluacion.generador import (
    cargar_plantilla_rubrica,
    generar_instrumento_evaluacion,
)
from config.models import AIResponse


def test_evaluacion_render_callable():
    assert callable(render)


def test_cargar_plantilla_rubrica():
    rubrica = cargar_plantilla_rubrica()
    assert rubrica is not None
    assert "niveles" in rubrica
    assert "dimensiones_sugeridas" in rubrica


@patch("modules.evaluacion.generador.generate")
def test_generar_instrumento_evaluacion(mock_generate):
    mock_generate.return_value = AIResponse(
        content="| Criterio | Insuficiente | Suficiente | Notable | Sobresaliente |\n|---|---|---|---|---|",
        model="gemini-2.0-flash",
        success=True,
    )
    res = generar_instrumento_evaluacion(
        tipo_instrumento="Rúbrica Analítica Competencial",
        tarea_evaluar="Exposición Oral",
        materia="Lengua",
        nivel_etapa="Secundaria",
        criterios_especificos="Claridad y expresión",
        ponderaciones="100%",
        incluir_dua=True,
    )
    assert res.success is True
    assert "Criterio" in res.content
