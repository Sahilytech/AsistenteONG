"""Datos institucionales que pueden reutilizarse en nuevos informes."""
import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "asistente.db"

class ReportDefaults:
    KEYS = ("entidad_emisora", "profesional_referencia", "colegiatura", "destinatario")
    def __init__(self, db_path=None):
        self.db_path = str(db_path or DB_PATH)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS report_defaults (id INTEGER PRIMARY KEY CHECK(id=1), data TEXT NOT NULL)")
    def load(self):
        with sqlite3.connect(self.db_path) as db:
            row = db.execute("SELECT data FROM report_defaults WHERE id=1").fetchone()
        if not row:
            return {}
        try:
            return json.loads(row[0])
        except Exception:
            return {}
    def save(self, data):
        clean = {k: str(data.get(k, "")).strip() for k in self.KEYS}
        with sqlite3.connect(self.db_path) as db:
            db.execute("INSERT INTO report_defaults(id,data) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data", (json.dumps(clean, ensure_ascii=False),))
        return clean
