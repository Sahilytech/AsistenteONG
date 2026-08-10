from pathlib import Path
from tempfile import TemporaryDirectory

from openpyxl import Workbook

from src.core.bulk_people_import import build_import_plan, commit_import
from src.core.document_ingestion import preview_document
from src.person_registry import PersonRegistry


def test_bulk_plan_maps_unknown_columns_without_persisting():
    with TemporaryDirectory() as tmp:
        db = Path(tmp) / "people.db"
        registry = PersonRegistry(db)
        rows = [{"Nombre completo": "Ana Pérez", "DNI": "123", "Dato inventado": "x"}]
        plan = build_import_plan(rows, registry)
        assert plan["valid_rows"] == 1
        assert plan["persisted"] is False
        assert plan["rows"][0]["data"]["name"] == "Ana Pérez"
        assert "Dato inventado" in plan["rows"][0]["unknown_fields"]
        assert registry.list_people() == []


def test_bulk_plan_detects_existing_person_and_commit_is_explicit():
    with TemporaryDirectory() as tmp:
        registry = PersonRegistry(Path(tmp) / "people.db")
        registry.upsert({"name": "Ana Pérez", "document_id": "123"})
        plan = build_import_plan([{"Nombre completo": "Ana Pérez", "DNI": "123", "Edad": 36}], registry)
        assert plan["potential_updates"] == 1
        assert plan["rows"][0]["confidence"] == "alta"
        assert registry.case_count(registry.list_people()[0]["person_id"]) == 0
        result = commit_import(plan, registry, selected_rows=[])
        assert result["persisted"] == 0
        assert len(registry.list_people()) == 1


def test_xlsx_can_feed_bulk_plan():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "personas.xlsx"
        wb = Workbook()
        ws = wb.active
        ws.append(["Nombre completo", "DNI", "Edad"])
        ws.append(["Luis Gómez", "456", 29])
        wb.save(path)
        preview = preview_document(path)
        registry = PersonRegistry(Path(tmp) / "people.db")
        plan = build_import_plan(preview["rows"], registry)
        assert plan["valid_rows"] == 1
        result = commit_import(plan, registry)
        assert result["created"] == 1
        assert registry.list_people()[0]["name"] == "Luis Gómez"
