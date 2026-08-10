"""Recursos nacionales verificables.

No se cargan nombres, teléfonos ni organizaciones ficticias. Los recursos sin
fuente oficial deben incorporarse desde el módulo de fuentes y quedar fechados.
"""

RESOURCES_DATABASE = {
    "emergencias": {"name":"Emergencias nacionales","source":"https://www.argentina.gob.ar/tema/emergencias","locations":[
        {"nombre":"Central de Emergencias Nacional","teléfono":"911","phone":"911","ciudad":"Argentina","horario":"24/7","tipo":"Policía y emergencias"},
        {"nombre":"Bomberos","teléfono":"100","phone":"100","ciudad":"Argentina","horario":"24/7","tipo":"Incendios y rescate"},
        {"nombre":"Defensa Civil","teléfono":"103","phone":"103","ciudad":"Argentina","horario":"24/7","tipo":"Emergencias y desastres"},
        {"nombre":"Emergencia ambiental","teléfono":"105","phone":"105","ciudad":"Argentina","horario":"24/7","tipo":"Emergencia ambiental"},
        {"nombre":"Emergencia náutica","teléfono":"106","phone":"106","ciudad":"Argentina","horario":"24/7","tipo":"Emergencia náutica"},
        {"nombre":"SAME","teléfono":"107","phone":"107","ciudad":"CABA y localidades de Provincia de Buenos Aires","horario":"24/7","tipo":"Emergencias médicas","jurisdiccion":"CABA/PBA"},
    ]},
    "violencia": {"name":"Violencia y protección","source":"https://www.argentina.gob.ar/tema/violenciayabuso","phone":[
        {"numero":"144","phone":"144","país":"Argentina","nombre":"Línea 144","especialidad":"Violencia y riesgo"},
        {"numero":"137","phone":"137","país":"Argentina","nombre":"Línea 137","especialidad":"Violencia familiar y sexual"},
    ]},
    "ninez": {"name":"Niñez y adolescencia","source":"https://www.argentina.gob.ar/node/481458","phone":[
        {"numero":"102","phone":"102","país":"Argentina","nombre":"Línea 102","especialidad":"Derechos de niñas, niños y adolescentes"},
    ]},
    "trata": {"name":"Trata y explotación","source":"https://www.argentina.gob.ar/justicia/politicacriminal/trata-de-personas/linea-nacional-gratuita-y-anonima-145","phone":[
        {"numero":"145","phone":"145","país":"Argentina","nombre":"Línea 145","especialidad":"Trata y explotación de personas"},
    ]},
}

def get_resource_by_type(resource_type: str) -> dict: return RESOURCES_DATABASE.get(resource_type,{})
def get_all_resources() -> dict: return RESOURCES_DATABASE

def get_emergency_numbers() -> list:
    return [{"numero":n,"tipo":t,"fuente":s} for n,t,s in [
        ("911","Emergencia general",RESOURCES_DATABASE["emergencias"]["source"]),("100","Bomberos",RESOURCES_DATABASE["emergencias"]["source"]),("103","Defensa Civil",RESOURCES_DATABASE["emergencias"]["source"]),("144","Violencia y riesgo",RESOURCES_DATABASE["violencia"]["source"]),("137","Violencia familiar y sexual",RESOURCES_DATABASE["violencia"]["source"]),("102","Niñez y adolescencia",RESOURCES_DATABASE["ninez"]["source"]),("145","Trata y explotación",RESOURCES_DATABASE["trata"]["source"])]]

def search_resources(keyword: str) -> list:
    q=(keyword or "").casefold().strip()
    if not q:return []
    results=[]
    for key,data in RESOURCES_DATABASE.items():
        category=data.get("name",key);source=data.get("source","")
        for item in data.get("locations",[])+data.get("phone",[]):
            hay=" ".join(str(v) for v in item.values()).casefold()
            if q in hay or q in category.casefold(): results.append({**item,"categoria":category,"fuente":source})
    return results
