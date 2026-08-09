"""Auditoría estructurada sin almacenar más datos personales de los necesarios."""
from datetime import datetime

class AuditLog:
    def __init__(self): self.events=[]
    def record(self, action, case_id=None, actor='local', metadata=None):
        event={'timestamp':datetime.now().isoformat(timespec='seconds'),'action':action,'case_id':case_id,'actor':actor,'metadata':metadata or {}}
        self.events.append(event)
        return event
    def list(self, case_id=None):
        return [e for e in self.events if case_id is None or e.get('case_id') == case_id]
