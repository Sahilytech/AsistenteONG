from datetime import datetime, timedelta

from src.core.explainable_analysis import analyze_case, compare_texts
from src.core.ngo_operations import NGOOperations, due_in


def test_explainable_analysis_exposes_reason_evidence_and_review():
    result = analyze_case(
        "Me echaron del trabajo y tengo las comunicaciones del empleador.",
        history=[{"case_id": "A-1", "date": "2026-01-10", "status": "cerrado", "text": "Consulta laboral por despido."}],
        evidence=[{"title": "Guía laboral", "content": "Procedimiento ante despido y documentación laboral."}],
    )
    assert result["category"] == "Situacion laboral"
    assert result["review_required"] is True
    assert result["evidence"]
    assert result["history_comparison"]
    assert result["explanation"]["positive_signals"]
    assert result["explanation"]["limitations"]


def test_negated_signal_is_explained_without_becoming_positive():
    result = analyze_case("No hubo violencia, solo necesito orientación.")
    assert result["negative_signals"] or result["explanation"]["negative_signals"]
    assert result["urgency"] != "muy alta"


def test_text_comparison_is_not_a_decision():
    result = compare_texts("Problema laboral y despido", "Despido y consulta laboral")
    assert "despido" in result["common_signals"]
    assert result["review_required"] is True


def test_operations_track_referrals_tasks_followups_and_overdue():
    ops = NGOOperations()
    ops.add_referral("C-1", "Línea 144")
    ops.add_task("C-1", "Revisar documentación", due_in(-1))
    ops.add_followup("C-1", due_in(7), "teléfono")
    dashboard = ops.dashboard(datetime.now())
    assert dashboard["pending_referrals"] == 1
    assert dashboard["overdue_tasks"] == 1
    assert dashboard["pending_followups"] == 1


def test_invalid_referral_status_is_rejected():
    ops = NGOOperations()
    ops.add_referral("C-1", "Recurso")
    try:
        ops.update_referral("Recurso", "inventado")
    except ValueError:
        return
    assert False, "Debe rechazar estados de derivación desconocidos"
