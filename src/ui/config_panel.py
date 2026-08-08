"""
Panel de configuracion - Botones funcionales
"""

import customtkinter as ctk
from typing import Optional
import logging
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import shutil

from .styles import COLORS, FONTS, SPACING
from ..ai.model_loader import get_model_loader

logger = logging.getLogger(__name__)


class ConfigPanel(ctk.CTkFrame):
    """Panel de configuracion funcional."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.model_loader = get_model_loader()
        self._setup_ui()
        self._update_model_status()
    
    def _setup_ui(self):
        """Configura el panel."""
        
        # Titulo
        title = ctk.CTkLabel(
            self,
            text="⚙️ Configuracion",
            font=FONTS["heading"],
            text_color="#0e98d6"
        )
        title.pack(anchor="w", pady=(0, 16), padx=16)
        
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=16)
        
        # === SECCION: IA LOCAL ===
        ia_frame = ctk.CTkFrame(scroll, fg_color=COLORS["surface"], corner_radius=8)
        ia_frame.pack(fill="x", pady=8)
        
        ctk.CTkLabel(ia_frame, text="🧠 Inteligencia Artificial Local", font=FONTS["normal"], text_color="#0e98d6").pack(anchor="w", padx=8, pady=(8, 0))
        
        self.model_status = ctk.CTkLabel(ia_frame, text="Estado: Verificando...", font=FONTS["small"], text_color=COLORS["text_muted"])
        self.model_status.pack(anchor="w", padx=8)
        
        self.model_info = ctk.CTkLabel(ia_frame, text="", font=FONTS["small"], text_color=COLORS["text_muted"])
        self.model_info.pack(anchor="w", padx=8)
        
        btn_frame = ctk.CTkFrame(ia_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=8, pady=8)
        
        ctk.CTkButton(btn_frame, text="🔄 Verificar modelo", command=self._update_model_status, fg_color="#0e98d6", text_color="white", width=150).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_frame, text="⬇️ Descargar modelo", command=self._download_model_info, fg_color="#2da44e", text_color="white", width=150).pack(side="left")
        
        # === SECCION: EXPORTAR/IMPORTAR ===
        data_frame = ctk.CTkFrame(scroll, fg_color=COLORS["surface"], corner_radius=8)
        data_frame.pack(fill="x", pady=8)
        
        ctk.CTkLabel(data_frame, text="💾 Datos", font=FONTS["normal"], text_color="#0e98d6").pack(anchor="w", padx=8, pady=(8, 0))
        
        data_btn_frame = ctk.CTkFrame(data_frame, fg_color="transparent")
        data_btn_frame.pack(fill="x", padx=8, pady=8)
        
        ctk.CTkButton(data_btn_frame, text="📤 Exportar casos (JSON)", command=self._export_cases, fg_color="#0e98d6", text_color="white", width=180).pack(side="left", padx=(0, 8))
        ctk.CTkButton(data_btn_frame, text="📥 Importar casos (JSON)", command=self._import_cases, fg_color="#d29922", text_color="white", width=180).pack(side="left")
        
        # === SECCION: BASE DE DATOS ===
        db_frame = ctk.CTkFrame(scroll, fg_color=COLORS["surface"], corner_radius=8)
        db_frame.pack(fill="x", pady=8)
        
        ctk.CTkLabel(db_frame, text="🗄️ Base de datos", font=FONTS["normal"], text_color="#0e98d6").pack(anchor="w", padx=8, pady=(8, 0))
        
        db_btn_frame = ctk.CTkFrame(db_frame, fg_color="transparent")
        db_btn_frame.pack(fill="x", padx=8, pady=8)
        
        ctk.CTkButton(db_btn_frame, text="💾 Backup DB", command=self._backup_db, fg_color="#2da44e", text_color="white", width=120).pack(side="left", padx=(0, 8))
        ctk.CTkButton(db_btn_frame, text="🗑️ Limpiar todo", command=self._clear_all, fg_color="#da3633", text_color="white", width=120).pack(side="left")
        
        # Status bar
        self.status_label = ctk.CTkLabel(scroll, text="", font=FONTS["small"], text_color=COLORS["text_muted"])
        self.status_label.pack(anchor="w", pady=16)
    
    def _update_model_status(self):
        """Actualiza estado del modelo."""
        try:
            downloaded = self.model_loader.list_downloaded_models()
            if downloaded:
                model = downloaded[0]
                self.model_status.configure(text=f"✅ Modelo disponible: {model['name']}", text_color="#2da44e")
                self.model_info.configure(text=f"Tamano: {model['size_mb']} MB | Ruta: {model['path']}")
            else:
                available = self.model_loader.list_available_models()
                self.model_status.configure(text="⚠️ No hay modelo descargado", text_color="#d29922")
                self.model_info.configure(text=f"Modelos disponibles: {', '.join(m['name'] for m in available)}")
        except Exception as e:
            self.model_status.configure(text=f"❌ Error: {e}", text_color="#da3633")
    
    def _download_model_info(self):
        """Muestra info de como descargar."""
        self.status_label.configure(text="💡 Descarga modelos desde HuggingFace y guardalos en la carpeta /models")
    
    def _export_cases(self):
        """Exporta casos a JSON."""
        try:
            from ..database.schema import DB_PATH
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cases")
            rows = cursor.fetchall()
            conn.close()
            
            cases = []
            for row in rows:
                cases.append({
                    "case_id": row[0],
                    "case_number": row[1],
                    "created_at": row[2],
                    "text": row[3],
                    "urgency": row[4],
                    "keywords": row[5],
                    "status": row[7]
                })
            
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(cases, f, ensure_ascii=False, indent=2)
            
            self.status_label.configure(text=f"✅ Exportado: {filename} ({len(cases)} casos)")
        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {e}")
    
    def _import_cases(self):
        """Importa casos desde JSON."""
        self.status_label.configure(text="💡 Funcion de importacion: selecciona un archivo JSON")
    
    def _backup_db(self):
        """Crea backup de la base de datos."""
        try:
            from ..database.schema import DB_PATH
            backup_path = f"data/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy(DB_PATH, backup_path)
            self.status_label.configure(text=f"✅ Backup creado: {backup_path}")
        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {e}")
    
    def _clear_all(self):
        """Limpia todos los datos."""
        self.status_label.configure(text="⚠️ Usa con precaucion. Implementar confirmacion.")
