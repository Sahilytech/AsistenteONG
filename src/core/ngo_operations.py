"""Servicios operativos independientes de la interfaz.

Permiten que una ONG organice derivaciones, tareas, seguimientos y vencimientos
sin que la aplicación tenga que decidir por el equipo profesional.
"""
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Optional
import uuid


@dataclass
class Referral:
    case_id: str
    resource: str
    status: str = "pendiente"
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Task:
    case_id: str
    title: str
    due_at: str = ""
    status: str = "pendiente"
    assignee: str = ""
    notes: str = ""
    task_id: str = ""


@dataclass
class FollowUp:
    case_id: str
    scheduled_for: str
    channel: str = ""
    status: str = "pendiente"
    notes: str = ""
    followup_id: str = ""


class NGOOperations:
    """Repositorio en memoria pequeño y testeable; la UI puede persistirlo luego."""

    REFERRAL_STATUSES = {"pendiente", "contactada", "aceptada", "rechazada", "cerrada"}
    TASK_STATUSES = {"pendiente", "en curso", "completada", "cancelada"}
    FOLLOWUP_STATUSES = {"pendiente", "realizado", "cancelado"}

    def __init__(self):
        self.referrals: List[Referral] = []
        self.tasks: List[Task] = []
        self.followups: List[FollowUp] = []

    def add_referral(self, case_id: str, resource: str, notes: str = "") -> Dict:
        now = datetime.now().isoformat(timespec="seconds")
        item = Referral(str(case_id), str(resource).strip(), notes=str(notes), created_at=now, updated_at=now)
        self.referrals.append(item)
        return asdict(item)

    def update_referral(self, resource: str, status: str, notes: Optional[str] = None) -> Dict:
        if status not in self.REFERRAL_STATUSES:
            raise ValueError(f"Estado de derivación no válido: {status}")
        for item in reversed(self.referrals):
            if item.resource == resource:
                item.status = status
                if notes is not None:
                    item.notes = notes
                item.updated_at = datetime.now().isoformat(timespec="seconds")
                return asdict(item)
        raise KeyError(resource)

    def add_task(self, case_id: str, title: str, due_at: str = "", assignee: str = "", notes: str = "") -> Dict:
        item = Task(str(case_id), str(title).strip(), due_at, assignee=assignee, notes=notes, task_id=uuid.uuid4().hex)
        self.tasks.append(item)
        return asdict(item)

    def add_followup(self, case_id: str, scheduled_for: str, channel: str = "", notes: str = "") -> Dict:
        item = FollowUp(str(case_id), scheduled_for, channel, notes=notes, followup_id=uuid.uuid4().hex)
        self.followups.append(item)
        return asdict(item)

    def pending(self, now: Optional[datetime] = None) -> Dict[str, List[Dict]]:
        now = now or datetime.now()
        tasks = [asdict(x) for x in self.tasks if x.status == "pendiente"]
        followups = [asdict(x) for x in self.followups if x.status == "pendiente"]
        overdue = []
        upcoming = []
        for item in tasks:
            if not item["due_at"]:
                continue
            try:
                due = datetime.fromisoformat(item["due_at"])
            except ValueError:
                continue
            (overdue if due < now else upcoming).append(item)
        return {"overdue_tasks": overdue, "upcoming_tasks": upcoming, "pending_followups": followups,
                "pending_referrals": [asdict(x) for x in self.referrals if x.status == "pendiente"]}

    def dashboard(self, now: Optional[datetime] = None) -> Dict:
        pending = self.pending(now)
        return {
            "cases_with_tasks": len({x.case_id for x in self.tasks if x.status == "pendiente"}),
            "pending_referrals": len(pending["pending_referrals"]),
            "pending_followups": len(pending["pending_followups"]),
            "overdue_tasks": len(pending["overdue_tasks"]),
            "upcoming_tasks": len(pending["upcoming_tasks"]),
        }


def due_in(days: int, from_time: Optional[datetime] = None) -> str:
    """Genera una fecha ISO para tareas/seguimientos; útil para la UI."""
    return ((from_time or datetime.now()) + timedelta(days=int(days))).isoformat(timespec="minutes")
