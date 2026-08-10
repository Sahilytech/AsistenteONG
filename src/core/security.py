"""Controles de seguridad y privacidad para datos sensibles de la ONG.

No sustituye una política institucional ni asesoramiento profesional.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any


SENSITIVE_KEYS = {
    "dni", "documento", "cuil", "telefono", "phone", "email", "correo",
    "direccion", "domicilio", "fecha_nacimiento", "birth_date", "sexualidad",
    "orientacion_sexual", "identidad_genero", "genero", "nombre_completo",
}


@dataclass(frozen=True)
class SecurityResult:
    allowed: bool
    reason: str


def redact_value(key: str, value: Any) -> Any:
    """Redacta valores personales para logs, diagnósticos y exportaciones."""
    if value is None:
        return None
    if key.lower() in SENSITIVE_KEYS:
        return "[REDACTADO]"
    return value


def redact_record(record: dict[str, Any]) -> dict[str, Any]:
    return {key: redact_value(key, value) for key, value in record.items()}


def stable_case_reference(case_id: str, secret: str) -> str:
    """Genera una referencia no reversible para uso interno."""
    payload = f"{secret}:{case_id}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def validate_import(path: str, allowed_extensions: set[str] | None = None) -> SecurityResult:
    """Valida una importación por extensión antes de procesarla."""
    allowed = allowed_extensions or {".pdf", ".xlsx", ".xls", ".csv", ".txt", ".docx"}
    suffix = path.lower().rsplit(".", 1)[-1] if "." in path else ""
    extension = f".{suffix}" if suffix else ""
    if extension not in allowed:
        return SecurityResult(False, "tipo de archivo no permitido")
    return SecurityResult(True, "archivo permitido")


def sanitize_filename(name: str) -> str:
    """Evita rutas y caracteres de control al guardar documentos importados."""
    name = name.replace("\\", "/").split("/")[-1]
    name = re.sub(r"[\x00-\x1f<>:\"|?*]", "_", name).strip()
    return name or "documento"


def security_summary() -> dict[str, Any]:
    return {
        "local_processing": True,
        "logs_redact_sensitive_data": True,
        "professional_review_required": True,
        "supported_imports": ["pdf", "xlsx", "xls", "csv", "txt", "docx"],
    }
