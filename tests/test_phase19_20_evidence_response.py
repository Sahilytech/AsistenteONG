from src.core.evidence_response import build_evidence_response, compare_case_with_documents


def test_response_keeps_evidence_separate_from_decision():
    result = build_evidence_response(
        "La persona refiere despido y consulta por su situación laboral.",
        [{"title": "registro.pdf", "content": "El documento menciona despido y situación laboral.", "page": 3}],
    )
    assert result["evidence"]
    assert "despido" in result["evidence"][0]["matched_terms"]
    assert result["evidence_only"] is True
    assert result["is_decision"] is False
    assert result["review_required"] is True


def test_comparison_has_traceability():
    result = compare_case_with_documents("consulta laboral", [{"title": "guia.pdf", "content": "consulta laboral", "source_url": "file:///guia.pdf"}])
    assert result["comparison"]["documents_considered"] == 1
    assert result["comparison"]["documents_with_matches"] == 1
    assert result["evidence"][0]["source"] == "guia.pdf"
