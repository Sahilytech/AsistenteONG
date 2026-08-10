"""Analizador local y explicable de informes sociales.

No diagnostica ni toma decisiones profesionales. Resume datos cargados,
calcula indicadores simples y señala campos que requieren revisión humana.
"""
import re
from datetime import date, datetime


class SocialReportAnalyzer:
    REQUIRED = {
        "entidad_emisora": "Entidad emisora", "profesional": "Profesional de referencia",
        "destinatario": "Destinatario", "motivo": "Motivo", "nombre_completo": "Nombre completo",
        "documento": "Documento", "fecha_nacimiento": "Fecha de nacimiento", "miembros_hogar": "Miembros del hogar",
        "ingresos": "Ingresos", "situacion_laboral": "Situación laboral", "egresos": "Egresos básicos",
        "tenencia": "Régimen de tenencia", "condiciones_vivienda": "Condiciones de vivienda",
        "servicios_entorno": "Servicios y entorno", "salud": "Situación sanitaria", "educacion": "Educación",
        "diagnostico": "Valoración social / juicio técnico", "propuesta": "Propuesta de intervención",
    }
    RISK_PATTERNS = {
        "riesgo de vida o emergencia": [r"peligro actual", r"emergencia", r"no respira", r"inconsciente", r"amenaza de muerte"],
        "violencia": [r"golpe", r"agresi", r"violencia", r"amenaz", r"abuso", r"hostigamiento", r"acoso"],
        "violencia sexual": [r"violaci", r"abuso sexual", r"tocamiento", r"sin consentimiento"],
        "niñez o adolescencia": [r"menor", r"niñ", r"niña", r"niño", r"adolesc"],
        "dependencia o discapacidad": [r"dependencia", r"discapacidad", r"cuidador", r"cuidados permanentes"],
        "precariedad económica": [r"sin ingresos", r"desemple", r"sin trabajo", r"pobreza", r"deuda", r"sin comida", r"no puede pagar"],
        "precariedad habitacional": [r"sin vivienda", r"calle", r"desalojo", r"hacinamiento", r"vivienda precaria", r"sin agua", r"sin electricidad"],
        "barrera educativa": [r"abandono escolar", r"no asiste", r"deserción", r"desercion", r"sin escolariz"],
        "salud": [r"enfermedad crónica", r"enfermedad cronica", r"tratamiento", r"medicación", r"medicacion", r"adicción", r"adiccion"],
    }

    def analyze(self, data):
        data = data or {}
        text = " ".join(str(data.get(k, "")) for k in data).lower()
        missing = [label for key, label in self.REQUIRED.items() if not str(data.get(key, "")).strip()]
        indicators = [label for label, patterns in self.RISK_PATTERNS.items() if any(re.search(p, text) for p in patterns)]
        household = self._household_count(data.get("miembros_hogar", ""))
        rooms = self._first_number(data.get("condiciones_vivienda", ""), r"(?:habitaciones?|ambientes?)\s*[:=]?\s*(\d+)")
        overcrowding = round(household / rooms, 2) if household and rooms else None
        income = self._money_total(data.get("ingresos", "")); expenses = self._money_total(data.get("egresos", ""))
        balance = None if income is None or expenses is None else round(income - expenses, 2)
        derived = {}
        birth = self._parse_date(data.get("fecha_nacimiento", ""))
        if birth:
            today = date.today(); derived["edad_calculada"] = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        consistency = []
        stated_age = self._first_number(data.get("edad", ""), r"(\d{1,3})")
        if stated_age and derived.get("edad_calculada") and abs(stated_age - derived["edad_calculada"]) > 1:
            consistency.append("La edad declarada no coincide con la edad calculada a partir de la fecha de nacimiento.")
        if balance is not None and balance < 0: consistency.append("Los egresos declarados superan los ingresos declarados.")
        if overcrowding is not None and overcrowding > 2: consistency.append("La relación declarada entre convivientes y habitaciones requiere revisión por posible hacinamiento.")
        level = "Revisión prioritaria" if indicators else ("Información incompleta" if missing else "Sin indicadores automáticos destacados")
        return {
            "level": level, "completeness": round(100 * (len(self.REQUIRED) - len(missing)) / len(self.REQUIRED)),
            "missing_fields": missing, "risk_indicators": indicators, "strengths": self._strengths(data),
            "household_members": household, "rooms": rooms, "persons_per_room": overcrowding,
            "income_total": income, "expenses_total": expenses, "balance": balance, "derived": derived,
            "consistency_flags": consistency, "recommendations": self._recommendations(indicators, missing, consistency),
            "disclaimer": "Análisis orientativo generado por reglas locales. No es diagnóstico, peritaje ni decisión profesional; debe ser revisado por el/la profesional responsable.",
        }

    def _recommendations(self, indicators, missing, consistency):
        out=[]
        if missing: out.append("Completar los campos faltantes antes de emitir el informe.")
        if indicators: out.append("Revisar manualmente los indicadores detectados y confirmar contexto, temporalidad y nivel de riesgo.")
        if "precariedad económica" in indicators: out.append("Verificar ingresos, prestaciones disponibles, gastos esenciales y recursos de apoyo económico.")
        if "precariedad habitacional" in indicators: out.append("Verificar condiciones de habitabilidad, servicios básicos y alternativas habitacionales.")
        if "niñez o adolescencia" in indicators: out.append("Revisar necesidades de protección y situación educativa de niños, niñas o adolescentes involucrados.")
        if "violencia" in indicators or "violencia sexual" in indicators: out.append("Priorizar una entrevista segura y valorar necesidades de protección, acompañamiento y derivación especializada.")
        if consistency: out.append("Resolver las inconsistencias señaladas antes de cerrar el informe.")
        return out or ["Mantener revisión profesional y actualizar el informe si cambia la situación social."]

    def _strengths(self, data):
        text=" ".join(str(data.get(k,"")) for k in ("dinamica_familiar","fortalezas","situacion_laboral","educacion","servicios_entorno")).lower();labels=[]
        for term,label in [("apoyo","Red de apoyo declarada"),("estable","Elemento de estabilidad"),("empleo","Inserción laboral"),("trabajo","Actividad laboral"),("escolar","Vinculación educativa"),("agua","Acceso a servicios básicos")]:
            if term in text and label not in labels: labels.append(label)
        return labels

    @staticmethod
    def _first_number(value, pattern=r"(\d+(?:[.,]\d+)?)"):
        m=re.search(pattern,str(value or ""),re.I)
        if not m:return None
        try:return float(m.group(1).replace(",","."))
        except ValueError:return None
    @staticmethod
    def _household_count(value):
        lines=[x for x in str(value or "").splitlines() if x.strip()]
        if len(lines)>1:return len(lines)
        m=re.search(r"(?:personas?|miembros?)\s*[:=]\s*(\d+)",str(value or ""),re.I)
        return int(m.group(1)) if m else None
    @staticmethod
    def _money_total(value):
        matches=re.findall(r"(?:\$|ars\s*)\s*([0-9][0-9.]*)(?:,([0-9]{1,2}))?",str(value or ""),re.I)
        if not matches:return None
        total=0.0
        for whole,cents in matches:
            try:total+=float(whole.replace(".","")+("."+cents if cents else ""))
            except ValueError:pass
        return round(total,2)
    @staticmethod
    def _parse_date(value):
        raw=str(value or "").strip()
        for fmt in ("%Y-%m-%d","%d/%m/%Y"):
            try:return datetime.strptime(raw,fmt).date()
            except ValueError:continue
        return None
