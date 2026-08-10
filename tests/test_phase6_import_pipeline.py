from src.core.import_pipeline import prepare_import


def test_prepare_import_keeps_import_reviewable():
    result = prepare_import(r"C:\datos\personas.xlsx")
    assert result["allowed"] is True
    assert result["filename"] == "personas.xlsx"
    assert result["requires_review"] is True
    assert result["persisted"] is False


def test_prepare_import_rejects_executable():
    result = prepare_import(r"C:\datos\personas.exe")
    assert result["allowed"] is False
