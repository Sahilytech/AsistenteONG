"""
Panel de búsqueda y filtrado de recursos
Organismos, teléfonos, información de ayuda
"""

import customtkinter as ctk
from typing import List, Dict
import logging

from .styles import COLORS, FONTS, SPACING

logger = logging.getLogger(__name__)


# Recursos de ejemplo (en producción vienen de DB)
SAMPLE_RESOURCES = {
    "hospital": [
        {"name": "Hospital Central", "phone": "911", "region": "CABA", "hours": "24/7"},
        {"name": "Hospital Clínico", "phone": "4444-1234", "region": "CABA", "hours": "24/7"},
        {"name": "Hospital San Martín", "phone": "4567-8901", "region": "GBA", "hours": "Lun-Vie 8-18"},
    ],
    "refugio": [
        {"name": "Refugio María", "phone": "0800-555-1234", "region": "CABA", "hours": "24/7"},
        {"name": "Casa de las Mujeres", "phone": "4111-2345", "region": "CABA", "hours": "24/7"},
        {"name": "Hogar de Tránsito", "phone": "3456-7890", "region": "GBA", "hours": "24/7"},
    ],
    "abogado": [
        {"name": "Asesoría Legal Gratuita", "phone": "0800-333-4444", "region": "CABA", "hours": "Lun-Vie 9-17"},
        {"name": "Defensoría Pública", "phone": "4321-0987", "region": "CABA", "hours": "Lun-Vie 8-16"},
        {"name": "Centro Jurídico", "phone": "5678-1234", "region": "GBA", "hours": "Lun-Jue 10-18"},
    ],
    "psicólogo": [
        {"name": "Centro de Salud Mental", "phone": "4111-5555", "region": "CABA", "hours": "Lun-Vie 8-20"},
        {"name": "Consultorio Psicológico", "phone": "3333-6666", "region": "CABA", "hours": "Lun-Sáb 9-18"},
    ],
    "linea_crisis": [
        {"name": "Línea de Crisis 24/7", "phone": "0800-666-7777", "region": "Nacional", "hours": "24/7"},
        {"name": "Teleasistencia", "phone": "0800-888-9999", "region": "Nacional", "hours": "24/7"},
    ]
}

RESOURCE_TYPES = {
    "hospital": "🏥 Hospital",
    "refugio": "🏠 Refugio",
    "abogado": "⚖️ Asesoría Legal",
    "psicólogo": "🧠 Psicólogo",
    "linea_crisis": "📞 Línea Crisis"
}

REGIONS = ["Todas", "CABA", "GBA", "Nacional", "Otro"]


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
            width=150
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
        """Realiza búsqueda con filtros."""
        selected_type = self.type_var.get()
        selected_region = self.region_var.get()
        
        # Convertir tipo seleccionado de vuelta a clave
        type_key = None
        if selected_type != "Todos":
            for key, label in RESOURCE_TYPES.items():
                if label == selected_type:
                    type_key = key
                    break
        
        # Filtrar recursos
        results = []
        
        if type_key:
            resources = SAMPLE_RESOURCES.get(type_key, [])
        else:
            # Si "Todos", combinar todos
            resources = []
            for res_list in SAMPLE_RESOURCES.values():
                resources.extend(res_list)
        
        # Filtrar por región
        for res in resources:
            if selected_region == "Todas" or res["region"] == selected_region:
                results.append(res)
        
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
        name_label = ctk.CTkLabel(
            card,
            text=f"📍 {resource['name']}",
            font=FONTS["normal"],
            text_color=COLORS["primary"],
            justify="left"
        )
        name_label.pack(anchor="w", pady=(SPACING["sm"], 0), padx=SPACING["sm"])
        
        # Teléfono
        phone_label = ctk.CTkLabel(
            card,
            text=f"☎️  {resource['phone']}",
            font=FONTS["small"],
            text_color=COLORS["text"],
            justify="left"
        )
        phone_label.pack(anchor="w", padx=SPACING["sm"])
        
        # Región y horario
        info_label = ctk.CTkLabel(
            card,
            text=f"📍 {resource['region']} | 🕐 {resource['hours']}",
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
            command=lambda: self._copy_phone(resource['phone'])
        )
        copy_btn.pack(anchor="e", pady=(0, SPACING["sm"]), padx=SPACING["sm"])
    
    def _copy_phone(self, phone: str):
        """Copia teléfono al portapapeles."""
        try:
            import subprocess
            # Windows
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
            process.communicate(phone.encode('utf-8'))
            logger.info(f"✅ Copiado: {phone}")
        except:
            logger.warning("No se pudo copiar al portapapeles")
