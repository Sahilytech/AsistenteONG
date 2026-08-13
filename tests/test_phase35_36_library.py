from pathlib import Path
from src.knowledge.memory import LocalMemory
from src.knowledge.smart_retriever import retrieve, compare_texts

def test_retriever_returns_explainable_evidence(tmp_path):
    db = tmp_path / "knowledge.db"
    memory = LocalMemory(db)
    memory.save("file:///guia.pdf", "archivo local", "Guía laboral", "Despido y derechos", "La guía explica el despido y los derechos laborales.")
    result = retrieve("despido derechos", memory=memory)
    assert result
    assert result[0]["matched_terms"]
    assert result[0]["is_decision"] is False
    assert result[0]["requires_review"] is True

def test_page_evidence_preserves_provenance(tmp_path):
    memory = LocalMemory(tmp_path / "knowledge.db")
    source = "file:///guia.pdf"
    memory.save_page(source, 2, "Guía laboral", "Información sobre despido", "texto")
    rows = memory.page_evidence(source, "despido")
    assert rows and rows[0]["page"] == 2
    assert "despido" in rows[0]["matched_terms"]

def test_comparison_is_not_a_decision():
    result = compare_texts("consulta por despido laboral", "antecedente de despido laboral")
    assert "despido" in result["common_terms"]
    assert result["is_decision"] is False
    assert result["requires_review"] is True
