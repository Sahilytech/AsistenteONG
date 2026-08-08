"""
Panel de búsqueda y filtrado de recursos - Usa resources_data.py real
"""

import customtkinter as ctk
from typing import List, Dict
import logging

from .styles import COLORS, FONTS, SPACING
from ..resources_data import RESOURCES_DATABASE

logger = logging.getLogger(__name__)

# Extraer tipos de recursos de la base de datos real
RESOURCE_TYPES = {}
for key, value in RESOURCES_DATABASE.items():
    RESOURCE_TYPES[key] = value.get("name", key)

REGIONS = ["Todas", "CABA", "GBA", "La Plata", "Mendoza", "Bahía Blanca", "Nacional", "USA", "Europa", "Uruguay", "Chile", "Otro"]


class ResourcesPanel(ctk.CTkFrame):
    """Panel para búsqueda y filtrado de recursos."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.current_results = []
        self._setup_ui()

    def _setup_ui(self):
        """Configura el panel."""

        # Título
        title = ctk.CTkLabel(
            self,
            text="🔍 Búsqueda de Recursos",
            font=FONTS["heading"],
            text_color=COLORS["primary"]
        )
        title.pack(anchor="w", pady=(0, SPACING["md"]), padx=SPACING["md"])

        # Frame de filtros
        filter_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"])
        filter_frame.pack(fill="x", padx=SPACING["md"], pady=(0, SPACING["md"]))

        # Tipo de recurso
        ctk.CTkLabel(filter_frame, text="Tipo:", text_color=COLORS["text"]).pack(side="left", padx=5, pady=10)
        self.type_var = ctk.StringVar(value="Todos")
        type_combo = ctk.CTkComboBox(
            filter_frame,
            values=["Todos"] + list(RESOURCE_TYPES.values()),
            variable=self.type_var,
            command=self._on_filter_change,
            fg_color=COLORS["border"],
            text_color=COLORS["text"],
            width=180
        )
        type_combo.pack(side="left", padx=5, pady=10)

        # Región
        ctk.CTkLabel(filter_frame, text="Región:", text_color=COLORS["text"]).pack(side="left", padx=5, pady=10)
        self.region_var = ctk.StringVar(value="Todas")
        region_combo = ctk.CTkComboBox(
            filter_frame,
            values=REGIONS,
            variable=self.region_var,
            command=self._on_filter_change,
            fg_color=COLORS["border"],
            text_color=COLORS["text"],
            width=120
        )
        region_combo.pack(side="left", padx=5, pady=10)

        # Botón buscar
        search_btn = ctk.CTkButton(
            filter_frame,
            text="🔎 Buscar",
            command=self._on_search,
            fg_color=COLORS["primary"],
            text_color="white",
            width=100
        )
        search_btn.pack(side="left", padx=5, pady=10)

        # Frame de resultados con scroll
        results_container = ctk.CTkFrame(self, fg_color="transparent")
        results_container.pack(fill="both", expand=True, padx=SPACING["md"], pady=SPACING["md"])

        # Label de resultados
        self.results_label = ctk.CTkLabel(
            results_container,
            text="",
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        )
        self.results_label.pack(anchor="w", pady=(0, SPACING["sm"]))

        # Scroll de resultados
        self.results_scroll = ctk.CTkScrollableFrame(
            results_container,
            fg_color=COLORS["surface"],
            label_text="Resultados"
        )
        self.results_scroll.pack(fill="both", expand=True)

        # Inicializar con búsqueda vacía
        self._on_search()

    def _on_filter_change(self, choice=None):
        """Al cambiar filtro, buscar automáticamente."""
        self._on_search()

    def _on_search(self):
        """Realiza búsqueda con filtros usando datos reales."""
        selected_type = self.type_var.get()
        selected_region = self.region_var.get()

        # Convertir tipo seleccionado de vuelta a clave
        type_key = None
        if selected_type != "Todos":
            for key, label in RESOURCE_TYPES.items():
                if label == selected_type:
                    type_key = key
                    break

        # Filtrar recursos de la base de datos REAL
        results = []

        if type_key:
            # Buscar solo en ese tipo
            resource_data = RESOURCES_DATABASE.get(type_key, {})
            items = resource_data.get("phone", []) + resource_data.get("locations", [])
            for item in items:
                if selected_region == "Todas" or item.get("país", item.get("ciudad", "")) == selected_region:
                    results.append(item)
        else:
            # Todos los tipos
            for key, resource_data in RESOURCES_DATABASE.items():
                items = resource_data.get("phone", []) + resource_data.get("locations", [])
                for item in items:
                    if selected_region == "Todas" or item.get("país", item.get("ciudad", "")) == selected_region:
                        results.append(item)

        self.current_results = results
        self._display_results(results, selected_type, selected_region)

    def _display_results(self, results: List[Dict], type_filter: str, region_filter: str):
        """Muestra resultados en el panel."""

        # Limpiar scroll anterior
        for widget in self.results_scroll.winfo_children():
            widget.destroy()

        # Actualizar label
        self.results_label.configure(
            text=f"📊 {len(results)} recurso(s) encontrado(s)"
        )

        if not results:
            no_results = ctk.CTkLabel(
                self.results_scroll,
                text="❌ No hay recursos que coincidan con los filtros",
                text_color=COLORS["text_muted"],
                font=FONTS["small"]
            )
            no_results.pack(pady=SPACING["lg"])
            return

        # Mostrar cada recurso
        for resource in results:
            self._create_resource_card(resource)

    def _create_resource_card(self, resource: Dict):
        """Crea tarjeta de recurso."""

        card = ctk.CTkFrame(self.results_scroll, fg_color=COLORS["border"], corner_radius=8)
        card.pack(fill="x", pady=SPACING["sm"], padx=5)

        # Nombre
        name = resource.get("nombre", resource.get("name", "Sin nombre"))
        name_label = ctk.CTkLabel(
            card,
            text=f"📍 {name}",
            font=FONTS["normal"],
            text_color=COLORS["primary"],
            justify="left"
        )
        name_label.pack(anchor="w", pady=(SPACING["sm"], 0), padx=SPACING["sm"])

        # Teléfono
        phone = resource.get("numero", resource.get("teléfono", resource.get("phone", "N/A")))
        phone_label = ctk.CTkLabel(
            card,
            text=f"☎️  {phone}",
            font=FONTS["small"],
            text_color=COLORS["text"],
            justify="left"
        )
        phone_label.pack(anchor="w", padx=SPACING["sm"])

        # Ubicación y horario
        region = resource.get("país", resource.get("ciudad", "N/A"))
        hours = resource.get("horario", resource.get("hours", "N/A"))
        tipo = resource.get("tipo", resource.get("especialidades", "General"))

        info_parts = [f"📍 {region}"]
        if hours != "N/A":
            info_parts.append(f"🕐 {hours}")
        if tipo != "General" and tipo:
            info_parts.append(f"📋 {tipo}")

        info_label = ctk.CTkLabel(
            card,
            text=" | ".join(info_parts),
            font=FONTS["small"],
            text_color=COLORS["text_muted"],
            justify="left"
        )
        info_label.pack(anchor="w", pady=(0, SPACING["sm"]), padx=SPACING["sm"])

        # Botón copiar teléfono
        copy_btn = ctk.CTkButton(
            card,
            text="📋 Copiar teléfono",
            font=FONTS["small"],
            width=120,
            height=25,
            fg_color=COLORS["primary"],
            text_color="white",
            command=lambda p=phone: self._copy_phone(p)
        )
        copy_btn.pack(anchor="e", pady=(0, SPACING["sm"]), padx=SPACING["sm"])

    def _copy_phone(self, phone: str):
        """Copia teléfono al portapapeles."""
        try:
            import subprocess
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
            process.communicate(str(phone).encode('utf-8'))
            logger.info(f"✅ Copiado: {phone}")
        except:
            logger.warning("No se pudo copiar al portapapeles")
