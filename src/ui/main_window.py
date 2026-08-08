"""
Ventana principal PROFESIONAL v0.9 - Asistente ONG
Sarah Lee Olivera - Herramienta Offline 100% para ONGs
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
from .branding import BRAND_COLORS, PROJECT_INFO
from .styles import COLORS, FONTS, SPACING, get_theme_colors, set_theme, get_current_theme

logger = logging.getLogger(__name__)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AboutPanel(ctk.CTkFrame):
    """Panel con información del proyecto (SIN foto personal)."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._setup_ui()

    def _setup_ui(self):
        """Configura panel About sin foto."""
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=15, pady=15)

        # Título
        ctk.CTkLabel(
            scroll,
            text="🆘 Asistente ONG",
            font=("Helvetica", 22, "bold"),
            text_color=BRAND_COLORS["primary"]
        ).pack(anchor="w", pady=(0, 5))

        ctk.CTkLabel(
            scroll,
            text=PROJECT_INFO["subtitle"],
            font=("Helvetica", 14),
            text_color="#AAAAAA"
        ).pack(anchor="w", pady=(0, 15))

        # Descripción
        ctk.CTkLabel(
            scroll,
            text=PROJECT_INFO["description"],
            font=("Helvetica", 11),
            justify="left",
            wraplength=350
        ).pack(anchor="w", pady=10)

        # Separador
        ctk.CTkFrame(scroll, height=1, fg_color="#333333").pack(fill="x", pady=15)

        # CCOMUSOC
        ctk.CTkLabel(
            scroll,
            text="🤝 Apoyado por CCOMUSOC",
            font=("Helvetica", 12, "bold"),
            text_color=BRAND_COLORS["primary"]
        ).pack(anchor="w", pady=(0, 5))

        ctk.CTkLabel(
            scroll,
            text="Cooperativa de Tecnología Social",
            font=("Helvetica", 10),
            text_color="#999999"
        ).pack(anchor="w", pady=(0, 15))

        # Separador
        ctk.CTkFrame(scroll, height=1, fg_color="#333333").pack(fill="x", pady=15)

        # Disclaimer
        ctk.CTkLabel(
            scroll,
            text="⚖️ Este software:\n• Es código abierto\n• Orientado al bien común\n• Nunca reemplaza criterio humano\n• Protege la privacidad 100%",
            font=("Helvetica", 10),
            text_color="#999999",
            justify="left",
            wraplength=350
        ).pack(anchor="w")


class MainWindow:
    """Ventana principal - Interfaz profesional completa."""

    def __init__(self):
        """Inicializa."""
        self.root = ctk.CTk()
        self.root.title("🆘 Asistente ONG v0.9 | Offline 100%")
        self.root.geometry("2000x950")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.current_theme = "dark"

        logger.info("🚀 Inicializando MainWindow v0.9...")
        self._setup_ui()

    def _setup_ui(self):
        """Configura UI completa con 6 tabs."""

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
            text="🆘 Asistente ONG\nv0.9 - PROFESIONAL",
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
            text="OFFLINE 100%\nSin conexión a internet\nDatos protegidos localmente",
            font=("Helvetica", 9),
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
            text="🌓 Cambiar Tema",
            command=self._toggle_theme,
            fg_color=BRAND_COLORS["primary"],
            text_color="white",
            width=150
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

        # Tab 5: AYUDA
        help_tab = self.tab_view.add("❓ Ayuda")
        self.help = HelpPanel(help_tab, fg_color="#0d0d0d")
        self.help.pack(fill="both", expand=True)

        # Tab 6: Acerca de
        about_tab = self.tab_view.add("ℹ️ Acerca de")
        self.about = AboutPanel(about_tab, fg_color="#0d0d0d")
        self.about.pack(fill="both", expand=True)

        logger.info("✅ UI PROFESIONAL COMPLETADA v0.9")

    def _on_case_submit(self, case_number: str, case_text: str):
        """Procesa nuevo caso."""
        try:
            logger.info(f"📋 Caso ingresado: {case_number}")

            # Mostrar análisis
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

            logger.info("✅ Caso procesado exitosamente")

        except Exception as e:
            logger.error(f"❌ Error: {e}", exc_info=True)

    def _toggle_theme(self):
        """Cambia tema claro/oscuro con colores completos."""
        if self.current_theme == "dark":
            ctk.set_appearance_mode("light")
            set_theme("light")
            self.current_theme = "light"
            self._apply_light_theme()
        else:
            ctk.set_appearance_mode("dark")
            set_theme("dark")
            self.current_theme = "dark"
            self._apply_dark_theme()
        logger.info(f"🌓 Tema: {self.current_theme}")

    def _apply_light_theme(self):
        """Aplica colores de tema claro a todos los widgets."""
        colors = get_theme_colors()
        try:
            self.root.configure(fg_color=colors["background"])
        except:
            pass

    def _apply_dark_theme(self):
        """Aplica colores de tema oscuro."""
        try:
            self.root.configure(fg_color="#0d0d0d")
        except:
            pass

    def run(self):
        """Ejecuta aplicación."""
        logger.info("🚀 Aplicación iniciada...")
        self.root.mainloop()

    def close(self):
        """Cierra aplicación."""
        self.root.quit()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
