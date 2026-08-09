"""Plan de intervención explicable y seguimiento del caso."""
from datetime import datetime


def build_intervention(case, analysis=None):
    analysis = analysis or getattr(case, "combined_analysis", {}) or {}
    profile = analysis.get("profile", {}) if isinstance(analysis, dict) else {}
    needs = analysis.get("needs", []) or profile.get("needs", []) or []
    actions = []
    for need in needs:
        label = need if isinstance(need, str) else need.get("name", "Necesidad")
        actions.append({"need": label, "action": "Recopilar información y definir derivación con el profesional responsable.", "status": "pendiente"})
    if not actions:
        actions.append({"need": "Información insuficiente", "action": "Completar entrevista y revisar el caso antes de definir una intervención.", "status": "pendiente"})
    return {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "objective": "Definir próximos pasos verificables sin sustituir el criterio profesional.",
        "actions": actions,
        "next_review": None,
    }


def add_action(plan, need, action):
    plan = dict(plan or {})
    plan.setdefault("actions", []).append({"need": need, "action": action, "status": "pendiente"})
    return plan
