"""
Ventana principal - COMPLETAMENTE INTEGRADA Y FUNCIONAL
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
from .help_panel import HelpPanel
from .branding import BRAND_COLORS
from .styles import COLORS, FONTS

from ..case_manager import CaseManager
from ..config_manager import ConfigManager

logger = logging.getLogger(__name__)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AboutPanel(ctk.CTkFrame):
    """Panel de creadora - SIN FOTO."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura panel."""
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            scroll,
            text="👩‍💻 Sarah Lee Olivera",
            font=FONTS["heading"],
            text_color=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 10))
        
        ctk.CTkLabel(
            scroll,
            text="Desarrolladora & Creadora",
            font=("Helvetica", 12),
            text_color=COLORS["text_muted"]
        ).pack(anchor="w", pady=(0, 5))
        
        ctk.CTkLabel(
            scroll,
            text="📧 sarahleeoliveraok@gmail.com",
            font=("Helvetica", 11),
            text_color=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 20))
        
        bio_text = """Desarrolladora comprometida con crear tecnología para el bien común. Este proyecto es una herramienta offline para organizaciones sociales que protege privacidad.

🤝 Apoyado por CCOMUSOC (ccomusoc.com.ar)

✅ Código abierto
✅ 100% Offline
✅ Privacidad garantizada
✅ Licencia Social Ética 2026"""
        
        ctk.CTkLabel(
            scroll,
            text=bio_text,
            font=("Helvetica", 10),
            justify="left",
            text_color=COLORS["text"],
            wraplength=350
        ).pack(anchor="w", pady=10)


class MainWindow:
    """Ventana principal."""
    
    def __init__(self):
        """Inicializa."""
        self.root = ctk.CTk()
        self.root.title("🆘 Asistente ONG v0.9 | Sarah Lee Olivera | Offline 100%")
        self.root.geometry("2000x950")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.case_manager = CaseManager()
        self.config_manager = ConfigManager()
        self.current_theme = "dark"
        
        logger.info("🚀 MainWindow inicializando...")
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura UI."""
        
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # SIDEBAR IZQUIERDO
        left_sidebar = ctk.CTkFrame(main_frame, width=420, fg_color=COLORS["background"])
        left_sidebar.grid(row=0, column=0, sticky="nsew")
        left_sidebar.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkFrame(left_sidebar, fg_color="transparent")
        header.pack(pady=15, padx=15, fill="x")
        
        # Logo
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
            text="🆘 Asistente ONG\nv0.9 Sarah Lee",
            font=FONTS["heading"],
            text_color=COLORS["primary"],
            justify="left"
        ).pack(side="left", anchor="w")
        
        # Ingreso de casos
        self.case_input = CaseInputFrame(
            left_sidebar,
            on_submit=self._on_case_submit,
            fg_color=COLORS["background"]
        )
        self.case_input.pack(fill="both", expand=True)
        
        # Footer
        ctk.CTkLabel(
            left_sidebar,
            text="OFFLINE 100%\nv0.9 Profesional",
            font=("Helvetica", 9),
            text_color=COLORS["text_muted"],
            justify="center"
        ).pack(pady=10)
        
        # PANEL CENTRAL
        center_panel = ctk.CTkFrame(main_frame)
        center_panel.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        center_panel.grid_rowconfigure(1, weight=1)
        
        # Toolbar
        toolbar = ctk.CTkFrame(center_panel, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(
            toolbar,
            text="🌓 Tema",
            command=self._toggle_theme,
            fg_color=COLORS["primary"],
            text_color="white",
            width=100
        ).pack(side="left", padx=(0, 10))
        
        # Tabs
        self.tab_view = ctk.CTkTabview(center_panel, fg_color=COLORS["surface"])
        self.tab_view.pack(fill="both", expand=True)
        
        # Dashboard
        dashboard_tab = self.tab_view.add("📊 Dashboard")
        self.dashboard = DashboardFrame(dashboard_tab, case_manager=self.case_manager, fg_color=COLORS["background"])
        self.dashboard.pack(fill="both", expand=True)
        
        # Análisis
        analysis_tab = self.tab_view.add("📋 Análisis")
        self.results = ResultsFrame(analysis_tab, config_manager=self.config_manager, fg_color=COLORS["surface"])
        self.results.pack(fill="both", expand=True)
        
        # Recursos
        resources_tab = self.tab_view.add("📞 Recursos")
        self.resources = ResourcesPanel(resources_tab, fg_color=COLORS["background"])
        self.resources.pack(fill="both", expand=True)
        
        # Config
        config_tab = self.tab_view.add("⚙️ Config")
        self.config = ConfigPanel(config_tab, fg_color=COLORS["background"])
        self.config.pack(fill="both", expand=True)
        
        # Ayuda
        help_tab = self.tab_view.add("❓ Ayuda")
        self.help = HelpPanel(help_tab, fg_color=COLORS["background"])
        self.help.pack(fill="both", expand=True)
        
        # Creadora
        about_tab = self.tab_view.add("👩‍💻 Creadora")
        self.about = AboutPanel(about_tab, fg_color=COLORS["background"])
        self.about.pack(fill="both", expand=True)
        
        logger.info("✅ UI COMPLETAMENTE INTEGRADA")
    
    def _on_case_submit(self, case_number: str, case_text: str):
        """Procesa caso."""
        try:
            logger.info(f"📋 Analizando: {case_text[:50]}")
            
            # Analizar
            analysis = self.config_manager.analyze(case_text)
            
            # Crear caso
            case = self.case_manager.create_case(
                text=case_text,
                urgency=analysis["urgency"],
                keywords=analysis["keywords"]
            )
            
            # Mostrar resultados
            self.results.show_analysis(case.case_number, case_text, analysis)
            
            # Actualizar dashboard
            self.dashboard.update_stats(
                analysis["urgency"],
                "general",
                case.case_number
            )
            
            # Cambiar a tab Análisis
            self.tab_view.set("📋 Análisis")
            
            logger.info(f"✅ Caso {case.case_number} procesado")
            
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
        """Ejecuta."""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
