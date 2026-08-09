"""Estado y reglas de transición del expediente."""
from datetime import datetime

STATES = ('borrador','abierto','en_evaluacion','en_intervencion','en_seguimiento','cerrado','archivado')
TRANSITIONS = {
    'borrador': {'abierto'},
    'abierto': {'en_evaluacion','cerrado'},
    'en_evaluacion': {'en_intervencion','en_seguimiento','cerrado'},
    'en_intervencion': {'en_seguimiento','cerrado'},
    'en_seguimiento': {'cerrado'},
    'cerrado': {'archivado','abierto'},
    'archivado': set(),
}

def can_transition(current, target):
    return target in TRANSITIONS.get(current, set())

def transition(case, target, actor='sistema'):
    current = case.get('status','borrador')
    if current == target:
        return case
    if not can_transition(current,target):
        raise ValueError(f'Transición no permitida: {current} -> {target}')
    result=dict(case)
    result['status']=target
    result['status_updated_at']=datetime.now().isoformat(timespec='seconds')
    result['status_updated_by']=actor
    return result
