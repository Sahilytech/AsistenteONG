"""Modelo de genograma simple y portable para el perfil social."""

def create_genogram(members=None, relationships=None):
    return {
        "members": list(members or []),
        "relationships": list(relationships or []),
    }


def add_member(genogram, name, age=None, role="", occupation=""):
    item = {"id": f"member-{len(genogram.get('members', [])) + 1}", "name": name, "age": age, "role": role, "occupation": occupation}
    genogram.setdefault("members", []).append(item)
    return genogram


def add_relationship(genogram, source, target, relation, quality=""):
    genogram.setdefault("relationships", []).append({"source": source, "target": target, "relation": relation, "quality": quality})
    return genogram
