"""Ventana principal: navegación lateral y espacio de trabajo integrado."""
import customtkinter as ctk, logging, inspect
from pathlib import Path
from PIL import Image
from .results_panel import ResultsFrame
from .resources_panel import ResourcesPanel
from .dashboard import DashboardFrame
from .config_panel import ConfigPanel
from .help_panel import HelpPanel
from .integrated_case_panel import IntegratedCasePanel
from .cases_panel import CasesPanel
from .people_panel import PeoplePanel
from .pdf_library_panel import PDFLibraryPanel
from .workspace_panels import FollowUpPanel, AgendaPanel
from .security_center import SecurityCenter
from .onboarding import show_first_run
from .styles import COLORS, FONTS
from ..case_manager import CaseManager
from ..config_manager import ConfigManager
from ..knowledge.memory import LocalMemory
from ..person_registry import PersonRegistry
from ..knowledge.case_document_matcher import build_case_context
from ..core.security_controls import SessionGuard

logger = logging.getLogger(__name__)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AboutPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=28, pady=22)
        ctk.CTkLabel(scroll, text="Acerca de Asistente ONG", font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(scroll, text="Personas · casos · documentación · seguimiento", font=FONTS["subheading"], text_color=COLORS["primary"]).pack(anchor="w", pady=(4, 18))
        for title, text in [
            ("PROPÓSITO", "Herramienta de apoyo para equipos de asistencia. Organiza información y tareas repetitivas sin reemplazar la revisión profesional."),
            ("PERSONAS Y CASOS", "Una persona puede tener múltiples casos. El registro de persona se reutiliza y cada atención queda como un caso separado dentro de su historial."),
            ("DOCUMENTACIÓN", "Los PDFs se procesan localmente y sus fragmentos relevantes pueden recuperarse al analizar un caso. Las coincidencias se muestran como apoyo documental, no como conclusiones."),
            ("PRIVACIDAD", "El almacenamiento prioriza este equipo. Los campos personales sensibles son opcionales y la organización debe cargar únicamente lo necesario."),
            ("LÍMITES", "El análisis no diagnostica ni decide por sí solo cuestiones legales, sanitarias o de protección. Requiere revisión humana."),
        ]:
            card = ctk.CTkFrame(scroll, fg_color=COLORS["surface_alt"], corner_radius=16, border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", pady=6)
            ctk.CTkLabel(card, text=title, font=FONTS["subheading"], text_color=COLORS["primary"]).pack(anchor="w", padx=20, pady=(15, 6))
            ctk.CTkLabel(card, text=text, font=FONTS["body"], text_color=COLORS["text"], justify="left", anchor="w", wraplength=950).pack(fill="x", padx=20, pady=(0, 18))


class MainWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Asistente ONG | Triaje y Canalización")
        self.root.geometry("1500x900")
        self.root.minsize(1080, 700)
        self.root.configure(fg_color=COLORS["background"])
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.nav_buttons = []
        self._ui_ready = False
        self._initializing = True
        self._setup_shell()
        # Tk puede pintar la pantalla de carga antes de iniciar los servicios pesados.
        self.root.after_idle(self._initialize_services)

    def _setup_shell(self):
        self.loading_frame = ctk.CTkFrame(self.root, fg_color=COLORS["background"], corner_radius=0)
        self.loading_frame.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.loading_frame, text="ASISTENTE ONG", font=FONTS["title"], text_color=COLORS["primary"]).place(relx=.5, rely=.44, anchor="center")
        ctk.CTkLabel(self.loading_frame, text="Preparando espacio de trabajo…", font=FONTS["body"], text_color=COLORS["text_muted"]).place(relx=.5, rely=.51, anchor="center")
        self.loading_bar = ctk.CTkProgressBar(self.loading_frame, width=360, mode="indeterminate", progress_color=COLORS["primary"])
        self.loading_bar.place(relx=.5, rely=.57, anchor="center")
        self.loading_bar.start()

    def _initialize_services(self):
        try:
            self.case_manager = CaseManager()
            self.person_registry = PersonRegistry()
            self.config_manager = ConfigManager()
            self.memory = LocalMemory()
            self.session_guard = SessionGuard(timeout_seconds=900)
            self.session_guard.start()
            self.session_verifier = None
            self._lock_window = None
            self._setup_ui()
            self.root.app_controller = self
            self.root.bind_all("<Any-KeyPress>", self._activity_event, add="+")
            self.root.bind_all("<Any-Button>", self._activity_event, add="+")
            self.root.bind("<Control-n>", lambda _e: self.open_new_case())
            self.root.bind("<Control-b>", lambda _e: self.select_tab("Biblioteca"))
            self.root.bind("<Control-k>", lambda _e: self._focus_analysis())
            self.root.bind("<Escape>", lambda _e: self._close_active_dialog())
            self.root.after(1000, self._maximize_after_start)
            self.root.after(1000, self._session_tick)
            self._ui_ready = True
            self._initializing = False
            self.loading_bar.stop()
            self.loading_frame.grid_remove()
            self.select_tab("Inicio")
            self.root.after(100, lambda: show_first_run(self.root))
        except Exception as exc:
            self._initializing = False
            logger.error("Error inicializando la aplicación: %s", exc, exc_info=True)
            try:
                self.loading_bar.stop()
                self.loading_frame.grid_remove()
                error = ctk.CTkLabel(self.root, text="No se pudo iniciar el entorno", font=FONTS["title"], text_color=COLORS["text"])
                error.grid(row=0, column=0, sticky="nsew")
            except Exception:
                pass
            raise

    def _focus_analysis(self):
        self.select_tab("Análisis")
        frame = self.frames.get("Análisis")
        for widget_name in ("search_entry", "query_entry", "input_box"):
            widget = getattr(frame, widget_name, None)
            if widget is not None:
                try:
                    widget.focus_set()
                    return
                except Exception:
                    pass

    def _close_active_dialog(self):
        if self._lock_window is not None:
            try:
                self._lock_window.focus_set()
            except Exception:
                pass

    def _maximize_after_start(self):
        try:
            self.root.state("zoomed")
        except Exception:
            try:
                self.root.attributes("-zoomed", True)
            except Exception:
                pass

    def _activity_event(self, _event=None):
        if not self.session_guard.locked:
            self.session_guard.touch()

    def _session_tick(self):
        try:
            if self.session_verifier and not self.session_guard.check():
                self.show_lock_screen()
        finally:
            self.root.after(1000, self._session_tick)

    def set_session_verifier(self, verifier):
        self.session_verifier = verifier
        self.session_guard.start()

    def show_lock_screen(self):
        if self._lock_window is not None and self._lock_window.winfo_exists():
            self._lock_window.lift()
            return
        if not self.session_verifier:
            self.select_tab("Seguridad")
            return
        self.session_guard.lock()
        win = ctk.CTkToplevel(self.root)
        self._lock_window = win
        win.title("Sesión bloqueada")
        win.geometry("620x380")
        win.minsize(520, 330)
        win.protocol("WM_DELETE_WINDOW", lambda: None)
        win.transient(self.root)
        win.grab_set()
        ctk.CTkLabel(win, text="Sesión bloqueada", font=FONTS["title"], text_color=COLORS["text"]).pack(pady=(55, 8))
        ctk.CTkLabel(win, text="La aplicación se bloqueó para proteger la información local.", font=FONTS["body"], text_color=COLORS["text_muted"], wraplength=470, justify="center").pack(pady=(0, 22))
        entry = ctk.CTkEntry(win, placeholder_text="Frase de desbloqueo", show="•", width=360)
        entry.pack(pady=8)
        status = ctk.CTkLabel(win, text="", font=FONTS["tiny"], text_color=COLORS["text_muted"])
        status.pack(pady=6)

        def unlock(_event=None):
            if self.session_guard.unlock(entry.get(), self.session_verifier):
                win.grab_release()
                win.destroy()
                self._lock_window = None
            else:
                status.configure(text="Frase incorrecta.")
                entry.delete(0, "end")

        ctk.CTkButton(win, text="Desbloquear", command=unlock, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"], width=180).pack(pady=16)
        entry.bind("<Return>", unlock)
        entry.focus_set()

    def _setup_ui(self):
        # El root usa GRID; no mezclar PACK y GRID directamente dentro del mismo padre.
        main = ctk.CTkFrame(self.root, fg_color=COLORS["background"], corner_radius=0)
        main.grid(row=0, column=0, sticky="nsew")
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)
        self.main_frame = main

        sidebar = ctk.CTkFrame(main, width=265, fg_color=COLORS["surface_alt"], corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        brand = ctk.CTkFrame(sidebar, fg_color=COLORS["surface"], corner_radius=18, border_width=1, border_color=COLORS["border"])
        brand.pack(fill="x", padx=12, pady=12)
        try:
            path = Path(__file__).parent.parent.parent / "assets" / "logo_g.png"
            if path.exists():
                im = Image.open(path).convert("RGBA")
                im.thumbnail((52, 52))
                li = ctk.CTkImage(light_image=im, dark_image=im, size=(52, 52))
                lab = ctk.CTkLabel(brand, image=li, text="")
                lab.image = li
                lab.pack(side="left", padx=(10, 8), pady=10)
        except Exception:
            pass
        titlebox = ctk.CTkFrame(brand, fg_color="transparent")
        titlebox.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(titlebox, text="Asistente ONG", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(titlebox, text="Personas · Casos · Triaje", font=FONTS["tiny"], text_color=COLORS["text_muted"]).pack(anchor="w")
        ctk.CTkLabel(titlebox, text="NubiWorks", font=FONTS["small_bold"], text_color=COLORS["primary"]).pack(anchor="w", pady=(4, 0))
        ctk.CTkButton(sidebar, text="＋  Nuevo caso", height=44, corner_radius=11, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"], font=FONTS["body_bold"], command=self.open_new_case).pack(fill="x", padx=12, pady=(2, 12))
        nav = ctk.CTkScrollableFrame(sidebar, fg_color="transparent")
        nav.pack(fill="both", expand=True, padx=6)
        for target in ["Inicio", "Personas", "Casos", "Caso + Informe", "Análisis", "Seguimiento", "Recursos", "Biblioteca", "Agenda", "Seguridad", "Configuración", "Ayuda", "Acerca de"]:
            b = ctk.CTkButton(nav, text=target, height=36, anchor="w", corner_radius=9, fg_color="transparent", hover_color=COLORS["primary_soft"], text_color=COLORS["text"], font=FONTS["body"], command=lambda t=target: self.select_tab(t))
            b.pack(fill="x", padx=4, pady=2)
            self.nav_buttons.append((target, b))
        status = ctk.CTkFrame(sidebar, fg_color=COLORS["success_soft"], corner_radius=13)
        status.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(status, text="●  LOCAL FIRST", font=FONTS["small_bold"], text_color=COLORS["success"]).pack(anchor="w", padx=12, pady=(9, 2))
        ctk.CTkLabel(status, text="Personas, casos y documentos en este equipo", font=FONTS["tiny"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=12, pady=(0, 9))

        workspace = ctk.CTkFrame(main, fg_color=COLORS["background"], corner_radius=0)
        workspace.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=14)
        workspace.grid_rowconfigure(0, weight=1)
        workspace.grid_columnconfigure(0, weight=1)
        specs = [("Inicio", DashboardFrame), ("Personas", PeoplePanel), ("Casos", CasesPanel), ("Caso + Informe", IntegratedCasePanel), ("Análisis", ResultsFrame), ("Seguimiento", FollowUpPanel), ("Recursos", ResourcesPanel), ("Biblioteca", PDFLibraryPanel), ("Agenda", AgendaPanel), ("Seguridad", SecurityCenter), ("Configuración", ConfigPanel), ("Ayuda", HelpPanel), ("Acerca de", AboutPanel)]
        for name, cls in specs:
            params = inspect.signature(cls.__init__).parameters
            kwargs = {"fg_color": COLORS["background"]}
            if "case_manager" in params:
                kwargs["case_manager"] = self.case_manager
            if "person_registry" in params:
                kwargs["person_registry"] = self.person_registry
            if "config_manager" in params:
                kwargs["config_manager"] = self.config_manager
            if "session_guard" in params:
                kwargs["session_guard"] = self.session_guard
            if "on_secret_configured" in params:
                kwargs["on_secret_configured"] = self.set_session_verifier
            if name == "Casos":
                kwargs["on_analyze"] = self._on_case_submit
            try:
                frame = cls(workspace, **kwargs)
            except TypeError as exc:
                logger.warning("Panel %s: %s", name, exc)
                frame = cls(workspace, fg_color=COLORS["background"])
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

    def select_tab(self, target):
        frame = self.frames.get(target)
        if frame:
            frame.tkraise()
        for name, b in self.nav_buttons:
            b.configure(fg_color=COLORS["primary"] if name == target else "transparent", text_color=COLORS["surface"] if name == target else COLORS["text"])

    def open_new_case(self):
        if not self._ui_ready:
            return
        self.select_tab("Casos")
        self.frames["Casos"].show_new_case()

    def _on_case_submit(self, case_text, metadata):
        try:
            if not metadata.get("person_id") and metadata.get("person_name"):
                pid, _ = self.person_registry.upsert({"name": metadata["person_name"], "contact": metadata.get("contact", "")})
                metadata["person_id"] = pid
            analysis = self.config_manager.analyze(case_text)
            try:
                analysis["knowledge_matches"] = build_case_context(case_text)["matches"]
            except Exception:
                analysis["knowledge_matches"] = []
            case = self.case_manager.create_case(text=case_text, urgency=analysis["urgency"], keywords=analysis["keywords"], metadata=metadata, analysis=analysis)
            self.frames["Casos"].close_editor()
            self.frames["Análisis"].show_analysis(case.case_number, case_text, analysis)
            self.frames["Caso + Informe"].refresh_cases()
            self.select_tab("Análisis")
            for name in ("Inicio", "Casos", "Personas"):
                try:
                    self.frames[name].refresh()
                except Exception:
                    pass
        except Exception as exc:
            logger.error("Error procesando caso: %s", exc, exc_info=True)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    MainWindow().run()
