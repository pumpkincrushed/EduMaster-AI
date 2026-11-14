"""
Tests para el módulo de Materiales y Recursos Didácticos — EduMaster AI
"""

from unittest.mock import patch
from modules.materiales import render
from modules.materiales.generador import (
    listar_plantillas_unidades,
    cargar_plantilla_unidad,
    generar_material_didactico,
)
from config.models import AIResponse


def test_plantillas_unidades_disponibles():
    plantillas = listar_plantillas_unidades()
    assert "situacion_aprendizaje_lomloe" in plantillas
    assert "guia_alumnado" in plantillas
    assert "adaptacion_dua" in plantillas


def test_cargar_plantilla_unidad():
    sa = cargar_plantilla_unidad("situacion_aprendizaje_lomloe")
    assert sa is not None
    assert "secciones" in sa
    assert len(sa["secciones"]) > 0

    inexistente = cargar_plantilla_unidad("no_existe_404")
    assert inexistente is None


def test_materiales_render_callable():
    assert callable(render)


@patch("modules.materiales.generador.generate")
def test_generar_material_didactico(mock_generate):
    mock_generate.return_value = AIResponse(
        content="# Situación de Aprendizaje\nSecuencia didáctica por sesiones...",
        model="gemini-2.0-flash",
        success=True,
    )
    res = generar_material_didactico(
        tipo_recurso="Situación de Aprendizaje (LOMLOE)",
        titulo="Cambio Climático",
        materia="Biología",
        nivel_etapa="3º ESO",
        duracion_sesiones="6 sesiones",
        metodologia="ABP",
        objetivos_consigna="Foco en biodiversidad",
        esquema="1. Justificación\n2. Actividades",
    )
    assert res.success is True
    assert "Situación de Aprendizaje" in res.content
