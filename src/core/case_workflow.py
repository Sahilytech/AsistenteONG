"""Flujo simple y coherente del expediente.

Los estados visibles usan lenguaje operativo habitual para equipos de asistencia.
Se mantienen aliases de estados antiguos para compatibilidad con instalaciones/tests previos.
"""
from datetime import datetime

STATES = ('nuevo', 'en análisis', 'revisado', 'derivado', 'en seguimiento', 'cerrado')
TRANSITIONS = {
    'nuevo': {'en análisis', 'cerrado'},
    'en análisis': {'revisado', 'derivado', 'en seguimiento', 'cerrado'},
    'revisado': {'derivado', 'en seguimiento', 'cerrado', 'en análisis'},
    'derivado': {'en seguimiento', 'revisado', 'cerrado'},
    'en seguimiento': {'revisado', 'cerrado'},
    'cerrado': {'revisado'},
    # Compatibilidad con el flujo anterior del proyecto.
    'borrador': {'abierto'},
    'abierto': {'revisado', 'derivado', 'cerrado'},
}


def can_transition(current, target):
    return target in TRANSITIONS.get(current, set())


def transition(case, target, actor='sistema'):
    current = case.get('status', 'nuevo')
    if current == target:
        return dict(case)
    if not can_transition(current, target):
        raise ValueError(f'Transición no permitida: {current} -> {target}')
    result = dict(case)
    result['status'] = target
    result['status_updated_at'] = datetime.now().isoformat(timespec='seconds')
    result['status_updated_by'] = actor
    return result
