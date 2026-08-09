"""Perfil integral y reglas de composición del caso."""
from __future__ import annotations
import re
from datetime import datetime


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def build_case_context(text: str, social_report: dict | None = None, location: dict | None = None) -> dict:
    report = social_report or {}
    return {
        "summary": normalize_text(text),
        "social_report": report,
        "location": location or {},
        "needs": report.get("needs", []),
        "people": report.get("household_members", []),
        "vulnerabilities": report.get("vulnerabilities", []),
        "strengths": report.get("strengths", []),
        "missing_information": [],
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }


def merge_case_context(context: dict, updates: dict) -> dict:
    result = dict(context or {})
    for key, value in (updates or {}).items():
        if value is not None:
            result[key] = value
    return result
