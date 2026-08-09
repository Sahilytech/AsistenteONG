"""Seguimiento temporal de un caso."""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional

@dataclass
class TimelineEvent:
    event_type: str
    title: str
    description: str = ""
    created_at: str = ""
    actor: str = ""
    status: str = "registrado"

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat(timespec="seconds")

    def to_dict(self) -> Dict:
        return asdict(self)


def next_action(events: List[TimelineEvent]) -> Optional[TimelineEvent]:
    pending = [e for e in events if e.status == "pendiente"]
    return pending[0] if pending else None
