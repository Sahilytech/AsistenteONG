"""Acciones reutilizables del espacio de trabajo: cada botón ejecuta una tarea concreta."""
import customtkinter as ctk
from .styles import COLORS, FONTS

class ActionHub(ctk.CTkFrame):
    def __init__(self, parent, actions=None, **kwargs):
        super().__init__(parent, fg_color=COLORS['surface'], corner_radius=16, border_width=1, border_color=COLORS['border'], **kwargs)
        self.actions = actions or []
        for i, item in enumerate(self.actions):
            label, command = item
            ctk.CTkButton(self, text=label, command=command, height=38, corner_radius=10,
                          fg_color=COLORS['primary'] if i == 0 else COLORS['surface_alt'],
                          hover_color=COLORS['primary_dark'] if i == 0 else COLORS['primary_soft'],
                          text_color=COLORS['surface'] if i == 0 else COLORS['text'],
                          font=FONTS['body_bold'] if i == 0 else FONTS['body']).pack(side='left', padx=6, pady=10)
