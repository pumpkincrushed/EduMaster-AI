"""
Tests para el módulo unificado de revisión y análisis — EduMaster AI
"""

from modules.revision.analisis import calcular_metricas
from modules.revision import render_analisis, render_redaccion, render


def test_calcular_metricas():
    texto = "Este es un primer párrafo de prueba. Contiene varias frases bien construidas.\n\nEste es un segundo párrafo diferente."
    metricas = calcular_metricas(texto)

    assert metricas["Palabras"] > 0
    assert metricas["Frases"] == 3
    assert metricas["Párrafos"] == 2
    assert metricas["Diversidad léxica (TTR)"] > 0
    assert metricas["Media palabras/frase"] > 0


def test_revision_exports():
    assert callable(render_analisis)
    assert callable(render_redaccion)
    assert callable(render)
