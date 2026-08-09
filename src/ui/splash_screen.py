"""Splash de Asistente ONG: animación de circuitos, identidad NubiWorks y carga progresiva."""
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
WHITE="#FFFFFF"; BLUE="#0e98d6"; DARK="#111111"; LIGHT="#E7F5FB"; MUTED="#66717A"

class SplashScreen:
    def __init__(self,on_complete=None):
        self.on_complete=on_complete; self.root=tk.Tk(); self.root.overrideredirect(True); self.root.configure(bg=WHITE)
        self.width,self.height=1000,650; sw,sh=self.root.winfo_screenwidth(),self.root.winfo_screenheight(); self.root.geometry(f"{self.width}x{self.height}+{(sw-self.width)//2}+{(sh-self.height)//2}")
        self.canvas=tk.Canvas(self.root,width=self.width,height=self.height,bg=WHITE,highlightthickness=0); self.canvas.pack()
        self._particles=[]; self._nodes=[]; self._rings=[]; self._after_ids=[]; self._closing=False; self._tick=0; self._logo_y=250
        self._draw_background(); self._load_logo(); self._draw_content(); self._create_progress()
    def _draw_background(self):
        self.canvas.create_rectangle(18,18,982,632,outline=LIGHT,width=2)
        self.canvas.create_rectangle(34,34,966,616,outline="#F4FAFD",width=1)
        # Circuitos superiores e inferiores.
        for y,direction in ((58,1),(592,-1)):
            self.canvas.create_line(55,y,945,y,fill=LIGHT,width=2)
            for x in range(70,930,72):
                self.canvas.create_line(x,y,x+34*direction,y,fill=BLUE,width=1)
                node=self.canvas.create_oval(x-3,y-3,x+3,y+3,fill=LIGHT,outline=""); self._nodes.append(node)
        branches=[(75,58,75,130),(160,58,160,105),(270,58,270,145),(730,58,730,125),(840,58,840,105),(925,58,925,150),(75,592,75,520),(170,592,170,545),(280,592,280,500),(720,592,720,525),(835,592,835,550),(925,592,925,505)]
        for x1,y1,x2,y2 in branches:
            self.canvas.create_line(x1,y1,x2,y2,fill=BLUE,width=1); self.canvas.create_oval(x2-4,y2-4,x2+4,y2+4,fill=BLUE,outline="")
        # Circuitos laterales.
        for x,sgn in ((55,1),(945,-1)):
            for i in range(5):
                y=170+i*70; end=x+sgn*70; self.canvas.create_line(x,y,end,y,fill=LIGHT,width=2); self.canvas.create_line(end,y,end,y+24,fill=BLUE,width=1); self.canvas.create_oval(end-4,y+20,end+4,y+28,fill=LIGHT,outline="")
        # Órbitas alrededor del logo.
        for r in (112,128,144): self._rings.append(self.canvas.create_oval(500-r,self._logo_y-r,500+r,self._logo_y+r,outline=LIGHT,width=1))
        for i in range(22):
            p=self.canvas.create_oval(0,0,6,6,fill=BLUE,outline=""); self._particles.append({"id":p,"x":55+(i*41)%890,"y":90+(i*23)%470,"dx":0.8 if i%2 else -0.6})
    def _load_logo(self):
        paths=[Path(__file__).parent.parent.parent/"assets"/"logo.png",Path(__file__).parent.parent.parent/"assets"/"logo_g.png",Path("assets/logo.png"),Path("assets/logo_g.png")]
        for path in paths:
            if path.exists():
                img=Image.open(path).convert("RGBA"); img.thumbnail((230,230)); self.logo_img=ImageTk.PhotoImage(img); self.logo=self.canvas.create_image(500,self._logo_y,image=self.logo_img); return
        self.logo=self.canvas.create_text(500,self._logo_y,text="C",font=("Helvetica",90,"bold"),fill=BLUE)
    def _draw_content(self):
        self.canvas.create_text(500,390,text="ASISTENTE ONG",font=("Helvetica",34,"bold"),fill=DARK)
        self.canvas.create_text(500,425,text="Triaje y Canalización",font=("Helvetica",14),fill=MUTED)
        self.canvas.create_text(500,450,text="TECNOLOGÍA LOCAL  ·  PRIVACIDAD  ·  APOYO PROFESIONAL",font=("Helvetica",9,"bold"),fill=BLUE)
        self.loading_text=self.canvas.create_text(500,492,text="Preparando entorno local...",font=("Helvetica",10),fill=MUTED)
        self.percent_text=self.canvas.create_text(500,516,text="0%",font=("Helvetica",9,"bold"),fill=BLUE)
        self.canvas.create_text(500,608,text="NubiWorks",font=("Helvetica",11,"bold"),fill=BLUE)
        self.canvas.create_text(500,626,text="Tecnología con impacto social",font=("Helvetica",8),fill=MUTED)
    def _create_progress(self):
        self.canvas.create_rectangle(190,532,810,548,fill=LIGHT,outline="")
        self.progress_bar=self.canvas.create_rectangle(190,532,190,548,fill=BLUE,outline="")
        self.progress_glow=self.canvas.create_rectangle(190,532,190,548,fill="#57BCE7",outline="")
    def update_progress(self,value,text=None):
        if self._closing:return
        width=620*max(0,min(100,value))/100; self.canvas.coords(self.progress_bar,190,532,190+width,548); glow=min(width,620); self.canvas.coords(self.progress_glow,max(190,190+width-16),532,190+glow,548); self.canvas.itemconfig(self.loading_text,text=text or f"Cargando... {value}%"); self.canvas.itemconfig(self.percent_text,text=f"{value}%"); self.root.update_idletasks()
    def _schedule(self,delay,callback):
        if not self._closing:self._after_ids.append(self.root.after(delay,callback))
    def _animate(self):
        if self._closing:return
        self._tick+=1; offset=4 if (self._tick//20)%2==0 else -4; self.canvas.coords(self.logo,500,self._logo_y+offset)
        for i,node in enumerate(self._nodes): self.canvas.itemconfig(node,fill=BLUE if (self._tick+i*4)%50<12 else LIGHT)
        for i,r in enumerate(self._rings): self.canvas.itemconfig(r,outline=BLUE if (self._tick+i*11)%70<12 else LIGHT)
        for p in self._particles:
            p["x"]+=p["dx"]
            if p["x"]>940:p["x"]=60
            if p["x"]<60:p["x"]=940
            self.canvas.coords(p["id"],p["x"]-3,p["y"]-3,p["x"]+3,p["y"]+3)
        self._schedule(40,self._animate)
    def start_loading(self):
        steps=[(3,"Iniciando Asistente ONG..."),(8,"Preparando entorno local..."),(14,"Comprobando configuración institucional..."),(21,"Verificando almacenamiento local..."),(29,"Inicializando base de datos..."),(37,"Comprobando protección de datos..."),(45,"Cargando clasificador contextual..."),(53,"Cargando reglas y categorías de triaje..."),(61,"Preparando memoria local..."),(69,"Indexando recursos de asistencia..."),(77,"Preparando informes sociales..."),(85,"Cargando dashboard y filtros..."),(92,"Verificando componentes de interfaz..."),(97,"Comprobando fuentes oficiales configuradas..."),(100,"Sistema listo")]
        def step(i=0):
            if self._closing:return
            if i>=len(steps): self._schedule(1500,self._finish); return
            p,t=steps[i]; self.update_progress(p,t); self._schedule(720 if p<100 else 1100,lambda i=i:step(i+1))
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
