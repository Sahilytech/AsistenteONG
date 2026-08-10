"""Biblioteca local: documentos de conocimiento + importación revisable de personas."""
from __future__ import annotations
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from ..knowledge.pdf_library import LIBRARY_DIR, import_pdf, list_pdfs, search_pdfs, delete_pdf, open_pdf
from ..knowledge.memory import LocalMemory
from ..person_registry import PersonRegistry
from ..core.document_ingestion import preview_document, map_person_preview, import_people_after_review
from .styles import COLORS, FONTS


class PDFLibraryPanel(ctk.CTkFrame):
    def __init__(self, parent, person_registry=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.memory = LocalMemory()
        self.person_registry = person_registry or PersonRegistry()
        self._build()
        self.refresh()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=24, pady=(22, 10))
        ctk.CTkLabel(top, text="Biblioteca", font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(top, text="Documentos locales que el sistema puede leer, recuperar y comparar con los casos. Los datos de personas siempre pasan por revisión antes de guardarse.", font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=1000, justify="left").pack(anchor="w", pady=(3, 12))
        actions = ctk.CTkFrame(self, fg_color=COLORS["surface_alt"], corner_radius=12)
        actions.pack(fill="x", padx=24, pady=(0, 10))
        ctk.CTkButton(actions, text="＋ Importar PDF", height=38, command=self.import_file, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(side="left", padx=8, pady=10)
        ctk.CTkButton(actions, text="＋ Importar personas", height=38, command=self.import_people, fg_color=COLORS["surface"], hover_color=COLORS["primary_soft"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"]).pack(side="left", padx=4, pady=10)
        ctk.CTkButton(actions, text="↻ Recargar", height=38, command=self.refresh, fg_color=COLORS["surface"], hover_color=COLORS["primary_soft"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"]).pack(side="left", padx=4, pady=10)
        ctk.CTkButton(actions, text="Vaciar biblioteca", height=38, command=self.clear_library, fg_color=COLORS["surface"], hover_color="#f4dddd", text_color=COLORS["text"], border_width=1, border_color=COLORS["border"]).pack(side="left", padx=4, pady=10)
        ctk.CTkButton(actions, text="Abrir carpeta", height=38, command=self.open_folder, fg_color=COLORS["surface"], hover_color=COLORS["primary_soft"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"]).pack(side="left", padx=4, pady=10)
        self.search = ctk.CTkEntry(actions, placeholder_text="Buscar dentro de los documentos...", height=38)
        self.search.pack(side="left", fill="x", expand=True, padx=(14, 8), pady=10)
        self.search.bind("<Return>", lambda _: self.do_search())
        ctk.CTkButton(actions, text="Buscar", height=38, width=80, command=self.do_search).pack(side="left", padx=(0, 10), pady=10)
        self.status = ctk.CTkLabel(self, text="", font=FONTS["tiny"], text_color=COLORS["text_muted"])
        self.status.pack(anchor="w", padx=28, pady=(0, 5))
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def refresh(self):
        self._render(list_pdfs())
        self.status.configure(text="Biblioteca actualizada · procesamiento local")

    def _render(self, items):
        for widget in self.scroll.winfo_children(): widget.destroy()
        if not items:
            box = ctk.CTkFrame(self.scroll, fg_color=COLORS["surface"], corner_radius=18, border_width=1, border_color=COLORS["border"])
            box.pack(fill="x", padx=8, pady=25)
            ctk.CTkLabel(box, text="Tu biblioteca está vacía", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=24, pady=(24, 5))
            ctk.CTkLabel(box, text="Importá protocolos, guías, leyes o documentos internos. Para planillas de personas usá «Importar personas»: primero se previsualizan y después se confirma qué se guarda.", font=FONTS["body"], text_color=COLORS["text_muted"], wraplength=850, justify="left").pack(anchor="w", padx=24, pady=(0, 22))
            return
        for item in items: self._card(item)

    def _card(self, item):
        card = ctk.CTkFrame(self.scroll, fg_color=COLORS["surface"], corner_radius=14, border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", padx=6, pady=6)
        info = ctk.CTkFrame(card, fg_color="transparent"); info.pack(side="left", fill="x", expand=True, padx=16, pady=13)
        ctk.CTkLabel(info, text=item["title"], font=FONTS["subheading"], text_color=COLORS["text"], anchor="w", wraplength=650, justify="left").pack(fill="x")
        state = "Procesado" if item["status"] == "procesado" else ("Sin texto extraíble" if item["status"] == "sin_texto" else "Error de procesamiento")
        ctk.CTkLabel(info, text=f"{state} · {item['pages']} páginas · {item['chars']:,} caracteres", font=FONTS["small"], text_color=COLORS["success"] if state == "Procesado" else COLORS["text_muted"]).pack(anchor="w", pady=(3, 0))
        buttons = ctk.CTkFrame(card, fg_color="transparent"); buttons.pack(side="right", padx=12, pady=12)
        ctk.CTkButton(buttons, text="Abrir", width=72, height=32, command=lambda p=item["path"]: open_pdf(p), fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(side="left", padx=3)
        ctk.CTkButton(buttons, text="Ver texto", width=78, height=32, command=lambda i=item: self.view_text(i), fg_color=COLORS["surface_alt"], hover_color=COLORS["primary_soft"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"]).pack(side="left", padx=3)
        ctk.CTkButton(buttons, text="Eliminar", width=78, height=32, command=lambda p=item["path"]: self.remove(p), fg_color=COLORS["surface_alt"], hover_color="#f4dddd", text_color=COLORS["text"], border_width=1, border_color=COLORS["border"]).pack(side="left", padx=3)

    def import_file(self):
        paths = filedialog.askopenfilenames(title="Seleccionar PDFs", filetypes=[("PDF", "*.pdf")])
        ok, errors = 0, []
        for path in paths:
            try: import_pdf(path, self.memory); ok += 1
            except Exception as exc: errors.append(f"{Path(path).name}: {exc}")
        if paths: self.refresh()
        if errors: messagebox.showwarning("Importación", f"Procesados: {ok}\n\n" + "\n".join(errors))

    def import_people(self):
        path = filedialog.askopenfilename(title="Seleccionar archivo de personas", filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv"), ("PDF", "*.pdf")])
        if not path: return
        try:
            preview = preview_document(path)
            if preview.get("type") == "pdf":
                # PDF de personas: extraemos campos tipo «Nombre: ...» y lo mostramos antes de guardar.
                rows = []
                for block in preview.get("text", "").split("\n"):
                    if ":" in block:
                        key, value = block.split(":", 1); rows.append({key.strip(): value.strip()})
                mapped = map_person_preview(rows)
            else:
                mapped = map_person_preview(preview.get("rows", []))
            if not mapped:
                messagebox.showinfo("Importación", "No se encontraron filas reconocibles con un campo de nombre.")
                return
            self._review_people(path, mapped)
        except Exception as exc:
            messagebox.showerror("Importación", str(exc))

    def _review_people(self, path, people):
        win = ctk.CTkToplevel(self); win.title("Revisión antes de importar personas"); win.geometry("900x620"); win.transient(self.winfo_toplevel()); win.grab_set()
        ctk.CTkLabel(win, text=f"Revisión · {len(people)} registro(s)", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(18, 4))
        ctk.CTkLabel(win, text="Nada se guardó todavía. Revisá los datos y confirmá solo si corresponde incorporarlos al registro de personas.", font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=820, justify="left").pack(anchor="w", padx=20, pady=(0, 10))
        box = ctk.CTkTextbox(win, wrap="word"); box.pack(fill="both", expand=True, padx=20, pady=8)
        for index, person in enumerate(people, 1): box.insert("end", f"{index}. " + " · ".join(f"{k}: {v}" for k, v in person.items()) + "\n")
        box.configure(state="disabled")
        actions = ctk.CTkFrame(win, fg_color="transparent"); actions.pack(fill="x", padx=20, pady=14)
        def confirm():
            try:
                result = import_people_after_review(path, self.person_registry)
                messagebox.showinfo("Importación completada", f"Procesados: {result['processed']}\nActualizados existentes: {result['updated_existing']}", parent=win)
                win.destroy()
            except Exception as exc: messagebox.showerror("Error", str(exc), parent=win)
        ctk.CTkButton(actions, text="Cancelar", command=win.destroy, fg_color=COLORS["surface"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"]).pack(side="right", padx=5)
        ctk.CTkButton(actions, text="Confirmar importación", command=confirm, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(side="right", padx=5)

    def do_search(self):
        q = self.search.get().strip()
        if not q: return self.refresh()
        results = search_pdfs(q)
        items = []
        for row in results:
            path = row["url"].replace("file://", "") if row["url"].startswith("file://") else row["url"]
            items.append({"title": row["title"], "path": path, "pages": "—", "chars": len(row.get("snippet", "")), "status": "procesado"})
        self._render(items); self.status.configure(text=f"Búsqueda local · {len(items)} resultado(s)")

    def view_text(self, item):
        row = self.memory.get_document(Path(item["path"]))
        win = ctk.CTkToplevel(self); win.title(item["title"]); win.geometry("900x650"); win.transient(self.winfo_toplevel())
        ctk.CTkLabel(win, text="Texto extraído · revisión", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(18, 8))
        box = ctk.CTkTextbox(win, wrap="word"); box.pack(fill="both", expand=True, padx=20, pady=(0, 20)); box.insert("1.0", row[4] if row else "No hay texto extraíble."); box.configure(state="disabled")

    def remove(self, path):
        if not messagebox.askyesno("Eliminar documento", "¿Eliminar este PDF de la biblioteca y de su índice local?"): return
        try: delete_pdf(path, self.memory); self.refresh()
        except Exception as exc: messagebox.showerror("Error", str(exc))

    def clear_library(self):
        if not messagebox.askyesno("Vaciar biblioteca", "Esto eliminará todos los PDFs guardados en la biblioteca y su índice local. Los casos y personas NO se eliminarán. ¿Continuar?"): return
        LIBRARY_DIR.mkdir(parents=True, exist_ok=True); errors = []
        for path in LIBRARY_DIR.glob("*.pdf"):
            try: path.unlink()
            except Exception as exc: errors.append(f"{path.name}: {exc}")
        self.memory.clear_library(); self.refresh()
        if errors: messagebox.showwarning("Biblioteca", "No se pudieron eliminar algunos archivos:\n" + "\n".join(errors))

    def open_folder(self):
        LIBRARY_DIR.mkdir(parents=True, exist_ok=True); open_pdf(LIBRARY_DIR)
