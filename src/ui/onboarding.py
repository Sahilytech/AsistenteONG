"""Tutorial inicial interactivo: corto, guiado y reutilizable."""
import customtkinter as ctk
from pathlib import Path
from .styles import COLORS, FONTS

FLAG = Path.home() / ".asistente_ong_tutorial_v3"

class Onboarding(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.steps = [
            ("Bienvenida", "La plataforma empieza completamente vacía. Vas a cargar tus propios casos, documentos y datos; no hay ejemplos escondidos.", None),
            ("1 · Crear un caso", "Entrá en Casos y elegí Nuevo caso. Escribí el relato y completá solo los datos necesarios. Guardá para continuar.", "Casos"),
            ("2 · Revisar el análisis", "El sistema muestra una prioridad orientativa, señales detectadas, preguntas pendientes y recursos. Siempre requiere revisión profesional.", "Análisis"),
            ("3 · Construir tu biblioteca", "Importá PDFs desde Biblioteca. Podés recargarla cuando agregues nuevos documentos. El texto se procesa localmente y puede ayudar a encontrar documentación relacionada.", "Biblioteca"),
            ("4 · Hacer seguimiento", "Después del análisis podés registrar acciones, responsables, fechas y derivaciones. La Agenda reúne las fechas que cargues.", "Seguimiento"),
            ("5 · Privacidad", "Los casos y documentos se almacenan localmente. Las funciones que consultan Internet deben ser explícitas y visibles para el usuario.", "Seguridad"),
            ("Listo", "Ya conocés el recorrido. Podés volver a abrir este tutorial desde Ayuda. La plataforma queda lista para que cargues información real.", "Inicio"),
        ]
        self.index = 0
        self.title("Primeros pasos · Asistente ONG")
        self.geometry("820x560")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self._build()
        self._render()

    def _build(self):
        self.configure(fg_color=COLORS["background"])
        box = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=20, border_width=1, border_color=COLORS["border"])
        box.pack(fill="both", expand=True, padx=24, pady=24)
        self.step = ctk.CTkLabel(box, text="", font=FONTS["title"], text_color=COLORS["text"], anchor="w")
        self.step.pack(fill="x", padx=30, pady=(30, 8))
        self.body = ctk.CTkLabel(box, text="", font=FONTS["body"], text_color=COLORS["text_muted"], justify="left", anchor="nw", wraplength=700)
        self.body.pack(fill="both", expand=True, padx=30, pady=8)
        foot = ctk.CTkFrame(box, fg_color="transparent")
        foot.pack(fill="x", padx=30, pady=(0, 26))
        self.progress = ctk.CTkLabel(foot, text="", font=FONTS["tiny"], text_color=COLORS["text_muted"])
        self.progress.pack(side="left")
        self.go = ctk.CTkButton(foot, text="Abrir sección", width=125, fg_color=COLORS["surface_alt"], hover_color=COLORS["primary_soft"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"], command=self._go_section)
        self.go.pack(side="right", padx=5)
        ctk.CTkButton(foot, text="Cerrar", width=85, fg_color="transparent", hover_color=COLORS["primary_soft"], text_color=COLORS["text_muted"], command=self.finish).pack(side="right", padx=5)
        self.next = ctk.CTkButton(foot, text="Siguiente", width=105, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"], command=self._next)
        self.next.pack(side="right")

    def _render(self):
        title, body, target = self.steps[self.index]
        self.step.configure(text=title)
        self.body.configure(text=body)
        self.progress.configure(text=f"Paso {self.index + 1} de {len(self.steps)}")
        self.go.configure(state="normal" if target else "disabled")
        self.next.configure(text="Empezar" if self.index == 0 else ("Finalizar" if self.index == len(self.steps) - 1 else "Siguiente"))

    def _next(self):
        if self.index >= len(self.steps) - 1:
            self.finish()
            return
        self.index += 1
        self._render()

    def _go_section(self):
        target = self.steps[self.index][2]
        if not target:
            return
        controller = getattr(self.parent, "app_controller", None)
        self.finish()
        if controller and hasattr(controller, "select_tab"):
            controller.select_tab(target)

    def finish(self):
        try:
            FLAG.write_text("completed", encoding="utf-8")
        except Exception:
            pass
        try:
            self.grab_release()
        except Exception:
            pass
        self.destroy()


def show_tutorial(parent):
    Onboarding(parent)


def show_first_run(parent):
    if not FLAG.exists():
        parent.after(350, lambda: Onboarding(parent))
