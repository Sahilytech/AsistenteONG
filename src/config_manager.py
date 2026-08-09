"""Motor local de triaje contextual, explicable y conservador.

No interpreta una palabra aislada como una emergencia. Distingue indicadores,
contexto y temas de consulta, usa frases completas y aplica reglas de negación.
"""
import logging,re,unicodedata
logger=logging.getLogger(__name__)

class ConfigManager:
    RISK_PHRASES={
      "Riesgo de Vida":["suicidio","suicida","matarme","matarse","arma","veneno","sobredosis","asfixia","apuñalar","disparar","inconsciente","no respira","no responde","paro cardíaco","paro cardiaco"],
      "Gravedad Física":["fractura","sangrado abundante","trauma severo","hospitalización","hospitalizacion","herida profunda","quemadura grave","quemaduras graves","quemadura extensa","muy grave","coma","apaleado","golpe muy fuerte"],
      "Violencia de Género":["golpeó","golpeo","amenazó","amenazo","controla","dominio","acoso","hostigamiento","discriminación","discriminacion","machista","violencia de género","violencia de genero","por ser mujer","la atacó","la ataco","la agredió","la agredio","violencia física","violencia fisica","violencia psicológica","violencia psicologica"],
      "Violencia Sexual":["violación","violacion","abuso sexual","tocamientos","forzado","sin consentimiento","violada","violado","acoso sexual","acto sexual"],
      "Salud Mental":["depresión","depresion","ansiedad","pánico","panico","autolesión","autolesion","adicción","adiccion","droga","alcohol","consumo problemático","consumo problematico","trastorno","psicosis"],
      "Necesidad Inmediata":["urgente","emergencia","sos","rápido","rapido","inmediato","ahora mismo"],
      "Laboral / Empleo":["despido","me despidieron","despidieron","despido injustificado","no me pagan","salario adeudado","sueldo adeudado","acoso laboral","maltrato laboral","trabajo en negro","empleo en negro","contrato laboral","contrato de trabajo","indemnización","indemnizacion","liquidación final","liquidacion final","horas extra no pagadas","problema con mi empleador"],
      "Orientación Legal":["abogado","demanda","custodia","divorcio","derechos legales","juicio","proceso legal","asesoría jurídica","asesoria juridica","justicia","tribunal","denuncia formal","denunciar formalmente","medida cautelar","orden judicial","carta documento"],
      "Recursos / Necesidades":["refugio","dinero","comida","vivienda","medicinas","alojamiento","asistencia","auxilio","alimento","hospedaje","sin hogar"],
      "Salud / Accidente":["quemadura","quemaduras","estufa","accidente","caída","caida","golpe","dolor","fiebre","herida","lesión","lesion","mareo","vómito","vomito","sangre","hospital","ambulancia"]
    }
    CONTEXT_KEYWORDS={
      "Relaciones y familia":["hijo","hija","niño","niña","bebe","bebé","madre","padre","mamá","mama","papá","papa","pareja","marido","esposo","novia","novio","ex pareja","expareja","familia"],
      "Relación laboral":["jefe","jefa","supervisor","supervisora","empleador","empleadora","patrón","patron","compañero de trabajo","compañera de trabajo","trabajo","empleo"],
      "Personas menores":["niño","niña","menor","adolescente","bebé","bebe","hijo","hija"],
      "Género y vínculo":["pareja","marido","esposo","novia","novio","ex pareja","expareja","por ser mujer"]
    }
    CRITICAL=["no respira","no responde","inconsciente","paro cardíaco","paro cardiaco"]
    SEVERE=["fractura","sangrado abundante","quemadura grave","quemaduras graves","quemadura extensa","muy grave","hospitalización","hospitalizacion","trauma severo"]
    LEGAL_STRONG=["abogado","demanda","juicio","proceso legal","asesoría jurídica","asesoria juridica","tribunal","medida cautelar","orden judicial","carta documento"]
    def __init__(self): logger.info("ConfigManager inicializado")
    @staticmethod
    def _norm(text):
        text=unicodedata.normalize("NFKC",text or "").lower().replace("’","'")
        return re.sub(r"\s+"," ",text.strip())
    @staticmethod
    def _phrase_regex(phrase):
        escaped=re.escape(phrase.lower().strip()).replace(r"\ ",r"\s+")
        return re.compile(r"(?<![\wáéíóúüñ])"+escaped+r"(?![\wáéíóúüñ])",re.IGNORECASE)
    def _is_negated(self,text,start):
        before=text[max(0,start-45):start]
        return bool(re.search(r"(?:\bno\b|\bsin\b|\bnunca\b|\bjamas\b|\bjamás\b)\s+(?:\w+\s+){0,3}$",before))
    def _found(self,text,phrases):
        found=[]
        for phrase in phrases:
            for match in self._phrase_regex(phrase).finditer(text):
                if not self._is_negated(text,match.start()): found.append(phrase); break
        return found
    def _context_found(self,text):
        result=[]
        for _,phrases in self.CONTEXT_KEYWORDS.items(): result.extend(self._found(text,phrases))
        return list(dict.fromkeys(result))
    def analyze(self,text,social_report=None):
        original=(text or "").strip(); report=social_report or {}; combined=self._norm(original+" "+self._report_text(report)); scores={}; risk_hits=[]
        for category,phrases in self.RISK_PHRASES.items():
            hits=self._found(combined,phrases)
            if hits: scores[category]=len(hits); risk_hits.extend(hits)
        context_hits=self._context_found(combined)
        life=bool(self._found(combined,self.CRITICAL)); severe=bool(self._found(combined,self.SEVERE)); sexual="Violencia Sexual" in scores; gender="Violencia de Género" in scores; health="Salud / Accidente" in scores
        labor="Laboral / Empleo" in scores
        legal_strong=bool(self._found(combined,self.LEGAL_STRONG)) or "Orientación Legal" in scores
        minor=bool(self._found(combined,["abuso infantil","maltrato infantil","explotación infantil","explotacion infantil"])) or (bool(self._found(combined,["menor","niño","niña","bebé","bebe","hijo","hija"])) and bool(self._found(combined,["abuso","maltrato","golpe","quemadura","accidente","lesión","lesion","amenaza","violencia"])))
        if minor:scores["Personas menores"]=scores.get("Personas menores",0)+1
        urgency=self._determine(scores,life,severe,sexual,gender,health,minor)
        if health: classification="Salud / accidente"
        elif gender: classification="Violencia de género"
        elif sexual: classification="Violencia sexual"
        elif labor: classification="Situación laboral"
        elif legal_strong: classification="Orientación legal"
        elif life: classification="Posible emergencia"
        else: classification="Consulta social"
        keywords=list(dict.fromkeys(risk_hits+context_hits))
        return {"urgency":urgency,"keywords":keywords[:24],"risk_keywords":list(dict.fromkeys(risk_hits))[:20],"context_keywords":context_hits[:16],"response":self._response(urgency,gender,legal_strong,health,labor,minor),"suggested_resources":self._resources(scores,gender,legal_strong,health,labor,minor),"scores":scores,"classification":classification,"confidence":self._confidence(scores,life,severe,gender,health,labor),"detected_context":self._context(scores,life,severe,gender,health,labor,minor),"priority_reason":self._priority_reason(urgency,scores,life,severe,gender,health,labor,minor),"next_questions":self._questions(urgency,gender,health,labor,minor),"combined_with_social_report":bool(report),"context_note":"Análisis local explicable. Contexto y palabras generales no elevan por sí solos la urgencia. Se priorizan indicadores concretos, relaciones entre señales y el relato completo. Revisar siempre el resultado con criterio profesional."}
    def _report_text(self,report):
        if not report:return ""
        keys=["nombre_completo","motivo","miembros_hogar","historia_familiar","dinamica_familiar","ingresos","situacion_laboral","egresos","tenencia","condiciones_vivienda","servicios_entorno","salud","educacion","diagnostico","fortalezas","vulnerabilidades","propuesta","observaciones"]
        return " ".join(str(report.get(k,"")) for k in keys if report.get(k))
    def _determine(self,s,life,severe,sexual,gender,health,minor):
        if life:return "Muy Alta"
        if severe or sexual:return "Alta"
        if health or gender or minor:return "Media"
        if "Necesidad Inmediata" in s:return "Media"
        return "Baja"
    def _priority_reason(self,u,s,life,severe,gender,health,labor,minor):
        if life:return "Se detectaron señales compatibles con una posible emergencia vital. La situación debe verificarse de inmediato por una persona profesional."
        if severe:return "Se detectaron señales compatibles con posible gravedad física. Hace falta confirmar el estado actual y seguir el protocolo correspondiente."
        if health:return "Hay indicadores de salud o accidente. La prioridad se mantiene orientativa porque la gravedad depende de síntomas, evolución y contexto."
        if gender:return "Hay indicadores concretos vinculados con violencia o una relación de poder. Conviene revisar seguridad, contexto y necesidades de protección."
        if minor:return "Hay una posible situación de riesgo que involucra a una persona menor. Ampliar información y aplicar el protocolo de protección correspondiente."
        if labor:return "Se identificó una situación relacionada con empleo o condiciones laborales. La prioridad no aumenta por mencionar trabajo o despido; conviene precisar hechos, fechas y documentación disponible."
        if "Necesidad Inmediata" in s:return "La persona expresa necesidad de atención pronta, pero el relato no aporta por sí solo un indicador concreto de gravedad. Ampliar información."
        return "No aparecen indicadores suficientes para elevar la prioridad con las reglas actuales. Esto no significa que el caso sea leve; revisar el relato completo."
    def _context(self,s,life,severe,gender,health,labor,minor):
        if life:return "Posible emergencia"
        if severe:return "Posible gravedad física"
        if health:return "Salud / accidente"
        if gender:return "Violencia de género / relación de poder"
        if labor:return "Situación laboral / empleo"
        if minor:return "Situación que involucra a una persona menor"
        return "Consulta general"
    def _confidence(self,s,life,severe,gender,health,labor):
        if life or severe:return "Alta"
        if sum(s.values())>=2 or gender or health or labor:return "Media"
        return "Baja"
    def _questions(self,u,g,health,labor,minor):
        if health:return ["¿Qué ocurrió y cuándo?","¿Qué síntomas o lesiones presenta actualmente?","¿La situación está estable o empeora?","¿Recibió atención profesional?","¿Hay algún indicador de gravedad que deba verificarse?"]
        if g:return ["¿Qué ocurrió y cuándo?","¿Quién ejerció la conducta y qué relación tiene con la persona?","¿Existe una relación de poder o dependencia?","¿La persona está a salvo ahora?","¿Qué apoyo necesita actualmente?"]
        if minor:return ["¿Qué ocurrió y cuándo?","¿La persona menor está a salvo ahora?","¿Quién está a cargo de sus cuidados?","¿Existe un riesgo actual?","¿Qué apoyo o intervención necesita?"]
        if labor:return ["¿Qué ocurrió y cuándo?","¿La relación laboral sigue vigente?","¿Qué decisión o conducta del empleador se produjo?","¿Existen contrato, recibos, comunicaciones u otra documentación?","¿Qué necesita la persona: información, orientación o derivación especializada?"]
        if u in ("Muy Alta","Alta"):return ["¿Existe peligro actual?","¿La persona está a salvo ahora?","¿Hay lesiones o una necesidad inmediata?","¿Dónde se encuentra la persona?"]
        return ["¿Qué ocurrió y cuándo?","¿Qué necesita la persona ahora?","¿Qué información falta para comprender la situación?","¿Hay algún riesgo o restricción que no figure en el relato?"]
    def _response(self,u,g,l,health,labor,minor):
        if health:return "SALUD / ACCIDENTE\n\nSe identificaron señales relacionadas con salud o un accidente. No es posible determinar la gravedad únicamente con palabras clave. Ampliar síntomas, evolución y atención recibida antes de decidir una derivación."
        if g:return "VIOLENCIA DE GÉNERO / RELACIÓN DE PODER\n\nSe identificaron indicadores concretos que justifican revisar seguridad, contexto y posibles relaciones de poder. Documentar el relato y seguir el protocolo profesional correspondiente."
        if minor:return "SITUACIÓN CON PERSONA MENOR\n\nSe identificaron referencias a una persona menor junto con un indicador de riesgo. Ampliar información y aplicar el protocolo de protección que corresponda."
        if labor:return "SITUACIÓN LABORAL\n\nEl relato contiene información relacionada con empleo o condiciones laborales. No se presume una infracción jurídica solo por mencionar un despido o un trabajo. Conviene precisar hechos, fechas, relación laboral y documentación antes de derivar."
        if l:return "ORIENTACIÓN LEGAL\n\nSe identificaron indicadores que sí justifican considerar orientación jurídica. Ampliar el relato, precisar el problema y revisar la normativa o protocolo aplicable antes de derivar."
        if u=="Muy Alta":return "POSIBLE EMERGENCIA\n\nSe detectaron indicadores compatibles con una situación que podría requerir atención inmediata. Confirmar la situación con una persona profesional."
        if u=="Alta":return "SITUACIÓN PRIORITARIA\n\nSe detectaron indicadores que justifican una valoración profesional prioritaria. Confirmar gravedad, seguridad y necesidades actuales."
        if u=="Media":return "SEGUIMIENTO PRIORITARIO\n\nHay señales que justifican ampliar información y definir el recurso adecuado. La prioridad es orientativa."
        return "ORIENTACIÓN INICIAL\n\nNo se detectaron indicadores suficientes para elevar la prioridad. El resultado no descarta una necesidad: completar información y revisar el contexto."
    def _resources(self,s,g,l,health,labor,minor):
        r=[]
        if health:r += ["orientación sanitaria","servicio de salud / emergencia local según gravedad"]
        if g:r += ["orientación especializada en violencia de género","acompañamiento","asesoría jurídica si corresponde"]
        if "Riesgo de Vida" in s:r += ["servicio de emergencias local","protocolo de crisis"]
        if minor:r += ["servicio local de protección de niñez"]
        if labor:r += ["orientación laboral","asesoría jurídica laboral si corresponde"]
        elif l:r += ["asesoría jurídica"]
        return list(dict.fromkeys(r))[:8]
