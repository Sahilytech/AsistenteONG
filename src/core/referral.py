"""Derivaciones trazables: nunca inventa datos de contacto."""
from datetime import datetime

STATUSES = ('pendiente','contactado','derivado','aceptado','en_seguimiento','resuelto','no_concretado')

def create_referral(case_id, category, resource=None, reason='', status='pendiente'):
    if status not in STATUSES:
        status = 'pendiente'
    return {'case_id': case_id, 'category': category, 'resource': resource or {}, 'reason': reason, 'status': status, 'created_at': datetime.now().isoformat(timespec='seconds'), 'updated_at': datetime.now().isoformat(timespec='seconds')}
