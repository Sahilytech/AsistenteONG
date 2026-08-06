"""
Ventana principal mejorada - Interfaz profesional
Sarah Lee Olivera - Asistente ONG
"""

import customtkinter as ctk
import logging
from pathlib import Path
from PIL import Image

from .case_input import CaseInputFrame
from .results_panel import ResultsFrame
from .resources_panel import ResourcesPanel
from .dashboard import DashboardPanel
from .branding import BRAND_COLORS, AUTHOR_BIO
from .styles import FONTS

logger = logging.getLogger(__name__)

# Tema global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AboutPanel(ctk.CTkFrame):
    """Panel con información sobre Sarah Lee Olivera."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura panel de información."""
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=15, pady=15)
        
        # FOTO DE SARAH
        try:
            img_path = Path(__file__).parent.parent.parent / "assets" / "sarah.jpg"
            if img_path.exists():
                pil_img = Image.open(img_path).resize((200, 250), Image.Resampling.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=pil_img, size=(200, 250))
                
                photo_label = ctk.CTkLabel(scroll, image=ctk_img, text="")
                photo_label.image = ctk_img
                photo_label.pack(pady=10)
        except Exception as e:
            logger.warning(f"No se pudo cargar foto: {e}")
        
        # Título
        title = ctk.CTkLabel(
            scroll,
            text="👩‍💻 Sobre Sarah",
            font=("Helvetica", 18, "bold"),
            text_color=BRAND_COLORS["primary"]
        )
        title.pack(anchor="w", pady=(10, 10))
        
        # Nombre
        name = ctk.CTkLabel(
            scroll,
            text=AUTHOR_BIO["name"],
            font=("Helvetica", 16, "bold")
        )
        name.pack(anchor="w")
        
        # Título
        role = ctk.CTkLabel(
            scroll,
            text=AUTHOR_BIO["title"],
            font=("Helvetica", 12),
            text_color="#AAAAAA"
        )
        role.pack(anchor="w")
        
        # Email
        email = ctk.CTkLabel(
            scroll,
            text=f"📧 {AUTHOR_BIO['email']}",
            font=("Helvetica", 11),
            text_color=BRAND_COLORS["primary"]
        )
        email.pack(anchor="w", pady=(5, 15))
        
        # Biografía
        bio = ctk.CTkLabel(
            scroll,
            text=AUTHOR_BIO["bio"],
            font=("Helvetica", 11),
            justify="left",
            wraplength=320
        )
        bio.pack(anchor="w", pady=10)
        
        # Separador
        sep = ctk.CTkFrame(scroll, height=1, fg_color="#333333")
        sep.pack(fill="x", pady=15)
        
        # Disclaimer
        disclaimer = ctk.CTkLabel(
            scroll,
            text="⚖️ Código abierto orientado al bien común.\nNunca reemplaza el criterio humano.",
            font=("Helvetica", 10),
            text_color="#999999",
            justify="left",
            wraplength=320
        )
        disclaimer.pack(anchor="w")


class MainWindow:
    """Ventana principal profesional."""
    
    def __init__(self):
        """Inicializa la ventana."""
        self.root = ctk.CTk()
        self.root.title("🆘 Asistente ONG - Triaje y Canalización")
        self.root.geometry("1900x900")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.current_theme = "dark"
        self.results = None
        
        logger.info("✅ Ventana principal inicializada")
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura interfaz completa."""
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=0)
        
        # --- SIDEBAR IZQUIERDO (Input) ---
        left_sidebar = ctk.CTkFrame(main_frame, width=400, fg_color="#0d0d0d")
        left_sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        left_sidebar.grid_rowconfigure(1, weight=1)
        
        # LOGO + Branding
        header_frame = ctk.CTkFrame(left_sidebar, fg_color="transparent")
        header_frame.pack(pady=15, padx=15, fill="x")
        
        # Logo
        try:
            logo_path = Path(__file__).parent.parent.parent / "assets" / "logo_g.png"
            if logo_path.exists():
                logo_img = Image.open(logo_path).resize((50, 50), Image.Resampling.LANCZOS)
                ctk_logo = ctk.CTkImage(light_image=logo_img, size=(50, 50))
                logo_label = ctk.CTkLabel(header_frame, image=ctk_logo, text="")
                logo_label.image = ctk_logo
                logo_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            logger.warning(f"Logo no cargado: {e}")
        
        # Texto header
        header_text = ctk.CTkLabel(
            header_frame,
            text="🆘 Asistente ONG",
            font=("Helvetica", 16, "bold"),
            text_color=BRAND_COLORS["primary"],
            justify="left"
        )
        header_text.pack(side="left", anchor="w")
        
        # Panel de entrada
        self.case_input = CaseInputFrame(
            left_sidebar,
            on_submit=self._on_case_submit,
            fg_color="#0d0d0d"
        )
        self.case_input.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Footer sidebar
        footer = ctk.CTkLabel(
            left_sidebar,
            text="v0.7.0 - Beta\nSarah Lee Olivera ©2025",
            font=("Helvetica", 9),
            text_color="#666666",
            justify="center"
        )
        footer.pack(pady=10, padx=10)
        
        # --- PANEL CENTRAL (Resultados) ---
        center_panel = ctk.CTkFrame(main_frame)
        center_panel.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        center_panel.grid_rowconfigure(0, weight=1)
        center_panel.grid_columnconfigure(0, weight=1)
        
        self.results = ResultsFrame(center_panel, fg_color="#161b22")
        self.results.grid(row=0, column=0, sticky="nsew")
        
        # --- SIDEBAR DERECHO (Tabs) ---
        right_sidebar = ctk.CTkFrame(main_frame, width=450, fg_color="#0d0d0d")
        right_sidebar.grid(row=0, column=2, sticky="nsew", padx=0, pady=0)
        right_sidebar.grid_rowconfigure(1, weight=1)
        
        # Botón theme toggle
        theme_btn = ctk.CTkButton(
            right_sidebar,
            text="🌓 Cambiar tema",
            command=self._toggle_theme,
            fg_color=BRAND_COLORS["primary"],
            text_color="white",
            font=("Helvetica", 12, "bold")
        )
        theme_btn.pack(pady=10, padx=15, fill="x")
        
        # Tabs
        self.tab_view = ctk.CTkTabview(right_sidebar, fg_color="#0d0d0d")
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Inicio
        inicio_tab = self.tab_view.add("📖 Inicio")
        self.dashboard = DashboardPanel(inicio_tab, fg_color="#0d0d0d")
        self.dashboard.pack(fill="both", expand=True)
        
        # Tab 2: Recursos
        resources_tab = self.tab_view.add("🔍 Recursos")
        self.resources_panel = ResourcesPanel(resources_tab, fg_color="#0d0d0d")
        self.resources_panel.pack(fill="both", expand=True)
        
        # Tab 3: Sobre Sarah
        about_tab = self.tab_view.add("👩‍💻 Sobre Sarah")
        self.about_panel = AboutPanel(about_tab, fg_color="#0d0d0d")
        self.about_panel.pack(fill="both", expand=True)
        
        logger.info("✅ UI COMPLETA")
    
    def _on_case_submit(self, case_number: str, case_text: str):
        """Maneja envío de caso."""
        try:
            logger.info(f"📋 Caso recibido: {case_number}")
            
            if not self.results:
                logger.error("❌ Results panel no inicializado")
                return
            
            logger.info(f"✅ Analizando: {case_number}")
            self.results.show_analysis(case_number, case_text)
            
        except Exception as e:
            logger.error(f"❌ Error en _on_case_submit: {e}", exc_info=True)
    
    def _toggle_theme(self):
        """Cambia entre temas."""
        try:
            if self.current_theme == "dark":
                ctk.set_appearance_mode("light")
                self.current_theme = "light"
            else:
                ctk.set_appearance_mode("dark")
                self.current_theme = "dark"
            logger.info(f"🌓 Tema: {self.current_theme}")
        except Exception as e:
            logger.error(f"Error en tema: {e}")
    
    def run(self):
        """Inicia la aplicación."""
        logger.info("🚀 Iniciando aplicación...")
        self.root.mainloop()
    
    def close(self):
        """Cierra la aplicación."""
        self.root.quit()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
