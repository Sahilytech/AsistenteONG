"""Splash visual para un arranque breve y consistente."""
import customtkinter as ctk
import time


def run_startup(load_callback):
    splash = ctk.CTk()
    splash.overrideredirect(True)
    splash.configure(fg_color="#ffffff")
    width, height = 560, 300
    sw, sh = splash.winfo_screenwidth(), splash.winfo_screenheight()
    splash.geometry(f"{width}x{height}+{(sw-width)//2}+{(sh-height)//2}")

    card = ctk.CTkFrame(splash, fg_color="#ffffff", corner_radius=24, border_width=1, border_color="#e6e6e6")
    card.pack(fill="both", expand=True, padx=10, pady=10)
    ctk.CTkLabel(card, text="Asistente ONG", font=("Montserrat", 30, "bold"), text_color="#111111").pack(pady=(48, 4))
    ctk.CTkLabel(card, text="Triaje · Casos · Informes · Recursos", font=("Montserrat", 14), text_color="#666666").pack()
    status = ctk.CTkLabel(card, text="Preparando…", font=("Montserrat", 12), text_color="#0e98d6")
    status.pack(pady=(35, 8))
    bar = ctk.CTkProgressBar(card, width=360, height=8, mode="determinate", progress_color="#0e98d6")
    bar.set(0)
    bar.pack()
    splash.update()

    for value, text in ((.25, "Preparando…"), (.50, "Cargando herramientas…"), (.75, "Preparando espacio local…"), (.90, "Abriendo…")):
        bar.set(value)
        status.configure(text=text)
        splash.update()
        time.sleep(.09)

    app = load_callback()
    bar.set(1)
    status.configure(text="Listo")
    splash.update()
    time.sleep(.12)
    splash.destroy()
    app.root.after(50, lambda: app.root.state("zoomed"))
    app.run()
