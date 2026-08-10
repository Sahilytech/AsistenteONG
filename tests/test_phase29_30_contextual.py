from src.core.contextual_analysis import analyze_person_case, compare_case_history


def test_contextual_analysis_connects_history_and_evidence_without_decision():
    result = analyze_person_case(
        "La persona informa un despido y solicita orientación laboral.",
        history=[{"id": "c1", "date": "2026-01-01", "text": "Consulta por despido y situación laboral."}],
        evidence=[{"title": "guia laboral", "content": "Orientación sobre despido laboral."}],
    )
    assert result["history"]["cases_considered"] == 1
    assert result["history"]["related_cases"]
    assert result["evidence"]["relevant_documents"]
    assert result["review_required"] is True
    assert result["decision"] is None


def test_history_comparison_is_not_a_decision():
    result = compare_case_history(
        "Consulta por despido laboral.",
        [{"id": "old", "text": "También hubo una consulta por despido."}],
    )
    assert result["related_cases"]
    assert result["decision"] is None
