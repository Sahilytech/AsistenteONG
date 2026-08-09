"""Ayuda, atajos y tutorial interactivo."""
import customtkinter as ctk
from .styles import COLORS, FONTS
from .onboarding import show_tutorial

class HelpPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._setup_ui()

    def _setup_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=22)
        ctk.CTkLabel(scroll, text="Ayuda", font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(scroll, text="Aprendé el recorrido, consultá los atajos y entendé qué hace cada parte del sistema.", font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=900).pack(anchor="w", pady=(3,16))
        ctk.CTkButton(scroll, text="Abrir tutorial interactivo", height=46, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"], command=lambda: show_tutorial(self.winfo_toplevel())).pack(anchor="w", pady=(0,18))

        self._section(scroll, "Atajos de teclado", [
            ("Ctrl + N", "Crear un nuevo caso"),
            ("Ctrl + K", "Ir rápidamente a búsqueda"),
            ("Ctrl + B", "Abrir Biblioteca"),
            ("Esc", "Cerrar el diálogo activo"),
        ])
        self._section(scroll, "Cómo empezar", [
            ("Inicio", "El panel principal muestra solamente tus propios datos. Si está vacío, todavía no cargaste información."),
            ("Casos", "Creá un expediente desde Nuevo caso. Escribí solamente la información necesaria y revisala antes de analizar."),
            ("Biblioteca", "Importá PDFs desde Biblioteca y usá Recargar carpeta cuando agregues documentación. Los PDFs con texto se procesan localmente."),
            ("Análisis", "Las reglas locales generan orientación y señales para revisión. Una coincidencia documental no se considera automáticamente una verdad."),
            ("Seguimiento", "Registrá acciones, responsables y fechas. La Agenda reúne las fechas guardadas."),
            ("Seguridad", "Revisá el estado de almacenamiento y las funciones que pueden utilizar conectividad externa."),
        ])
        self._section(scroll, "Importante", [
            ("Privacidad", "Los casos y documentos se almacenan localmente. No compartas información sensible fuera de los canales autorizados por tu organización."),
            ("Revisión humana", "El sistema es una herramienta de apoyo. No reemplaza profesionales ni decide por sí solo medidas legales, sanitarias o de protección."),
        ])

    def _section(self, parent, title, items):
        ctk.CTkLabel(parent, text=title, font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", pady=(12,6))
        for heading, text in items:
            card = ctk.CTkFrame(parent, fg_color=COLORS["surface_alt"], corner_radius=14, border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", pady=4)
            ctk.CTkLabel(card, text=heading, font=FONTS["small_bold"], text_color=COLORS["primary"], anchor="w").pack(fill="x", padx=18, pady=(11,2))
            ctk.CTkLabel(card, text=text, font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=900, justify="left", anchor="w").pack(fill="x", padx=18, pady=(0,12))
