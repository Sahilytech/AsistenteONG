"""
Ventana principal PROFESIONAL - Asistente ONG Completo
Sarah Lee Olivera - Herramienta para ONGs
"""

import customtkinter as ctk
import logging
from pathlib import Path
from PIL import Image

from .case_input import CaseInputFrame
from .results_panel import ResultsFrame
from .resources_panel import ResourcesPanel
from .dashboard import DashboardFrame
from .config_panel import ConfigPanel
from .branding import BRAND_COLORS, AUTHOR_BIO
from .styles import FONTS, COLORS

logger = logging.getLogger(__name__)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AboutPanel(ctk.CTkFrame):
    """Panel profesional con información de Sarah."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura panel About."""
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Foto de Sarah
        try:
            img_path = Path(__file__).parent.parent.parent / "assets" / "sarah.jpg"
            if img_path.exists():
                pil_img = Image.open(img_path).resize((180, 220), Image.Resampling.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=pil_img, size=(180, 220))
                photo = ctk.CTkLabel(scroll, image=ctk_img, text="")
                photo.image = ctk_img
                photo.pack(pady=15)
        except Exception as e:
            logger.warning(f"Foto no cargada: {e}")
        
        # Nombre
        ctk.CTkLabel(
            scroll,
            text=AUTHOR_BIO["name"],
            font=("Helvetica", 18, "bold"),
            text_color=BRAND_COLORS["primary"]
        ).pack(anchor="w", pady=(10, 0))
        
        # Título
        ctk.CTkLabel(
            scroll,
            text=AUTHOR_BIO["title"],
            font=("Helvetica", 11),
            text_color="#AAAAAA"
        ).pack(anchor="w")
        
        # Email
        ctk.CTkLabel(
            scroll,
            text=f"📧 {AUTHOR_BIO['email']}",
            font=("Helvetica", 10),
            text_color=BRAND_COLORS["primary"]
        ).pack(anchor="w", pady=(10, 15))
        
        # Biografía
        ctk.CTkLabel(
            scroll,
            text=AUTHOR_BIO["bio"],
            font=("Helvetica", 10),
            justify="left",
            wraplength=300
        ).pack(anchor="w", pady=10)
        
        # Separador
        ctk.CTkFrame(scroll, height=1, fg_color="#333333").pack(fill="x", pady=15)
        
        # Disclaimer
        ctk.CTkLabel(
            scroll,
            text="⚖️ Código abierto orientado al bien común.\nNunca reemplaza el criterio humano ni la atención profesional.",
            font=("Helvetica", 9),
            text_color="#999999",
            justify="left",
            wraplength=300
        ).pack(anchor="w")


class MainWindow:
    """Ventana principal - Interfaz completa profesional."""
    
    def __init__(self):
        """Inicializa."""
        self.root = ctk.CTk()
        self.root.title("🆘 Asistente ONG - Triaje y Canalización | Sarah Lee Olivera")
        self.root.geometry("2000x950")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.current_theme = "dark"
        
        logger.info("🚀 Inicializando MainWindow...")
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura UI completa."""
        
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # === SIDEBAR IZQUIERDO ===
        left_sidebar = ctk.CTkFrame(main_frame, width=420, fg_color="#0d0d0d")
        left_sidebar.grid(row=0, column=0, sticky="nsew")
        left_sidebar.grid_rowconfigure(1, weight=1)
        
        # Header con logo
        header = ctk.CTkFrame(left_sidebar, fg_color="transparent")
        header.pack(pady=15, padx=15, fill="x")
        
        try:
            logo_path = Path(__file__).parent.parent.parent / "assets" / "logo_g.png"
            if logo_path.exists():
                logo_img = Image.open(logo_path).resize((50, 50), Image.Resampling.LANCZOS)
                ctk_logo = ctk.CTkImage(light_image=logo_img, size=(50, 50))
                logo_label = ctk.CTkLabel(header, image=ctk_logo, text="")
                logo_label.image = ctk_logo
                logo_label.pack(side="left", padx=(0, 10))
        except:
            pass
        
        ctk.CTkLabel(
            header,
            text="🆘 Asistente ONG\nSarah Lee Olivera",
            font=("Helvetica", 14, "bold"),
            text_color=BRAND_COLORS["primary"],
            justify="left"
        ).pack(side="left", anchor="w")
        
        # Panel de entrada
        self.case_input = CaseInputFrame(
            left_sidebar,
            on_submit=self._on_case_submit,
            fg_color="#0d0d0d"
        )
        self.case_input.pack(fill="both", expand=True)
        
        # Footer
        ctk.CTkLabel(
            left_sidebar,
            text="v0.8.0 - Profesional\nSarah Lee Olivera ©2025",
            font=("Helvetica", 8),
            text_color="#666666",
            justify="center"
        ).pack(pady=10)
        
        # === PANEL CENTRAL CON TABS ===
        center_panel = ctk.CTkFrame(main_frame)
        center_panel.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        center_panel.grid_rowconfigure(1, weight=1)
        
        # Barra de herramientas
        toolbar = ctk.CTkFrame(center_panel, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 10))
        
        theme_btn = ctk.CTkButton(
            toolbar,
            text="🌓 Tema",
            command=self._toggle_theme,
            fg_color=BRAND_COLORS["primary"],
            text_color="white",
            width=80
        )
        theme_btn.pack(side="left", padx=(0, 10))
        
        # Tabs principales
        self.tab_view = ctk.CTkTabview(center_panel, fg_color="#161b22")
        self.tab_view.pack(fill="both", expand=True)
        
        # Tab 1: Dashboard
        dashboard_tab = self.tab_view.add("📊 Dashboard")
        self.dashboard = DashboardFrame(dashboard_tab, fg_color="#0d0d0d")
        self.dashboard.pack(fill="both", expand=True)
        
        # Tab 2: Análisis & Respuesta
        analysis_tab = self.tab_view.add("📋 Análisis")
        self.results = ResultsFrame(analysis_tab, fg_color="#161b22")
        self.results.pack(fill="both", expand=True)
        
        # Tab 3: Recursos
        resources_tab = self.tab_view.add("📞 Recursos")
        self.resources = ResourcesPanel(resources_tab, fg_color="#0d0d0d")
        self.resources.pack(fill="both", expand=True)
        
        # Tab 4: Configuración
        config_tab = self.tab_view.add("⚙️ Config")
        self.config = ConfigPanel(config_tab, fg_color="#0d0d0d")
        self.config.pack(fill="both", expand=True)
        
        # Tab 5: Sobre Sarah
        about_tab = self.tab_view.add("👩‍💻 Creadora")
        self.about = AboutPanel(about_tab, fg_color="#0d0d0d")
        self.about.pack(fill="both", expand=True)
        
        logger.info("✅ UI completamente configurada")
    
    def _on_case_submit(self, case_number: str, case_text: str):
        """Procesa nuevo caso."""
        try:
            logger.info(f"📋 Nuevo caso: {case_number}")
            
            # Mostrar en Análisis
            self.results.show_analysis(case_number, case_text)
            
            # Cambiar a tab de Análisis
            self.tab_view.set("📋 Análisis")
            
            # Actualizar Dashboard
            analysis = self.results.current_case
            if analysis:
                self.dashboard.update_stats(
                    analysis.get("urgency", "Baja"),
                    "general",
                    case_number
                )
            
            logger.info("✅ Caso procesado")
            
        except Exception as e:
            logger.error(f"❌ Error: {e}", exc_info=True)
    
    def _toggle_theme(self):
        """Cambia tema."""
        if self.current_theme == "dark":
            ctk.set_appearance_mode("light")
            self.current_theme = "light"
        else:
            ctk.set_appearance_mode("dark")
            self.current_theme = "dark"
        logger.info(f"🌓 Tema: {self.current_theme}")
    
    def run(self):
        """Ejecuta aplicación."""
        logger.info("🚀 Ejecutando app...")
        self.root.mainloop()
    
    def close(self):
        """Cierra aplicación."""
        self.root.quit()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
