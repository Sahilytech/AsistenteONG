"""
Ventana principal de la aplicación
Interfaz con CustomTkinter
"""

import customtkinter as ctk
import logging

logger = logging.getLogger(__name__)


class MainWindow:
    """Ventana principal de la aplicación."""
    
    def __init__(self):
        """Inicializa la ventana principal."""
        self.root = ctk.CTk()
        self.root.title("Asistente ONG - Triaje y Canalización")
        self.root.geometry("1200x700")
        
        logger.info("Ventana principal inicializada")
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario."""
        # Placeholder para UI
        label = ctk.CTkLabel(
            self.root, 
            text="Asistente de Triaje y Canalización\nv0.1.0",
            font=("Arial", 20, "bold")
        )
        label.pack(pady=20)
        
        subtitle = ctk.CTkLabel(
            self.root,
            text="Sistema en desarrollo...",
            font=("Arial", 12),
            text_color="gray"
        )
        subtitle.pack(pady=10)
    
    def run(self):
        """Inicia la aplicación."""
        logger.info("Iniciando UI...")
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
