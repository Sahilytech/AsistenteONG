"""Esquema normalizado del Informe Social."""
SECTIONS = (
    "professional", "person", "household", "socioeconomic", "housing",
    "health_education", "assessment", "intervention"
)


def empty_report():
    return {section: {} for section in SECTIONS}


def normalize_report(report):
    base = empty_report()
    for key, value in (report or {}).items():
        if key in base:
            base[key] = value if isinstance(value, dict) else {"value": value}
    return base


def completeness(report):
    normalized = normalize_report(report)
    filled = sum(bool(value) for value in normalized.values())
    return {"filled_sections": filled, "total_sections": len(SECTIONS), "percentage": round(filled / len(SECTIONS) * 100)}
