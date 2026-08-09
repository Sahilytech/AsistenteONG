"""
Ventana principal del Asistente ONG.
Interfaz de escritorio en modo claro, preparada para uso offline.
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
from .social_report_panel import SocialReportPanel
from .styles import COLORS, FONTS
from ..case_manager import CaseManager
from ..config_manager import ConfigManager

logger = logging.getLogger(__name__)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AboutPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=28, pady=24)
        ctk.CTkLabel(scroll, text="Acerca del proyecto", font=FONTS["title"], text_color=COLORS["primary"]).pack(anchor="w")
        ctk.CTkLabel(scroll, text="Asistente ONG · desarrollado con NubiWorks", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", pady=(5, 18))

        card = ctk.CTkFrame(scroll, fg_color=COLORS["surface"], corner_radius=12)
        card.pack(fill="x", pady=(0, 12))
        paragraphs = [
            "Mi nombre es Sarah Lee Olivera y soy una estudiante y desarrolladora de software de Argentina apasionada por crear tecnología con impacto social.",
            "Creo que la inteligencia artificial debe ser una herramienta para asistir a las personas, proteger su privacidad y facilitar el trabajo de quienes ayudan a otros. Por eso desarrollé este proyecto: una solución que funciona incluso sin conexión a Internet, pensada para que organizaciones sociales, fundaciones y equipos de asistencia puedan responder con mayor rapidez sin comprometer la confidencialidad de la información.",
            "Mi interés se centra en el desarrollo de aplicaciones, la inteligencia artificial local (offline), la accesibilidad y la creación de herramientas tecnológicas que puedan utilizarse en cualquier contexto, incluso donde los recursos son limitados.",
            "NubiWorks es mi proyecto y marca de tecnología, actualmente en proceso de formación. Este software es un proyecto de código abierto orientado al bien común. Su objetivo es apoyar el trabajo de profesionales y voluntarios, nunca reemplazar su criterio ni la atención humana.",
            "Gracias por utilizar esta herramienta y contribuir a que la tecnología pueda generar un impacto positivo en la sociedad.",
        ]
        for paragraph in paragraphs:
            ctk.CTkLabel(card, text=paragraph, font=FONTS["body"], text_color=COLORS["text"], justify="left", anchor="w", wraplength=920).pack(fill="x", padx=24, pady=(18, 0))
        ctk.CTkLabel(card, text="Sarah Lee Olivera", font=FONTS["heading"], text_color=COLORS["primary"]).pack(anchor="w", padx=24, pady=(22, 0))
        ctk.CTkLabel(card, text="Creadora y desarrolladora del proyecto · NubiWorks", font=FONTS["small"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=24, pady=(3, 22))
        ctk.CTkLabel(scroll, text="NubiWorks", font=("Helvetica", 20, "bold"), text_color=COLORS["primary"]).pack(anchor="center", pady=(16, 4))
        ctk.CTkLabel(scroll, text="Tecnología · IA offline · impacto social", font=FONTS["small"], text_color=COLORS["text_muted"]).pack(anchor="center")


class MainWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Asistente ONG | Triaje y Canalización")
        self.root.geometry("1500x900")
        self.root.minsize(1100, 700)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.case_manager = CaseManager()
        self.config_manager = ConfigManager()
        self._setup_ui()

    def _setup_ui(self):
        main_frame = ctk.CTkFrame(self.root, fg_color=COLORS["background"])
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        left_sidebar = ctk.CTkFrame(main_frame, width=350, fg_color=COLORS["background"])
        left_sidebar.grid(row=0, column=0, sticky="nsew")
        header = ctk.CTkFrame(left_sidebar, fg_color="transparent")
        header.pack(pady=15, padx=15, fill="x")
        try:
            logo_path = Path(__file__).parent.parent.parent / "assets" / "logo_g.png"
            if logo_path.exists():
                logo_img = Image.open(logo_path).resize((48, 48), Image.Resampling.LANCZOS)
                logo = ctk.CTkImage(light_image=logo_img, size=(48, 48))
                label = ctk.CTkLabel(header, image=logo, text="")
                label.image = logo
                label.pack(side="left", padx=(0, 10))
        except Exception:
            pass
        ctk.CTkLabel(header, text="Asistente ONG", font=FONTS["heading"], text_color=COLORS["primary"]).pack(side="left")
        self.case_input = CaseInputFrame(left_sidebar, on_submit=self._on_case_submit, fg_color=COLORS["background"])
        self.case_input.pack(fill="both", expand=True)
        ctk.CTkLabel(left_sidebar, text="OFFLINE 100%", font=FONTS["small"], text_color=COLORS["text_muted"]).pack(pady=10)
        center_panel = ctk.CTkFrame(main_frame, fg_color=COLORS["surface"])
        center_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        toolbar = ctk.CTkFrame(center_panel, fg_color="transparent")
        toolbar.pack(fill="x", padx=15, pady=(10, 5))
        ctk.CTkLabel(toolbar, text="Gestión de casos e informes", font=FONTS["heading"], text_color=COLORS["text"]).pack(side="left")
        self.tab_view = ctk.CTkTabview(center_panel, fg_color=COLORS["surface"])
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        dashboard_tab = self.tab_view.add("Dashboard")
        self.dashboard = DashboardFrame(dashboard_tab, case_manager=self.case_manager, fg_color=COLORS["background"])
        self.dashboard.pack(fill="both", expand=True)
        analysis_tab = self.tab_view.add("Análisis")
        self.results = ResultsFrame(analysis_tab, config_manager=self.config_manager, fg_color=COLORS["surface"])
        self.results.pack(fill="both", expand=True)
        report_tab = self.tab_view.add("Informe Social")
        self.social_report = SocialReportPanel(report_tab, fg_color=COLORS["background"])
        self.social_report.pack(fill="both", expand=True)
        resources_tab = self.tab_view.add("Recursos")
        self.resources = ResourcesPanel(resources_tab, fg_color=COLORS["background"])
        self.resources.pack(fill="both", expand=True)
        config_tab = self.tab_view.add("Configuración")
        self.config = ConfigPanel(config_tab, fg_color=COLORS["background"])
        self.config.pack(fill="both", expand=True)
        help_tab = self.tab_view.add("Ayuda")
        self.help = HelpPanel(help_tab, fg_color=COLORS["background"])
        self.help.pack(fill="both", expand=True)
        about_tab = self.tab_view.add("Acerca de")
        self.about = AboutPanel(about_tab, fg_color=COLORS["background"])
        self.about.pack(fill="both", expand=True)

    def _on_case_submit(self, case_number: str, case_text: str):
        try:
            analysis = self.config_manager.analyze(case_text)
            case = self.case_manager.create_case(text=case_text, urgency=analysis["urgency"], keywords=analysis["keywords"])
            self.results.show_analysis(case.case_number, case_text, analysis)
            self.dashboard.update_stats(analysis["urgency"], "general", case.case_number)
            self.tab_view.set("Análisis")
        except Exception as exc:
            logger.error("Error procesando caso: %s", exc, exc_info=True)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    MainWindow().run()
