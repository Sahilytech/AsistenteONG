"""Tutorial inicial interactivo: aparece una vez y puede repetirse desde Ayuda."""
import customtkinter as ctk
from pathlib import Path
from .styles import COLORS,FONTS
FLAG=Path.home()/".asistente_ong_tutorial_v2"
class Onboarding(ctk.CTkToplevel):
 def __init__(self,parent):
  super().__init__(parent); self.parent=parent; self.steps=[("Bienvenida","La plataforma está vacía a propósito. Primero cargás tu propia información; después el sistema la organiza y te ayuda a revisarla.",None),("1 · Crear un caso","Entrá en Casos → Nuevo caso. Escribí solamente la información necesaria y guardá el registro.","Casos"),("2 · Analizar","El análisis local muestra prioridad orientativa, señales, preguntas y recursos. No reemplaza la revisión profesional.","Análisis"),("3 · Biblioteca + PDF","En Biblioteca podés importar uno o varios PDFs. El texto se extrae en este equipo y queda disponible para búsquedas y como documentación relacionada con futuros análisis.","Biblioteca"),("4 · Seguimiento","Registrá acciones, responsables y fechas desde Seguimiento. La Agenda muestra las fechas que hayas cargado.","Seguimiento"),("5 · Privacidad","Los casos y PDFs permanecen en el almacenamiento local. Internet solo se utiliza cuando una función explícita lo necesita.","Seguridad"),("Listo","Ya conocés el recorrido. Podés volver a este tutorial desde Ayuda. No hay casos, documentos ni datos de ejemplo cargados.","Inicio")]; self.index=0; self.title("Primeros pasos · Asistente ONG"); self.geometry("820x560"); self.resizable(False,False); self.transient(parent); self.grab_set(); self._ui(); self._render()
 def _ui(self):
  self.configure(fg_color=COLORS["background"]); self.box=ctk.CTkFrame(self,fg_color=COLORS["surface"],corner_radius=20,border_width=1,border_color=COLORS["border"]); self.box.pack(fill="both",expand=True,padx=24,pady=24)
  self.step=ctk.CTkLabel(self.box,text="",font=FONTS["title"],text_color=COLORS["text"],anchor="w"); self.step.pack(fill="x",padx=30,pady=(30,8)); self.body=ctk.CTkLabel(self.box,text="",font=FONTS["body"],text_color=COLORS["text_muted"],justify="left",anchor="nw",wraplength=700); self.body.pack(fill="both",expand=True,padx=30,pady=8)
  foot=ctk.CTkFrame(self.box,fg_color="transparent"); foot.pack(fill="x",padx=30,pady=(0,26)); self.progress=ctk.CTkLabel(foot,text="",font=FONTS["tiny"],text_color=COLORS["text_muted"]); self.progress.pack(side="left"); self.go=ctk.CTkButton(foot,text="Abrir sección",width=125,fg_color=COLORS["surface_alt"],hover_color=COLORS["primary_soft"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"],command=self._go_section); self.go.pack(side="right",padx=5); ctk.CTkButton(foot,text="Cerrar",width=85,fg_color="transparent",hover_color=COLORS["primary_soft"],text_color=COLORS["text_muted"],command=self.finish).pack(side="right",padx=5); self.next=ctk.CTkButton(foot,text="Siguiente",width=105,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],command=self._next); self.next.pack(side="right")
 def _render(self):
  title,body,target=self.steps[self.index]; self.step.configure(text=title); self.body.configure(text=body); self.progress.configure(text=f"{self.index+1} de {len(self.steps)}"); self.go.configure(state="normal" if target else "disabled"); self.next.configure(text="Empezar" if self.index==0 else ("Finalizar" if self.index==len(self.steps)-1 else "Siguiente"))
 def _next(self):
  if self.index>=len(self.steps)-1:self.finish(); return
  self.index+=1; self._render()
 def _go_section(self):
  target=self.steps[self.index][2]
  if not target:return
  controller=getattr(self.parent,"app_controller",None) or self.parent
  self.finish()
  try:
   if hasattr(controller,"select_tab"): controller.select_tab(target)
  except Exception: pass
 def finish(self):
  try: FLAG.write_text("completed",encoding="utf-8")
  except Exception: pass
  try:self.grab_release()
  except Exception:pass
  self.destroy()
def show_tutorial(parent): Onboarding(parent)
def show_first_run(parent):
 if not FLAG.exists(): parent.after(450,lambda: Onboarding(parent))
