"""Registro de recursos con trazabilidad y jurisdicción."""

REQUIRED = ("name", "category", "jurisdiction", "source", "verified_at")


def validate_resource(resource):
    missing = [key for key in REQUIRED if not resource.get(key)]
    return {"valid": not missing, "missing": missing}


def register(resources, resource):
    check = validate_resource(resource)
    if not check["valid"]:
        raise ValueError("Recurso incompleto: " + ", ".join(check["missing"]))
    result = list(resources or [])
    result.append(dict(resource))
    return result


def find(resources, category=None, province=None, locality=None):
    result = []
    for item in resources or []:
        if category and item.get("category") != category: continue
        jurisdiction = item.get("jurisdiction") or {}
        if province and jurisdiction.get("province") != province: continue
        if locality and jurisdiction.get("locality") != locality: continue
        result.append(item)
    return result
