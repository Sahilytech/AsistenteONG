"""Splash screen: blanco predominante, azul #0e98d6 y circuitos."""
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

WHITE="#FFFFFF"; BLUE="#0e98d6"; BLACK="#000000"; LIGHT="#EAF6FC"; GRAY="#666666"

class SplashScreen:
    def __init__(self,on_complete=None):
        self.on_complete=on_complete; self.root=tk.Tk(); self.root.overrideredirect(True); self.root.configure(bg=WHITE)
        self.width=700; self.height=450; sw=self.root.winfo_screenwidth(); sh=self.root.winfo_screenheight(); self.root.geometry(f"{self.width}x{self.height}+{(sw-self.width)//2}+{(sh-self.height)//2}")
        self.canvas=tk.Canvas(self.root,width=self.width,height=self.height,bg=WHITE,highlightthickness=0); self.canvas.pack()
        self._draw_circuits(); self._load_logo(); self._draw_text(); self._create_progress_bar(); self.current_progress=0; self.loading_complete=False
    def _draw_circuits(self):
        for y in (30,80,370,420):
            self.canvas.create_line(40,y,660,y,fill=BLUE,width=1)
            for x in range(40,661,80): self.canvas.create_oval(x-3,y-3,x+3,y+3,fill=BLUE,outline="")
        for x in (30,670): self.canvas.create_line(x,40,x,410,fill=BLUE,width=1)
        for x,y in ((30,30),(670,30),(30,420),(670,420)): self.canvas.create_oval(x-5,y-5,x+5,y+5,fill=BLUE,outline="")
    def _load_logo(self):
        paths=[Path(__file__).parent.parent.parent/"assets"/"logo.png",Path(__file__).parent.parent.parent/"assets"/"logo_g.png",Path("assets/logo.png"),Path("assets/logo_g.png")]
        for p in paths:
            if p.exists():
                img=Image.open(p).convert("RGBA"); img.thumbnail((140,140)); self.logo_img=ImageTk.PhotoImage(img); self.canvas.create_image(350,165,image=self.logo_img); return
        self.canvas.create_text(350,165,text="ASISTENTE ONG",font=("Helvetica",26,"bold"),fill=BLUE)
    def _draw_text(self):
        self.canvas.create_text(350,275,text="ASISTENTE ONG",font=("Helvetica",28,"bold"),fill=BLACK)
        self.canvas.create_text(350,310,text="Triaje y Canalización Profesional",font=("Helvetica",12),fill=GRAY)
        self.canvas.create_text(350,335,text="Offline 100%",font=("Helvetica",10),fill=GRAY)
        self.loading_text=self.canvas.create_text(350,395,text="Inicializando...",font=("Helvetica",10),fill=GRAY)
    def _create_progress_bar(self):
        self.canvas.create_rectangle(180,360,520,370,fill=LIGHT,outline=""); self.progress_bar=self.canvas.create_rectangle(180,360,180,370,fill=BLUE,outline="")
    def update_progress(self,value,text=None):
        self.current_progress=value; width=340*max(0,min(100,value))/100; self.canvas.coords(self.progress_bar,180,360,180+width,370); self.canvas.itemconfig(self.loading_text,text or f"Cargando... {value}%"); self.root.update_idletasks()
    def start_loading(self):
        steps=[(10,"Inicializando..."),(30,"Cargando base local..."),(50,"Preparando interfaz..."),(70,"Cargando módulos..."),(90,"Verificando componentes..."),(100,"Listo")]
        def step(i=0):
            if i>=len(steps): self.root.after(350,self._finish); return
            p,t=steps[i]; self.update_progress(p,t); self.root.after(180,lambda:self._step_next(i))
        self._step_next=lambda i: step(i+1); step()
    def _finish(self): self.root.destroy(); self.on_complete() if self.on_complete else None
    def run(self): self.start_loading(); self.root.mainloop()

def show_splash(on_complete=None): SplashScreen(on_complete).run()
