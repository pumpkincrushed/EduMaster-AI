"""
EduMaster AI — Historial de revisiones (Fase posterior)

Funciones para guardar y recuperar el historial de sesiones.
"""

from typing import Optional
from database.connection import get_connection


def save_revision(
    original: str,
    revised: str,
    level: str,
    register: str,
    module: str = "humanizador",
) -> Optional[int]:
    """
    Guarda una revisión en la base de datos.

    Returns:
        ID de la revisión creada, o None si falla.
    """
    try:
        with get_connection() as conn:
            # Crear sesión
            cur = conn.execute(
                "INSERT INTO sessions (module) VALUES (?)", (module,)
            )
            session_id = cur.lastrowid

            # Guardar revisión
            cur2 = conn.execute(
                """INSERT INTO revisions (session_id, original_text, revised_text, level, register)
                   VALUES (?, ?, ?, ?, ?)""",
                (session_id, original, revised, level, register),
            )
            conn.commit()
            return cur2.lastrowid
    except Exception:
        return None


def get_recent_revisions(limit: int = 10) -> list[dict]:
    """Recupera las últimas revisiones guardadas."""
    try:
        with get_connection() as conn:
            rows = conn.execute(
                """SELECT r.id, r.level, r.register, r.created_at,
                          LENGTH(r.original_text) as orig_len,
                          LENGTH(r.revised_text) as rev_len
                   FROM revisions r
                   ORDER BY r.created_at DESC
                   LIMIT ?""",
                (limit,),
            ).fetchall()
            return [dict(row) for row in rows]
    except Exception:
        return []
