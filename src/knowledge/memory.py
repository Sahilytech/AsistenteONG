"""Memoria local: conserva resultados de fuentes oficiales y permite buscarlos offline."""
from __future__ import annotations
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "asistente.db"

class LocalMemory:
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or str(DB_PATH)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init(self):
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS knowledge_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_url TEXT UNIQUE,
                domain TEXT,
                title TEXT,
                snippet TEXT,
                content TEXT,
                saved_at TEXT
            )""")

    def save(self, source_url: str, domain: str, title: str, snippet: str, content: str = ""):
        with self._connect() as db:
            db.execute("""INSERT INTO knowledge_memory(source_url,domain,title,snippet,content,saved_at)
                VALUES(?,?,?,?,?,?) ON CONFLICT(source_url) DO UPDATE SET
                title=excluded.title,snippet=excluded.snippet,content=excluded.content,saved_at=excluded.saved_at""",
                (source_url, domain, title, snippet, content, datetime.now().isoformat(timespec="seconds")))

    def search(self, query: str, limit: int = 8):
        terms = [t.strip().lower() for t in query.split() if len(t.strip()) > 2]
        if not terms:
            return []
        where = " OR ".join(["lower(title) LIKE ?", "lower(snippet) LIKE ?", "lower(content) LIKE ?"] * len(terms))
        args = []
        for term in terms:
            like = f"%{term}%"
            args.extend([like, like, like])
        with self._connect() as db:
            rows = db.execute(f"SELECT source_url,domain,title,snippet,saved_at FROM knowledge_memory WHERE {where} ORDER BY saved_at DESC LIMIT ?", (*args, limit)).fetchall()
        return [dict(zip(("url","domain","title","snippet","saved_at"), row)) for row in rows]

    def count(self):
        with self._connect() as db:
            return db.execute("SELECT COUNT(*) FROM knowledge_memory").fetchone()[0]
