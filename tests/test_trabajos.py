"""
Tests para el módulo de Trabajos Académicos — EduMaster AI
"""

from unittest.mock import patch, MagicMock
from modules.trabajos import render
from modules.trabajos.generador import (
    listar_plantillas_disponibles,
    cargar_plantilla,
    sugerir_esquema,
    generar_contenido_trabajo,
)
from config.models import AIResponse


def test_plantillas_disponibles():
    plantillas = listar_plantillas_disponibles()
    assert "ensayo" in plantillas
    assert "tfm_innovacion" in plantillas
    assert "actividad" in plantillas


def test_cargar_plantilla():
    ensayo = cargar_plantilla("ensayo")
    assert ensayo is not None
    assert "secciones" in ensayo
    assert len(ensayo["secciones"]) > 0

    no_existe = cargar_plantilla("inexistente_123")
    assert no_existe is None


def test_trabajos_render_callable():
    assert callable(render)


@patch("modules.trabajos.generador.generate")
def test_sugerir_esquema(mock_generate):
    mock_generate.return_value = AIResponse(
        content="1. Intro\n2. Desarrollo\n3. Conclusión",
        model="gemini-2.0-flash",
        success=True,
    )
    res = sugerir_esquema("Ensayo Académico", "Tema de prueba", "Consigna")
    assert res.success is True
    assert "1. Intro" in res.content


@patch("modules.trabajos.generador.generate")
def test_generar_contenido_trabajo(mock_generate):
    mock_generate.return_value = AIResponse(
        content="# Título\nContenido desarrollado con [Cita requerida: Vigotsky, 1978]",
        model="gemini-2.0-flash",
        success=True,
    )
    res = generar_contenido_trabajo(
        tipo="Ensayo Académico",
        tema="Constructivismo en el aula",
        nivel_etapa="Secundaria",
        esquema="1. Intro\n2. Conclusión",
        consigna="Foco en Vigotsky",
    )
    assert res.success is True
    assert "Cita requerida" in res.content
