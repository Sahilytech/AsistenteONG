"""
Panel de Ayuda - Tutorial e Instrucciones
"""

import customtkinter as ctk
from .styles import COLORS, FONTS, SPACING

class HelpPanel(ctk.CTkFrame):
    """Panel con tutorial e instrucciones."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura panel de ayuda."""
        
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Título
        ctk.CTkLabel(
            scroll,
            text="📚 TUTORIAL Y AYUDA",
            font=("Helvetica", 20, "bold"),
            text_color=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 20))
        
        # Sección 1: Inicio Rápido
        self._section(scroll, "🚀 INICIO RÁPIDO (3 pasos)", [
            "1. Ingresa el NÚMERO DE CASO en el panel izquierdo",
            "2. Escribe la DESCRIPCIÓN del caso (qué pasó, quién llama)",
            "3. Clic en '✅ Analizar caso'",
            "",
            "El sistema detectará automáticamente:",
            "   • Nivel de urgencia (Muy Alta, Alta, Media, Baja)",
            "   • Palabras clave encontradas",
            "   • Respuesta borrador personalizada",
            "   • Recursos sugeridos"
        ])
        
        # Sección 2: Cómo Usar Cada Tab
        self._section(scroll, "📋 CÓMO USAR CADA TAB", [
            "📊 DASHBOARD:",
            "   • Ver total de casos procesados",
            "   • Estadísticas de urgencia",
            "   • Historial de casos de hoy y esta semana",
            "",
            "📊 ANÁLISIS:",
            "   • Ver resultado del análisis automático",
            "   • Editar respuesta borrador",
            "   • Copiar al portapapeles",
            "   • Ver recursos sugeridos",
            "",
            "📞 RECURSOS:",
            "   • Buscar por tipo (Hospital, Refugio, etc)",
            "   • Filtrar por región",
            "   • Copiar teléfonos directamente",
            "",
            "⚙️ CONFIGURACIÓN:",
            "   • Ver palabras clave de cada categoría",
            "   • Editar plantillas de respuesta",
            "",
            "❓ AYUDA:",
            "   • Ves este tutorial"
        ])
        
        # Sección 3: Niveles de Urgencia
        self._section(scroll, "🚨 ENTENDER LOS NIVELES DE URGENCIA", [
            "🔴 MUY ALTA (Emergencia inmediata):",
            "   → Riesgo de vida (suicidio, armas)",
            "   → Violencia severa con hospitalizaciones",
            "   → Menores en peligro",
            "   → Violencia sexual",
            "   ⏰ ACCIÓN: Contactar emergencias YA",
            "",
            "🟠 ALTA (Requiere atención urgente):",
            "   → Violencia doméstica activa",
            "   → Crisis de salud mental",
            "   → Necesidad inmediata",
            "   ⏰ ACCIÓN: Contactar en horas",
            "",
            "🟡 MEDIA (Orientación necesaria):",
            "   → Asesoría legal",
            "   → Necesidad de recursos",
            "   ⏰ ACCIÓN: Dentro de 24 horas",
            "",
            "⚪ BAJA (Información):",
            "   → Sin palabras clave detectadas",
            "   ⏰ ACCIÓN: Seguimiento rutinario"
        ])
        
        # Sección 4: Palabras Clave Importantes
        self._section(scroll, "🔑 PALABRAS CLAVE QUE BUSCA EL SISTEMA", [
            "🔴 Riesgo de Vida:",
            "   suicidio, matar, muerte, arma, veneno, sobredosis",
            "",
            "🔴 Violencia Severa:",
            "   golpes, sangre, fractura, trauma, hospital, emergency",
            "",
            "🔴 Menores:",
            "   niño, niña, hijo, hija, bebé, abuso infantil",
            "",
            "🔴 Violencia Sexual:",
            "   violación, abuso sexual, tocamientos, forzada",
            "",
            "🟠 Violencia Doméstica:",
            "   pareja, marido, novio, golpeó, amenaza, controla",
            "",
            "🟠 Salud Mental:",
            "   depresión, ansiedad, pánico, autolesión, adicción",
            "",
            "🟠 Necesidad Inmediata:",
            "   ahora, urgente, emergencia, ayuda, SOS",
            "",
            "🟡 Legal:",
            "   abogado, demanda, custodia, divorcio, derechos",
            "",
            "🟡 Recursos:",
            "   refugio, dinero, trabajo, comida, vivienda, medicinas"
        ])
        
        # Sección 5: Tips Importantes
        self._section(scroll, "💡 TIPS PARA OPERADORES", [
            "✅ SER EMPÁTICO: La persona está pasando algo difícil",
            "✅ USAR LA RESPUESTA COMO BORRADOR: Personaliza según el caso",
            "✅ SIEMPRE PRIORIZAR SEGURIDAD: Si es Muy Alta, llamá ahora",
            "✅ GUARDAR DATOS: Los datos quedan en el historial",
            "✅ OFFLINE FUNCIONA: Sin internet sigue funcionando TODO",
            "✅ TELÉFONOS A MANO: Ten los números de emergencia listos",
            "✅ ESCUCHAR: A veces la persona solo necesita ser escuchada",
            "✅ NO ES REEMPLAZO: Somos asistentes, no reemplazamos a profesionales"
        ])
        
        # Sección 6: Privacidad
        self._section(scroll, "🔒 PRIVACIDAD Y SEGURIDAD", [
            "✅ TODO ES LOCAL: Los datos no salen de esta computadora",
            "✅ SIN INTERNET: No necesita conexión para funcionar",
            "✅ CIFRADO: Los datos sensibles están protegidos",
            "✅ CONFIDENCIAL: Las víctimas pueden confiar en la privacidad",
            "✅ CUMPLE GDPR: Compatible con leyes de protección de datos"
        ])
    
    def _section(self, parent, title: str, items: list):
        """Crea una sección de ayuda."""
        ctk.CTkLabel(
            parent,
            text=title,
            font=("Helvetica", 14, "bold"),
            text_color=COLORS["primary"]
        ).pack(anchor="w", pady=(15, 10))
        
        for item in items:
            if item == "":
                ctk.CTkFrame(parent, height=5, fg_color="transparent").pack()
            else:
                ctk.CTkLabel(
                    parent,
                    text=item,
                    font=("Helvetica", 11),
                    text_color=COLORS["text"],
                    justify="left",
                    wraplength=400
                ).pack(anchor="w", padx=10, pady=2)
