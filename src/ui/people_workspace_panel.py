"""Ficha visual integral de persona para revisión profesional."""
from __future__ import annotations
import customtkinter as ctk
from .styles import COLORS, FONTS
from ..person_registry import PersonRegistry
from ..core.person_workspace import build_person_workspace
from ..knowledge.case_document_matcher import find_evidence

class PersonWorkspaceWindow:
    def __init__(self, parent, person: dict, registry: PersonRegistry | None = None):
        self.parent = parent
        self.registry = registry or PersonRegistry()
        self.person = person
        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"Ficha integral · {person.get('name','Persona')}")
        self.window.geometry("1120x820")
        self.window.minsize(900, 650)
        self.window.transient(parent)
        self._build()

    def _build(self):
        root = ctk.CTkScrollableFrame(self.window, fg_color=COLORS["background"])
        root.pack(fill="both", expand=True, padx=18, pady=18)
        head = ctk.CTkFrame(root, fg_color=COLORS["surface"], corner_radius=18, border_width=1, border_color=COLORS["border"])
        head.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(head, text=self.person.get("name", "Persona"), font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(16, 2))
        ctk.CTkLabel(head, text="Ficha integral · historial longitudinal · evidencia documental", font=FONTS["small"], text_color=COLORS["primary"]).pack(anchor="w", padx=20, pady=(0, 16))
        info = " · ".join(str(self.person.get(k)) for k in ("document_id", "birth_date", "gender_identity", "sexual_orientation") if self.person.get(k)) or "Sin datos adicionales cargados"
        ctk.CTkLabel(root, text=info, font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=1000).pack(anchor="w", padx=8, pady=(0, 10))
        cases = self.registry.cases(self.person["person_id"])
        workspace = build_person_workspace(self.person, cases, [])
        self._section(root, "HISTORIAL", f"{workspace['case_count']} caso(s) asociado(s)")
        timeline = ctk.CTkFrame(root, fg_color=COLORS["surface_alt"], corner_radius=14, border_width=1, border_color=COLORS["border"])
        timeline.pack(fill="x", pady=5)
        if not cases:
            ctk.CTkLabel(timeline, text="Todavía no hay casos asociados.", font=FONTS["small"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=16, pady=16)
        for case in cases:
            text = (case.get("text") or "").replace("\n", " ")
            card = ctk.CTkFrame(timeline, fg_color=COLORS["surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(card, text=case.get("case_number", "Caso"), font=FONTS["small_bold"], text_color=COLORS["primary"]).pack(anchor="w", padx=12, pady=(9, 1))
            ctk.CTkLabel(card, text=f"{case.get('created_at','')} · {case.get('case_type') or 'Caso'} · {case.get('status','')}", font=FONTS["tiny"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=12)
            ctk.CTkLabel(card, text=text[:500], font=FONTS["small"], text_color=COLORS["text"], wraplength=950, justify="left").pack(anchor="w", padx=12, pady=(3, 10))
            if text:
                evidence = find_evidence(text, limit=3)
                if evidence:
                    ctk.CTkLabel(card, text="Evidencia local relacionada", font=FONTS["small_bold"], text_color=COLORS["success"]).pack(anchor="w", padx=12, pady=(2, 2))
                    for item in evidence:
                        ctk.CTkLabel(card, text=f"• {item.get('title','Fuente')} — {item.get('snippet','')[:260]}", font=FONTS["tiny"], text_color=COLORS["text_muted"], wraplength=930, justify="left").pack(anchor="w", padx=18, pady=2)
        review = ctk.CTkFrame(root, fg_color=COLORS["warning_soft"], corner_radius=14, border_width=1, border_color=COLORS["border"])
        review.pack(fill="x", pady=10)
        ctk.CTkLabel(review, text="REVISIÓN PROFESIONAL REQUERIDA", font=FONTS["small_bold"], text_color=COLORS["warning"]).pack(anchor="w", padx=16, pady=(12, 3))
        ctk.CTkLabel(review, text="La documentación recuperada funciona como evidencia de apoyo. No constituye una decisión, diagnóstico ni conclusión automática.", font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=980, justify="left").pack(fill="x", padx=16, pady=(0, 12))

    @staticmethod
    def _section(parent, title, value):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=(8, 2))
        ctk.CTkLabel(row, text=title, font=FONTS["tiny"], text_color=COLORS["primary"]).pack(side="left")
        ctk.CTkLabel(row, text=value, font=FONTS["small"], text_color=COLORS["text_muted"]).pack(side="right")
