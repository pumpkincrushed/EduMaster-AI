"""
EduMaster AI — Conexión a base de datos SQLite (Fase posterior)

Esqueleto preparado para activarse en fases avanzadas del proyecto.
La base de datos guardará historial de revisiones y metadatos de sesión.
"""

import sqlite3
import os
from pathlib import Path
from config.settings import BASE_DIR

DB_PATH = BASE_DIR / "database" / "edumaster.db"


def get_connection() -> sqlite3.Connection:
    """
    Devuelve una conexión a la base de datos SQLite.
    Crea el archivo si no existe.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    """
    Crea las tablas necesarias si no existen.
    Llamar una vez al inicio de la aplicación cuando se active la DB.
    """
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS revisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                original_text TEXT,
                revised_text TEXT,
                level TEXT,
                register TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        """)
        conn.commit()
