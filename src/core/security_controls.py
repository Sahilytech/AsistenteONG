"""Controles locales de seguridad para sesión y copias cifradas.

No almacena contraseñas ni claves en texto plano. Las copias usan AES-GCM y
PBKDF2 para derivar una clave desde una frase secreta proporcionada por el
operador.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

MAGIC = b"ASISTENTE-ONG-BACKUP-v1\n"


def _derive_key(secret: str, salt: bytes) -> bytes:
    if not secret or len(secret) < 8:
        raise ValueError("La frase secreta debe tener al menos 8 caracteres.")
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=310_000)
    return kdf.derive(secret.encode("utf-8"))


def create_encrypted_backup(source_dir: str | Path, output_file: str | Path, secret: str) -> Path:
    """Empaqueta archivos de datos y genera una copia cifrada autenticada."""
    source = Path(source_dir)
    output = Path(output_file)
    if not source.exists() or not source.is_dir():
        raise FileNotFoundError(source)
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    key = _derive_key(secret, salt)
    from io import BytesIO
    raw = BytesIO()
    with zipfile.ZipFile(raw, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in source.rglob("*"):
            if path.is_file() and path.resolve() != output.resolve():
                archive.write(path, path.relative_to(source).as_posix())
    metadata = json.dumps({"version": 1, "created_at": int(time.time())}, separators=(",", ":")).encode()
    encrypted = AESGCM(key).encrypt(nonce, metadata + b"\n" + raw.getvalue(), None)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(MAGIC + base64.b64encode(salt + nonce + encrypted))
    return output


def restore_encrypted_backup(backup_file: str | Path, target_dir: str | Path, secret: str) -> Path:
    """Desencripta y restaura una copia; rechaza rutas ZIP inseguras."""
    backup = Path(backup_file)
    target = Path(target_dir)
    blob = backup.read_bytes()
    if not blob.startswith(MAGIC):
        raise ValueError("Formato de copia no reconocido.")
    payload = base64.b64decode(blob[len(MAGIC):])
    salt, nonce, encrypted = payload[:16], payload[16:28], payload[28:]
    key = _derive_key(secret, salt)
    plaintext = AESGCM(key).decrypt(nonce, encrypted, None)
    _, zip_bytes = plaintext.split(b"\n", 1)
    target.mkdir(parents=True, exist_ok=True)
    from io import BytesIO
    with zipfile.ZipFile(BytesIO(zip_bytes), "r") as archive:
        root = target.resolve()
        for member in archive.infolist():
            destination = (target / member.filename).resolve()
            if os.path.commonpath([str(root), str(destination)]) != str(root):
                raise ValueError("La copia contiene una ruta insegura.")
        archive.extractall(target)
    return target


@dataclass
class SessionGuard:
    timeout_seconds: int = 900
    last_activity: float = 0.0
    locked: bool = False

    def start(self) -> None:
        self.last_activity = time.monotonic()
        self.locked = False

    def touch(self) -> None:
        self.last_activity = time.monotonic()
        self.locked = False

    def check(self, now: float | None = None) -> bool:
        if self.locked:
            return False
        current = time.monotonic() if now is None else now
        if self.last_activity <= 0 or current - self.last_activity >= self.timeout_seconds:
            self.locked = True
            return False
        return True

    def lock(self) -> None:
        self.locked = True

    def unlock(self, secret: str, verifier: str) -> bool:
        candidate = hashlib.sha256(secret.encode("utf-8")).hexdigest()
        if secrets.compare_digest(candidate, verifier):
            self.touch()
            return True
        return False


def secret_verifier(secret: str) -> str:
    if not secret:
        raise ValueError("La frase secreta no puede estar vacía.")
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()
