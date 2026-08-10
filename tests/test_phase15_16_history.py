from src.core.person_history import build_person_longitudinal_view, compare_person_cases, build_person_timeline


def _cases():
    return [
        {"case_number": "C-001", "created_at": "2026-01-10T10:00:00", "case_type": "laboral", "status": "cerrado", "urgency": "media", "text": "Consulta por despido y documentación laboral."},
        {"case_number": "C-002", "created_at": "2026-03-10T10:00:00", "case_type": "laboral", "status": "abierto", "urgency": "alta", "text": "Nuevo relato sobre despido y documentación laboral pendiente."},
    ]


def test_timeline_orders_cases_and_keeps_person_identity():
    result = build_person_timeline({"person_id": "P1", "name": "Ana"}, list(reversed(_cases())))
    assert result["person_id"] == "P1"
    assert result["case_count"] == 2
    assert [x["case_number"] for x in result["events"]] == ["C-001", "C-002"]


def test_comparison_exposes_recurring_signals_without_deciding():
    result = compare_person_cases(_cases())
    assert "despido" in result["recurring_signals"]
    assert "documentación" in result["common_signals"]
    assert result["evidence_only"] is True
    assert result["review_required"] is True


def test_longitudinal_view_contains_timeline_and_comparison():
    result = build_person_longitudinal_view({"person_id": "P1", "name": "Ana"}, _cases())
    assert result["timeline"]["case_count"] == 2
    assert result["comparison"]["cases_considered"] == 2
    assert result["comparison"]["review_required"] is True
