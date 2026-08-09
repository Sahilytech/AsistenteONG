"""Splash animado de Asistente ONG con identidad visual NubiWorks."""
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

WHITE = "#FFFFFF"
BLUE = "#0e98d6"
BLACK = "#000000"
LIGHT = "#EAF6FC"
GRAY = "#666666"


class SplashScreen:
    def __init__(self, on_complete=None):
        self.on_complete = on_complete
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.configure(bg=WHITE)
        self.width, self.height = 760, 500
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+{(sw-self.width)//2}+{(sh-self.height)//2}")
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg=WHITE, highlightthickness=0)
        self.canvas.pack()
        self._particles = []
        self._pulse_nodes = []
        self._logo_y = 175
        self._logo_direction = 1
        self._draw_background()
        self._load_logo()
        self._draw_text()
        self._create_progress_bar()
        self.current_progress = 0
        self._animation_tick = 0

    def _draw_background(self):
        # Circuitos con nodos y trazos secundarios para dar sensación de movimiento.
        circuit_y = (35, 78, 420, 463)
        for y in circuit_y:
            self.canvas.create_line(25, y, 735, y, fill=LIGHT, width=2)
            for x in range(45, 736, 70):
                self.canvas.create_line(x, y, x + 25, y, fill=BLUE, width=1)
                node = self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=BLUE, outline="")
                self._pulse_nodes.append(node)
        for x in (25, 735):
            self.canvas.create_line(x, 35, x, 463, fill=LIGHT, width=2)
        branches = [
            (90, 78, 90, 125), (170, 35, 170, 115), (590, 78, 590, 125),
            (670, 35, 670, 115), (110, 420, 110, 365), (650, 420, 650, 365),
        ]
        for x1, y1, x2, y2 in branches:
            self.canvas.create_line(x1, y1, x2, y2, fill=BLUE, width=1)
            self.canvas.create_oval(x2-4, y2-4, x2+4, y2+4, fill=BLUE, outline="")
        # Puntos móviles que recorren los circuitos.
        for i in range(8):
            dot = self.canvas.create_oval(0, 0, 5, 5, fill=BLUE, outline="")
            self._particles.append({"id": dot, "x": 35 + i * 95, "y": 35 if i % 2 == 0 else 463, "direction": 1 if i % 2 == 0 else -1})

    def _load_logo(self):
        paths = [
            Path(__file__).parent.parent.parent / "assets" / "logo.png",
            Path(__file__).parent.parent.parent / "assets" / "logo_g.png",
            Path("assets/logo.png"), Path("assets/logo_g.png"),
        ]
        for path in paths:
            if path.exists():
                img = Image.open(path).convert("RGBA")
                img.thumbnail((190, 190))
                self.logo_img = ImageTk.PhotoImage(img)
                self.logo = self.canvas.create_image(380, self._logo_y, image=self.logo_img)
                return
        self.logo = self.canvas.create_text(380, self._logo_y, text="ASISTENTE ONG", font=("Helvetica", 30, "bold"), fill=BLUE)

    def _draw_text(self):
        self.canvas.create_text(380, 285, text="ASISTENTE ONG", font=("Helvetica", 30, "bold"), fill=BLACK)
        self.canvas.create_text(380, 320, text="Triaje y Canalización Profesional", font=("Helvetica", 12), fill=GRAY)
        self.canvas.create_text(380, 343, text="Offline 100%  •  Privacidad local", font=("Helvetica", 10), fill=GRAY)
        self.loading_text = self.canvas.create_text(380, 405, text="Inicializando...", font=("Helvetica", 10), fill=GRAY)
        self.canvas.create_text(380, 482, text="NubiWorks", font=("Helvetica", 9), fill=GRAY)

    def _create_progress_bar(self):
        self.canvas.create_rectangle(190, 370, 570, 381, fill=LIGHT, outline="")
        self.progress_bar = self.canvas.create_rectangle(190, 370, 190, 381, fill=BLUE, outline="")

    def update_progress(self, value, text=None):
        self.current_progress = value
        width = 380 * max(0, min(100, value)) / 100
        self.canvas.coords(self.progress_bar, 190, 370, 190 + width, 381)
        self.canvas.itemconfig(self.loading_text, text=text or f"Cargando... {value}%")
        self.root.update_idletasks()

    def _animate(self):
        self._animation_tick += 1
        offset = 2 if (self._animation_tick // 8) % 2 == 0 else -2
        self.canvas.coords(self.logo, 380, self._logo_y + offset)
        for index, node in enumerate(self._pulse_nodes):
            if (self._animation_tick + index * 3) % 30 < 8:
                self.canvas.itemconfig(node, fill=BLUE)
            else:
                self.canvas.itemconfig(node, fill=LIGHT)
        for particle in self._particles:
            particle["x"] += 2 * particle["direction"]
            if particle["x"] > 725:
                particle["x"] = 35
            elif particle["x"] < 35:
                particle["x"] = 725
            self.canvas.coords(particle["id"], particle["x"]-2.5, particle["y"]-2.5, particle["x"]+2.5, particle["y"]+2.5)
        self.root.after(45, self._animate)

    def start_loading(self):
        steps = [(10, "Inicializando..."), (30, "Cargando base local..."), (50, "Preparando interfaz..."),
                 (70, "Cargando módulos..."), (90, "Verificando componentes..."), (100, "Listo")]
        def step(i=0):
            if i >= len(steps):
                self.root.after(350, self._finish)
                return
            progress, text = steps[i]
            self.update_progress(progress, text)
            self.root.after(180, lambda: step(i + 1))
        self._animate()
        step()

    def _finish(self):
        self.root.destroy()
        if self.on_complete:
            self.on_complete()

    def run(self):
        self.start_loading()
        self.root.mainloop()


def show_splash(on_complete=None):
    SplashScreen(on_complete).run()
