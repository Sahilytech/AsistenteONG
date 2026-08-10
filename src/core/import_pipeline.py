"""Pipeline seguro de entrada para documentos de personas y casos."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .security import sanitize_filename, validate_import


def prepare_import(path: str) -> dict[str, Any]:
    """Prepara un archivo para importación sin leerlo todavía.

    La lectura/interpretación concreta queda desacoplada para que cada formato
    pueda tener un parser especializado y revisión antes de persistir datos.
    """
    validation = validate_import(path)
    safe_name = sanitize_filename(Path(path).name)
    return {
        "allowed": validation.allowed,
        "reason": validation.reason,
        "filename": safe_name,
        "extension": Path(safe_name).suffix.lower(),
        "requires_review": True,
        "persisted": False,
    }
