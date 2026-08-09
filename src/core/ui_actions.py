"""Catálogo semántico de acciones de UI para evitar botones sin propósito."""
ACTIONS = {
    'new_case': 'Crear un expediente nuevo',
    'open_case': 'Abrir y revisar un expediente existente',
    'save_report': 'Guardar cambios del informe social',
    'analyze_case': 'Analizar el relato y el informe conjuntamente',
    'add_followup': 'Programar una acción de seguimiento',
    'add_referral': 'Registrar una derivación',
    'search_resources': 'Buscar recursos disponibles y verificar su fuente',
    'save_document': 'Guardar un documento en la biblioteca local',
    'export_report': 'Generar una copia del informe para revisión',
    'privacy_view': 'Ocultar datos personales en la vista actual',
}

def explain(action):
    return ACTIONS.get(action, 'Acción no documentada')
