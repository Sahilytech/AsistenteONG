import pytest
from src.core.social_report import empty_report, normalize_report, completeness
from src.core.resource_registry import validate_resource, register, find
from src.core.audit import event, append
from src.core.export_schema import export_case


def test_social_report_has_all_sections():
    report = empty_report()
    assert len(report) == 8
    assert completeness(report)["percentage"] == 0
    report["person"] = {"name": "Persona"}
    assert completeness(report)["percentage"] > 0


def test_resource_requires_traceable_source():
    assert validate_resource({"name": "X"})["valid"] is False
    resource = {"name": "X", "category": "legal", "jurisdiction": {"province": "Salta"}, "source": "fuente oficial", "verified_at": "2026-08-09"}
    resources = register([], resource)
    assert find(resources, province="Salta") == [resource]


def test_audit_events_are_append_only():
    item = event("case_created", actor="profesional", case_id="CASE-1")
    assert append([], item)[0]["case_id"] == "CASE-1"


def test_anonymized_export_hides_personal_data():
    data = export_case({"person": {"name": "Ana", "dni": "123"}, "category": "salud"}, anonymized=True)
    assert data["person"]["name"] == "[OCULTO]"
    assert data["category"] == "salud"
