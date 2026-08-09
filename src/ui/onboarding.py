"""Tutorial inicial: aparece una sola vez y puede omitirse."""
import tkinter as tk
import customtkinter as ctk
from pathlib import Path
from .styles import COLORS,FONTS

FLAG=Path.home()/".asistente_ong_tutorial_v1"

class Onboarding(ctk.CTkToplevel):
 def __init__(self,parent):
  super().__init__(parent); self.parent=parent; self.steps=[("Bienvenida","Asistente ONG organiza la atención en un flujo simple: crear el caso, completar sus datos, analizar, revisar y hacer seguimiento."),("1 · Casos","Acá se crea cada caso. Los datos de la persona, el tipo de situación, la zona y el relato quedan juntos en el mismo registro."),("2 · Análisis","El motor local revisa indicadores y muestra prioridad, contexto, motivo de la prioridad, preguntas pendientes y recursos sugeridos. El resultado siempre se revisa."),("3 · Seguimiento","Después del análisis podés registrar acciones, fechas, derivaciones y estado del caso sin perder el contexto original."),("4 · Privacidad","La aplicación funciona offline. Los datos permanecen en el equipo y no se envían a Internet."),("Listo","Ya conocés el recorrido principal. Podés volver a este contenido desde Ayuda cuando quieras.")]; self.index=0; self.title("Primeros pasos · Asistente ONG"); self.geometry("760x500"); self.resizable(False,False); self.transient(parent); self.grab_set(); self._ui(); self._render()
 def _ui(self):
  self.configure(fg_color=COLORS["background"]); self.box=ctk.CTkFrame(self,fg_color=COLORS["surface"],corner_radius=20,border_width=1,border_color=COLORS["border"]); self.box.pack(fill="both",expand=True,padx=24,pady=24)
  self.step=ctk.CTkLabel(self.box,text="",font=FONTS["title"],text_color=COLORS["text"]); self.step.pack(anchor="w",padx=30,pady=(30,8)); self.body=ctk.CTkLabel(self.box,text="",font=FONTS["body"],text_color=COLORS["text_muted"],justify="left",anchor="nw",wraplength=650); self.body.pack(fill="both",expand=True,padx=30,pady=8)
  foot=ctk.CTkFrame(self.box,fg_color="transparent"); foot.pack(fill="x",padx=30,pady=(0,26)); self.progress=ctk.CTkLabel(foot,text="",font=FONTS["tiny"],text_color=COLORS["text_muted"]); self.progress.pack(side="left"); ctk.CTkButton(foot,text="Omitir tutorial",width=120,fg_color="transparent",hover_color=COLORS["primary_soft"],text_color=COLORS["text_muted"],command=self.finish).pack(side="right",padx=5); self.next=ctk.CTkButton(foot,text="Siguiente",width=110,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],command=self._next); self.next.pack(side="right")
 def _render(self):
  title,body=self.steps[self.index]; self.step.configure(text=title); self.body.configure(text=body); self.progress.configure(text=f"{self.index+1} de {len(self.steps)}"); self.next.configure(text="Empezar" if self.index==0 else ("Finalizar" if self.index==len(self.steps)-1 else "Siguiente"))
 def _next(self):
  if self.index>=len(self.steps)-1:self.finish(); return
  self.index+=1; self._render()
 def finish(self):
  try: FLAG.write_text("completed",encoding="utf-8")
  except Exception: pass
  self.grab_release(); self.destroy()

def show_first_run(parent):
 if not FLAG.exists(): parent.after(450,lambda: Onboarding(parent))
