"""Memoria local SQLite-like desacoplada para documentos y fuentes."""
from datetime import datetime

class KnowledgeStore:
    def __init__(self, repository=None):
        self.repository = repository if repository is not None else []

    def add(self, title, content, source='', jurisdiction='', category='', verified_at=None):
        item={'id':len(self.repository)+1,'title':title,'content':content,'source':source,'jurisdiction':jurisdiction,'category':category,'verified_at':verified_at or datetime.now().isoformat(timespec='seconds')}
        self.repository.append(item)
        return item

    def search(self, query, jurisdiction=None, category=None):
        terms=[t.casefold() for t in str(query or '').split() if len(t)>2]
        results=[]
        for item in self.repository:
            if jurisdiction and item.get('jurisdiction') != jurisdiction: continue
            if category and item.get('category') != category: continue
            hay=' '.join(str(item.get(k,'')) for k in ('title','content','category','jurisdiction')).casefold()
            score=sum(hay.count(term) for term in terms)
            if score: results.append((score,item))
        return [item for _,item in sorted(results,key=lambda x:x[0],reverse=True)]
