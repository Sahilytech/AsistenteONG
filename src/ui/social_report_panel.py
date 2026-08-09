"""Formulario profesional de Informe Social."""
import json
import logging
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox
import customtkinter as ctk
from .styles import COLORS, FONTS
from ..report_generator import generate_social_report

logger = logging.getLogger(__name__)
DATA_DIR = Path(__file__).parent.parent.parent / "data"
DEFAULTS_PATH = DATA_DIR / "institution_defaults.json"

class SocialReportPanel(ctk.CTkFrame):
    """Formulario de Informe Social con siete bloques profesionales."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs); self.entries={}; self.textboxes={}; self._setup_ui(); self._load_defaults()
    def _setup_ui(self):
        scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.pack(fill="both",expand=True,padx=18,pady=18)
        ctk.CTkLabel(scroll,text="Informe Social Profesional",font=FONTS["title"],text_color=COLORS["primary"]).pack(anchor="w")
        ctk.CTkLabel(scroll,text="Formulario estructurado para valoración, diagnóstico y propuesta de intervención.",font=FONTS["body"],text_color=COLORS["text_muted"]).pack(anchor="w",pady=(3,18))
        self._section(scroll,"1. Datos del profesional e institución",[("entidad_emisora","Entidad emisora"),("profesional","Profesional de referencia"),("colegiatura","Número de colegiatura / matrícula"),("destinatario","Destinatario"),("fecha_emision","Fecha de emisión",date.today().isoformat()),("motivo","Fecha y motivo de la solicitud")])
        self._section(scroll,"2. Identificación de la persona de referencia",[("nombre_completo","Nombres y apellidos completos"),("documento","DNI / NIE / Pasaporte"),("domicilio","Domicilio actual"),("telefono","Teléfono"),("email","Correo electrónico"),("fecha_nacimiento","Fecha de nacimiento"),("edad","Edad"),("sexo","Sexo"),("nacionalidad","Nacionalidad"),("estado_civil","Estado civil")])
        self._text_section(scroll,"3. Unidad de convivencia y dinámica familiar",[("miembros_hogar","Miembros del hogar (parentesco, edad y ocupación)"),("historia_familiar","Antecedentes e historia familiar"),("dinamica_familiar","Dinámica y vínculos (apoyo, conflicto, cuidados, etc.)"),("genograma","Genograma / observaciones visuales (opcional)")])
        self._text_section(scroll,"4. Situación socioeconómica y laboral",[("ingresos","Fuentes de ingresos y sustento"),("situacion_laboral","Situación laboral de los integrantes"),("egresos","Egresos básicos: alquiler, servicios, alimentación, etc.")])
        self._text_section(scroll,"5. Habitabilidad y vivienda",[("tenencia","Régimen de tenencia"),("condiciones_vivienda","Condiciones materiales, habitaciones y hacinamiento"),("servicios_entorno","Servicios y entorno: agua, electricidad, transporte y barrio")])
        self._text_section(scroll,"6. Salud y educación",[("salud","Situación sanitaria, discapacidad, dependencia o tratamientos relevantes"),("educacion","Nivel educativo y asistencia escolar de menores")])
        self._text_section(scroll,"7. Diagnóstico, valoración y propuesta",[("diagnostico","Juicio técnico / valoración social"),("fortalezas","Fortalezas y factores protectores"),("vulnerabilidades","Vulnerabilidades y factores de riesgo"),("propuesta","Propuesta de intervención / recursos a activar"),("observaciones","Observaciones finales")])
        buttons=ctk.CTkFrame(scroll,fg_color="transparent"); buttons.pack(fill="x",pady=(10,5))
        ctk.CTkButton(buttons,text="Guardar borrador",command=self.save_draft,fg_color=COLORS["primary"],text_color="white",width=150).pack(side="left",padx=(0,8))
        ctk.CTkButton(buttons,text="Generar PDF",command=self.export_pdf,fg_color=COLORS["primary"],text_color="white",width=130).pack(side="left",padx=8)
        ctk.CTkButton(buttons,text="Exportar JSON",command=self.export_json,fg_color="transparent",border_width=1,border_color=COLORS["primary"],text_color=COLORS["primary"],width=140).pack(side="left",padx=8)
        ctk.CTkButton(buttons,text="Limpiar",command=self.clear_form,fg_color="transparent",border_width=1,border_color=COLORS["border"],text_color=COLORS["text"],width=100).pack(side="left",padx=8)
        ctk.CTkLabel(scroll,text="Los datos se almacenan localmente. Verificá el contenido antes de emitir o compartir un informe.",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=800).pack(anchor="w",pady=(8,15))
    def _section(self,parent,title,fields):
        frame=ctk.CTkFrame(parent,fg_color=COLORS["surface"],corner_radius=8); frame.pack(fill="x",pady=7)
        ctk.CTkLabel(frame,text=title,font=FONTS["heading"],text_color=COLORS["primary"]).pack(anchor="w",padx=14,pady=(12,8))
        for item in fields:
            key,label=item[:2]; default=item[2] if len(item)>2 else ""; row=ctk.CTkFrame(frame,fg_color="transparent"); row.pack(fill="x",padx=14,pady=4)
            ctk.CTkLabel(row,text=label,width=230,anchor="w",text_color=COLORS["text"]).pack(side="left"); entry=ctk.CTkEntry(row,height=34); entry.pack(side="left",fill="x",expand=True)
            if default: entry.insert(0,default)
            self.entries[key]=entry
    def _text_section(self,parent,title,fields):
        frame=ctk.CTkFrame(parent,fg_color=COLORS["surface"],corner_radius=8); frame.pack(fill="x",pady=7)
        ctk.CTkLabel(frame,text=title,font=FONTS["heading"],text_color=COLORS["primary"]).pack(anchor="w",padx=14,pady=(12,8))
        for key,label in fields:
            ctk.CTkLabel(frame,text=label,anchor="w",text_color=COLORS["text"]).pack(anchor="w",padx=14,pady=(5,3)); box=ctk.CTkTextbox(frame,height=85,fg_color=COLORS["background"],text_color=COLORS["text"]); box.pack(fill="x",padx=14,pady=(0,7)); self.textboxes[key]=box
    def collect_data(self):
        data={k:w.get().strip() for k,w in self.entries.items()}; data.update({k:w.get("1.0","end").strip() for k,w in self.textboxes.items()}); data["document_type"]="Informe Social Profesional"; data["generated_at"]=date.today().isoformat(); return data
    def _load_defaults(self):
        try:
            if not DEFAULTS_PATH.exists(): return
            data=json.loads(DEFAULTS_PATH.read_text(encoding="utf-8"))
            for key in ("entidad_emisora","profesional","colegiatura","destinatario"):
                if key in data and key in self.entries and not self.entries[key].get(): self.entries[key].insert(0,data[key])
        except Exception as exc: logger.warning("No se pudieron cargar los valores fijados: %s",exc)
    def save_draft(self):
        try:
            DATA_DIR.mkdir(parents=True,exist_ok=True); data=self.collect_data(); DEFAULTS_PATH.write_text(json.dumps({k:data.get(k,"") for k in ("entidad_emisora","profesional","colegiatura","destinatario")},ensure_ascii=False,indent=2),encoding="utf-8"); (DATA_DIR/"ultimo_informe_social.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8"); messagebox.showinfo("Guardado","Borrador guardado localmente.")
        except Exception as exc: logger.exception("Error guardando informe"); messagebox.showerror("Error",f"No se pudo guardar el informe:\n{exc}")
    def export_json(self):
        try:
            path=filedialog.asksaveasfilename(title="Exportar informe social",defaultextension=".json",filetypes=[("Informe JSON","*.json")],initialfile="informe_social.json")
            if path: Path(path).write_text(json.dumps(self.collect_data(),ensure_ascii=False,indent=2),encoding="utf-8"); messagebox.showinfo("Exportado","Informe exportado correctamente.")
        except Exception as exc: messagebox.showerror("Error",f"No se pudo exportar el informe:\n{exc}")
    def export_pdf(self):
        try:
            path=filedialog.asksaveasfilename(title="Generar informe PDF",defaultextension=".pdf",filetypes=[("PDF","*.pdf")],initialfile="informe_social.pdf")
            if path: generate_social_report(self.collect_data(),path); messagebox.showinfo("PDF generado","Informe PDF generado correctamente.")
        except Exception as exc: logger.exception("Error generando PDF"); messagebox.showerror("Error",f"No se pudo generar el PDF:\n{exc}")
    def clear_form(self):
        for w in self.entries.values(): w.delete(0,"end")
        for w in self.textboxes.values(): w.delete("1.0","end")
        self._load_defaults()
