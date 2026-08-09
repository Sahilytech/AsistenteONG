"""Representación segura para exportar un expediente sin depender de UI."""
from .privacy import redact_personal


def export_case(case, anonymized=False):
    data = dict(case or {})
    if anonymized:
        for key in ('person', 'professional', 'household'):
            if isinstance(data.get(key), dict):
                data[key] = redact_personal(data[key])
    return data
