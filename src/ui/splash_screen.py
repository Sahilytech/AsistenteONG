"""Splash animado de Asistente ONG con identidad NubiWorks."""
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

WHITE="#FFFFFF"; BLUE="#0e98d6"; BLACK="#000000"; LIGHT="#EAF6FC"; GRAY="#66717A"

class SplashScreen:
    def __init__(self,on_complete=None):
        self.on_complete=on_complete; self.root=tk.Tk(); self.root.overrideredirect(True); self.root.configure(bg=WHITE)
        self.width,self.height=900,600; sw,sh=self.root.winfo_screenwidth(),self.root.winfo_screenheight(); self.root.geometry(f"{self.width}x{self.height}+{(sw-self.width)//2}+{(sh-self.height)//2}")
        self.canvas=tk.Canvas(self.root,width=self.width,height=self.height,bg=WHITE,highlightthickness=0); self.canvas.pack()
        self._particles=[]; self._pulse_nodes=[]; self._rings=[]; self._logo_y=190; self._animation_tick=0; self._after_ids=[]; self._closing=False
        self._draw_background(); self._load_logo(); self._draw_text(); self._create_progress_bar()
    def _draw_background(self):
        self.canvas.create_rectangle(18,18,882,582,outline=LIGHT,width=2)
        for y in (42,92,508,558):
            self.canvas.create_line(35,y,865,y,fill=LIGHT,width=2)
            for x in range(50,866,70):
                self.canvas.create_line(x,y,x+28,y,fill=BLUE,width=1); self._pulse_nodes.append(self.canvas.create_oval(x-3,y-3,x+3,y+3,fill=BLUE,outline=""))
        branches=[(90,92,90,155),(165,42,165,120),(255,42,255,82),(645,42,645,120),(735,92,735,155),(810,42,810,105),(90,508,90,445),(180,558,180,480),(720,508,720,445),(810,558,810,480),(320,42,320,95),(580,558,580,495)]
        for x1,y1,x2,y2 in branches:self.canvas.create_line(x1,y1,x2,y2,fill=BLUE,width=1); self.canvas.create_oval(x2-4,y2-4,x2+4,y2+4,fill=BLUE,outline="")
        for side in (1,-1):
            base=50 if side==1 else 850
            for i in range(4):
                y=170+i*65; end=base+(75 if side==1 else -75); self.canvas.create_line(base,y,end,y,fill=LIGHT,width=2); self.canvas.create_line(end,y,end,y+28,fill=BLUE,width=1); self.canvas.create_oval(end-4,y+24,end+4,y+32,fill=BLUE,outline="")
        for i in range(16):
            dot=self.canvas.create_oval(0,0,7,7,fill=BLUE,outline=""); self._particles.append({"id":dot,"x":45+i*52,"y":42 if i%2==0 else 558,"direction":1 if i%2==0 else -1})
        for r in (92,104,116): self._rings.append(self.canvas.create_oval(450-r,self._logo_y-r,450+r,self._logo_y+r,outline=LIGHT,width=1))
    def _load_logo(self):
        paths=[Path(__file__).parent.parent.parent/"assets"/"logo.png",Path(__file__).parent.parent.parent/"assets"/"logo_g.png",Path("assets/logo.png"),Path("assets/logo_g.png")]
        for path in paths:
            if path.exists():
                img=Image.open(path).convert("RGBA"); img.thumbnail((260,260)); self.logo_img=ImageTk.PhotoImage(img); self.logo=self.canvas.create_image(450,self._logo_y,image=self.logo_img); return
        self.logo=self.canvas.create_text(450,self._logo_y,text="ASISTENTE ONG",font=("Helvetica",34,"bold"),fill=BLUE)
    def _draw_text(self):
        self.canvas.create_text(450,318,text="ASISTENTE ONG",font=("Helvetica",32,"bold"),fill=BLACK); self.canvas.create_text(450,350,text="Triaje y Canalización Profesional",font=("Helvetica",13),fill=GRAY); self.canvas.create_text(450,374,text="OFFLINE 100%   •   PRIVACIDAD LOCAL   •   DATOS LOCALES",font=("Helvetica",9,"bold"),fill=BLUE); self.loading_text=self.canvas.create_text(450,420,text="Inicializando entorno...",font=("Helvetica",10),fill=GRAY); self.percent_text=self.canvas.create_text(450,444,text="0%",font=("Helvetica",9,"bold"),fill=BLUE); self.canvas.create_text(450,575,text="NubiWorks",font=("Helvetica",10,"bold"),fill=GRAY); self.canvas.create_text(450,558,text="Tecnología con impacto social",font=("Helvetica",8),fill=GRAY)
    def _create_progress_bar(self): self.canvas.create_rectangle(170,458,730,474,fill=LIGHT,outline=""); self.progress_bar=self.canvas.create_rectangle(170,458,170,474,fill=BLUE,outline="")
    def update_progress(self,value,text=None):
        if self._closing:return
        self.current_progress=value; width=560*max(0,min(100,value))/100; self.canvas.coords(self.progress_bar,170,458,170+width,474); self.canvas.itemconfig(self.loading_text,text=text or f"Cargando... {value}%"); self.canvas.itemconfig(self.percent_text,text=f"{value}%"); self.root.update_idletasks()
    def _schedule(self,delay,callback):
        if not self._closing:self._after_ids.append(self.root.after(delay,callback))
    def _animate(self):
        if self._closing:return
        self._animation_tick+=1; phase=self._animation_tick%90; offset=3 if phase<45 else -3; self.canvas.coords(self.logo,450,self._logo_y+offset)
        for index,node in enumerate(self._pulse_nodes): self.canvas.itemconfig(node,fill=BLUE if (self._animation_tick+index*3)%42<11 else LIGHT)
        for i,r in enumerate(self._rings): self.canvas.itemconfig(r,outline=BLUE if (self._animation_tick+i*9)%54<10 else LIGHT)
        for p in self._particles:
            p["x"]+=1.6*p["direction"]
            if p["x"]>855:p["x"]=45
            elif p["x"]<45:p["x"]=855
            self.canvas.coords(p["id"],p["x"]-3,p["y"]-3,p["x"]+3,p["y"]+3)
        self._schedule(40,self._animate)
    def start_loading(self):
        steps=[(4,"Inicializando entorno local..."),(10,"Comprobando configuración..."),(18,"Verificando privacidad y almacenamiento..."),(27,"Inicializando base de datos..."),(36,"Cargando clasificador contextual..."),(45,"Cargando reglas de triaje..."),(54,"Cargando categorías y filtros..."),(63,"Indexando recursos de asistencia..."),(72,"Preparando generador de informes..."),(81,"Verificando componentes de interfaz..."),(90,"Preparando dashboard y estadísticas..."),(97,"Finalizando configuración..."),(100,"Sistema listo")]
        def step(i=0):
            if self._closing:return
            if i>=len(steps): self._schedule(1400,self._finish); return
            p,t=steps[i]; self.update_progress(p,t); self._schedule(950 if p<100 else 1200,lambda i=i:step(i+1))
        self._animate(); step()
    def _finish(self):
        if self._closing:return
        self._closing=True
        for aid in self._after_ids:
            try:self.root.after_cancel(aid)
            except tk.TclError:pass
        self._after_ids.clear(); self.root.destroy()
        if self.on_complete:self.on_complete()
    def run(self): self.start_loading(); self.root.mainloop()

def show_splash(on_complete=None): SplashScreen(on_complete).run()
