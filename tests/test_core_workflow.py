from src.core.case_workflow import can_transition, transition
from src.core.knowledge_store import KnowledgeStore
from src.core.audit_log import AuditLog

def test_workflow():
    assert can_transition('borrador','abierto')
    assert not can_transition('borrador','cerrado')
    case=transition({'status':'borrador'},'abierto')
    assert case['status']=='abierto'

def test_knowledge_search():
    store=KnowledgeStore()
    store.add('Recurso laboral','orientación laboral','oficial','CABA','laboral')
    assert store.search('laboral')[0]['title']=='Recurso laboral'

def test_audit():
    log=AuditLog(); event=log.record('case_created','CASE-1')
    assert event['action']=='case_created'
    assert len(log.list('CASE-1'))==1
