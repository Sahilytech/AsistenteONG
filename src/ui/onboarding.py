"""Tutorial inicial interactivo: guiado, reutilizable y orientado a un primer arranque vacío."""
import customtkinter as ctk
from pathlib import Path
from .styles import COLORS, FONTS

FLAG = Path.home() / ".asistente_ong_tutorial_v4"


class Onboarding(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.steps = [
            ("Bienvenida", "La plataforma empieza completamente vacía. No hay personas, casos ni ejemplos ocultos. Todo lo que cargues queda bajo el control de la organización.", None),
            ("1 · Configurar la organización", "Antes de trabajar con información real, entrá en Configuración y cargá los datos institucionales que deban aparecer en los informes. Podés cambiarlos después.", "Configuración"),
            ("2 · Crear una persona y un caso", "Entrá en Personas o Casos. Una persona se registra una sola vez y puede tener muchos casos. Cada nueva atención se guarda como un caso separado dentro de su historial.", "Personas"),
            ("3 · Revisar el análisis", "El sistema organiza señales, preguntas pendientes, historial y evidencia. El resultado es orientativo y siempre requiere revisión profesional.", "Análisis"),
            ("4 · Construir la Biblioteca", "Importá PDFs institucionales, protocolos y material de referencia. Podés recargar la biblioteca después de agregar documentos. Los textos se procesan localmente y conservan su procedencia para revisión.", "Biblioteca"),
            ("5 · Importar una base existente", "Si tu ONG ya tiene una planilla, usá la vista previa y el mapeo de columnas. Nada debe persistirse hasta que el operador confirme explícitamente la importación.", "Personas"),
            ("6 · Seguimiento", "Registrá acciones, responsables, fechas y derivaciones. La Agenda reúne las fechas cargadas y permite mantener el trabajo operativo ordenado.", "Seguimiento"),
            ("7 · Seguridad", "Revisá bloqueo de sesión, backup y permisos antes de usar datos reales. El modo base es local/offline y las consultas externas deben ser explícitas.", "Seguridad"),
            ("Listo", "Ya conocés el recorrido completo. Podés volver a abrir este tutorial desde Ayuda cuando quieras. Empezá con datos ficticios para familiarizarte y luego seguí el protocolo interno de tu organización.", "Inicio"),
        ]
        self.index = 0
        self.title("Primeros pasos · Asistente ONG")
        self.geometry("860x600")
        self.minsize(760, 540)
        self.resizable(True, True)
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
        self.body = ctk.CTkLabel(box, text="", font=FONTS["body"], text_color=COLORS["text_muted"], justify="left", anchor="nw", wraplength=760)
        self.body.pack(fill="both", expand=True, padx=30, pady=8)
        foot = ctk.CTkFrame(box, fg_color="transparent")
        foot.pack(fill="x", padx=30, pady=(0, 26))
        self.progress = ctk.CTkLabel(foot, text="", font=FONTS["tiny"], text_color=COLORS["text_muted"])
        self.progress.pack(side="left")
        self.go = ctk.CTkButton(foot, text="Abrir sección", width=135, fg_color=COLORS["surface_alt"], hover_color=COLORS["primary_soft"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"], command=self._go_section)
        self.go.pack(side="right", padx=5)
        ctk.CTkButton(foot, text="Cerrar", width=85, fg_color="transparent", hover_color=COLORS["primary_soft"], text_color=COLORS["text_muted"], command=self.finish).pack(side="right", padx=5)
        self.next = ctk.CTkButton(foot, text="Siguiente", width=110, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"], command=self._next)
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
