"""Arranque visual: carga breve y entrada fluida a pantalla completa."""
from __future__ import annotations
import customtkinter as ctk
from .styles import COLORS, FONTS

class StartupScreen(ctk.CTkFrame):
    def __init__(self, parent, on_ready, **kwargs):
        super().__init__(parent, fg_color=COLORS["background"], **kwargs)
        self._on_ready = on_ready
        self._progress = 0
        self._build()
        self.after(80, self._tick)

    def _build(self):
        box = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=24, border_width=1, border_color=COLORS["border"])
        box.place(relx=.5, rely=.5, anchor="center", relwidth=.42, relheight=.32)
        ctk.CTkLabel(box, text="Asistente ONG", font=FONTS["title"], text_color=COLORS["text"]).pack(pady=(42, 4))
        ctk.CTkLabel(box, text="Preparando tu espacio de trabajo", font=FONTS["body"], text_color=COLORS["text_muted"]).pack()
        self.status = ctk.CTkLabel(box, text="Iniciando…", font=FONTS["small"], text_color=COLORS["primary"])
        self.status.pack(pady=(24, 10))
        self.bar = ctk.CTkProgressBar(box, width=300, progress_color=COLORS["primary"])
        self.bar.pack()
        self.bar.set(0)

    def _tick(self):
        self._progress += 8
        self.bar.set(min(self._progress / 100, 1))
        messages = [(8,"Inicializando"),(32,"Preparando datos"),(56,"Cargando biblioteca"),(80,"Preparando interfaz"),(96,"Listo")]
        self.status.configure(text=next((m for p,m in reversed(messages) if self._progress >= p), "Iniciando…"))
        if self._progress >= 100:
            self.after(120, self._finish)
        else:
            self.after(45, self._tick)

    def _finish(self):
        self.pack_forget()
        self._on_ready()
