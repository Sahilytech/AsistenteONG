"""Importación masiva segura de personas: previsualizar, normalizar y decidir.

La fase de previsualización nunca persiste datos. El operador obtiene un plan
explicable con filas válidas, campos reconocidos y posibles duplicados. La
persistencia ocurre únicamente mediante ``commit_import`` después de una
revisión explícita.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, datetime
import re
from typing import Any, Iterable

from ..person_registry import FIELDS, PersonRegistry


def _norm(value: Any) -> str:
    value = "" if value is None else str(value)
    return re.sub(r"\s+", " ", value.strip().casefold())


@dataclass(frozen=True)
class ImportRow:
    source_row: int
    data: dict[str, Any]
    recognized_fields: list[str]
    unknown_fields: list[str]
    warnings: list[str]
    match: dict[str, Any] | None
    confidence: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _aliases() -> dict[str, str]:
    return {_norm(alias): field for field, aliases in FIELDS.items() for alias in aliases}


def normalize_row(row: dict[str, Any]) -> tuple[dict[str, Any], list[str], list[str]]:
    aliases = _aliases()
    mapped: dict[str, Any] = {}
    recognized: list[str] = []
    unknown: list[str] = []
    for key, value in row.items():
        field = aliases.get(_norm(key))
        if field:
            if not str(mapped.get(field, "")).strip() and value not in (None, ""):
                mapped[field] = value
            if field not in recognized:
                recognized.append(field)
        elif str(key).strip():
            unknown.append(str(key))
    return mapped, recognized, unknown


def _confidence(data: dict[str, Any], match: dict[str, Any] | None) -> str:
    if match and data.get("document_id"):
        return "alta"
    if match and data.get("name") and data.get("birth_date"):
        return "alta"
    if match:
        return "media"
    if data.get("name"):
        return "nueva"
    return "incompleta"


def build_import_plan(rows: Iterable[dict[str, Any]], registry: PersonRegistry) -> dict[str, Any]:
    """Construye un plan de importación sin escribir en la base."""
    planned: list[ImportRow] = []
    seen_keys: dict[str, int] = {}
    for source_row, raw in enumerate(rows, 2):
        data, recognized, unknown = normalize_row(raw)
        warnings: list[str] = []
        if not data.get("name"):
            warnings.append("Falta nombre o identificador de persona.")
        if unknown:
            warnings.append("Hay columnas no reconocidas; no se importarán automáticamente.")
        key = _norm(data.get("document_id")) or f"name:{_norm(data.get('name'))}|birth:{_norm(data.get('birth_date'))}"
        if key and key in seen_keys:
            warnings.append(f"Posible duplicado dentro del archivo: fila {seen_keys[key]}.")
        elif key:
            seen_keys[key] = source_row
        match = registry.find_match(data) if data.get("name") else None
        if match:
            warnings.append("Coincide con una persona existente; se propone actualizar campos no vacíos.")
        planned.append(ImportRow(source_row, data, recognized, unknown, warnings, match, _confidence(data, match)))

    valid = sum(bool(row.data.get("name")) for row in planned)
    updates = sum(bool(row.match) for row in planned if row.data.get("name"))
    return {
        "rows": [row.to_dict() for row in planned],
        "total_rows": len(planned),
        "valid_rows": valid,
        "new_people": max(0, valid - updates),
        "potential_updates": updates,
        "requires_review": True,
        "persisted": False,
    }


def commit_import(plan: dict[str, Any], registry: PersonRegistry, selected_rows: Iterable[int] | None = None) -> dict[str, int]:
    """Persiste únicamente filas seleccionadas de un plan ya revisado."""
    if not plan.get("requires_review"):
        raise ValueError("La importación debe pasar por revisión antes de persistir.")
    allowed = set(selected_rows) if selected_rows is not None else {r["source_row"] for r in plan.get("rows", [])}
    created = updated = skipped = 0
    for row in plan.get("rows", []):
        if row.get("source_row") not in allowed:
            skipped += 1
            continue
        data = row.get("data") or {}
        if not data.get("name"):
            skipped += 1
            continue
        _, was_created = registry.upsert(data)
        if was_created:
            created += 1
        else:
            updated += 1
    return {"created": created, "updated": updated, "skipped": skipped, "persisted": created + updated}
