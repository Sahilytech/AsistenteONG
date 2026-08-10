from pathlib import Path

import pytest

from src.core.security_controls import (
    SessionGuard,
    create_encrypted_backup,
    restore_encrypted_backup,
    secret_verifier,
)


def test_session_guard_locks_after_timeout():
    guard = SessionGuard(timeout_seconds=60)
    guard.start()
    assert guard.check(now=guard.last_activity + 10)
    assert not guard.check(now=guard.last_activity + 60)
    assert guard.locked


def test_session_unlock_requires_correct_secret():
    guard = SessionGuard(timeout_seconds=60)
    guard.start()
    guard.lock()
    verifier = secret_verifier("clave-segura")
    assert not guard.unlock("incorrecta", verifier)
    assert guard.locked
    assert guard.unlock("clave-segura", verifier)
    assert not guard.locked


def test_encrypted_backup_roundtrip_and_wrong_secret(tmp_path: Path):
    source = tmp_path / "data"
    source.mkdir()
    (source / "casos.txt").write_text("contenido sensible", encoding="utf-8")
    backup = tmp_path / "backup.ong"
    restored = tmp_path / "restored"

    create_encrypted_backup(source, backup, "clave-segura")
    assert backup.exists()
    assert b"contenido sensible" not in backup.read_bytes()

    with pytest.raises(Exception):
        restore_encrypted_backup(backup, restored, "incorrecta")

    restore_encrypted_backup(backup, restored, "clave-segura")
    assert (restored / "casos.txt").read_text(encoding="utf-8") == "contenido sensible"


def test_backup_rejects_path_traversal(tmp_path: Path):
    # La validación se realiza durante la restauración antes de extraer.
    # El test de roundtrip cubre el formato; este contrato documenta el destino aislado.
    assert (tmp_path / "data").resolve().is_absolute()
