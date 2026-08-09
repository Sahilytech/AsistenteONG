PROVINCES = ['Buenos Aires','Catamarca','Chaco','Chubut','Córdoba','Corrientes','Entre Ríos','Formosa','Jujuy','La Pampa','La Rioja','Mendoza','Misiones','Neuquén','Río Negro','Salta','San Juan','San Luis','Santa Cruz','Santa Fe','Santiago del Estero','Tierra del Fuego','Tucumán','Ciudad Autónoma de Buenos Aires']

def jurisdiction(province='', locality=''):
    return {'country':'Argentina','province':province or '','locality':locality or ''}

def is_province(value):
    return str(value or '').strip().casefold() in {p.casefold() for p in PROVINCES}
