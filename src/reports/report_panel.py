"""
Panel de Informes Sociales - UI completa para crear, editar y exportar
Colores: Blanco, Negro, Azul #0e98d6
"""

import customtkinter as ctk
from typing import Optional
import logging
from datetime import datetime

from .styles import COLORS, FONTS, SPACING
from ..reports.social_report import InformeSocial, InformeManager, MiembroFamiliar
from ..reports.pdf_generator import PDFGenerator

logger = logging.getLogger(__name__)


class ReportPanel(ctk.CTkFrame):
    """Panel completo para gestión de informes sociales."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.informe_manager = InformeManager()
        self.current_informe: Optional[InformeSocial] = None
        self._setup_ui()

    def _setup_ui(self):
        """Configura la interfaz de informes."""

        # Título
        title = ctk.CTkLabel(
            self,
            text="📄 Informes Sociales",
            font=FONTS["heading"],
            text_color="#0e98d6"
        )
        title.pack(anchor="w", pady=(0, 16), padx=16)

        # Barra de herramientas
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=16, pady=(0, 16))

        ctk.CTkButton(
            toolbar,
            text="➕ Nuevo Informe",
            command=self._nuevo_informe,
            fg_color="#0e98d6",
            text_color="white",
            width=140
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            toolbar,
            text="💾 Guardar",
            command=self._guardar_informe,
            fg_color="#2da44e",
            text_color="white",
            width=100
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            toolbar,
            text="📄 Exportar PDF",
            command=self._exportar_pdf,
            fg_color="#0e98d6",
            text_color="white",
            width=120
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            toolbar,
            text="📋 Listar Informes",
            command=self._listar_informes,
            fg_color="#6e7681",
            text_color="white",
            width=120
        ).pack(side="left")

        # Tabs de secciones
        self.tab_view = ctk.CTkTabview(self, fg_color="#161b22")
        self.tab_view.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # Tab 1: Datos Profesional
        self._setup_tab_profesional()

        # Tab 2: Identificación
        self._setup_tab_identificacion()

        # Tab 3: Unidad Convivencia
        self._setup_tab_convivencia()

        # Tab 4: Socioeconómica
        self._setup_tab_socioeconomica()

        # Tab 5: Habitabilidad
        self._setup_tab_habitabilidad()

        # Tab 6: Salud/Educación
        self._setup_tab_salud_educacion()

        # Tab 7: Diagnóstico
        self._setup_tab_diagnostico()

        # Inicializar con nuevo informe
        self._nuevo_informe()

    def _setup_tab_profesional(self):
        """Tab 1: Datos del profesional."""
        tab = self.tab_view.add("1. Profesional")
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        self.prof_entries = {}
        fields = [
            ("entidad_emisora", "Entidad Emisora:"),
            ("profesional_nombre", "Nombre del Profesional:"),
            ("profesional_apellidos", "Apellidos:"),
            ("numero_colegiatura", "Nº Colegiatura:"),
            ("destinatario", "Destinatario:"),
            ("fecha_emision", "Fecha de Emisión (DD/MM/AAAA):"),
            ("motivo", "Motivo del Informe:"),
        ]

        for key, label in fields:
            ctk.CTkLabel(scroll, text=label, font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
            entry = ctk.CTkEntry(scroll, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
            entry.pack(fill="x", pady=(0, 4))
            self.prof_entries[key] = entry

    def _setup_tab_identificacion(self):
        """Tab 2: Datos de identificación."""
        tab = self.tab_view.add("2. Identificación")
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        self.iden_entries = {}
        fields = [
            ("nombres", "Nombres:"),
            ("apellidos", "Apellidos:"),
            ("dni_nie", "DNI/NIE:"),
            ("pasaporte", "Pasaporte:"),
            ("direccion", "Dirección:"),
            ("telefono", "Teléfono:"),
            ("telefono_alt", "Teléfono Alternativo:"),
            ("email", "Email:"),
            ("fecha_nacimiento", "Fecha de Nacimiento (DD/MM/AAAA):"),
            ("edad", "Edad:"),
            ("nacionalidad", "Nacionalidad:"),
        ]

        for key, label in fields:
            ctk.CTkLabel(scroll, text=label, font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
            entry = ctk.CTkEntry(scroll, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
            entry.pack(fill="x", pady=(0, 4))
            self.iden_entries[key] = entry

        # Sexo
        ctk.CTkLabel(scroll, text="Sexo:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.iden_sexo = ctk.CTkComboBox(scroll, values=["", "Masculino", "Femenino", "Otro"], fg_color=COLORS["surface"], text_color=COLORS["text"])
        self.iden_sexo.pack(fill="x", pady=(0, 4))

        # Estado civil
        ctk.CTkLabel(scroll, text="Estado Civil:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.iden_estado_civil = ctk.CTkComboBox(scroll, values=["", "Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Unión libre"], fg_color=COLORS["surface"], text_color=COLORS["text"])
        self.iden_estado_civil.pack(fill="x", pady=(0, 4))

    def _setup_tab_convivencia(self):
        """Tab 3: Unidad de convivencia."""
        tab = self.tab_view.add("3. Convivencia")
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll, text="Miembros de la Unidad de Convivencia", font=FONTS["heading"], text_color="#0e98d6").pack(anchor="w", pady=(0, 8))

        # Frame para agregar miembros
        add_frame = ctk.CTkFrame(scroll, fg_color=COLORS["surface"])
        add_frame.pack(fill="x", pady=(0, 8))

        self.miembro_nombre = ctk.CTkEntry(add_frame, placeholder_text="Nombre", fg_color=COLORS["border"], text_color=COLORS["text"], width=120)
        self.miembro_nombre.pack(side="left", padx=4, pady=4)

        self.miembro_parentesco = ctk.CTkComboBox(add_frame, values=["Padre", "Madre", "Hijo", "Hija", "Cónyuge", "Abuelo", "Abuela", "Otro"], fg_color=COLORS["border"], text_color=COLORS["text"], width=100)
        self.miembro_parentesco.pack(side="left", padx=4, pady=4)

        self.miembro_edad = ctk.CTkEntry(add_frame, placeholder_text="Edad", fg_color=COLORS["border"], text_color=COLORS["text"], width=60)
        self.miembro_edad.pack(side="left", padx=4, pady=4)

        self.miembro_ocupacion = ctk.CTkEntry(add_frame, placeholder_text="Ocupación", fg_color=COLORS["border"], text_color=COLORS["text"], width=100)
        self.miembro_ocupacion.pack(side="left", padx=4, pady=4)

        self.miembro_situacion = ctk.CTkComboBox(add_frame, values=["Empleado", "Desempleado", "Jubilado", "Estudiante", "Discapacidad", "Otro"], fg_color=COLORS["border"], text_color=COLORS["text"], width=100)
        self.miembro_situacion.pack(side="left", padx=4, pady=4)

        self.miembro_ingresos = ctk.CTkEntry(add_frame, placeholder_text="Ingresos", fg_color=COLORS["border"], text_color=COLORS["text"], width=80)
        self.miembro_ingresos.pack(side="left", padx=4, pady=4)

        ctk.CTkButton(add_frame, text="➕ Agregar", command=self._agregar_miembro, fg_color="#0e98d6", text_color="white", width=80).pack(side="left", padx=4, pady=4)

        # Lista de miembros
        self.miembros_list = ctk.CTkScrollableFrame(scroll, fg_color=COLORS["surface"], label_text="Miembros Agregados")
        self.miembros_list.pack(fill="both", expand=True, pady=(0, 8))

        self.miembros_agregados = []

        # Historia familiar
        ctk.CTkLabel(scroll, text="Historia y Dinámica Familiar:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.historia_familiar = ctk.CTkTextbox(scroll, height=80, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.historia_familiar.pack(fill="x", pady=(0, 4))

        # Dinámica
        ctk.CTkLabel(scroll, text="Tipo de Relaciones:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.dinamica_relaciones = ctk.CTkComboBox(scroll, values=["", "Conflictivas", "De apoyo", "Neutras", "Mixtas"], fg_color=COLORS["surface"], text_color=COLORS["text"])
        self.dinamica_relaciones.pack(fill="x", pady=(0, 4))

    def _setup_tab_socioeconomica(self):
        """Tab 4: Socioeconómica."""
        tab = self.tab_view.add("4. Socioeconómica")
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # INGRESOS
        ctk.CTkLabel(scroll, text="💰 INGRESOS MENSUALES", font=FONTS["heading"], text_color="#0e98d6").pack(anchor="w", pady=(0, 8))

        self.ingresos_entries = {}
        ingresos_fields = [
            ("salarios", "Salarios:"),
            ("pensiones", "Pensiones:"),
            ("subsidios", "Subsidios/Ayudas:"),
            ("otros", "Otros Ingresos:"),
        ]

        for key, label in ingresos_fields:
            frame = ctk.CTkFrame(scroll, fg_color="transparent")
            frame.pack(fill="x", pady=2)
            ctk.CTkLabel(frame, text=label, font=FONTS["normal"], text_color=COLORS["text"], width=150).pack(side="left")
            entry = ctk.CTkEntry(frame, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
            entry.pack(side="left", fill="x", expand=True)
            self.ingresos_entries[key] = entry

        # EGRESOS
        ctk.CTkLabel(scroll, text="💸 EGRESOS MENSUALES", font=FONTS["heading"], text_color="#0e98d6").pack(anchor="w", pady=(16, 8))

        self.egresos_entries = {}
        egresos_fields = [
            ("alquiler", "Alquiler:"),
            ("hipoteca", "Hipoteca:"),
            ("servicios", "Servicios (luz, agua, gas):"),
            ("alimentacion", "Alimentación:"),
            ("otros", "Otros Egresos:"),
        ]

        for key, label in egresos_fields:
            frame = ctk.CTkFrame(scroll, fg_color="transparent")
            frame.pack(fill="x", pady=2)
            ctk.CTkLabel(frame, text=label, font=FONTS["normal"], text_color=COLORS["text"], width=150).pack(side="left")
            entry = ctk.CTkEntry(frame, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
            entry.pack(side="left", fill="x", expand=True)
            self.egresos_entries[key] = entry

        # Situación empleo
        ctk.CTkLabel(scroll, text="Situación de Empleo Principal:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(16, 0))
        self.situacion_empleo = ctk.CTkComboBox(scroll, values=["", "Empleado/a", "Desempleado/a", "Informal", "Jubilado/a", "Estudiante", "Otro"], fg_color=COLORS["surface"], text_color=COLORS["text"])
        self.situacion_empleo.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(scroll, text="Duración del Desempleo (si aplica):", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.duracion_desempleo = ctk.CTkEntry(scroll, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.duracion_desempleo.pack(fill="x", pady=(0, 4))

    def _setup_tab_habitabilidad(self):
        """Tab 5: Habitabilidad."""
        tab = self.tab_view.add("5. Habitabilidad")
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        fields_combo = [
            ("regimen_tenencia", "Régimen de Tenencia:", ["", "Propia", "Alquilada", "Cedida", "Precariedad", "Situación de calle"]),
            ("tipo_vivienda", "Tipo de Vivienda:", ["", "Casa", "Departamento", "Cuarto", "Choza", "Refugio", "Otro"]),
            ("hacinamiento", "Hacinamiento:", ["", "Sí", "No"]),
            ("estado_infraestructura", "Estado de Infraestructura:", ["", "Buena", "Regular", "Mala", "Precaria"]),
            ("materiales", "Materiales de Construcción:", ["", "Ladrillo", "Madera", "Cartón", "Chapa", "Mixto", "Otro"]),
            ("acceso_transporte", "Acceso a Transporte:", ["", "Bueno", "Regular", "Difícil"]),
        ]

        self.hab_entries = {}
        self.hab_combos = {}

        for key, label, values in fields_combo:
            ctk.CTkLabel(scroll, text=label, font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
            combo = ctk.CTkComboBox(scroll, values=values, fg_color=COLORS["surface"], text_color=COLORS["text"])
            combo.pack(fill="x", pady=(0, 4))
            self.hab_combos[key] = combo

        # Números
        ctk.CTkLabel(scroll, text="Número de Habitaciones:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.hab_habitaciones = ctk.CTkEntry(scroll, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.hab_habitaciones.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(scroll, text="Número de Dormitorios:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.hab_dormitorios = ctk.CTkEntry(scroll, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.hab_dormitorios.pack(fill="x", pady=(0, 4))

        # Servicios
        ctk.CTkLabel(scroll, text="Servicios Básicos:", font=FONTS["heading"], text_color="#0e98d6").pack(anchor="w", pady=(16, 8))

        self.serv_agua = ctk.CTkCheckBox(scroll, text="Agua Potable", text_color=COLORS["text"])
        self.serv_agua.pack(anchor="w", pady=2)

        self.serv_electricidad = ctk.CTkCheckBox(scroll, text="Electricidad", text_color=COLORS["text"])
        self.serv_electricidad.pack(anchor="w", pady=2)

        self.serv_gas = ctk.CTkCheckBox(scroll, text="Gas", text_color=COLORS["text"])
        self.serv_gas.pack(anchor="w", pady=2)

        self.serv_cloacas = ctk.CTkCheckBox(scroll, text="Cloacas", text_color=COLORS["text"])
        self.serv_cloacas.pack(anchor="w", pady=2)

        ctk.CTkLabel(scroll, text="Equipamiento del Barrio:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.hab_equipamiento = ctk.CTkTextbox(scroll, height=60, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.hab_equipamiento.pack(fill="x", pady=(0, 4))

    def _setup_tab_salud_educacion(self):
        """Tab 6: Salud y educación."""
        tab = self.tab_view.add("6. Salud/Educación")
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # SALUD
        ctk.CTkLabel(scroll, text="🏥 SALUD", font=FONTS["heading"], text_color="#0e98d6").pack(anchor="w", pady=(0, 8))

        ctk.CTkLabel(scroll, text="Enfermedades Crónicas:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.sal_enfermedades = ctk.CTkTextbox(scroll, height=60, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.sal_enfermedades.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(scroll, text="Discapacidades:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.sal_discapacidades = ctk.CTkTextbox(scroll, height=60, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.sal_discapacidades.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(scroll, text="Situación de Dependencia:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.sal_dependencia = ctk.CTkComboBox(scroll, values=["", "Ninguna", "Grado I (Leve)", "Grado II (Moderada)", "Grado III (Severa)"], fg_color=COLORS["surface"], text_color=COLORS["text"])
        self.sal_dependencia.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(scroll, text="Adicciones:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.sal_adicciones = ctk.CTkTextbox(scroll, height=40, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.sal_adicciones.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(scroll, text="Medicamentos:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.sal_medicamentos = ctk.CTkTextbox(scroll, height=40, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.sal_medicamentos.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(scroll, text="Cobertura de Salud:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.sal_cobertura = ctk.CTkComboBox(scroll, values=["", "Obra Social", "PAMI", "Sin cobertura", "Otra"], fg_color=COLORS["surface"], text_color=COLORS["text"])
        self.sal_cobertura.pack(fill="x", pady=(0, 4))

        # EDUCACIÓN
        ctk.CTkLabel(scroll, text="📚 EDUCACIÓN", font=FONTS["heading"], text_color="#0e98d6").pack(anchor="w", pady=(16, 8))

        ctk.CTkLabel(scroll, text="Nivel Académico:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.edu_nivel = ctk.CTkComboBox(scroll, values=["", "Sin instrucción", "Primario incompleto", "Primario completo", "Secundario incompleto", "Secundario completo", "Terciario", "Universitario"], fg_color=COLORS["surface"], text_color=COLORS["text"])
        self.edu_nivel.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(scroll, text="Asistencia Escolar:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.edu_asistencia = ctk.CTkComboBox(scroll, values=["", "Regular", "Irregular", "Abandonó", "Nunca asistió"], fg_color=COLORS["surface"], text_color=COLORS["text"])
        self.edu_asistencia.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(scroll, text="Escolaridad de Menores:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.edu_menores = ctk.CTkTextbox(scroll, height=60, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.edu_menores.pack(fill="x", pady=(0, 4))

    def _setup_tab_diagnostico(self):
        """Tab 7: Diagnóstico."""
        tab = self.tab_view.add("7. Diagnóstico")
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll, text="📝 JUICIO TÉCNICO PROFESIONAL", font=FONTS["heading"], text_color="#0e98d6").pack(anchor="w", pady=(0, 8))
        ctk.CTkLabel(scroll, text="Análisis interpretativo y objetivo sobre la situación:", font=FONTS["small"], text_color=COLORS["text_muted"]).pack(anchor="w")
        self.diag_juicio = ctk.CTkTextbox(scroll, height=100, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.diag_juicio.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(scroll, text="⚠️ VULNERABILIDADES IDENTIFICADAS", font=FONTS["heading"], text_color="#0e98d6").pack(anchor="w", pady=(8, 8))
        self.diag_vulnerabilidades = ctk.CTkTextbox(scroll, height=80, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.diag_vulnerabilidades.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(scroll, text="💪 FORTALEZAS IDENTIFICADAS", font=FONTS["heading"], text_color="#0e98d6").pack(anchor="w", pady=(8, 8))
        self.diag_fortalezas = ctk.CTkTextbox(scroll, height=80, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.diag_fortalezas.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(scroll, text="📋 PROPUESTA DE INTERVENCIÓN", font=FONTS["heading"], text_color="#0e98d6").pack(anchor="w", pady=(8, 8))
        self.diag_propuesta = ctk.CTkTextbox(scroll, height=100, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.diag_propuesta.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(scroll, text="📞 RECURSOS SOLICITADOS", font=FONTS["heading"], text_color="#0e98d6").pack(anchor="w", pady=(8, 8))
        self.diag_recursos = ctk.CTkTextbox(scroll, height=60, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.diag_recursos.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(scroll, text="⏱️ PLAZO DE INTERVENCIÓN:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.diag_plazo = ctk.CTkEntry(scroll, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.diag_plazo.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(scroll, text="🔄 SEGUIMIENTO PROPUESTO:", font=FONTS["normal"], text_color=COLORS["text"]).pack(anchor="w", pady=(8, 0))
        self.diag_seguimiento = ctk.CTkEntry(scroll, fg_color=COLORS["surface"], text_color=COLORS["text"], border_color=COLORS["border"])
        self.diag_seguimiento.pack(fill="x", pady=(0, 4))

    def _nuevo_informe(self):
        """Crea un nuevo informe vacío."""
        self.current_informe = self.informe_manager.create_informe()
        self._limpiar_formulario()
        logger.info("📄 Nuevo informe creado")

    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        # Profesional
        for entry in self.prof_entries.values():
            entry.delete(0, "end")

        # Identificación
        for entry in self.iden_entries.values():
            entry.delete(0, "end")
        self.iden_sexo.set("")
        self.iden_estado_civil.set("")

        # Miembros
        for widget in self.miembros_list.winfo_children():
            widget.destroy()
        self.miembros_agregados = []
        self.historia_familiar.delete("1.0", "end")
        self.dinamica_relaciones.set("")

        # Socioeconómica
        for entry in self.ingresos_entries.values():
            entry.delete(0, "end")
        for entry in self.egresos_entries.values():
            entry.delete(0, "end")
        self.situacion_empleo.set("")
        self.duracion_desempleo.delete(0, "end")

        # Habitabilidad
        for combo in self.hab_combos.values():
            combo.set("")
        self.hab_habitaciones.delete(0, "end")
        self.hab_dormitorios.delete(0, "end")
        self.serv_agua.deselect()
        self.serv_electricidad.deselect()
        self.serv_gas.deselect()
        self.serv_cloacas.deselect()
        self.hab_equipamiento.delete("1.0", "end")

        # Salud/Educación
        self.sal_enfermedades.delete("1.0", "end")
        self.sal_discapacidades.delete("1.0", "end")
        self.sal_dependencia.set("")
        self.sal_adicciones.delete("1.0", "end")
        self.sal_medicamentos.delete("1.0", "end")
        self.sal_cobertura.set("")
        self.edu_nivel.set("")
        self.edu_asistencia.set("")
        self.edu_menores.delete("1.0", "end")

        # Diagnóstico
        self.diag_juicio.delete("1.0", "end")
        self.diag_vulnerabilidades.delete("1.0", "end")
        self.diag_fortalezas.delete("1.0", "end")
        self.diag_propuesta.delete("1.0", "end")
        self.diag_recursos.delete("1.0", "end")
        self.diag_plazo.delete(0, "end")
        self.diag_seguimiento.delete(0, "end")

    def _agregar_miembro(self):
        """Agrega un miembro a la unidad de convivencia."""
        nombre = self.miembro_nombre.get().strip()
        if not nombre:
            return

        miembro = MiembroFamiliar(
            nombre=nombre,
            parentesco=self.miembro_parentesco.get(),
            edad=int(self.miembro_edad.get()) if self.miembro_edad.get().isdigit() else 0,
            ocupacion=self.miembro_ocupacion.get(),
            situacion_laboral=self.miembro_situacion.get(),
            ingresos=float(self.miembro_ingresos.get()) if self.miembro_ingresos.get() else 0.0
        )

        self.miembros_agregados.append(miembro)

        # Mostrar en lista
        card = ctk.CTkFrame(self.miembros_list, fg_color=COLORS["border"], corner_radius=4)
        card.pack(fill="x", pady=2, padx=2)

        info = f"{miembro.nombre} ({miembro.parentesco}) - {miembro.edad} años - {miembro.ocupacion}"
        ctk.CTkLabel(card, text=info, font=FONTS["small"], text_color=COLORS["text"]).pack(side="left", padx=4)

        ctk.CTkButton(card, text="❌", command=lambda c=card, m=miembro: self._eliminar_miembro(c, m),
                     fg_color=COLORS["danger"], text_color="white", width=30, height=20).pack(side="right", padx=4)

        # Limpiar campos
        self.miembro_nombre.delete(0, "end")
        self.miembro_edad.delete(0, "end")
        self.miembro_ocupacion.delete(0, "end")
        self.miembro_ingresos.delete(0, "end")

    def _eliminar_miembro(self, card, miembro):
        """Elimina un miembro de la lista."""
        card.destroy()
        self.miembros_agregados.remove(miembro)

    def _guardar_informe(self):
        """Guarda el informe actual en la base de datos."""
        if not self.current_informe:
            self.current_informe = self.informe_manager.create_informe()

        # Datos profesional
        self.current_informe.datos_profesional.entidad_emisora = self.prof_entries["entidad_emisora"].get()
        self.current_informe.datos_profesional.profesional_nombre = self.prof_entries["profesional_nombre"].get()
        self.current_informe.datos_profesional.profesional_apellidos = self.prof_entries["profesional_apellidos"].get()
        self.current_informe.datos_profesional.numero_colegiatura = self.prof_entries["numero_colegiatura"].get()
        self.current_informe.datos_profesional.destinatario = self.prof_entries["destinatario"].get()
        self.current_informe.datos_profesional.fecha_emision = self.prof_entries["fecha_emision"].get()
        self.current_informe.datos_profesional.motivo = self.prof_entries["motivo"].get()

        # Identificación
        self.current_informe.datos_identificacion.nombres = self.iden_entries["nombres"].get()
        self.current_informe.datos_identificacion.apellidos = self.iden_entries["apellidos"].get()
        self.current_informe.datos_identificacion.dni_nie = self.iden_entries["dni_nie"].get()
        self.current_informe.datos_identificacion.pasaporte = self.iden_entries["pasaporte"].get()
        self.current_informe.datos_identificacion.direccion = self.iden_entries["direccion"].get()
        self.current_informe.datos_identificacion.telefono = self.iden_entries["telefono"].get()
        self.current_informe.datos_identificacion.telefono_alt = self.iden_entries["telefono_alt"].get()
        self.current_informe.datos_identificacion.email = self.iden_entries["email"].get()
        self.current_informe.datos_identificacion.fecha_nacimiento = self.iden_entries["fecha_nacimiento"].get()
        self.current_informe.datos_identificacion.edad = int(self.iden_entries["edad"].get()) if self.iden_entries["edad"].get().isdigit() else 0
        self.current_informe.datos_identificacion.nacionalidad = self.iden_entries["nacionalidad"].get()
        self.current_informe.datos_identificacion.sexo = self.iden_sexo.get()
        self.current_informe.datos_identificacion.estado_civil = self.iden_estado_civil.get()

        # Unidad convivencia
        self.current_informe.unidad_convivencia.miembros = self.miembros_agregados
        self.current_informe.unidad_convivencia.historia_familiar = self.historia_familiar.get("1.0", "end").strip()
        self.current_informe.unidad_convivencia.dinamica_relaciones = self.dinamica_relaciones.get()

        # Socioeconómica
        self.current_informe.socioeconomica.ingresos_salarios = float(self.ingresos_entries["salarios"].get() or 0)
        self.current_informe.socioeconomica.ingresos_pensiones = float(self.ingresos_entries["pensiones"].get() or 0)
        self.current_informe.socioeconomica.ingresos_subsidios = float(self.ingresos_entries["subsidios"].get() or 0)
        self.current_informe.socioeconomica.ingresos_otros = float(self.ingresos_entries["otros"].get() or 0)
        self.current_informe.socioeconomica.egresos_alquiler = float(self.egresos_entries["alquiler"].get() or 0)
        self.current_informe.socioeconomica.egresos_hipoteca = float(self.egresos_entries["hipoteca"].get() or 0)
        self.current_informe.socioeconomica.egresos_servicios = float(self.egresos_entries["servicios"].get() or 0)
        self.current_informe.socioeconomica.egresos_alimentacion = float(self.egresos_entries["alimentacion"].get() or 0)
        self.current_informe.socioeconomica.egresos_otros = float(self.egresos_entries["otros"].get() or 0)
        self.current_informe.socioeconomica.situacion_empleo_principal = self.situacion_empleo.get()
        self.current_informe.socioeconomica.duracion_desempleo = self.duracion_desempleo.get()

        # Habitabilidad
        self.current_informe.habitabilidad.regimen_tenencia = self.hab_combos["regimen_tenencia"].get()
        self.current_informe.habitabilidad.tipo_vivienda = self.hab_combos["tipo_vivienda"].get()
        self.current_informe.habitabilidad.num_habitaciones = int(self.hab_habitaciones.get() or 0)
        self.current_informe.habitabilidad.num_dormitorios = int(self.hab_dormitorios.get() or 0)
        self.current_informe.habitabilidad.hacinamiento = self.hab_combos["hacinamiento"].get()
        self.current_informe.habitabilidad.estado_infraestructura = self.hab_combos["estado_infraestructura"].get()
        self.current_informe.habitabilidad.materiales = self.hab_combos["materiales"].get()
        self.current_informe.habitabilidad.acceso_transporte = self.hab_combos["acceso_transporte"].get()
        self.current_informe.habitabilidad.agua_potable = self.serv_agua.get()
        self.current_informe.habitabilidad.electricidad = self.serv_electricidad.get()
        self.current_informe.habitabilidad.gas = self.serv_gas.get()
        self.current_informe.habitabilidad.cloacas = self.serv_cloacas.get()
        self.current_informe.habitabilidad.equipamiento_barrio = self.hab_equipamiento.get("1.0", "end").strip()

        # Salud/Educación
        self.current_informe.salud_educacion.enfermedades_cronicas = self.sal_enfermedades.get("1.0", "end").strip()
        self.current_informe.salud_educacion.discapacidades = self.sal_discapacidades.get("1.0", "end").strip()
        self.current_informe.salud_educacion.situacion_dependencia = self.sal_dependencia.get()
        self.current_informe.salud_educacion.adicciones = self.sal_adicciones.get("1.0", "end").strip()
        self.current_informe.salud_educacion.medicamentos = self.sal_medicamentos.get("1.0", "end").strip()
        self.current_informe.salud_educacion.cobertura_salud = self.sal_cobertura.get()
        self.current_informe.salud_educacion.nivel_academico = self.edu_nivel.get()
        self.current_informe.salud_educacion.asistencia_escolar = self.edu_asistencia.get()
        self.current_informe.salud_educacion.escolaridad_menores = self.edu_menores.get("1.0", "end").strip()

        # Diagnóstico
        self.current_informe.diagnostico.juicio_tecnico = self.diag_juicio.get("1.0", "end").strip()
        self.current_informe.diagnostico.vulnerabilidades = self.diag_vulnerabilidades.get("1.0", "end").strip()
        self.current_informe.diagnostico.fortalezas = self.diag_fortalezas.get("1.0", "end").strip()
        self.current_informe.diagnostico.propuesta_intervencion = self.diag_propuesta.get("1.0", "end").strip()
        self.current_informe.diagnostico.recursos_solicitados = self.diag_recursos.get("1.0", "end").strip()
        self.current_informe.diagnostico.plazo_intervencion = self.diag_plazo.get()
        self.current_informe.diagnostico.seguimiento = self.diag_seguimiento.get()

        # Guardar
        if self.informe_manager.save_informe(self.current_informe):
            logger.info(f"✅ Informe guardado: {self.current_informe.id}")

    def _exportar_pdf(self):
        """Exporta el informe actual a PDF."""
        if not self.current_informe:
            logger.warning("No hay informe para exportar")
            return

        # Primero guardar
        self._guardar_informe()

        # Generar PDF
        try:
            generator = PDFGenerator()
            path = generator.generate_pdf(self.current_informe)
            logger.info(f"✅ PDF exportado: {path}")
        except Exception as e:
            logger.error(f"Error exportando PDF: {e}")

    def _listar_informes(self):
        """Muestra lista de informes guardados."""
        informes = self.informe_manager.list_informes()
        logger.info(f"📋 {len(informes)} informes guardados")
