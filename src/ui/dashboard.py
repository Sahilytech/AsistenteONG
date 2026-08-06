"""
Dashboard principal - Información del proyecto y estado
"""

import customtkinter as ctk
from .styles import COLORS, FONTS, SPACING

PROJECT_INFO = {
    "title": "🆘 Asistente ONG",
    "subtitle": "Caja de Herramientas para Líneas de Ayuda",
    "version": "v0.7.0 - Beta",
    
    "problem": """
    💔 EL PROBLEMA REAL:
    Las pequeñas organizaciones sociales que atienden violencia de género, 
    derechos humanos y asesoría legal reciben DECENAS de mensajes desesperados.
    
    Sin recursos suficientes, se colapsan. La información sensible viaja por 
    internet. El tiempo es crítico.
    """,
    
    "solution": """
    ⚡ LA SOLUCIÓN:
    Una herramienta en un PENDRIVE que:
    
    ✓ Funciona OFFLINE 100% (privacidad garantizada)
    ✓ Clasifica urgencias automáticamente (riesgo de vida, menores)
    ✓ Detecta palabras clave de peligro
    ✓ Redacta respuestas borrador legales
    ✓ Acceso a base de datos local de emergencias
    ✓ Sin conexión a internet (datos seguros)
    ✓ Opera sin requisitos técnicos avanzados
    """,
    
    "how_it_works": """
    🔧 CÓMO FUNCIONA:
    
    1. Recibir: Operador ingresa mensaje/transcripción de víctima
    2. Analizar: Sistema detecta palabras clave de urgencia
    3. Clasificar: Asigna nivel de urgencia (Muy Alta/Alta/Media/Baja)
    4. Sugerir: Recomienda recursos locales (hospitales, abogados, refugios)
    5. Redactar: Genera respuesta borrador con pasos legales
    6. Responder: Operador revisa y envía (criterio humano siempre)
    
    ⏱️ Todo en <500ms. 100% local.
    """,
    
    "features": [
        "🎯 Detección de Urgencias (IA local, reglas)",
        "📞 Base de Datos de Emergencias Actualizada",
        "📝 Redactor Automático de Respuestas",
        "🔐 Cifrado AES-256 (datos en reposo)",
        "👤 Autenticación (acceso protegido)",
        "📊 Auditoría Completa (registro de acciones)",
        "🌍 Soporte Multi-Región (CABA, GBA, etc)",
        "🌓 Tema Claro/Oscuro",
        "⚙️ Configurable para cada ONG",
        "📦 Distribución en Pendrive"
    ]
}


class DashboardPanel(ctk.CTkFrame):
    """Panel de dashboard con información del proyecto."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura el dashboard."""
        
        # Scroll principal
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=SPACING["md"], pady=SPACING["md"])
        
        # Título
        title = ctk.CTkLabel(
            scroll,
            text=PROJECT_INFO["title"],
            font=("Helvetica", 24, "bold"),
            text_color=COLORS["primary"]
        )
        title.pack(anchor="w", pady=(0, 5))
        
        # Subtítulo
        subtitle = ctk.CTkLabel(
            scroll,
            text=PROJECT_INFO["subtitle"],
            font=("Helvetica", 14),
            text_color=COLORS["text_muted"]
        )
        subtitle.pack(anchor="w", pady=(0, SPACING["md"]))
        
        # Versión
        version = ctk.CTkLabel(
            scroll,
            text=PROJECT_INFO["version"],
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        )
        version.pack(anchor="w", pady=(0, SPACING["lg"]))
        
        # --- EL PROBLEMA ---
        self._create_section(scroll, PROJECT_INFO["problem"], COLORS["danger"])
        
        # --- LA SOLUCIÓN ---
        self._create_section(scroll, PROJECT_INFO["solution"], COLORS["primary"])
        
        # --- CÓMO FUNCIONA ---
        self._create_section(scroll, PROJECT_INFO["how_it_works"], COLORS["text"])
        
        # --- CARACTERÍSTICAS ---
        self._create_features_section(scroll)
        
        # Footer
        footer = ctk.CTkLabel(
            scroll,
            text="Desarrollado por Sarah Lee Olivera\nPara organizaciones que luchan por la justicia social",
            font=FONTS["small"],
            text_color=COLORS["text_muted"],
            justify="center"
        )
        footer.pack(pady=SPACING["lg"], anchor="center")
    
    def _create_section(self, parent, text: str, color: str):
        """Crea una sección de contenido."""
        
        section = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=10)
        section.pack(fill="x", pady=SPACING["md"])
        
        content = ctk.CTkLabel(
            section,
            text=text,
            font=FONTS["small"],
            text_color=color,
            justify="left",
            wraplength=600
        )
        content.pack(padx=SPACING["md"], pady=SPACING["md"], anchor="w")
    
    def _create_features_section(self, parent):
        """Crea sección de características."""
        
        features_title = ctk.CTkLabel(
            parent,
            text="✨ CARACTERÍSTICAS",
            font=FONTS["heading"],
            text_color=COLORS["primary"]
        )
        features_title.pack(anchor="w", pady=(SPACING["lg"], SPACING["sm"]))
        
        features_frame = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=10)
        features_frame.pack(fill="x", pady=(0, SPACING["md"]))
        
        for feature in PROJECT_INFO["features"]:
            feature_label = ctk.CTkLabel(
                features_frame,
                text=feature,
                font=FONTS["small"],
                text_color=COLORS["text"],
                justify="left"
            )
            feature_label.pack(anchor="w", padx=SPACING["md"], pady=SPACING["xs"])
