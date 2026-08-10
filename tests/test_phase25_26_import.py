from src.core.intelligent_case_import import extract_case_candidates, build_import_review


def test_document_extraction_is_review_only():
    result = extract_case_candidates("Nombre: Ana Perez; Fecha de nacimiento: 01/02/2000; Fecha de atención: 10/08/2026; Motivo: despido")
    assert result["people"][0]["name"] == "Ana Perez"
    assert result["cases"][0]["date"] == "10/08/2026"
    assert "despido" in result["signals"]
    assert result["requires_review"] is True
    assert result["persisted"] is False
    assert result["decision"] is None


def test_pdf_review_contains_provenance_and_never_persists():
    review = build_import_review({"type": "pdf", "filename": "ficha.pdf", "fingerprint": "abc", "text": "Nombre: Ana Perez; Motivo: vivienda"})
    assert review["filename"] == "ficha.pdf"
    assert review["source_fingerprint"] == "abc"
    assert review["people"]
    assert review["persisted"] is False
    assert review["accepted"] == []
    assert review["rejected"] == []
