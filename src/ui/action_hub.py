"""Acciones contextuales reutilizables.

Cada botón debe tener un callback real. Las acciones inválidas se ignoran para
que una configuración incompleta no rompa toda la ventana.
"""
import customtkinter as ctk

try:
    from .styles import COLORS, FONTS
except ImportError:
    COLORS = {
        "surface": "#FFFFFF", "border": "#D9E2EA", "primary": "#0e98d6",
        "primary_dark": "#0878AA", "surface_alt": "#F4F8FA", "primary_soft": "#E3F4FB",
        "text": "#111111",
    }
    FONTS = {"body": ("Montserrat", 13), "body_bold": ("Montserrat", 13, "bold")}


class ActionHub(ctk.CTkFrame):
    def __init__(self, parent, actions=None, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS.get("surface", "#FFFFFF"),
            corner_radius=16,
            border_width=1,
            border_color=COLORS.get("border", "#D9E2EA"),
            **kwargs,
        )
        self.actions = []
        for item in actions or []:
            if not isinstance(item, (tuple, list)) or len(item) != 2:
                continue
            label, command = item
            if not callable(command):
                continue
            self.add_action(str(label), command, primary=(len(self.actions) == 0))

    def add_action(self, label, command, primary=False):
        button = ctk.CTkButton(
            self,
            text=label,
            command=command,
            height=38,
            corner_radius=10,
            fg_color=COLORS.get("primary", "#0e98d6") if primary else COLORS.get("surface_alt", "#F4F8FA"),
            hover_color=COLORS.get("primary_dark", "#0878AA") if primary else COLORS.get("primary_soft", "#E3F4FB"),
            text_color="#FFFFFF" if primary else COLORS.get("text", "#111111"),
            font=FONTS.get("body_bold", ("Montserrat", 13, "bold")) if primary else FONTS.get("body", ("Montserrat", 13)),
        )
        button.pack(side="left", padx=6, pady=10)
        self.actions.append(button)
        return button
