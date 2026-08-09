"""Pantalla de inicio del Asistente ONG."""

import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

BLANCO = "#FFFFFF"
AZUL = "#0e98d6"
NEGRO = "#000000"
GRIS = "#666666"


class SplashScreen:
    def __init__(self, on_complete=None):
        self.on_complete = on_complete
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.configure(bg=BLANCO)
        self.width, self.height = 700, 450
        x = (self.root.winfo_screenwidth() - self.width) // 2
        y = (self.root.winfo_screenheight() - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg=BLANCO, highlightthickness=0)
        self.canvas.pack()
        self._draw_circuits()
        self._load_logo()
        self._draw_text()
        self._create_progress_bar()
        self.current_progress = 0
        self.loading_complete = False

    def _draw_circuits(self):
        for y in (28, 422):
            self.canvas.create_line(35, y, 665, y, fill=AZUL, width=1)
            for x in range(35, 666, 70):
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=AZUL, outline="")
                self.canvas.create_line(x, y, x, y + (20 if y < 100 else -20), fill=AZUL, width=1)
        for x in (28, 672):
            self.canvas.create_line(x, 45, x, 405, fill=AZUL, width=1)
            for y in range(55, 406, 70):
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=AZUL, outline="")

    def _load_logo(self):
        paths = [
            Path(__file__).parent.parent.parent / "assets" / "logo.png",
            Path(__file__).parent.parent.parent / "assets" / "logo_g.png",
        ]
        for path in paths:
            if path.exists():
                try:
                    img = Image.open(path).convert("RGBA")
                    img.thumbnail((150, 150), Image.Resampling.LANCZOS)
                    self.logo_img = ImageTk.PhotoImage(img)
                    self.logo_id = self.canvas.create_image(self.width // 2, 155, image=self.logo_img)
                    return
                except Exception as exc:
                    logger.warning("Logo no disponible: %s", exc)
        self.canvas.create_text(self.width // 2, 155, text="ASISTENTE ONG", font=("Helvetica", 28, "bold"), fill=AZUL)

    def _draw_text(self):
        self.canvas.create_text(self.width // 2, 260, text="ASISTENTE ONG", font=("Helvetica", 28, "bold"), fill=NEGRO)
        self.canvas.create_text(self.width // 2, 295, text="Triaje y Canalización Profesional", font=("Helvetica", 12), fill=GRIS)
        self.canvas.create_text(self.width // 2, 320, text="Offline 100%", font=("Helvetica", 10), fill=GRIS)
        self.loading_text = self.canvas.create_text(self.width // 2, 395, text="Inicializando...", font=("Helvetica", 10), fill=GRIS)

    def _create_progress_bar(self):
        self.canvas.create_rectangle(180, 350, 520, 360, fill="#E8E8E8", outline="")
        self.progress_bar = self.canvas.create_rectangle(180, 350, 180, 360, fill=AZUL, outline="")

    def update_progress(self, value, text=None):
        self.current_progress = value
        width = 340 * (value / 100)
        self.canvas.coords(self.progress_bar, 180, 350, 180 + width, 360)
        self.canvas.itemconfig(self.loading_text, text=text or f"Cargando... {value}%")
        self.root.update_idletasks()

    def start_loading(self):
        steps = [(15, "Inicializando..."), (35, "Cargando datos..."), (55, "Preparando interfaz..."), (75, "Cargando módulos..."), (90, "Verificando..."), (100, "Listo")]
        def step(index=0):
            if index >= len(steps):
                self.loading_complete = True
                self.root.after(250, self._finish)
                return
            value, text = steps[index]
            self.update_progress(value, text)
            self.root.after(350, lambda: step(index + 1))
        step()

    def _finish(self):
        self.root.destroy()
        if self.on_complete:
            self.on_complete()

    def run(self):
        self.start_loading()
        self.root.mainloop()


def show_splash(on_complete=None):
    SplashScreen(on_complete=on_complete).run()
