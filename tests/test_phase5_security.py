from src.core.security import redact_record, sanitize_filename, stable_case_reference, validate_import


def test_sensitive_data_is_redacted():
    result = redact_record({"nombre_completo": "Ana", "dni": "123", "categoria": "laboral"})
    assert result["nombre_completo"] == "[REDACTADO]"
    assert result["dni"] == "[REDACTADO]"
    assert result["categoria"] == "laboral"


def test_import_validation_and_filename_sanitization():
    assert validate_import("casos.pdf").allowed
    assert validate_import("casos.xlsx").allowed
    assert not validate_import("programa.exe").allowed
    assert sanitize_filename(r"..\secret:name?.pdf") == "secret_name_.pdf"


def test_case_reference_is_stable_and_non_plaintext():
    first = stable_case_reference("case-123", "local-secret")
    assert first == stable_case_reference("case-123", "local-secret")
    assert "case-123" not in first
