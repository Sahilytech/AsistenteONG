from datetime import datetime

def create_followup(case_id, action, due_at=None, owner=''):
    return {'case_id':case_id,'action':action,'due_at':due_at,'owner':owner,'status':'pendiente','created_at':datetime.now().isoformat(timespec='seconds')}

def pending(items):
    return [x for x in (items or []) if x.get('status') not in ('resuelto','cancelado')]
