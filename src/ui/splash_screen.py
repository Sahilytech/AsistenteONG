"""Splash animado de Asistente ONG con identidad visual NubiWorks."""
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

WHITE="#FFFFFF"; BLUE="#0e98d6"; BLACK="#000000"; LIGHT="#EAF6FC"; GRAY="#66717A"

class SplashScreen:
    def __init__(self,on_complete=None):
        self.on_complete=on_complete; self.root=tk.Tk(); self.root.overrideredirect(True); self.root.configure(bg=WHITE)
        self.width,self.height=800,520; sw,sh=self.root.winfo_screenwidth(),self.root.winfo_screenheight(); self.root.geometry(f"{self.width}x{self.height}+{(sw-self.width)//2}+{(sh-self.height)//2}")
        self.canvas=tk.Canvas(self.root,width=self.width,height=self.height,bg=WHITE,highlightthickness=0); self.canvas.pack()
        self._particles=[]; self._pulse_nodes=[]; self._logo_y=175; self._animation_tick=0
        self._draw_background(); self._load_logo(); self._draw_text(); self._create_progress_bar(); self.current_progress=0
    def _draw_background(self):
        for y in (32,78,442,488):
            self.canvas.create_line(22,y,778,y,fill=LIGHT,width=2)
            for x in range(40,779,62):
                self.canvas.create_line(x,y,x+20,y,fill=BLUE,width=1)
                self._pulse_nodes.append(self.canvas.create_oval(x-3,y-3,x+3,y+3,fill=BLUE,outline=""))
        for x in (22,778): self.canvas.create_line(x,32,x,488,fill=LIGHT,width=2)
        branches=[(82,78,82,138),(156,32,156,105),(250,32,250,82),(550,78,550,138),(644,32,644,105),(718,78,718,138),(110,442,110,382),(210,488,210,418),(590,442,590,382),(690,488,690,418)]
        for x1,y1,x2,y2 in branches:
            self.canvas.create_line(x1,y1,x2,y2,fill=BLUE,width=1); self.canvas.create_oval(x2-4,y2-4,x2+4,y2+4,fill=BLUE,outline="")
        for i in range(12):
            dot=self.canvas.create_oval(0,0,6,6,fill=BLUE,outline=""); self._particles.append({"id":dot,"x":40+i*62,"y":32 if i%2==0 else 488,"direction":1 if i%2==0 else -1})
    def _load_logo(self):
        paths=[Path(__file__).parent.parent.parent/"assets"/"logo.png",Path(__file__).parent.parent.parent/"assets"/"logo_g.png",Path("assets/logo.png"),Path("assets/logo_g.png")]
        for path in paths:
            if path.exists():
                img=Image.open(path).convert("RGBA"); img.thumbnail((230,230)); self.logo_img=ImageTk.PhotoImage(img); self.logo=self.canvas.create_image(400,self._logo_y,image=self.logo_img); return
        self.logo=self.canvas.create_text(400,self._logo_y,text="ASISTENTE ONG",font=("Helvetica",32,"bold"),fill=BLUE)
    def _draw_text(self):
        self.canvas.create_text(400,295,text="ASISTENTE ONG",font=("Helvetica",31,"bold"),fill=BLACK)
        self.canvas.create_text(400,330,text="Triaje y Canalización Profesional",font=("Helvetica",12),fill=GRAY)
        self.canvas.create_text(400,353,text="Offline 100%  •  Privacidad local",font=("Helvetica",10),fill=GRAY)
        self.loading_text=self.canvas.create_text(400,405,text="Inicializando...",font=("Helvetica",10),fill=GRAY)
        self.canvas.create_text(400,505,text="NubiWorks",font=("Helvetica",9),fill=GRAY)
    def _create_progress_bar(self):
        self.canvas.create_rectangle(170,370,630,382,fill=LIGHT,outline="")
        self.progress_bar=self.canvas.create_rectangle(170,370,170,382,fill=BLUE,outline="")
    def update_progress(self,value,text=None):
        self.current_progress=value; width=460*max(0,min(100,value))/100; self.canvas.coords(self.progress_bar,170,370,170+width,382); self.canvas.itemconfig(self.loading_text,text=text or f"Cargando... {value}%"); self.root.update_idletasks()
    def _animate(self):
        self._animation_tick+=1; phase=self._animation_tick%80; offset=3 if phase<40 else -3; self.canvas.coords(self.logo,400,self._logo_y+offset)
        for index,node in enumerate(self._pulse_nodes): self.canvas.itemconfig(node,fill=BLUE if (self._animation_tick+index*3)%36<10 else LIGHT)
        for p in self._particles:
            p["x"]+=1.8*p["direction"]
            if p["x"]>765:p["x"]=35
            elif p["x"]<35:p["x"]=765
            self.canvas.coords(p["id"],p["x"]-3,p["y"]-3,p["x"]+3,p["y"]+3)
        self.root.after(45,self._animate)
    def start_loading(self):
        # Carga deliberadamente más larga y suave: ~7.5 segundos.
        steps=[(5,"Inicializando entorno..."),(15,"Verificando privacidad local..."),(28,"Preparando base de datos..."),(42,"Cargando módulos..."),(57,"Preparando sistema de triaje..."),(72,"Preparando informes sociales..."),(86,"Verificando recursos..."),(96,"Preparando interfaz..."),(100,"Listo")]
        def step(i=0):
            if i>=len(steps): self.root.after(650,self._finish); return
            p,t=steps[i]; self.update_progress(p,t); self.root.after(720 if p<100 else 900,lambda:step(i+1))
        self._animate(); step()
    def _finish(self): self.root.destroy(); self.on_complete() if self.on_complete else None
    def run(self): self.start_loading(); self.root.mainloop()

def show_splash(on_complete=None): SplashScreen(on_complete).run()
