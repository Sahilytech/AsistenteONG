"""Esquema estructurado del informe social.

Los campos son deliberadamente neutrales: el sistema organiza información,
pero no inventa diagnósticos ni conclusiones profesionales.
"""
from dataclasses import dataclass, field, asdict
from typing import Dict, List

@dataclass
class SocialReport:
    institution: str = ""
    professional: str = ""
    professional_license: str = ""
    recipient: str = ""
    issue_date: str = ""
    reason: str = ""
    person_name: str = ""
    legal_id: str = ""
    contact: str = ""
    address: str = ""
    birth_date: str = ""
    age: str = ""
    nationality: str = ""
    civil_status: str = ""
    household: List[Dict] = field(default_factory=list)
    family_history: str = ""
    family_dynamics: str = ""
    income_sources: List[str] = field(default_factory=list)
    employment_status: str = ""
    basic_expenses: List[str] = field(default_factory=list)
    tenure: str = ""
    housing_conditions: str = ""
    services: List[str] = field(default_factory=list)
    health: str = ""
    education: str = ""
    professional_assessment: str = ""
    intervention_proposal: str = ""
    strengths: List[str] = field(default_factory=list)
    vulnerabilities: List[str] = field(default_factory=list)
    genogram: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return asdict(self)

    def missing_core_fields(self) -> List[str]:
        fields = []
        for name, value in (("institución", self.institution), ("profesional", self.professional),
                            ("destinatario", self.recipient), ("motivo", self.reason),
                            ("persona de referencia", self.person_name)):
            if not str(value).strip():
                fields.append(name)
        return fields


def combine_case_and_report(case_text: str, report: SocialReport) -> Dict:
    """Devuelve contexto combinado para el motor sin convertirlo en diagnóstico."""
    return {
        "case_text": case_text,
        "social_report": report.to_dict(),
        "missing_report_fields": report.missing_core_fields(),
        "instruction": "Analizar el relato y el informe como un único contexto y señalar información faltante.",
    }
