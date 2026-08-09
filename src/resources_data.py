"""Recursos nacionales verificables.

No se cargan nombres, teléfonos ni organizaciones ficticias. Los recursos sin
fuente oficial deben incorporarse desde el módulo de fuentes y quedar fechados.
"""

RESOURCES_DATABASE = {
    "emergencias": {
        "name": "Emergencias nacionales",
        "source": "https://www.argentina.gob.ar/tema/emergencias",
        "locations": [
            {"nombre": "Central de Emergencias Nacional", "teléfono": "911", "ciudad": "Argentina", "horario": "24/7", "tipo": "Policía y emergencias"},
            {"nombre": "Bomberos", "teléfono": "100", "ciudad": "Argentina", "horario": "24/7", "tipo": "Incendios y rescate"},
            {"nombre": "Defensa Civil", "teléfono": "103", "ciudad": "Argentina", "horario": "24/7", "tipo": "Emergencias y desastres"},
            {"nombre": "Emergencia ambiental", "teléfono": "105", "ciudad": "Argentina", "horario": "24/7", "tipo": "Emergencia ambiental"},
            {"nombre": "Emergencia náutica", "teléfono": "106", "ciudad": "Argentina", "horario": "24/7", "tipo": "Emergencia náutica"},
            {"nombre": "SAME", "teléfono": "107", "ciudad": "CABA y localidades de Provincia de Buenos Aires", "horario": "24/7", "tipo": "Emergencias médicas", "jurisdiccion": "CABA/PBA"},
        ],
    },
    "violencia": {
        "name": "Violencia y protección",
        "source": "https://www.argentina.gob.ar/tema/violenciayabuso",
        "phone": [
            {"numero": "144", "país": "Argentina", "nombre": "Línea 144", "especialidad": "Violencia y riesgo"},
            {"numero": "137", "país": "Argentina", "nombre": "Línea 137", "especialidad": "Violencia familiar y sexual"},
        ],
    },
    "ninez": {
        "name": "Niñez y adolescencia",
        "source": "https://www.argentina.gob.ar/node/481458",
        "phone": [
            {"numero": "102", "país": "Argentina", "nombre": "Línea 102", "especialidad": "Derechos de niñas, niños y adolescentes"},
        ],
    },
    "trata": {
        "name": "Trata y explotación",
        "source": "https://www.argentina.gob.ar/justicia/politicacriminal/trata-de-personas/linea-nacional-gratuita-y-anonima-145",
        "phone": [
            {"numero": "145", "país": "Argentina", "nombre": "Línea 145", "especialidad": "Trata y explotación de personas"},
        ],
    },
}


def get_resource_by_type(resource_type: str) -> dict:
    return RESOURCES_DATABASE.get(resource_type, {})


def get_all_resources() -> dict:
    return RESOURCES_DATABASE


def get_emergency_numbers() -> list:
    return [
        {"numero": "911", "tipo": "Emergencia general", "fuente": RESOURCES_DATABASE["emergencias"]["source"]},
        {"numero": "100", "tipo": "Bomberos", "fuente": RESOURCES_DATABASE["emergencias"]["source"]},
        {"numero": "103", "tipo": "Defensa Civil", "fuente": RESOURCES_DATABASE["emergencias"]["source"]},
        {"numero": "144", "tipo": "Violencia y riesgo", "fuente": RESOURCES_DATABASE["violencia"]["source"]},
        {"numero": "137", "tipo": "Violencia familiar y sexual", "fuente": RESOURCES_DATABASE["violencia"]["source"]},
        {"numero": "102", "tipo": "Niñez y adolescencia", "fuente": RESOURCES_DATABASE["ninez"]["source"]},
        {"numero": "145", "tipo": "Trata y explotación", "fuente": RESOURCES_DATABASE["trata"]["source"]},
    ]


def search_resources(keyword: str) -> list:
    """Busca únicamente en el catálogo local de fuentes oficiales."""
    q = (keyword or "").casefold().strip()
    if not q:
        return []
    results = []
    for key, data in RESOURCES_DATABASE.items():
        category = data.get("name", key)
        source = data.get("source", "")
        for item in data.get("locations", []):
            hay = " ".join(str(v) for v in item.values()).casefold()
            if q in hay or q in category.casefold():
                results.append({**item, "categoria": category, "fuente": source})
        for item in data.get("phone", []):
            hay = " ".join(str(v) for v in item.values()).casefold()
            if q in hay or q in category.casefold():
                results.append({**item, "categoria": category, "fuente": source})
    return results
