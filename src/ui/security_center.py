"""Centro de seguridad y copias para la interfaz local."""
from __future__ import annotations

import datetime
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from ..core.security_controls import create_encrypted_backup, restore_encrypted_backup, secret_verifier
from .styles import COLORS, FONTS


class SecurityCenter(ctk.CTkScrollableFrame):
    """Panel operativo: sesión, backup cifrado y restauración explícita."""

    def __init__(self, parent, session_guard=None, on_secret_configured=None, **kwargs):
        kwargs.pop("fg_color", None)
        super().__init__(parent, fg_color=COLORS["background"], **kwargs)
        self.session_guard = session_guard
        self.on_secret_configured = on_secret_configured
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Centro de Seguridad", font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w", padx=24, pady=(22, 2))
        ctk.CTkLabel(self, text="Protegé la sesión y gestioná copias cifradas sin salir de la aplicación.", font=FONTS["small"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=24, pady=(0, 18))

        session = self._card("Sesión", "El programa puede bloquearse automáticamente después de un período sin actividad. La frase se usa solo para verificar el desbloqueo y no se guarda en texto plano.")
        self.timeout = ctk.CTkEntry(session, placeholder_text="Minutos de inactividad (1–120)")
        self.timeout.insert(0, str(max(1, int((self.session_guard.timeout_seconds if self.session_guard else 900) / 60))))
        self.timeout.pack(fill="x", padx=18, pady=5)
        self.secret = ctk.CTkEntry(session, placeholder_text="Nueva frase de desbloqueo", show="•")
        self.secret.pack(fill="x", padx=18, pady=5)
        self.secret_confirm = ctk.CTkEntry(session, placeholder_text="Repetir frase", show="•")
        self.secret_confirm.pack(fill="x", padx=18, pady=5)
        row = ctk.CTkFrame(session, fg_color="transparent"); row.pack(fill="x", padx=18, pady=(5, 14))
        ctk.CTkButton(row, text="Guardar seguridad", command=self._save_security, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(side="left")
        ctk.CTkButton(row, text="Bloquear ahora", command=self._lock_now, fg_color=COLORS["surface"], hover_color=COLORS["primary_soft"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"]).pack(side="left", padx=8)
        self.session_status = ctk.CTkLabel(session, text="", font=FONTS["tiny"], text_color=COLORS["text_muted"]); self.session_status.pack(anchor="w", padx=18, pady=(0, 12))

        backup = self._card("Backup cifrado", "La copia incluye los datos locales de la aplicación dentro de un archivo cifrado y autenticado. Elegí una frase distinta y fuerte; sin ella no se puede restaurar la copia.")
        self.backup_path = ctk.CTkEntry(backup, placeholder_text="Archivo de destino (.ong)"); self.backup_path.pack(fill="x", padx=18, pady=5)
        brow = ctk.CTkFrame(backup, fg_color="transparent"); brow.pack(fill="x", padx=18, pady=5)
        ctk.CTkButton(brow, text="Elegir destino", command=self._choose_backup, fg_color=COLORS["surface"], hover_color=COLORS["primary_soft"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"]).pack(side="left")
        ctk.CTkButton(brow, text="Crear backup", command=self._backup, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(side="left", padx=8)
        self.backup_secret = ctk.CTkEntry(backup, placeholder_text="Frase del backup", show="•"); self.backup_secret.pack(fill="x", padx=18, pady=5)
        self.backup_status = ctk.CTkLabel(backup, text="", font=FONTS["tiny"], text_color=COLORS["text_muted"]); self.backup_status.pack(anchor="w", padx=18, pady=(2, 12))

        restore = self._card("Restaurar backup", "La restauración sobrescribe archivos con el mismo nombre en el destino elegido. Hacé una copia de seguridad antes de reemplazar datos existentes.")
        self.restore_path = ctk.CTkEntry(restore, placeholder_text="Archivo .ong"); self.restore_path.pack(fill="x", padx=18, pady=5)
        rrow = ctk.CTkFrame(restore, fg_color="transparent"); rrow.pack(fill="x", padx=18, pady=5)
        ctk.CTkButton(rrow, text="Elegir backup", command=self._choose_restore, fg_color=COLORS["surface"], hover_color=COLORS["primary_soft"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"]).pack(side="left")
        ctk.CTkButton(rrow, text="Elegir carpeta destino", command=self._choose_target, fg_color=COLORS["surface"], hover_color=COLORS["primary_soft"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"]).pack(side="left", padx=8)
        self.restore_target = ctk.CTkEntry(restore, placeholder_text="Carpeta destino"); self.restore_target.pack(fill="x", padx=18, pady=5)
        self.restore_secret = ctk.CTkEntry(restore, placeholder_text="Frase del backup", show="•"); self.restore_secret.pack(fill="x", padx=18, pady=5)
        ctk.CTkButton(restore, text="Restaurar", command=self._restore, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(anchor="e", padx=18, pady=(5, 14))
        self.restore_status = ctk.CTkLabel(restore, text="", font=FONTS["tiny"], text_color=COLORS["text_muted"]); self.restore_status.pack(anchor="w", padx=18, pady=(0, 12))

        info = self._card("Buenas prácticas", "No compartas el archivo de backup ni su frase. Restaurá únicamente en una carpeta confiable. El sistema mantiene la decisión profesional fuera de cualquier automatización.")
        ctk.CTkLabel(info, text="Última actualización del centro: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), font=FONTS["tiny"], text_color=COLORS["text_soft"]).pack(anchor="w", padx=18, pady=(0, 14))

    def _card(self, title, text):
        card = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=14, border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", padx=24, pady=6)
        ctk.CTkLabel(card, text=title, font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=18, pady=(14, 3))
        ctk.CTkLabel(card, text=text, font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=920, justify="left").pack(fill="x", padx=18, pady=(0, 10))
        return card

    def _save_security(self):
        try:
            minutes = int(self.timeout.get().strip())
            if not 1 <= minutes <= 120:
                raise ValueError("El tiempo debe estar entre 1 y 120 minutos.")
            secret = self.secret.get()
            if len(secret) < 8 or secret != self.secret_confirm.get():
                raise ValueError("La frase debe tener al menos 8 caracteres y coincidir.")
            if self.session_guard:
                self.session_guard.timeout_seconds = minutes * 60
            if self.on_secret_configured:
                self.on_secret_configured(secret_verifier(secret))
            self.secret.delete(0, "end"); self.secret_confirm.delete(0, "end")
            self.session_status.configure(text=f"Seguridad actualizada. Bloqueo por inactividad: {minutes} min.")
        except ValueError as exc:
            self.session_status.configure(text=str(exc))

    def _lock_now(self):
        if not self.session_guard:
            return
        if not getattr(self.winfo_toplevel(), "app_controller", None).session_verifier:
            self.session_status.configure(text="Primero configurá una frase de desbloqueo.")
            return
        self.session_guard.lock()
        self.winfo_toplevel().app_controller.show_lock_screen()

    def _choose_backup(self):
        path = filedialog.asksaveasfilename(title="Guardar backup cifrado", defaultextension=".ong", filetypes=[("Backup Asistente ONG", "*.ong")])
        if path:
            self.backup_path.delete(0, "end"); self.backup_path.insert(0, path)

    def _backup(self):
        output = self.backup_path.get().strip(); secret = self.backup_secret.get()
        if not output or len(secret) < 8:
            self.backup_status.configure(text="Elegí un destino y usá una frase de al menos 8 caracteres."); return
        source = Path(__file__).resolve().parents[2] / "data"
        try:
            create_encrypted_backup(source, output, secret)
            self.backup_secret.delete(0, "end")
            self.backup_status.configure(text=f"Backup cifrado creado: {Path(output).name}")
        except Exception as exc:
            self.backup_status.configure(text=f"No se pudo crear el backup: {exc}")

    def _choose_restore(self):
        path = filedialog.askopenfilename(title="Seleccionar backup", filetypes=[("Backup Asistente ONG", "*.ong")])
        if path:
            self.restore_path.delete(0, "end"); self.restore_path.insert(0, path)

    def _choose_target(self):
        path = filedialog.askdirectory(title="Elegir carpeta destino")
        if path:
            self.restore_target.delete(0, "end"); self.restore_target.insert(0, path)

    def _restore(self):
        backup, target, secret = self.restore_path.get().strip(), self.restore_target.get().strip(), self.restore_secret.get()
        if not backup or not target or len(secret) < 8:
            self.restore_status.configure(text="Seleccioná backup, carpeta destino y frase."); return
        if not messagebox.askyesno("Restaurar backup", "La restauración puede reemplazar archivos existentes en el destino. ¿Continuar?"):
            return
        try:
            restore_encrypted_backup(backup, target, secret)
            self.restore_secret.delete(0, "end")
            self.restore_status.configure(text="Backup restaurado correctamente. Reiniciá la aplicación para recargar los datos.")
        except Exception as exc:
            self.restore_status.configure(text=f"No se pudo restaurar: {exc}")
