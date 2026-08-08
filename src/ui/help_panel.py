"""
Panel de ayuda - Tutorial interactivo paso a paso
"""

import customtkinter as ctk
from typing import List, Dict
import logging

from .styles import COLORS, FONTS, SPACING

logger = logging.getLogger(__name__)


TUTORIAL_STEPS = [
    {
        "title": "1️⃣ Bienvenida",
        "content": """Bienvenido al Asistente ONG.

Esta herramienta te ayuda a:
• Organizar casos de lineas de ayuda
• Detectar urgencias automaticamente
• Encontrar recursos relevantes
• Generar borradores de respuesta
• Crear informes sociales profesionales

Todo funciona 100% OFFLINE. Sin internet."""
    },
    {
        "title": "2️⃣ Crear un caso",
        "content": """Para crear un caso:

1. El numero se genera automaticamente
2. Escribi la descripcion en el panel izquierdo
3. Hace clic en "Analizar y Guardar caso"
4. El sistema detecta la urgencia y categoria

💡 Tip: Cuanto mas detalle des, mejor el analisis."""
    },
    {
        "title": "3️⃣ Revisar el analisis",
        "content": """En la pestana "Analisis" vas a ver:

• 🚨 Nivel de urgencia (Muy Alta a Baja)
• 🔑 Palabras clave detectadas
• 📨 Borrador de respuesta automatico
• 📞 Recursos sugeridos

⚠️ IMPORTANTE: El borrador es solo una guia.
Siempre revisalo antes de enviarlo."""
    },
    {
        "title": "4️⃣ Informes Sociales",
        "content": """En la pestana "Informes":

• Completa los 7 tabs con datos del caso
• Agrega miembros de la unidad de convivencia
• Guarda el informe en la base de datos
• Exporta a PDF profesional

Los informes siguen la estructura estandar
de trabajo social con todas las secciones
requeridas."""
    },
    {
        "title": "5️⃣ Buscar recursos",
        "content": """En la pestana "Recursos":

• Filtra por tipo (salud, legal, etc.)
• Filtra por region
• Hace clic en "Copiar telefono"
• Los datos vienen de la base local

💡 Si no encontras algo, podes agregarlo
en Configuracion."""
    },
    {
        "title": "6️⃣ Dashboard",
        "content": """El Dashboard muestra:

• 📋 Total de casos
• 🔴 Casos de muy alta urgencia
• 📅 Casos de hoy y esta semana
• 📜 Historial reciente

Todo se guarda automaticamente en la base
de datos local."""
    },
    {
        "title": "7️⃣ Configuracion",
        "content": """En Configuracion podes:

• Cambiar entre tema claro/oscuro
• Ver estado de la IA local
• Exportar/Importar datos
• Configurar el modelo de IA

💡 Para usar IA avanzada, descarga un
modelo GGUF en la carpeta /models."""
    },
    {
        "title": "8️⃣ Modo offline",
        "content": """La app funciona sin internet:

• ✅ Analisis por reglas (siempre)
• ✅ Base de datos local
• ✅ Recursos locales
• ✅ Informes y PDFs
• ⚠️ IA avanzada (solo si descargaste modelo)

Para actualizar recursos necesitas internet
temporalmente."""
    },
    {
        "title": "9️⃣ Privacidad",
        "content": """Tus datos estan protegidos:

• 🔒 Todo queda en tu computadora
• 🔒 Sin enviar a servidores externos
• 🔒 Sin conexion a internet requerida
• 🔒 Base de datos local cifrada

Solo vos tenes acceso a la informacion."""
    },
    {
        "title": "🔟 Atajos de teclado",
        "content": """Atajos utiles:

• Ctrl+N: Nuevo caso
• Ctrl+S: Guardar informe
• Ctrl+E: Exportar PDF
• Ctrl+T: Cambiar tema
• F1: Esta ayuda

💡 El sistema guarda automaticamente
cada 30 segundos."""
    }
]


class HelpPanel(ctk.CTkFrame):
    """Panel de ayuda con tutorial paso a paso."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.current_step = 0
        self._setup_ui()

    def _setup_ui(self):
        """Configura el panel de ayuda."""

        # Titulo
        title = ctk.CTkLabel(
            self,
            text="❓ Centro de Ayuda",
            font=FONTS["heading"],
            text_color="#0e98d6"
        )
        title.pack(anchor="w", pady=(0, 16), padx=16)

        # Indicador de paso
        self.step_indicator = ctk.CTkLabel(
            self,
            text=f"Paso 1 de {len(TUTORIAL_STEPS)}",
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        )
        self.step_indicator.pack(anchor="w", padx=16)

        # Barra de progreso
        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(fill="x", padx=16, pady=8)
        self.progress.set(1 / len(TUTORIAL_STEPS))

        # Frame del contenido
        self.content_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=8)
        self.content_frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Titulo del paso
        self.step_title = ctk.CTkLabel(
            self.content_frame,
            text="",
            font=FONTS["heading"],
            text_color="#0e98d6",
            wraplength=500,
            justify="left"
        )
        self.step_title.pack(anchor="w", padx=16, pady=(16, 8))

        # Contenido del paso
        self.step_content = ctk.CTkLabel(
            self.content_frame,
            text="",
            font=FONTS["normal"],
            text_color=COLORS["text"],
            wraplength=500,
            justify="left"
        )
        self.step_content.pack(anchor="w", padx=16, pady=(0, 16))

        # Botones de navegacion
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=16, pady=16)

        self.prev_btn = ctk.CTkButton(
            nav_frame,
            text="◀ Anterior",
            command=self._prev_step,
            fg_color=COLORS["muted"],
            text_color="white",
            width=120
        )
        self.prev_btn.pack(side="left")

        self.next_btn = ctk.CTkButton(
            nav_frame,
            text="Siguiente ▶",
            command=self._next_step,
            fg_color="#0e98d6",
            text_color="white",
            width=120
        )
        self.next_btn.pack(side="right")

        # Mostrar primer paso
        self._show_step(0)

    def _show_step(self, index: int):
        """Muestra un paso especifico."""
        if 0 <= index < len(TUTORIAL_STEPS):
            step = TUTORIAL_STEPS[index]
            self.step_title.configure(text=step["title"])
            self.step_content.configure(text=step["content"])
            self.step_indicator.configure(text=f"Paso {index + 1} de {len(TUTORIAL_STEPS)}")
            self.progress.set((index + 1) / len(TUTORIAL_STEPS))

            # Actualizar botones
            self.prev_btn.configure(state="normal" if index > 0 else "disabled")
            self.next_btn.configure(state="normal" if index < len(TUTORIAL_STEPS) - 1 else "disabled")

            self.current_step = index

    def _next_step(self):
        """Paso siguiente."""
        if self.current_step < len(TUTORIAL_STEPS) - 1:
            self._show_step(self.current_step + 1)

    def _prev_step(self):
        """Paso anterior."""
        if self.current_step > 0:
            self._show_step(self.current_step - 1)
