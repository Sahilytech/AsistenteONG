"""Auditoría mínima y estructurada para acciones profesionales."""
from datetime import datetime


def event(action, actor='', case_id='', details=None):
    return {'timestamp': datetime.now().isoformat(timespec='seconds'), 'action': action, 'actor': actor, 'case_id': case_id, 'details': details or {}}


def append(log, item):
    result = list(log or [])
    result.append(item)
    return result
