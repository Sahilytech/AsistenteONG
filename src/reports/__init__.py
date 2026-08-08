"""
Módulo de reportes e informes sociales
"""

from .social_report import InformeSocial, InformeManager, MiembroFamiliar
from .pdf_generator import PDFGenerator
from .report_panel import ReportPanel

__all__ = ['InformeSocial', 'InformeManager', 'MiembroFamiliar', 'PDFGenerator', 'ReportPanel']
