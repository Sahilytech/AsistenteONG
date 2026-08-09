"""Catálogo local de recursos. Diseñado para crecer con fuentes oficiales verificadas."""
from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass
class Resource:
    name: str
    category: str
    jurisdiction: str = "Nacional"
    organization: str = ""
    phone: str = ""
    website: str = ""
    address: str = ""
    hours: str = ""
    requirements: str = ""
    source: str = ""
    updated_at: str = ""
    verified: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)


class ResourceCatalog:
    def __init__(self):
        self._resources: List[Resource] = []

    def add(self, resource: Resource) -> None:
        self._resources.append(resource)

    def search(self, category: str = "", jurisdiction: str = "", query: str = "") -> List[Resource]:
        terms = [x.lower() for x in query.split() if x.strip()]
        result = []
        for item in self._resources:
            haystack = " ".join([item.name, item.category, item.organization, item.jurisdiction]).lower()
            if category and category.lower() not in item.category.lower():
                continue
            if jurisdiction and jurisdiction.lower() not in item.jurisdiction.lower():
                continue
            if terms and not all(term in haystack for term in terms):
                continue
            result.append(item)
        return result
