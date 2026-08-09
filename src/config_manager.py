"""Motor de triaje local explicable y contextual."""
import logging, re
from typing import Dict, List
logger=logging.getLogger(__name__)

class ConfigManager:
    KEYWORDS={
      "Riesgo de Vida":["suicidio","suicida","matarme","matarse","arma","veneno","sobredosis","asfixia","apuñalar","disparar","inconsciente","no respira","no responde","paro cardíaco","paro cardiaco"],
      "Violencia Severa":["fractura","sangre","trauma","hospitalización","hospitalizacion","urgencia","grave","crítico","critico","coma","herida","apaleado","molido","quemadura grave","quemaduras graves"],
      "Menores":["niño","niña","hijo","hija","bebé","bebe","infante","menor","abuso infantil","maltrato infantil","explotación infantil"],
      "Violencia Sexual":["violación","violacion","abuso sexual","tocamientos","forzado","sin consentimiento","violada","violado","acoso sexual"],
      "Violencia Doméstica":["pareja","marido","esposo","novia","novio","ex","golpeó","golpeo","amenaza","controla","aislada","control","dependencia","dominio"],
      "Salud Mental":["depresión","depresion","ansiedad","pánico","panico","autolesión","autolesion","adicción","adiccion","droga","alcohol","consumo","trastorno","psicosis"],
      "Necesidad Inmediata":["urgente","emergencia","sos","rápido","rapido","inmediato","prisa","ahora mismo"],
      "Asesoría Legal":["abogado","demanda","custodia","divorcio","derechos","juicio","proceso","legal","ley","justicia","tribunal"],
      "Recursos":["refugio","dinero","trabajo","comida","vivienda","medicinas","alojamiento","asistencia","auxilio","alimento","hospedaje"],
      "Accidente / Salud Física":["me quemé","se quemó","me queme","se quemo","quemé","queme","quemadura","quemado","quemada","me lastimé","se lastimó","accidente","caída","caida","me corté","se cortó","me corte","se corto","corte accidental","cocinando","estufa"]}
    ACCIDENT_CONTEXT=["accidente","accidental","cocinando","cocinar","estufa","horno","se quemó","se quemo","me quemé","me queme","se cortó","se corto","me corté","me corte","caída","caida"]
    CRITICAL=["no respira","no responde","inconsciente","paro cardíaco","paro cardiaco"]
    SEVERE=["quemadura grave","quemaduras graves","muy grave","hospitalización","hospitalizacion","sangrado abundante","fractura"]
    def __init__(self): logger.info("ConfigManager inicializado")
    @staticmethod
    def _found(text, phrases): return [p for p in phrases if p in text]
    def analyze(self,text:str)->Dict:
        original=text.strip(); normalized=re.sub(r"\s+"," ",original.lower()); found=[]; scores={}
        for cat,words in self.KEYWORDS.items():
            hits=self._found(normalized,words)
            if hits: scores[cat]=len(hits); found.extend(hits)
        accident=bool(self._found(normalized,self.ACCIDENT_CONTEXT)) or "Accidente / Salud Física" in scores
        life=bool(self._found(normalized,self.CRITICAL)) or "Riesgo de Vida" in scores
        severe=bool(self._found(normalized,self.SEVERE))
        violence=any(x in scores for x in ("Violencia Sexual","Violencia Doméstica"))
        if accident and not violence and not life:
            urgency="Alta" if severe else ("Media" if any(x in normalized for x in ["dolor","dolor intenso","ampolla","sangrado","médico","medico"]) else "Baja")
            classification="Accidente / Salud Física"; response=self._accident_response(urgency); resources=["atención-médica"]
        else:
            urgency=self._determine(scores); classification="Triaje social"; response=self._response(urgency); resources=self._resources(scores)
        confidence=self._confidence(scores,accident,life,severe)
        return {"urgency":urgency,"keywords":list(dict.fromkeys(found))[:12],"response":response,"suggested_resources":resources,"scores":scores,"classification":classification,"confidence":confidence,"detected_context":self._context_label(accident,violence,life,severe),"next_questions":self._next_questions(classification,urgency),"context_note":"Resultado generado por reglas locales explicables. Debe ser revisado y confirmado por un profesional."}
    def _determine(self,s):
        if "Riesgo de Vida" in s or "Violencia Sexual" in s:return "Muy Alta"
        if "Violencia Doméstica" in s or "Violencia Severa" in s:return "Alta"
        if any(x in s for x in ("Salud Mental","Asesoría Legal","Necesidad Inmediata","Menores")):return "Media"
        return "Baja"
    def _confidence(self,s,accident,life,severe):
        n=sum(s.values())
        if life or severe:return "Alta"
        if accident:return "Media"
        return "Media" if n>=2 else "Baja"
    def _context_label(self,a,v,l,s):
        if l:return "Indicadores de posible emergencia"
        if a:return "Accidente o salud física"
        if v:return "Posible violencia interpersonal"
        if s:return "Indicadores de gravedad"
        return "Consulta general"
    def _next_questions(self,c,u):
        if c=="Accidente / Salud Física": return ["¿Cuándo ocurrió?","¿Qué parte del cuerpo está afectada?","¿La persona está consciente y respira normalmente?","¿La lesión parece leve o requiere valoración médica?"]
        if u in ("Muy Alta","Alta"): return ["¿Existe peligro actual?","¿La persona está a salvo ahora?","¿Hay lesiones o necesidad médica inmediata?","¿Dónde se encuentra la persona?"]
        return ["¿Qué ocurrió y cuándo?","¿Qué necesita la persona ahora?","¿Hay algún riesgo que no esté mencionado en el relato?"]
    def _accident_response(self,u):
        return f"""ACCIDENTE / SALUD FÍSICA\n\nEl relato contiene indicadores de un posible accidente o lesión física. Prioridad automática: {u}.\n\nVERIFICAR:\n1. Qué ocurrió y cuándo.\n2. Estado actual de la persona y síntomas.\n3. Si requiere valoración médica.\n4. Si aparecen signos de gravedad, buscar atención de emergencia local.\n\nEl sistema no diagnostica ni determina la gravedad clínica."""
    def _response(self,u):
        return {"Muy Alta":"POSIBLE EMERGENCIA\n\nHay indicadores que requieren verificación profesional inmediata. Confirmar el peligro actual y, si existe una emergencia, contactar al servicio local correspondiente.","Alta":"SITUACIÓN URGENTE\n\nPriorizar valoración profesional. Confirmar seguridad, gravedad y necesidad de intervención inmediata.","Media":"SEGUIMIENTO PRIORITARIO\n\nAmpliar información, identificar necesidades y derivar al recurso adecuado.","Baja":"ORIENTACIÓN\n\nNo se detectaron indicadores suficientes de urgencia con las reglas actuales. Revisar el relato completo."}[u]
    def _resources(self,s):
        r=[]
        if "Riesgo de Vida" in s or "Violencia Sexual" in s:r += ["emergencia","línea-crisis"]
        if "Violencia Doméstica" in s:r += ["defensoría","refugio"]
        if "Salud Mental" in s:r += ["salud-mental"]
        if "Asesoría Legal" in s:r += ["asesoría-legal"]
        if "Menores" in s:r += ["protección-de-niñez"]
        if "Recursos" in s:r += ["asistencia-social"]
        return list(dict.fromkeys(r))[:6]
