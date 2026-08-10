"""Control de acceso local, simple y auditable para Asistente ONG."""
from __future__ import annotations
from dataclasses import dataclass

ROLE_PERMISSIONS = {
    "administracion": {"view", "create", "edit", "delete", "export", "manage_users", "audit"},
    "profesional": {"view", "create", "edit", "export", "audit"},
    "operador": {"view", "create", "edit"},
    "consulta": {"view"},
}

@dataclass(frozen=True)
class AccessContext:
    user_id: str
    role: str

    def can(self, permission: str) -> bool:
        return permission in ROLE_PERMISSIONS.get(self.role, set())

def allowed_roles() -> list[str]:
    return list(ROLE_PERMISSIONS)

def can(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())

def require(context: AccessContext, permission: str) -> None:
    if not context.can(permission):
        raise PermissionError(f"El rol '{context.role}' no tiene permiso para '{permission}'.")
