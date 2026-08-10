from src.core.person_workspace import build_person_workspace


def test_workspace_ui_contract_has_history_evidence_and_review_boundary():
    ws = build_person_workspace(
        {"person_id": "p1", "name": "Persona"},
        [{"id": "c1", "created_at": "2026-08-10", "text": "Consulta laboral"}],
        [{"title": "protocolo.pdf", "snippet": "información relevante"}],
    )
    assert ws["case_count"] == 1
    assert ws["timeline"][0]["case_id"] == "c1"
    assert ws["evidence"][0]["title"] == "protocolo.pdf"
    assert ws["evidence_only"]
    assert not ws["is_decision"]
    assert ws["review_required"]
