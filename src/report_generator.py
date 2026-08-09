"""Generación de informes sociales en PDF con estructura profesional."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

BLUE=colors.HexColor("#0e98d6"); BLACK=colors.black; GRAY=colors.HexColor("#666666")

def _styles():
    styles=getSampleStyleSheet()
    return {"title":ParagraphStyle("ReportTitle",parent=styles["Title"],fontName="Helvetica-Bold",fontSize=17,textColor=BLUE,spaceAfter=12),"section":ParagraphStyle("Section",parent=styles["Heading2"],fontName="Helvetica-Bold",fontSize=11,textColor=BLUE,spaceBefore=10,spaceAfter=6),"body":ParagraphStyle("Body",parent=styles["BodyText"],fontName="Helvetica",fontSize=9.5,leading=13,textColor=BLACK),"muted":ParagraphStyle("Muted",parent=styles["BodyText"],fontName="Helvetica",fontSize=8,textColor=GRAY)}

def _safe(value): return str(value or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>")

def generate_social_report(data:dict,output_path:str)->str:
    path=Path(output_path); path.parent.mkdir(parents=True,exist_ok=True); styles=_styles()
    doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=45,bottomMargin=45,title="Informe Social Profesional")
    story=[Paragraph("INFORME SOCIAL PROFESIONAL",styles["title"]),Paragraph("Instrumento técnico y documental de Trabajo Social · revisión profesional obligatoria",styles["muted"]),Spacer(1,10)]
    if data.get("case_number") or data.get("case_text"):
        story.append(Paragraph("Expediente asociado",styles["section"])); rows=[[Paragraph("Caso",styles["body"]),Paragraph(_safe(data.get("case_number")),styles["body"])],[Paragraph("Relato recibido",styles["body"]),Paragraph(_safe(data.get("case_text")),styles["body"])]]; table=Table(rows,colWidths=[145,355]); table.setStyle(_table_style()); story.extend([table,Spacer(1,7)])
    sections=[("1. Datos del profesional e institución",[("entidad_emisora","Entidad emisora"),("profesional_referencia","Profesional de referencia"),("colegiatura","Número de colegiatura / matrícula"),("destinatario","Destinatario"),("fecha_emision","Fecha de emisión"),("motivo","Motivo de la solicitud")]),("2. Datos de identificación de la persona de referencia",[("nombre_completo","Nombres y apellidos completos"),("documento","DNI / NIE / pasaporte"),("domicilio","Domicilio actual"),("telefono","Teléfono"),("correo","Correo electrónico"),("fecha_nacimiento","Fecha de nacimiento"),("edad","Edad"),("sexo","Sexo"),("nacionalidad","Nacionalidad"),("estado_civil","Estado civil")]),("3. Composición de la unidad de convivencia y dinámica familiar",[("miembros_hogar","Miembros del hogar: parentesco, edad y ocupación"),("genograma","Genograma / vínculos familiares"),("historia_familiar","Antecedentes familiares"),("dinamica_familiar","Dinámica y relaciones familiares")]),("4. Situación socioeconómica y laboral",[("ingresos","Fuentes de ingresos y sustento"),("situacion_laboral","Situación laboral"),("egresos","Egresos básicos")]),("5. Habitabilidad y vivienda",[("tenencia","Régimen de tenencia"),("condiciones_vivienda","Condiciones materiales, habitaciones y hacinamiento"),("servicios_entorno","Servicios y entorno")]),("6. Situación de salud y educación",[("salud","Estado sanitario, discapacidad, dependencia o consumo problemático"),("educacion","Nivel educativo y asistencia escolar")]),("7. Diagnóstico, valoración social y propuesta",[("diagnostico","Juicio técnico / valoración social"),("fortalezas","Fortalezas y factores protectores"),("vulnerabilidades","Vulnerabilidades y necesidades"),("propuesta","Propuesta de intervención / recurso solicitado"),("observaciones","Observaciones y límites de la información")])]
    for title,fields in sections:
        story.append(Paragraph(_safe(title),styles["section"])); rows=[[Paragraph(f"<b>{_safe(label)}</b>",styles["body"]),Paragraph(_safe(data.get(key)),styles["body"])] for key,label in fields]; table=Table(rows,colWidths=[175,325]); table.setStyle(_table_style()); story.extend([table,Spacer(1,7)])
    analysis=data.get("combined_analysis") or data.get("analysis") or {}
    if analysis:
        story.append(Paragraph("Análisis integral del caso + informe",styles["section"]))
        rows=[[Paragraph("Prioridad orientativa",styles["body"]),Paragraph(_safe(analysis.get("urgency")),styles["body"])],[Paragraph("Clasificación",styles["body"]),Paragraph(_safe(analysis.get("classification")),styles["body"])],[Paragraph("Confianza orientativa",styles["body"]),Paragraph(_safe(analysis.get("confidence")),styles["body"])],[Paragraph("Contexto",styles["body"]),Paragraph(_safe(analysis.get("detected_context")),styles["body"])],[Paragraph("Indicadores",styles["body"]),Paragraph(_safe(", ".join(analysis.get("keywords",[]))),styles["body"])],[Paragraph("Motivo de prioridad",styles["body"]),Paragraph(_safe(analysis.get("priority_reason")),styles["body"])],[Paragraph("Información pendiente",styles["body"]),Paragraph(_safe("\n".join(analysis.get("next_questions",[]))),styles["body"])]]; table=Table(rows,colWidths=[175,325]); table.setStyle(_table_style()); story.extend([table,Spacer(1,7),Paragraph(_safe(analysis.get("context_note")),styles["muted"])])
    story.extend([Spacer(1,15),Paragraph("Firma y sello del profesional: ______________________________________________",styles["body"]),Spacer(1,12),Paragraph("Documento generado como borrador técnico. Debe ser revisado, validado y emitido por el profesional responsable. El sistema no sustituye el criterio profesional.",styles["muted"])])
    doc.build(story); return str(path)

def _table_style():
    return TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("GRID",(0,0),(-1,-1),0.35,colors.HexColor("#D9D9D9")),("BACKGROUND",(0,0),(0,-1),colors.HexColor("#F7F7F7")),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)])
