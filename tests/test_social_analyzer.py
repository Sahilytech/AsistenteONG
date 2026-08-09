from src.social_analyzer import SocialReportAnalyzer


def test_social_report_detects_missing_fields_and_risk():
    result = SocialReportAnalyzer().analyze({
        "entidad_emisora": "ONG",
        "profesional": "Profesional",
        "destinatario": "Juzgado",
        "motivo": "Medida de protección",
        "nombre_completo": "Persona de referencia",
        "documento": "DNI",
        "miembros_hogar": "Persona adulta\nNiña de 10 años",
        "ingresos": "ARS 200000",
        "situacion_laboral": "Desempleo",
        "egresos": "ARS 250000",
        "tenencia": "Alquiler",
        "condiciones_vivienda": "2 habitaciones; hacinamiento",
        "servicios_entorno": "Sin agua estable",
        "salud": "Tratamiento en curso",
        "educacion": "La niña no asiste a la escuela",
        "fecha_nacimiento": "1990-01-01",
        "edad": "36",
        "diagnostico": "Valoración pendiente",
        "propuesta": "Solicitar recurso",
    })
    assert result["completeness"] < 100
    assert "niñez o adolescencia" in result["risk_indicators"]
    assert result["balance"] == -50000
    assert result["persons_per_room"] == 1.0
    assert result["consistency_flags"]


def test_social_report_calculates_age():
    result = SocialReportAnalyzer().analyze({"fecha_nacimiento": "2000-01-01", "edad": "26"})
    assert result["derived"]["edad_calculada"] >= 26
