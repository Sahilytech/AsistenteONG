"""
Pantalla de inicio (Splash Screen)
Logo flotante, barra de carga ROSA, mini circuitos decorativos
Colores: Negro fondo, Azul #0e98d6 circuitos, Rosa #FF69B4 barra
"""

import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import threading
import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Colores
NEGRO = "#0d0d0d"
AZUL = "#0e98d6"
ROSA = "#FF69B4"
BLANCO = "#FFFFFF"
GRIS = "#333333"


class SplashScreen:
    """Pantalla de inicio profesional con animaciones."""

    def __init__(self, on_complete=None):
        """
        Args:
            on_complete: Callback cuando termina la carga
        """
        self.on_complete = on_complete
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Sin bordes
        self.root.attributes('-topmost', True)
        self.root.configure(bg=NEGRO)

        # Dimensiones
        self.width = 700
        self.height = 450

        # Centrar en pantalla
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - self.width) // 2
        y = (screen_h - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

        # Canvas principal
        self.canvas = Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg=NEGRO,
            highlightthickness=0
        )
        self.canvas.pack()

        # Dibujar elementos
        self._draw_circuits()
        self._draw_grid()
        self._load_logo()
        self._draw_text()
        self._create_progress_bar()

        # Animación de partículas
        self.particles = []
        self._create_particles()

        self.loading_complete = False
        self.current_progress = 0

        logger.info("🎬 Splash screen inicializado")

    def _draw_circuits(self):
        """Dibuja mini circuitos decorativos tipo PCB."""
        # Circuitos horizontales superiores
        for y in [30, 80]:
            # Línea principal
            self.canvas.create_line(50, y, 650, y, fill=AZUL, width=1)
            # Nodos
            for x in range(50, 651, 80):
                self.canvas.create_oval(x-4, y-4, x+4, y+4, fill=AZUL, outline="")
                # Ramificaciones pequeñas
                if x % 160 == 50:
                    self.canvas.create_line(x, y, x, y+25, fill=AZUL, width=1)
                    self.canvas.create_oval(x-2, y+23, x+2, y+27, fill=AZUL, outline="")

        # Circuitos horizontales inferiores
        for y in [370, 420]:
            self.canvas.create_line(50, y, 650, y, fill=AZUL, width=1)
            for x in range(50, 651, 80):
                self.canvas.create_oval(x-4, y-4, x+4, y+4, fill=AZUL, outline="")
                if x % 160 == 50:
                    self.canvas.create_line(x, y, x, y-25, fill=AZUL, width=1)
                    self.canvas.create_oval(x-2, y-27, x+2, y-23, fill=AZUL, outline="")

        # Circuitos verticales laterales
        for x in [30, 670]:
            self.canvas.create_line(x, 50, x, 400, fill=AZUL, width=1)
            for y in range(50, 401, 70):
                self.canvas.create_oval(x-4, y-4, x+4, y+4, fill=AZUL, outline="")

        # Esquinas decorativas
        self._draw_corner(30, 30, 1, 1)    # Arriba izquierda
        self._draw_corner(670, 30, -1, 1)   # Arriba derecha
        self._draw_corner(30, 420, 1, -1)   # Abajo izquierda
        self._draw_corner(670, 420, -1, -1) # Abajo derecha

    def _draw_corner(self, x, y, dx, dy):
        """Dibuja una esquina decorativa de circuito."""
        size = 25
        self.canvas.create_line(x, y, x + size*dx, y, fill=AZUL, width=2)
        self.canvas.create_line(x, y, x, y + size*dy, fill=AZUL, width=2)
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=ROSA, outline="")

    def _draw_grid(self):
        """Dibuja grid sutil de fondo."""
        for x in range(0, self.width, 40):
            self.canvas.create_line(x, 0, x, self.height, fill="#1a1a1a", width=1)
        for y in range(0, self.height, 40):
            self.canvas.create_line(0, y, self.width, y, fill="#1a1a1a", width=1)

    def _load_logo(self):
        """Carga logo flotante."""
        try:
            # Buscar logo en assets
            logo_paths = [
                Path(__file__).parent.parent.parent / "assets" / "logo.png",
                Path(__file__).parent.parent.parent / "assets" / "logo_g.png",
                Path("assets/logo.png"),
                Path("assets/logo_g.png"),
            ]

            logo_path = None
            for path in logo_paths:
                if path.exists():
                    logo_path = path
                    break

            if logo_path:
                img = Image.open(logo_path).resize((140, 140), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                self.logo_id = self.canvas.create_image(
                    self.width//2, 170,
                    image=self.logo_img,
                    tags="logo"
                )
            else:
                # Logo placeholder si no hay imagen
                self.canvas.create_text(
                    self.width//2, 170,
                    text="🆘",
                    font=("Segoe UI Emoji", 80),
                    fill=AZUL,
                    tags="logo"
                )
        except Exception as e:
            logger.warning(f"No se pudo cargar logo: {e}")
            self.canvas.create_text(
                self.width//2, 170,
                text="🆘",
                font=("Segoe UI Emoji", 80),
                fill=AZUL,
                tags="logo"
            )

    def _draw_text(self):
        """Dibuja textos."""
        # Título principal
        self.canvas.create_text(
            self.width//2, 280,
            text="ASISTENTE ONG",
            font=("Helvetica", 28, "bold"),
            fill=BLANCO,
            tags="title"
        )

        # Subtítulo
        self.canvas.create_text(
            self.width//2, 315,
            text="Triaje y Canalización Profesional",
            font=("Helvetica", 12),
            fill=GRIS,
            tags="subtitle"
        )

        # Versión
        self.canvas.create_text(
            self.width//2, 340,
            text="v0.9 | Offline 100%",
            font=("Helvetica", 10),
            fill="#555555",
            tags="version"
        )

        # Texto de carga
        self.loading_text = self.canvas.create_text(
            self.width//2, 395,
            text="Inicializando...",
            font=("Helvetica", 10),
            fill=GRIS,
            tags="loading_text"
        )

    def _create_progress_bar(self):
        """Crea barra de progreso ROSA."""
        # Fondo de la barra
        bar_y = 365
        bar_height = 8
        self.canvas.create_rectangle(
            200, bar_y - bar_height//2,
            500, bar_y + bar_height//2,
            fill="#222222", outline="",
            tags="progress_bg"
        )

        # Barra de progreso (rosa)
        self.progress_bar = self.canvas.create_rectangle(
            200, bar_y - bar_height//2,
            200, bar_y + bar_height//2,
            fill=ROSA, outline="",
            tags="progress_bar"
        )

        # Brillo de la barra
        self.progress_glow = self.canvas.create_rectangle(
            200, bar_y - bar_height//2 - 2,
            200, bar_y + bar_height//2 + 2,
            fill="", outline=ROSA, width=1,
            tags="progress_glow"
        )

    def _create_particles(self):
        """Crea partículas flotantes decorativas."""
        import random
        for _ in range(15):
            x = random.randint(50, 650)
            y = random.randint(50, 400)
            size = random.randint(2, 4)
            particle = self.canvas.create_oval(
                x-size, y-size, x+size, y+size,
                fill=AZUL, outline="",
                stipple="gray50"
            )
            self.particles.append({
                "id": particle,
                "x": x, "y": y,
                "vx": random.uniform(-0.5, 0.5),
                "vy": random.uniform(-0.5, 0.5),
                "size": size
            })

    def _animate_particles(self):
        """Anima partículas flotantes."""
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]

            # Rebote en bordes
            if p["x"] < 30 or p["x"] > 670:
                p["vx"] *= -1
            if p["y"] < 30 or p["y"] > 420:
                p["vy"] *= -1

            self.canvas.coords(
                p["id"],
                p["x"] - p["size"], p["y"] - p["size"],
                p["x"] + p["size"], p["y"] + p["size"]
            )

        if not self.loading_complete:
            self.root.after(50, self._animate_particles)

    def update_progress(self, value: int, text: str = None):
        """Actualiza barra de progreso.

        Args:
            value: 0-100
            text: Texto opcional de estado
        """
        self.current_progress = value

        # Calcular ancho de la barra
        bar_width = (value / 100) * 300  # 300 = 500 - 200

        # Actualizar barra
        self.canvas.coords(
            self.progress_bar,
            200, 361,
            200 + bar_width, 369
        )

        # Actualizar glow
        self.canvas.coords(
            self.progress_glow,
            200, 359,
            200 + bar_width, 371
        )

        # Actualizar texto
        if text:
            self.canvas.itemconfig(self.loading_text, text=text)
        else:
            self.canvas.itemconfig(self.loading_text, text=f"Cargando... {value}%")

        self.root.update_idletasks()

    def start_loading(self):
        """Inicia secuencia de carga simulada."""
        def load_sequence():
            steps = [
                (10, "Inicializando base de datos..."),
                (25, "Cargando recursos..."),
                (40, "Verificando modelos IA..."),
                (55, "Cargando interfaz..."),
                (70, "Preparando componentes..."),
                (85, "Casi listo..."),
                (100, "¡Listo!"),
            ]

            for progress, text in steps:
                time.sleep(0.4)  # Simular carga
                self.root.after(0, lambda p=progress, t=text: self.update_progress(p, t))

            time.sleep(0.5)
            self.loading_complete = True

            # Cerrar splash y ejecutar callback
            self.root.after(100, self._finish)

        # Iniciar animación de partículas
        self._animate_particles()

        # Iniciar carga en thread separado
        thread = threading.Thread(target=load_sequence, daemon=True)
        thread.start()

    def _finish(self):
        """Finaliza splash screen."""
        self.root.destroy()
        if self.on_complete:
            self.on_complete()

    def run(self):
        """Ejecuta splash screen."""
        self.start_loading()
        self.root.mainloop()


def show_splash(on_complete=None):
    """Muestra splash screen y ejecuta callback al terminar.

    Args:
        on_complete: Función a ejecutar cuando termine la carga
    """
    splash = SplashScreen(on_complete=on_complete)
    splash.run()


if __name__ == "__main__":
    # Test standalone
    def on_done():
        print("✅ Carga completa!")

    show_splash(on_done)
