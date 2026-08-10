from src.core.person_workspace import build_person_workspace, summarize_workspace


def test_person_workspace_unifies_history_and_evidence_without_decision():
    ws = build_person_workspace(
        {"id": "p1", "name": "Persona"},
        [{"id": "c2", "date": "2026-08-02", "title": "Segundo"}, {"id": "c1", "date": "2026-01-02", "title": "Primero"}],
        [{"source": "documento.pdf", "content": "evidencia"}],
    )
    assert ws["person"]["id"] == "p1"
    assert [c["id"] for c in ws["cases"]] == ["c1", "c2"]
    assert len(ws["evidence"]) == 1
    assert ws["evidence_only"] is True
    assert ws["is_decision"] is False
    assert ws["review_required"] is True


def test_workspace_summary():
    ws = build_person_workspace({"id": "p1"}, [{"id": "c1"}], [])
    summary = summarize_workspace(ws)
    assert summary == {"case_count": 1, "evidence_count": 0, "review_required": True, "has_history": True}
