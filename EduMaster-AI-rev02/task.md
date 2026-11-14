# EduMaster AI — Tareas y Estado de Implementación

## Arquitectura Reorganizada (Completada al 100%)

### 1. Creación de contenido original
- [x] **Trabajos (`modules/trabajos/`):** Ensayos, propuestas de TFM y actividades a partir de esquemas propios, con prevención activa de citas alucinadas (`[Cita requerida]`).
- [x] **Materiales (`modules/materiales/`):** Generador de situaciones de aprendizaje (LOMLOE), guías de trabajo y adaptaciones DUA por nivel educativo.
- [x] **Evaluación (`modules/evaluacion/`):** Rúbricas analíticas en tabla, listas de cotejo e instrumentos formativos con principios DUA.

### 2. Revisión y prevención del plagio
- [x] **Analizar (`modules/revision/analisis.py`):** Diagnóstico lingüístico y cuantitativo sin modificar el texto ni prejuzgar autoría IA vs. humana.
- [x] **Revisar (`modules/revision/redaccion.py`):** Corrección de estilo, cohesión y rigor académico con comparación lado a lado y editor editable.
- [x] **Investigar (`modules/investigacion/`):** Gestor APA 7 (parentéticas, narrativas y bibliografía), verificador de fuentes y DOIs en vivo con Crossref, detector de citas ausentes y analizador de similitud documental.

### 3. Entrega y acompañamiento
- [x] **Documentos (`modules/documentos/`):** Exportación y maquetación centralizada en Word (`.docx`) y PDF (`.pdf`) con metadatos universitarios.
- [x] **Normativa (`modules/normativa/`):** Consultor curricular LOMLOE, Reales Decretos y decretos autonómicos (Galicia y CCAA), con generador de justificación jurídica.
- [x] **Asistente (`modules/asistente/`):** Tutor inteligente interactivo y router pedagógico para orientar al usuario a la herramienta adecuada.

### Plantillas Curriculares y Académicas (`templates/`)
- [x] `templates/trabajos/ensayo.json`
- [x] `templates/trabajos/tfm_innovacion.json`
- [x] `templates/trabajos/actividad.json`
- [x] `templates/unidades/situacion_aprendizaje_lomloe.json`
- [x] `templates/unidades/guia_alumnado.json`
- [x] `templates/unidades/adaptacion_dua.json`
- [x] `templates/rubricas/rubrica_analitica.json`

### Suite de Pruebas Unitarias (`tests/`)
- [x] `tests/test_ai.py` (5 tests)
- [x] `tests/test_documents.py` (15 tests)
- [x] `tests/test_sources.py` (6 tests)
- [x] `tests/test_revision.py` (2 tests)
- [x] `tests/test_trabajos.py` (5 tests)
- [x] `tests/test_materiales.py` (4 tests)
- [x] `tests/test_investigacion.py` (8 tests)
- [x] `tests/test_documentos_modulo.py` (3 tests)
- [x] `tests/test_evaluacion.py` (3 tests)
- [x] `tests/test_normativa.py` (3 tests)
- [x] `tests/test_asistente.py` (2 tests)
- **Total:** 56 pruebas pasando con éxito (100%).
