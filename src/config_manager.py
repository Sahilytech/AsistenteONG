"""Motor de triaje local explicable y contextual.

Prioriza coincidencias de palabras completas y frases, evita falsos positivos por
subcadenas (por ejemplo, 'ex' dentro de 'extraño') y separa contexto de indicadores.
"""
import logging,re,unicodedata
logger=logging.getLogger(__name__)

class ConfigManager:
    RISK_PHRASES={
      "Riesgo de Vida":["suicidio","suicida","matarme","matarse","arma","veneno","sobredosis","asfixia","apuñalar","disparar","inconsciente","no respira","no responde","paro cardíaco","paro cardiaco"],
      "Violencia Severa":["fractura","sangrado abundante","trauma severo","hospitalización","hospitalizacion","herida profunda","quemadura grave","quemaduras graves","quemadura extensa","muy grave","coma","apaleado","molido"],
      "Violencia de Género":["golpeó","golpeo","amenaza","amenazó","amenazo","controla","control","dependencia","dominio","acoso","hostigamiento","discriminación","discriminacion","machista","violencia de género","violencia de genero","por ser mujer","la atacó","la ataco","la agredió","la agredio","violencia física","violencia fisica","violencia psicológica","violencia psicologica"],
      "Violencia Sexual":["violación","violacion","abuso sexual","tocamientos","forzado","sin consentimiento","violada","violado","acoso sexual","acto sexual"],
      "Salud Mental":["depresión","depresion","ansiedad","pánico","panico","autolesión","autolesion","adicción","adiccion","droga","alcohol","consumo problemático","consumo problematico","trastorno","psicosis"],
      "Necesidad Inmediata":["urgente","emergencia","sos","rápido","rapido","inmediato","prisa","ahora mismo"],
      "Asesoría Legal":["abogado","demanda","custodia","divorcio","derechos","juicio","proceso legal","ley","justicia","tribunal","denuncia","denunciar","despido","laboral","trabajo","horario laboral"],
      "Recursos":["refugio","dinero","trabajo","comida","vivienda","medicinas","alojamiento","asistencia","auxilio","alimento","hospedaje"],
      "Salud / Accidente":["quemadura","quemaduras","estufa","accidente","caída","caida","golpe","dolor","fiebre","herida","lesión","lesion","mareo","vómito","vomito","sangre","hospital","ambulancia"]
    }
    CONTEXT_KEYWORDS={
      "Relaciones y familia":["hijo","hija","niño","niña","bebe","bebé","madre","padre","mamá","mama","papá","papa","pareja","marido","esposo","novia","novio","ex pareja","expareja","familia"],
      "Relación laboral":["jefe","jefa","supervisor","supervisora","empleador","empleadora","patrón","patron","compañero de trabajo","compañera de trabajo"],
      "Personas menores":["niño","niña","menor","adolescente","bebé","bebe","hijo","hija"],
      "Género y vínculo":["pareja","marido","esposo","novia","novio","ex pareja","expareja","por ser mujer"]
    }
    CRITICAL=["no respira","no responde","inconsciente","paro cardíaco","paro cardiaco"]
    SEVERE=["fractura","sangrado abundante","quemadura grave","quemaduras graves","quemadura extensa","muy grave","hospitalización","hospitalizacion","trauma severo"]
    def __init__(self): logger.info("ConfigManager inicializado")
    @staticmethod
    def _norm(text):
        text=unicodedata.normalize("NFKC",text or "").lower()
        text=text.replace("’","'")
        return re.sub(r"\s+"," ",text.strip())
    @staticmethod
    def _phrase_regex(phrase):
        escaped=re.escape(phrase.lower().strip()).replace(r"\ ",r"\s+")
        return re.compile(r"(?<![\wáéíóúüñ])"+escaped+r"(?![\wáéíóúüñ])",re.IGNORECASE)
    def _is_negated(self,text,start):
        before=text[max(0,start-28):start]
        return bool(re.search(r"(?:\bno\b|\bsin\b|\bnunca\b|\bjamás\b|\bjamas\b)\s+(?:\w+\s+){0,2}$",before))
    def _found(self,text,phrases):
        found=[]
        for phrase in phrases:
            for match in self._phrase_regex(phrase).finditer(text):
                if not self._is_negated(text,match.start()):
                    found.append(phrase)
                    break
        return found
    def _context_found(self,text):
        result=[]
        for category,phrases in self.CONTEXT_KEYWORDS.items():
            hits=self._found(text,phrases)
            if hits: result.extend(hits)
        return list(dict.fromkeys(result))
    def analyze(self,text,social_report=None):
        original=(text or "").strip()
        report=social_report or {}
        report_text=self._report_text(report)
        combined=self._norm(original+" "+report_text)
        scores={}; risk_hits=[]; context_hits=[]
        for category,phrases in self.RISK_PHRASES.items():
            hits=self._found(combined,phrases)
            if hits: scores[category]=len(hits); risk_hits.extend(hits)
        context_hits=self._context_found(combined)
        life=bool(self._found(combined,self.CRITICAL)) or "Riesgo de Vida" in scores
        severe=bool(self._found(combined,self.SEVERE)) or "Violencia Severa" in scores
        sexual="Violencia Sexual" in scores
        gender="Violencia de Género" in scores
        legal="Asesoría Legal" in scores
        health="Salud / Accidente" in scores
        minor_context=bool(self._found(combined,["abuso infantil","maltrato infantil","explotación infantil","explotacion infantil"])) or (bool(self._found(combined,["menor","niño","niña","bebé","bebe","hijo","hija"])) and bool(self._found(combined,["abuso","maltrato","golpe","quemadura","accidente","lesión","lesion","amenaza","violencia"])))
        if minor_context: scores["Personas menores"]=scores.get("Personas menores",0)+1
        urgency=self._determine(scores,life,severe,sexual,gender,health,minor_context)
        classification="Violencia de Género" if gender else ("Violencia Sexual" if sexual else ("Posible emergencia" if life else ("Salud / accidente" if health else ("Asesoría / orientación" if legal else "Triaje social"))))
        keywords=list(dict.fromkeys(risk_hits+context_hits))
        return {"urgency":urgency,"keywords":keywords[:24],"risk_keywords":list(dict.fromkeys(risk_hits))[:20],"context_keywords":context_hits[:16],"response":self._response(urgency,gender,legal,health,minor_context),"suggested_resources":self._resources(scores,gender,legal,health,minor_context),"scores":scores,"classification":classification,"confidence":self._confidence(scores,life,severe,gender,health),"detected_context":self._context(scores,life,severe,gender,health,minor_context),"priority_reason":self._priority_reason(urgency,scores,life,severe,gender,health,minor_context),"next_questions":self._questions(urgency,gender,health,minor_context),"combined_with_social_report":bool(report),"context_note":"Resultado generado por reglas locales explicables. Las palabras de contexto no elevan por sí solas la urgencia; el sistema prioriza indicadores concretos y el relato completo. Requiere revisión profesional."}
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
    def _priority_reason(self,u,s,life,severe,gender,health,minor):
        if life:return "Se detectaron indicadores compatibles con una posible emergencia vital. Requiere verificación inmediata."
        if severe:return "Se detectaron indicadores de posible gravedad física. La prioridad se eleva para facilitar una valoración profesional."
        if health:return "Se detectaron indicadores de salud o accidente. La gravedad no puede determinarse solo por palabras clave; conviene ampliar síntomas, evolución y necesidad de atención."
        if gender:return "Se detectaron indicadores concretos de violencia o desigualdad vinculados al género. Revisar seguridad, contexto y necesidades de protección."
        if minor:return "Se detectó una posible situación que involucra a una persona menor junto con un indicador de riesgo. Requiere ampliar información y seguir el protocolo correspondiente."
        if u=="Media":return "Hay indicadores que justifican ampliar información y realizar seguimiento prioritario."
        return "No aparecen indicadores de urgencia en las reglas actuales. Esto no significa que el caso sea leve: el profesional debe revisar el relato completo."
    def _context(self,s,life,severe,gender,health,minor):
        if life:return "Indicadores de posible emergencia"
        if severe:return "Indicadores de gravedad física"
        if health:return "Salud / accidente"
        if gender:return "Posible violencia de género / relación de poder"
        if minor:return "Posible situación de riesgo que involucra a una persona menor"
        return "Consulta general"
    def _confidence(self,s,life,severe,gender,health): return "Alta" if life or severe or (gender and sum(s.values())>=2) else ("Media" if s else "Baja")
    def _questions(self,u,g,health,minor):
        q=[]
        if health:q += ["¿Qué ocurrió y cuándo?","¿Qué síntomas o lesiones presenta actualmente?","¿La situación está empeorando o permanece estable?","¿Ya recibió atención profesional?","¿Hay algún indicador de gravedad que deba verificarse?"]
        elif g:q += ["¿Qué ocurrió y cuándo?","¿Quién ejerció la conducta y qué relación tiene con la persona?","¿Existe una relación de poder o dependencia?","¿La persona está a salvo ahora?","¿Qué necesita: orientación, protección, acompañamiento o asesoría legal?"]
        elif minor:q += ["¿Qué ocurrió y cuándo?","¿La persona menor está a salvo ahora?","¿Quién está a cargo de sus cuidados?","¿Existe un riesgo actual?","¿Qué intervención o apoyo necesita?"]
        elif u in ("Muy Alta","Alta"):q += ["¿Existe peligro actual?","¿La persona está a salvo ahora?","¿Hay lesiones o necesidad inmediata?","¿Dónde se encuentra la persona?"]
        else:q += ["¿Qué ocurrió y cuándo?","¿Qué necesita la persona ahora?","¿Hay algún riesgo no mencionado en el relato?"]
        return q
    def _response(self,u,g,l,health,minor):
        if health:return "SALUD / ACCIDENTE\n\nSe detectaron indicadores relacionados con salud o un accidente. El sistema no determina la gravedad: ampliar información, verificar el estado actual y seguir el protocolo profesional correspondiente."
        if g:return "VIOLENCIA DE GÉNERO / RELACIÓN DE PODER\n\nEl relato contiene indicadores concretos que justifican revisar el caso desde una perspectiva de género y de posibles relaciones de poder. Priorizar una entrevista segura y documentar lo relatado."
        if minor:return "SITUACIÓN CON PERSONA MENOR\n\nSe detectaron indicadores de riesgo junto con referencias a una persona menor. Ampliar información y aplicar el protocolo de protección correspondiente."
        if l:return "ORIENTACIÓN LEGAL\n\nHay indicadores de una posible necesidad de asesoría jurídica. Ampliar el relato y revisar la situación concreta antes de derivar."
        return {"Muy Alta":"POSIBLE EMERGENCIA\n\nHay indicadores que requieren verificación profesional inmediata.","Alta":"SITUACIÓN URGENTE\n\nPriorizar valoración profesional y confirmar seguridad y gravedad.","Media":"SEGUIMIENTO PRIORITARIO\n\nAmpliar información, identificar necesidades y derivar al recurso adecuado.","Baja":"ORIENTACIÓN\n\nNo se detectaron indicadores suficientes de urgencia con las reglas actuales."}[u]
    def _resources(self,s,g,l,health,minor):
        r=[]
        if health:r += ["orientación sanitaria","emergencia local si corresponde"]
        if g:r += ["orientación especializada en violencia de género","asesoría legal","acompañamiento"]
        if "Riesgo de Vida" in s:r += ["emergencia","línea de crisis"]
        if minor:r += ["protección de niñez"]
        if l:r += ["asesoría legal"]
        return list(dict.fromkeys(r))[:8]
