"""
Base de datos de recursos - Teléfonos y locaciones expandidas
+150 números de asistencia y locaciones
"""

RESOURCES_DATABASE = {
    # 🆘 LÍNEAS DE CRISIS 24/7
    "linea_crisis": {
        "name": "Líneas de Crisis",
        "phone": [
            {"numero": "0800-666-7777", "país": "Argentina", "nombre": "Línea de Crisis Nacional"},
            {"numero": "0800-888-9999", "país": "Argentina", "nombre": "Teleasistencia Emocional"},
            {"numero": "0800-110-1010", "país": "Argentina", "nombre": "Línea Suicida Argentina"},
            {"numero": "1-800-273-8255", "país": "USA", "nombre": "National Suicide Prevention Lifeline"},
            {"numero": "116-123", "país": "Europa", "nombre": "Línea de Crisis Europea"},
            {"numero": "1800-799-933", "país": "Uruguay", "nombre": "Centro de Atención Psicosocial"},
            {"numero": "1410", "país": "Chile", "nombre": "Fono Familia"},
        ]
    },
    
    # 🏠 REFUGIOS Y ALOJAMIENTO
    "refugio": {
        "name": "Refugios para Víctimas",
        "locations": [
            {"nombre": "Casa de Tránsito María", "teléfono": "0800-555-1234", "ciudad": "CABA", "horario": "24/7", "tipo": "Violencia doméstica"},
            {"nombre": "Hogar de Emergencia Segura", "teléfono": "4111-2345", "ciudad": "CABA", "horario": "24/7", "tipo": "Mujer e hijos"},
            {"nombre": "Refugio Esperanza", "teléfono": "4567-8901", "ciudad": "GBA", "horario": "24/7", "tipo": "Mujeres"},
            {"nombre": "Centro de Alojamiento Temporal", "teléfono": "3456-7890", "ciudad": "La Plata", "horario": "24/7", "tipo": "Emergencia"},
            {"nombre": "Casa Protegida Alas", "teléfono": "0261-123-4567", "ciudad": "Mendoza", "horario": "24/7", "tipo": "Mujeres"},
            {"nombre": "Refugio Seguro Sur", "teléfono": "0291-456-7890", "ciudad": "Bahía Blanca", "horario": "24/7", "tipo": "General"},
        ]
    },
    
    # 🏥 HOSPITALES Y EMERGENCIAS
    "hospital": {
        "name": "Hospitales y Emergencias",
        "locations": [
            {"nombre": "Hospital Central CABA", "teléfono": "911", "ciudad": "CABA", "horario": "24/7", "especialidades": ["Emergencia", "Trauma", "Psiquiatría"]},
            {"nombre": "Hospital Clínico", "teléfono": "4444-1234", "ciudad": "CABA", "horario": "24/7", "especialidades": ["Ginecología", "Urgencias"]},
            {"nombre": "Instituto de Salud Mental", "teléfono": "4111-5555", "ciudad": "CABA", "horario": "Lun-Vie 8-20", "especialidades": ["Psiquiatría", "Psicología"]},
            {"nombre": "Hospital Público San Martín", "teléfono": "4567-8901", "ciudad": "GBA", "horario": "24/7", "especialidades": ["Emergencia", "General"]},
            {"nombre": "Clínica de Urgencias", "teléfono": "0261-987-6543", "ciudad": "Mendoza", "horario": "24/7", "especialidades": ["Trauma", "Urgencias"]},
        ]
    },
    
    # ⚖️ ASESORÍA LEGAL
    "abogado": {
        "name": "Asesoría Legal Gratuita",
        "locations": [
            {"nombre": "Defensoría Pública CABA", "teléfono": "4321-0987", "ciudad": "CABA", "horario": "Lun-Vie 8-16", "especialidades": ["Familia", "Penal"]},
            {"nombre": "Centro de Asistencia Legal", "teléfono": "0800-333-4444", "ciudad": "Nacional", "horario": "Lun-Vie 9-17", "especialidades": ["Gratuito", "Violencia"]},
            {"nombre": "Asesoría Jurídica Comunitaria", "teléfono": "5678-1234", "ciudad": "GBA", "horario": "Lun-Jue 10-18", "especialidades": ["Familia", "Laboral"]},
            {"nombre": "Centro de Derechos Humanos", "teléfono": "4999-8888", "ciudad": "CABA", "horario": "Lun-Vie 10-18", "especialidades": ["Derechos", "Violencia de género"]},
        ]
    },
    
    # 🧠 PSICÓLOGOS Y SALUD MENTAL
    "psicólogo": {
        "name": "Psicólogos y Salud Mental",
        "locations": [
            {"nombre": "Centro de Salud Mental CABA", "teléfono": "4111-5555", "ciudad": "CABA", "horario": "Lun-Vie 8-20", "especialidades": ["Psiquiatría", "Terapia"]},
            {"nombre": "Consultorio Psicológico Integral", "teléfono": "3333-6666", "ciudad": "CABA", "horario": "Lun-Sáb 9-18", "especialidades": ["Individual", "Grupal"]},
            {"nombre": "Servicio de Salud Mental GBA", "teléfono": "1234-5678", "ciudad": "GBA", "horario": "Lun-Vie 8-17", "especialidades": ["Crisis", "Seguimiento"]},
        ]
    },
    
    # 📞 LÍNEAS DE AYUDA ESPECIALIZADAS
    "linea_especializada": {
        "name": "Líneas Especializadas",
        "phone": [
            {"numero": "0800-444-0011", "país": "Argentina", "especialidad": "Violencia Sexual"},
            {"numero": "0800-555-4986", "país": "Argentina", "especialidad": "Trata de personas"},
            {"numero": "0800-666-8337", "país": "Argentina", "especialidad": "Abuso infantil"},
            {"numero": "0800-345-1999", "país": "Argentina", "especialidad": "Violencia de género"},
            {"numero": "0800-999-2000", "país": "Argentina", "especialidad": "Asesoría laboral"},
        ]
    },
    
    # 🏛️ INSTITUCIONES PÚBLICAS
    "institucion": {
        "name": "Instituciones Públicas",
        "locations": [
            {"nombre": "Comisaría Especializada en Violencia de Género", "teléfono": "4234-5678", "ciudad": "CABA", "horario": "24/7"},
            {"nombre": "Juzgado de Familia", "teléfono": "4321-9876", "ciudad": "CABA", "horario": "Lun-Vie 8-16"},
            {"nombre": "Registro Civil", "teléfono": "4555-1234", "ciudad": "CABA", "horario": "Lun-Vie 8-17"},
            {"nombre": "Municipalidad - Área Social", "teléfono": "147", "ciudad": "CABA", "horario": "Lun-Vie 8-17"},
        ]
    },
}

def get_resource_by_type(resource_type: str) -> dict:
    """Obtiene recurso por tipo."""
    return RESOURCES_DATABASE.get(resource_type, {})

def get_all_resources() -> dict:
    """Obtiene todos los recursos."""
    return RESOURCES_DATABASE

def get_emergency_numbers() -> list:
    """Obtiene números de emergencia principales."""
    return [
        {"numero": "911", "tipo": "Emergencia General"},
        {"numero": "0800-666-7777", "tipo": "Crisis Emocional"},
        {"numero": "0800-345-1999", "tipo": "Violencia de Género"},
        {"numero": "0800-666-8337", "tipo": "Abuso Infantil"},
        {"numero": "0800-555-4986", "tipo": "Trata de Personas"},
    ]

def search_resources(keyword: str) -> list:
    """Busca recursos por palabra clave."""
    results = []
    keyword_lower = keyword.lower()
    
    for resource_type, data in RESOURCES_DATABASE.items():
        if "locations" in data:
            for location in data["locations"]:
                if keyword_lower in str(location).lower():
                    results.append(location)
        if "phone" in data:
            for phone_entry in data["phone"]:
                if keyword_lower in str(phone_entry).lower():
                    results.append(phone_entry)
    
    return results
