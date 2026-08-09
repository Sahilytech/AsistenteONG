"""Utilidades de minimización para vistas y capacitación."""

def redact_personal(data):
    if not isinstance(data, dict): return data
    hidden={'name','full_name','dni','document','phone','email','address'}
    return {k: ('[OCULTO]' if k in hidden and v else v) for k,v in data.items()}
