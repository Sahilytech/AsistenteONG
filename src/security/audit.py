"""Registro de auditoría local sin almacenar el contenido sensible del caso."""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List

@dataclass
class AuditEvent:
    action: str
    actor: str = "sistema"
    case_number: str = ""
    detail: str = ""
    created_at: str = ""
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat(timespec="seconds")
    def to_dict(self) -> Dict:
        return asdict(self)

class AuditLog:
    def __init__(self):
        self.events: List[AuditEvent] = []
    def record(self, action: str, actor: str = "sistema", case_number: str = "", detail: str = "") -> AuditEvent:
        event = AuditEvent(action, actor, case_number, detail)
        self.events.append(event)
        return event
    def export(self) -> List[Dict]:
        return [event.to_dict() for event in self.events]
