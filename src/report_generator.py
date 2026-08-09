"""Generación de informes sociales en PDF."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

BLUE=colors.HexColor("#0e98d6"); BLACK=colors.black; GRAY=colors.HexColor("#666666")

def _styles():
 styles=getSampleStyleSheet(); return {"title":ParagraphStyle("ReportTitle",parent=styles["Title"],fontName="Helvetica-Bold",fontSize=17,textColor=BLUE,spaceAfter=12),"section":ParagraphStyle("Section",parent=styles["Heading2"],fontName="Helvetica-Bold",fontSize=11,textColor=BLUE,spaceBefore=10,spaceAfter=6),"body":ParagraphStyle("Body",parent=styles["BodyText"],fontName="Helvetica",fontSize=9.5,leading=13,textColor=BLACK),"muted":ParagraphStyle("Muted",parent=styles["BodyText"],fontName="Helvetica",fontSize=8,textColor=GRAY)}

def _safe(value): return str(value or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>")

def generate_social_report(data:dict,output_path:str)->str:
 path=Path(output_path); path.parent.mkdir(parents=True,exist_ok=True); styles=_styles(); doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=45,bottomMargin=45,title="Informe Social Profesional")
 story=[Paragraph("INFORME SOCIAL PROFESIONAL",styles["title"]),Paragraph("Documento de valoración social — uso profesional",styles["muted"]),Spacer(1,10)]
 sections=[("1. Datos del profesional e institución",["entidad_emisora","profesional","colegiatura","destinatario","fecha_emision","motivo"]),("2. Identificación de la persona de referencia",["nombre_completo","documento","domicilio","telefono","email","fecha_nacimiento","edad","sexo","nacionalidad","estado_civil"]),("3. Unidad de convivencia y dinámica familiar",["miembros_hogar","historia_familiar","dinamica_familiar","genograma"]),("4. Situación socioeconómica y laboral",["ingresos","situacion_laboral","egresos"]),("5. Habitabilidad y vivienda",["tenencia","condiciones_vivienda","servicios_entorno"]),("6. Salud y educación",["salud","educacion"]),("7. Diagnóstico, valoración y propuesta",["diagnostico","fortalezas","vulnerabilidades","propuesta","observaciones"])]
 labels={"entidad_emisora":"Entidad emisora","profesional":"Profesional de referencia","colegiatura":"Matrícula / colegiatura","destinatario":"Destinatario","fecha_emision":"Fecha de emisión","motivo":"Motivo","nombre_completo":"Nombre completo","documento":"Documento","domicilio":"Domicilio","telefono":"Teléfono","email":"Correo electrónico","fecha_nacimiento":"Fecha de nacimiento","edad":"Edad","sexo":"Sexo","nacionalidad":"Nacionalidad","estado_civil":"Estado civil","miembros_hogar":"Miembros del hogar","historia_familiar":"Historia familiar","dinamica_familiar":"Dinámica familiar","genograma":"Genograma / observaciones","ingresos":"Ingresos","situacion_laboral":"Situación laboral","egresos":"Egresos básicos","tenencia":"Régimen de tenencia","condiciones_vivienda":"Condiciones de vivienda","servicios_entorno":"Servicios y entorno","salud":"Situación sanitaria","educacion":"Educación","diagnostico":"Valoración social / juicio técnico","fortalezas":"Fortalezas y factores protectores","vulnerabilidades":"Vulnerabilidades y factores de riesgo","propuesta":"Propuesta de intervención","observaciones":"Observaciones finales"}
 for title,keys in sections:
  story.append(Paragraph(_safe(title),styles["section"])); rows=[[Paragraph(f"<b>{_safe(labels[k])}</b>",styles["body"]),Paragraph(_safe(data.get(k)),styles["body"])] for k in keys]; table=Table(rows,colWidths=[145,355]); table.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("GRID",(0,0),(-1,-1),0.35,colors.HexColor("#D9D9D9")),("BACKGROUND",(0,0),(0,-1),colors.HexColor("#F7F7F7")),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)])); story.extend([table,Spacer(1,7)])
 analysis=data.get("analysis") or {}
 if analysis:
  story.append(Paragraph("Análisis orientativo del sistema",styles["section"]))
  rows=[[Paragraph("Estado",styles["body"]),Paragraph(_safe(analysis.get("level")),styles["body"])],[Paragraph("Completitud",styles["body"]),Paragraph(f"{_safe(analysis.get('completeness'))}%",styles["body"])],[Paragraph("Indicadores",styles["body"]),Paragraph(_safe(", ".join(analysis.get("risk_indicators",[])) or "Ninguno detectado"),styles["body"])],[Paragraph("Inconsistencias",styles["body"]),Paragraph(_safe(" ".join(analysis.get("consistency_flags",[])) or "Ninguna detectada"),styles["body"])],[Paragraph("Recomendaciones",styles["body"]),Paragraph(_safe("\n".join(analysis.get("recommendations",[]))),styles["body"])]]
  table=Table(rows,colWidths=[145,355]); table.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("GRID",(0,0),(-1,-1),0.35,colors.HexColor("#D9D9D9")),("BACKGROUND",(0,0),(0,-1),colors.HexColor("#F7F7F7")),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)])); story.extend([table,Spacer(1,7),Paragraph(_safe(analysis.get("disclaimer")),styles["muted"])])
 story.extend([Spacer(1,15),Paragraph("Firma y sello del profesional: ______________________________________________",styles["body"]),Spacer(1,12),Paragraph("Documento generado por Asistente ONG. El contenido debe ser revisado y validado por el profesional responsable antes de su emisión.",styles["muted"])])
 doc.build(story); return str(path)
