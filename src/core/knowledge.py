"""Memoria documental offline-first con fuentes trazables."""
from datetime import datetime

def document(title, content, source='', jurisdiction='', category='', version=''):
    return {'title':title,'content':content,'source':source,'jurisdiction':jurisdiction,'category':category,'version':version,'updated_at':datetime.now().isoformat(timespec='seconds')}

def search(documents, query):
    terms = [x.casefold() for x in str(query or '').split() if len(x) > 2]
    scored=[]
    for doc in documents or []:
        hay=' '.join(str(doc.get(k,'')) for k in ('title','content','category','jurisdiction')).casefold()
        score=sum(hay.count(t) for t in terms)
        if score: scored.append((score,doc))
    return [doc for _,doc in sorted(scored,key=lambda x:x[0],reverse=True)]
