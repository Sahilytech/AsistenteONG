"""
Generador de PDF para Informes Sociales
Colores: Blanco, Negro, Azul #0e98d6
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

from .social_report import InformeSocial

logger = logging.getLogger(__name__)

# COLORES OFICIALES
AZUL = HexColor("#0e98d6")
NEGRO = HexColor("#000000")
BLANCO = HexColor("#FFFFFF")
GRIS_CLARO = HexColor("#F5F5F5")
GRIS_MEDIO = HexColor("#666666")


class PDFGenerator:
    """Generador de PDF profesional para informes sociales."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Configura estilos personalizados."""

        # Título principal
        self.styles.add(ParagraphStyle(
            name='TituloPrincipal',
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=AZUL,
            spaceAfter=20,
            alignment=TA_CENTER,
            borderWidth=2,
            borderColor=AZUL,
            borderPadding=10,
            backColor=GRIS_CLARO
        ))

        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='Subtitulo',
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=AZUL,
            spaceAfter=12,
            spaceBefore=16,
            borderWidth=1,
            borderColor=AZUL,
            borderPadding=5,
            backColor=GRIS_CLARO
        ))

        # Texto normal
        self.styles.add(ParagraphStyle(
            name='TextoNormal',
            fontName='Helvetica',
            fontSize=10,
            textColor=NEGRO,
            leading=14,
            alignment=TA_JUSTIFY
        ))

        # Texto etiqueta
        self.styles.add(ParagraphStyle(
            name='Etiqueta',
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=AZUL,
            leading=14
        ))

        # Texto valor
        self.styles.add(ParagraphStyle(
            name='Valor',
            fontName='Helvetica',
            fontSize=10,
            textColor=NEGRO,
            leading=14
        ))

        # Nota
        self.styles.add(ParagraphStyle(
            name='Nota',
            fontName='Helvetica-Oblique',
            fontSize=9,
            textColor=GRIS_MEDIO,
            leading=12,
            alignment=TA_LEFT
        ))

        # Pie de página
        self.styles.add(ParagraphStyle(
            name='PiePagina',
            fontName='Helvetica',
            fontSize=8,
            textColor=GRIS_MEDIO,
            alignment=TA_CENTER
        ))

    def generate_pdf(self, informe: InformeSocial, output_path: Optional[str] = None) -> str:
        """Genera PDF del informe social."""

        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"informe_social_{informe.datos_identificacion.apellidos}_{timestamp}.pdf"

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        story = []

        # === PORTADA ===
        story.append(self._create_header())
        story.append(Spacer(1, 30))

        # === 1. DATOS DEL PROFESIONAL E INSTITUCIÓN ===
        story.append(self._create_section("1. DATOS DEL PROFESIONAL E INSTITUCIÓN"))
        story.append(self._create_datos_profesional_table(informe.datos_profesional))
        story.append(Spacer(1, 12))

        # === 2. DATOS DE IDENTIFICACIÓN ===
        story.append(self._create_section("2. DATOS DE IDENTIFICACIÓN DEL USUARIO"))
        story.append(self._create_datos_identificacion_table(informe.datos_identificacion))
        story.append(Spacer(1, 12))

        # === 3. UNIDAD DE CONVIVENCIA ===
        story.append(self._create_section("3. COMPOSICIÓN DE LA UNIDAD DE CONVIVENCIA"))
        story.append(self._create_unidad_convivencia_table(informe.unidad_convivencia))
        story.append(Spacer(1, 12))

        # Nueva página
        story.append(PageBreak())

        # === 4. SITUACIÓN SOCIOECONÓMICA ===
        story.append(self._create_section("4. SITUACIÓN SOCIOECONÓMICA Y LABORAL"))
        story.append(self._create_socioeconomica_table(informe.socioeconomica))
        story.append(Spacer(1, 12))

        # === 5. HABITABILIDAD ===
        story.append(self._create_section("5. HABITABILIDAD Y VIVIENDA"))
        story.append(self._create_habitabilidad_table(informe.habitabilidad))
        story.append(Spacer(1, 12))

        # === 6. SALUD Y EDUCACIÓN ===
        story.append(self._create_section("6. SITUACIÓN DE SALUD Y EDUCACIÓN"))
        story.append(self._create_salud_educacion_table(informe.salud_educacion))
        story.append(Spacer(1, 12))

        # Nueva página
        story.append(PageBreak())

        # === 7. DIAGNÓSTICO Y PROPUESTA ===
        story.append(self._create_section("7. DIAGNÓSTICO SOCIAL Y PROPUESTA DE INTERVENCIÓN"))
        story.append(self._create_diagnostico_content(informe.diagnostico))
        story.append(Spacer(1, 20))

        # Firma
        story.append(self._create_firma_section())

        # Pie de página
        story.append(Spacer(1, 30))
        story.append(HRFlowable(width="100%", thickness=1, color=AZUL))
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            f"Documento generado el {datetime.now().strftime('%d/%m/%Y')} • Asistente ONG v0.9 • OFFLINE 100%",
            self.styles['PiePagina']
        ))

        # Construir PDF
        doc.build(story)

        logger.info(f"✅ PDF generado: {output_path}")
        return output_path

    def _create_header(self):
        """Crea el encabezado del documento."""
        header_data = [[
            Paragraph("<b>INFORME SOCIAL</b>", self.styles['TituloPrincipal'])
        ]]
        header_table = Table(header_data, colWidths=[16*cm])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), GRIS_CLARO),
            ('BOX', (0, 0), (-1, -1), 2, AZUL),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        return header_table

    def _create_section(self, title: str):
        """Crea una sección del informe."""
        return Paragraph(title, self.styles['Subtitulo'])

    def _create_datos_profesional_table(self, dp):
        """Tabla de datos del profesional."""
        data = [
            [Paragraph("<b>Entidad Emisora:</b>", self.styles['Etiqueta']), 
             Paragraph(dp.entidad_emisora or "No especificado", self.styles['Valor'])],
            [Paragraph("<b>Profesional:</b>", self.styles['Etiqueta']), 
             Paragraph(f"{dp.profesional_nombre} {dp.profesional_apellidos}".strip() or "No especificado", self.styles['Valor'])],
            [Paragraph("<b>Nº Colegiatura:</b>", self.styles['Etiqueta']), 
             Paragraph(dp.numero_colegiatura or "No especificado", self.styles['Valor'])],
            [Paragraph("<b>Destinatario:</b>", self.styles['Etiqueta']), 
             Paragraph(dp.destinatario or "No especificado", self.styles['Valor'])],
            [Paragraph("<b>Fecha:</b>", self.styles['Etiqueta']), 
             Paragraph(dp.fecha_emision or datetime.now().strftime("%d/%m/%Y"), self.styles['Valor'])],
            [Paragraph("<b>Motivo:</b>", self.styles['Etiqueta']), 
             Paragraph(dp.motivo or "No especificado", self.styles['Valor'])],
        ]

        table = Table(data, colWidths=[5*cm, 11*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, GRIS_MEDIO),
            ('BACKGROUND', (0, 0), (0, -1), GRIS_CLARO),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        return table

    def _create_datos_identificacion_table(self, di):
        """Tabla de datos de identificación."""
        data = [
            [Paragraph("<b>Nombres:</b>", self.styles['Etiqueta']), 
             Paragraph(di.nombres or "No especificado", self.styles['Valor']),
             Paragraph("<b>Apellidos:</b>", self.styles['Etiqueta']), 
             Paragraph(di.apellidos or "No especificado", self.styles['Valor'])],
            [Paragraph("<b>DNI/NIE:</b>", self.styles['Etiqueta']), 
             Paragraph(di.dni_nie or "No especificado", self.styles['Valor']),
             Paragraph("<b>Pasaporte:</b>", self.styles['Etiqueta']), 
             Paragraph(di.pasaporte or "No especificado", self.styles['Valor'])],
            [Paragraph("<b>Fecha Nac.:</b>", self.styles['Etiqueta']), 
             Paragraph(di.fecha_nacimiento or "No especificado", self.styles['Valor']),
             Paragraph("<b>Edad:</b>", self.styles['Etiqueta']), 
             Paragraph(str(di.edad) if di.edad else "No especificado", self.styles['Valor'])],
            [Paragraph("<b>Sexo:</b>", self.styles['Etiqueta']), 
             Paragraph(di.sexo or "No especificado", self.styles['Valor']),
             Paragraph("<b>Estado Civil:</b>", self.styles['Etiqueta']), 
             Paragraph(di.estado_civil or "No especificado", self.styles['Valor'])],
            [Paragraph("<b>Nacionalidad:</b>", self.styles['Etiqueta']), 
             Paragraph(di.nacionalidad or "No especificado", self.styles['Valor']),
             Paragraph("<b>Teléfono:</b>", self.styles['Etiqueta']), 
             Paragraph(di.telefono or "No especificado", self.styles['Valor'])],
            [Paragraph("<b>Dirección:</b>", self.styles['Etiqueta']), 
             Paragraph(di.direccion or "No especificado", self.styles['Valor']),
             Paragraph("<b>Email:</b>", self.styles['Etiqueta']), 
             Paragraph(di.email or "No especificado", self.styles['Valor'])],
        ]

        table = Table(data, colWidths=[3.5*cm, 5*cm, 3.5*cm, 5*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, GRIS_MEDIO),
            ('BACKGROUND', (0, 0), (0, -1), GRIS_CLARO),
            ('BACKGROUND', (2, 0), (2, -1), GRIS_CLARO),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        return table

    def _create_unidad_convivencia_table(self, uc):
        """Tabla de unidad de convivencia."""
        if not uc.miembros:
            return Paragraph("No se han registrado miembros de la unidad de convivencia.", self.styles['Nota'])

        # Encabezados
        data = [[
            Paragraph("<b>Nombre</b>", self.styles['Etiqueta']),
            Paragraph("<b>Parentesco</b>", self.styles['Etiqueta']),
            Paragraph("<b>Edad</b>", self.styles['Etiqueta']),
            Paragraph("<b>Ocupación</b>", self.styles['Etiqueta']),
            Paragraph("<b>Sit. Laboral</b>", self.styles['Etiqueta']),
            Paragraph("<b>Ingresos</b>", self.styles['Etiqueta']),
        ]]

        # Filas
        for m in uc.miembros:
            data.append([
                Paragraph(m.nombre or "-", self.styles['Valor']),
                Paragraph(m.parentesco or "-", self.styles['Valor']),
                Paragraph(str(m.edad) if m.edad else "-", self.styles['Valor']),
                Paragraph(m.ocupacion or "-", self.styles['Valor']),
                Paragraph(m.situacion_laboral or "-", self.styles['Valor']),
                Paragraph(f"${m.ingresos:,.2f}" if m.ingresos else "-", self.styles['Valor']),
            ])

        table = Table(data, colWidths=[4*cm, 3*cm, 1.5*cm, 3*cm, 3*cm, 2.5*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, GRIS_MEDIO),
            ('BACKGROUND', (0, 0), (-1, 0), AZUL),
            ('TEXTCOLOR', (0, 0), (-1, 0), BLANCO),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))

        elements = [table]

        if uc.historia_familiar:
            elements.append(Spacer(1, 8))
            elements.append(Paragraph("<b>Historia y Dinámica Familiar:</b>", self.styles['Etiqueta']))
            elements.append(Paragraph(uc.historia_familiar, self.styles['TextoNormal']))

        if uc.dinamica_relaciones:
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"<b>Tipo de Relaciones:</b> {uc.dinamica_relaciones}", self.styles['Valor']))

        return elements

    def _create_socioeconomica_table(self, se):
        """Tabla de situación socioeconómica."""
        data = [
            [Paragraph("<b>INGRESOS MENSUALES</b>", self.styles['Etiqueta']), 
             "", 
             Paragraph("<b>EGRESOS MENSUALES</b>", self.styles['Etiqueta']), 
             ""],
            [Paragraph("Salarios:", self.styles['Valor']), 
             Paragraph(f"${se.ingresos_salarios:,.2f}", self.styles['Valor']),
             Paragraph("Alquiler:", self.styles['Valor']), 
             Paragraph(f"${se.egresos_alquiler:,.2f}", self.styles['Valor'])],
            [Paragraph("Pensiones:", self.styles['Valor']), 
             Paragraph(f"${se.ingresos_pensiones:,.2f}", self.styles['Valor']),
             Paragraph("Hipoteca:", self.styles['Valor']), 
             Paragraph(f"${se.egresos_hipoteca:,.2f}", self.styles['Valor'])],
            [Paragraph("Subsidios:", self.styles['Valor']), 
             Paragraph(f"${se.ingresos_subsidios:,.2f}", self.styles['Valor']),
             Paragraph("Servicios:", self.styles['Valor']), 
             Paragraph(f"${se.egresos_servicios:,.2f}", self.styles['Valor'])],
            [Paragraph("Otros:", self.styles['Valor']), 
             Paragraph(f"${se.ingresos_otros:,.2f}", self.styles['Valor']),
             Paragraph("Alimentación:", self.styles['Valor']), 
             Paragraph(f"${se.egresos_alimentacion:,.2f}", self.styles['Valor'])],
            [Paragraph("Otros egresos:", self.styles['Valor']), 
             "",
             Paragraph(f"${se.egresos_otros:,.2f}", self.styles['Valor'])],
            [Paragraph("<b>TOTAL INGRESOS:</b>", self.styles['Etiqueta']), 
             Paragraph(f"<b>${se.ingresos_total():,.2f}</b>", self.styles['Etiqueta']),
             Paragraph("<b>TOTAL EGRESOS:</b>", self.styles['Etiqueta']), 
             Paragraph(f"<b>${se.egresos_total():,.2f}</b>", self.styles['Etiqueta'])],
            [Paragraph("<b>BALANCE:</b>", self.styles['Etiqueta']), 
             Paragraph(f"<b>${se.balance():,.2f}</b>", self.styles['Etiqueta']),
             Paragraph("<b>Sit. Empleo:</b>", self.styles['Etiqueta']), 
             Paragraph(se.situacion_empleo_principal or "No especificado", self.styles['Valor'])],
        ]

        table = Table(data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, GRIS_MEDIO),
            ('BACKGROUND', (0, 0), (1, 0), GRIS_CLARO),
            ('BACKGROUND', (2, 0), (3, 0), GRIS_CLARO),
            ('BACKGROUND', (0, 6), (1, 6), GRIS_CLARO),
            ('BACKGROUND', (2, 6), (3, 6), GRIS_CLARO),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        return table

    def _create_habitabilidad_table(self, hab):
        """Tabla de habitabilidad."""
        data = [
            [Paragraph("<b>Régimen de Tenencia:</b>", self.styles['Etiqueta']), 
             Paragraph(hab.regimen_tenencia or "No especificado", self.styles['Valor']),
             Paragraph("<b>Tipo de Vivienda:</b>", self.styles['Etiqueta']), 
             Paragraph(hab.tipo_vivienda or "No especificado", self.styles['Valor'])],
            [Paragraph("<b>Habitaciones:</b>", self.styles['Etiqueta']), 
             Paragraph(str(hab.num_habitaciones) if hab.num_habitaciones else "No especificado", self.styles['Valor']),
             Paragraph("<b>Dormitorios:</b>", self.styles['Etiqueta']), 
             Paragraph(str(hab.num_dormitorios) if hab.num_dormitorios else "No especificado", self.styles['Valor'])],
            [Paragraph("<b>Hacinamiento:</b>", self.styles['Etiqueta']), 
             Paragraph(hab.hacinamiento or "No especificado", self.styles['Valor']),
             Paragraph("<b>Estado:</b>", self.styles['Etiqueta']), 
             Paragraph(hab.estado_infraestructura or "No especificado", self.styles['Valor'])],
            [Paragraph("<b>Materiales:</b>", self.styles['Etiqueta']), 
             Paragraph(hab.materiales or "No especificado", self.styles['Valor']),
             Paragraph("<b>Transporte:</b>", self.styles['Etiqueta']), 
             Paragraph(hab.acceso_transporte or "No especificado", self.styles['Valor'])],
        ]

        table = Table(data, colWidths=[3.5*cm, 5*cm, 3.5*cm, 5*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, GRIS_MEDIO),
            ('BACKGROUND', (0, 0), (0, -1), GRIS_CLARO),
            ('BACKGROUND', (2, 0), (2, -1), GRIS_CLARO),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))

        elements = [table, Spacer(1, 8)]

        # Servicios
        servicios_data = [
            [Paragraph("<b>SERVICIOS BÁSICOS</b>", self.styles['Etiqueta']),
             Paragraph("<b>Estado</b>", self.styles['Etiqueta'])],
            [Paragraph("Agua Potable:", self.styles['Valor']),
             Paragraph("Sí" if hab.agua_potable else "No", self.styles['Valor'])],
            [Paragraph("Electricidad:", self.styles['Valor']),
             Paragraph("Sí" if hab.electricidad else "No", self.styles['Valor'])],
            [Paragraph("Gas:", self.styles['Valor']),
             Paragraph("Sí" if hab.gas else "No", self.styles['Valor'])],
            [Paragraph("Cloacas:", self.styles['Valor']),
             Paragraph("Sí" if hab.cloacas else "No", self.styles['Valor'])],
        ]

        serv_table = Table(servicios_data, colWidths=[6*cm, 6*cm])
        serv_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, GRIS_MEDIO),
            ('BACKGROUND', (0, 0), (-1, 0), AZUL),
            ('TEXTCOLOR', (0, 0), (-1, 0), BLANCO),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(serv_table)

        if hab.equipamiento_barrio:
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"<b>Equipamiento del Barrio:</b> {hab.equipamiento_barrio}", self.styles['Valor']))

        return elements

    def _create_salud_educacion_table(self, se):
        """Tabla de salud y educación."""
        data = [
            [Paragraph("<b>SALUD</b>", self.styles['Etiqueta']), 
             "", 
             Paragraph("<b>EDUCACIÓN</b>", self.styles['Etiqueta']), 
             ""],
            [Paragraph("Enfermedades Crónicas:", self.styles['Valor']), 
             Paragraph(se.enfermedades_cronicas or "No especificado", self.styles['Valor']),
             Paragraph("Nivel Académico:", self.styles['Valor']), 
             Paragraph(se.nivel_academico or "No especificado", self.styles['Valor'])],
            [Paragraph("Discapacidades:", self.styles['Valor']), 
             Paragraph(se.discapacidades or "No especificado", self.styles['Valor']),
             Paragraph("Asistencia Escolar:", self.styles['Valor']), 
             Paragraph(se.asistencia_escolar or "No especificado", self.styles['Valor'])],
            [Paragraph("Dependencia:", self.styles['Valor']), 
             Paragraph(se.situacion_dependencia or "No especificado", self.styles['Valor']),
             Paragraph("Escolaridad Menores:", self.styles['Valor']), 
             Paragraph(se.escolaridad_menores or "No especificado", self.styles['Valor'])],
            [Paragraph("Adicciones:", self.styles['Valor']), 
             Paragraph(se.adicciones or "No especificado", self.styles['Valor']),
             "", ""],
            [Paragraph("Cobertura Salud:", self.styles['Valor']), 
             Paragraph(se.cobertura_salud or "No especificado", self.styles['Valor']),
             "", ""],
        ]

        table = Table(data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, GRIS_MEDIO),
            ('BACKGROUND', (0, 0), (1, 0), GRIS_CLARO),
            ('BACKGROUND', (2, 0), (3, 0), GRIS_CLARO),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        return table

    def _create_diagnostico_content(self, diag):
        """Contenido del diagnóstico."""
        elements = []

        if diag.juicio_tecnico:
            elements.append(Paragraph("<b>7.1 JUICIO TÉCNICO PROFESIONAL</b>", self.styles['Etiqueta']))
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(diag.juicio_tecnico, self.styles['TextoNormal']))
            elements.append(Spacer(1, 12))

        if diag.vulnerabilidades:
            elements.append(Paragraph("<b>7.2 VULNERABILIDADES IDENTIFICADAS</b>", self.styles['Etiqueta']))
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(diag.vulnerabilidades, self.styles['TextoNormal']))
            elements.append(Spacer(1, 12))

        if diag.fortalezas:
            elements.append(Paragraph("<b>7.3 FORTALEZAS IDENTIFICADAS</b>", self.styles['Etiqueta']))
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(diag.fortalezas, self.styles['TextoNormal']))
            elements.append(Spacer(1, 12))

        if diag.propuesta_intervencion:
            elements.append(Paragraph("<b>7.4 PROPUESTA DE INTERVENCIÓN</b>", self.styles['Etiqueta']))
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(diag.propuesta_intervencion, self.styles['TextoNormal']))
            elements.append(Spacer(1, 12))

        if diag.recursos_solicitados:
            elements.append(Paragraph("<b>7.5 RECURSOS SOLICITADOS</b>", self.styles['Etiqueta']))
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(diag.recursos_solicitados, self.styles['TextoNormal']))
            elements.append(Spacer(1, 12))

        if diag.plazo_intervencion:
            elements.append(Paragraph(f"<b>Plazo de Intervención:</b> {diag.plazo_intervencion}", self.styles['Valor']))

        if diag.seguimiento:
            elements.append(Paragraph(f"<b>Seguimiento Propuesto:</b> {diag.seguimiento}", self.styles['Valor']))

        if not elements:
            elements.append(Paragraph("No se ha registrado diagnóstico social.", self.styles['Nota']))

        return elements

    def _create_firma_section(self):
        """Sección de firma."""
        firma_data = [
            ["", ""],
            ["______________________________", "______________________________"],
            ["Firma del Profesional", "Firma del Usuario/Representante"],
            ["", ""],
            ["Aclaración:", "Aclaración:"],
        ]

        firma_table = Table(firma_data, colWidths=[7*cm, 7*cm])
        firma_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        return firma_table
