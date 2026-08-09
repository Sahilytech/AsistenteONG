"""Motor de triaje local explicable y contextual. No realiza conexiones externas."""
import logging,re
logger=logging.getLogger(__name__)
class ConfigManager:
 KEYWORDS={"Riesgo de Vida":["suicidio","suicida","matarme","matarse","arma","veneno","sobredosis","asfixia","apuñalar","disparar","inconsciente","no respira","no responde","paro cardíaco","paro cardiaco"],"Violencia Severa":["fractura","sangre","trauma","hospitalización","hospitalizacion","urgencia","grave","crítico","critico","coma","herida","apaleado","molido","quemadura grave","quemaduras graves","sangrado abundante"],"Violencia de Género":["jefe","supervisor","empleador","empleadora","patrón","patron","compañero de trabajo","compañera de trabajo","pareja","marido","esposo","novia","novio","ex","golpeó","golpeo","amenaza","amenazó","amenazo","controla","aislada","control","dependencia","dominio","acoso","hostigamiento","discriminación","discriminacion","machista","violencia de género","violencia de genero","por ser mujer","no quiso","no quería","no queria","la atacó","la ataco","la agredió","la agredio"],"Violencia Sexual":["violación","violacion","abuso sexual","tocamientos","forzado","sin consentimiento","violada","violado","acoso sexual","acto sexual"],"Menores":["niño","niña","hijo","hija","bebé","bebe","infante","menor","abuso infantil","maltrato infantil","explotación infantil"],"Salud Mental":["depresión","depresion","ansiedad","pánico","panico","autolesión","autolesion","adicción","adiccion","droga","alcohol","consumo","trastorno","psicosis"],"Necesidad Inmediata":["urgente","emergencia","sos","rápido","rapido","inmediato","prisa","ahora mismo"],"Asesoría Legal":["abogado","demanda","custodia","divorcio","derechos","juicio","proceso","legal","ley","justicia","tribunal","denuncia","denunciar","despido","laboral","trabajo","horario laboral","jefe"],"Recursos":["refugio","dinero","trabajo","comida","vivienda","medicinas","alojamiento","asistencia","auxilio","alimento","hospedaje"]}
 CRITICAL=["no respira","no responde","inconsciente","paro cardíaco","paro cardiaco"]
 SEVERE=["fractura","sangrado abundante","quemadura grave","quemaduras graves","muy grave","hospitalización","hospitalizacion","trauma severo"]
 def __init__(self): logger.info("ConfigManager inicializado")
 def _found(self,text,phrases): return [p for p in phrases if p in text]
 def analyze(self,text):
  normalized=re.sub(r"\s+"," ",text.strip().lower()); found=[]; scores={}
  for cat,words in self.KEYWORDS.items():
   hits=self._found(normalized,words)
   if hits:scores[cat]=len(hits);found.extend(hits)
  life=bool(self._found(normalized,self.CRITICAL)) or "Riesgo de Vida" in scores; severe=bool(self._found(normalized,self.SEVERE)) or "Violencia Severa" in scores; gender="Violencia de Género" in scores or "Violencia Sexual" in scores; legal="Asesoría Legal" in scores
  urgency=self._determine(scores,life,severe,gender); classification="Violencia de Género" if gender else ("Posible emergencia" if life else ("Asesoría / orientación" if legal else "Triaje social"))
  return {"urgency":urgency,"keywords":list(dict.fromkeys(found))[:16],"response":self._response(urgency,gender,legal),"suggested_resources":self._resources(scores,gender,legal),"scores":scores,"classification":classification,"confidence":self._confidence(scores,life,severe,gender),"detected_context":self._context(scores,life,severe,gender),"priority_reason":self._priority_reason(urgency,scores,life,severe,gender),"next_questions":self._questions(urgency,gender),"context_note":"Resultado generado por reglas locales explicables. Es una orientación para ordenar la entrevista, no un diagnóstico ni una decisión profesional automática."}
 def _determine(self,s,life,severe,gender):
  if life:return "Muy Alta"
  if severe or "Violencia Sexual" in s:return "Alta"
  if gender:return "Media"
  if "Necesidad Inmediata" in s or "Menores" in s:return "Media"
  return "Baja"
 def _priority_reason(self,u,s,life,severe,gender):
  if life:return "Se detectaron indicadores compatibles con una posible emergencia vital. Requiere verificación inmediata."
  if severe:return "Se detectaron indicadores de posible gravedad física. La prioridad se eleva para facilitar una valoración profesional."
  if gender:return "Se detectaron indicadores de violencia o desigualdad vinculados al género, incluyendo una posible relación de poder o laboral. Aunque no se describa un peligro vital, requiere atención prioritaria y revisión del contexto."
  if u=="Media":return "Hay indicadores que justifican ampliar información y realizar seguimiento prioritario."
  return "No aparecen indicadores de urgencia en las reglas actuales. Esto no significa que el caso sea leve: el operador debe revisar el relato completo y confirmar contexto, riesgo y necesidades."
 def _context(self,s,life,severe,gender):
  if life:return "Indicadores de posible emergencia"
  if gender:return "Posible violencia de género / relación de poder"
  if severe:return "Indicadores de gravedad"
  return "Consulta general"
 def _confidence(self,s,life,severe,gender): return "Alta" if life or severe or (gender and sum(s.values())>=2) else ("Media" if s else "Baja")
 def _questions(self,u,g):
  if g:return ["¿Qué ocurrió y cuándo?","¿Quién ejerció la conducta y qué relación tiene con la persona?","¿Existe una relación de poder, dependencia laboral o económica?","¿La persona está a salvo ahora?","¿Qué necesita ahora: orientación, protección, acompañamiento o asesoría legal?"]
  if u in ("Muy Alta","Alta"):return ["¿Existe peligro actual?","¿La persona está a salvo ahora?","¿Hay lesiones o necesidad inmediata?","¿Dónde se encuentra la persona?"]
  return ["¿Qué ocurrió y cuándo?","¿Qué necesita la persona ahora?","¿Hay algún riesgo no mencionado en el relato?"]
 def _response(self,u,g,l):
  if g:return "VIOLENCIA DE GÉNERO / RELACIÓN DE PODER\n\nEl relato contiene indicadores que justifican revisar el caso desde una perspectiva de género y de posibles relaciones de poder. No se requiere que exista una lesión física para que el caso sea relevante.\n\nPriorizar una entrevista segura, documentar lo relatado y determinar necesidades de protección, acompañamiento y/o asesoría legal."
  if l:return "ORIENTACIÓN LEGAL\n\nHay indicadores de una posible necesidad de asesoría jurídica. Ampliar el relato y revisar la situación concreta antes de derivar."
  return {"Muy Alta":"POSIBLE EMERGENCIA\n\nHay indicadores que requieren verificación profesional inmediata.","Alta":"SITUACIÓN URGENTE\n\nPriorizar valoración profesional y confirmar seguridad y gravedad.","Media":"SEGUIMIENTO PRIORITARIO\n\nAmpliar información, identificar necesidades y derivar al recurso adecuado.","Baja":"ORIENTACIÓN\n\nNo se detectaron indicadores suficientes de urgencia con las reglas actuales."}[u]
 def _resources(self,s,g,l):
  r=[]
  if g:r += ["orientación especializada en violencia de género","asesoría-legal","acompañamiento"]
  if "Riesgo de Vida" in s:r += ["emergencia","línea-crisis"]
  if "Menores" in s:r += ["protección-de-niñez"]
  if l:r += ["asesoría-legal"]
  return list(dict.fromkeys(r))[:6]
