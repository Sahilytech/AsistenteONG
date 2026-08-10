from src.knowledge.semantic_retriever import LocalSemanticRetriever


def test_retriever_ranks_relevant_document_and_explains():
    docs = [
        {"url": "file://laboral.pdf", "domain": "archivo local", "title": "Despido laboral", "snippet": "Información sobre despido y derechos laborales.", "content": "despido laboral indemnización contrato"},
        {"url": "file://salud.pdf", "domain": "archivo local", "title": "Salud", "snippet": "Información sanitaria.", "content": "turnos médicos y centros de salud"},
    ]
    result = LocalSemanticRetriever().explain("despido laboral", docs)
    assert result["offline"] is True
    assert result["is_decision"] is False
    assert result["review_required"] is True
    assert result["results"][0]["source_url"] == "file://laboral.pdf"
    assert "despido" in result["results"][0]["matched_terms"]
    assert result["results"][0]["evidence_only"] is True


def test_empty_query_is_safe():
    assert LocalSemanticRetriever().rank("", [{"title": "x", "content": "x"}]) == []


def test_no_match_is_not_forced():
    docs = [{"url": "file://x", "title": "Salud", "content": "turnos médicos"}]
    assert LocalSemanticRetriever().rank("despido laboral", docs) == []
