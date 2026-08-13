"""Pantalla de inicio futurista, continua y adaptativa al tema."""
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

THEME_FILE = Path.home() / ".asistente_ong_theme"

def _theme():
    try:
        value = THEME_FILE.read_text(encoding="utf-8").strip().lower()
        return value if value in {"light", "dark"} else "light"
    except Exception:
        return "light"

class SplashScreen:
    def __init__(self, on_complete=None):
        self.on_complete = on_complete
        self.theme = _theme()
        self.dark = self.theme == "dark"
        self.bg = "#080D12" if self.dark else "#F7FBFD"
        self.text = "#F4F8FA" if self.dark else "#111820"
        self.muted = "#91A5AF" if self.dark else "#667780"
        self.line = "#1C3948" if self.dark else "#D9EAF1"
        self.line_soft = "#122631" if self.dark else "#EDF5F8"
        self.blue = "#36B7ED" if self.dark else "#0E98D6"
        self.blue_soft = "#173B4C" if self.dark else "#E5F5FB"
        self.root = tk.Tk(); self.root.overrideredirect(True); self.root.configure(bg=self.bg)
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.width, self.height = sw, sh; self.root.geometry(f"{sw}x{sh}+0+0")
        self.canvas = tk.Canvas(self.root, width=sw, height=sh, bg=self.bg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self._nodes, self._particles, self._rings, self._after_ids = [], [], [], []
        self._closing = False; self._tick = 0; self._logo_y = int(sh * .36)
        self._draw_background(); self._load_logo(); self._draw_content(); self._create_progress()

    def _draw_background(self):
        w, h = self.width, self.height
        self.canvas.create_rectangle(24, 24, w-24, h-24, outline=self.line, width=1)
        self.canvas.create_rectangle(40, 40, w-40, h-40, outline=self.line_soft, width=1)
        for y in (52, h-52):
            self.canvas.create_line(55, y, w-55, y, fill=self.line, width=1)
            for x in range(75, w-70, 78):
                self.canvas.create_line(x, y, x+30, y, fill=self.line, width=1)
                self._nodes.append(self.canvas.create_oval(x+26,y-3,x+32,y+3,fill=self.blue_soft,outline=""))
        for side in (55, w-55):
            sign = 1 if side == 55 else -1
            for i in range(5):
                y = 135 + i*88; x2 = side + sign*(58+(i%2)*24)
                self.canvas.create_line(side,y,x2,y,fill=self.line,width=1)
                self.canvas.create_line(x2,y,x2,y+26,fill=self.blue,width=1)
                self._nodes.append(self.canvas.create_oval(x2-4,y+22,x2+4,y+30,fill=self.blue,outline=""))
        for r in (92,112,134):
            self._rings.append(self.canvas.create_oval(w//2-r,self._logo_y-r,w//2+r,self._logo_y+r,outline=self.line,width=1))
        for i in range(22):
            x=75+(i*71)%max(1,w-150); y=85+(i*47)%max(1,h-240)
            item=self.canvas.create_oval(x-2,y-2,x+2,y+2,fill=self.blue,outline="")
            self._particles.append({"id":item,"x":x,"y":y,"dx":.45 if i%2 else -.35})

    def _load_logo(self):
        paths=[Path(__file__).parent.parent.parent/"assets"/"logo.png",Path(__file__).parent.parent.parent/"assets"/"logo_g.png",Path("assets/logo.png"),Path("assets/logo_g.png")]
        for path in paths:
            if path.exists():
                img=Image.open(path).convert("RGBA"); img.thumbnail((190,190),Image.Resampling.LANCZOS)
                self.logo_img=ImageTk.PhotoImage(img); self.logo=self.canvas.create_image(self.width//2,self._logo_y,image=self.logo_img); return
        self.logo=self.canvas.create_text(self.width//2,self._logo_y,text="A",font=("Helvetica",82,"bold"),fill=self.blue)

    def _draw_content(self):
        cx,h=self.width//2,self.height
        self.canvas.create_rectangle(cx-390,int(h*.55),cx+390,int(h*.90),fill=self.bg,outline="")
        self.canvas.create_text(cx,int(h*.595),text="ASISTENTE ONG",font=("Helvetica",30,"bold"),fill=self.text)
        self.canvas.create_text(cx,int(h*.655),text="Triaje · Canalización · Seguimiento",font=("Helvetica",14),fill=self.muted)
        self.canvas.create_text(cx,int(h*.705),text="LOCAL FIRST   ·   PRIVACIDAD   ·   OFFLINE",font=("Helvetica",9,"bold"),fill=self.blue)
        self.loading_text=self.canvas.create_text(cx,int(h*.775),text="Preparando entorno local…",font=("Helvetica",10),fill=self.muted)
        self.percent_text=self.canvas.create_text(cx,int(h*.815),text="0%",font=("Helvetica",9,"bold"),fill=self.blue)
        self.canvas.create_text(cx,h-30,text="NubiWorks · Tecnología con impacto social",font=("Helvetica",8),fill=self.muted)

    def _create_progress(self):
        left,right,y=self.width*.23,self.width*.77,self.height*.845
        self._progress_left,self._progress_right,self._progress_y=left,right,y
        self.canvas.create_rectangle(left,y,right,y+10,fill=self.blue_soft,outline="")
        self.progress_bar=self.canvas.create_rectangle(left,y,left,y+10,fill=self.blue,outline="")
        self.progress_glow=self.canvas.create_rectangle(left,y,left,y+10,fill=self.blue,outline="")

    def update_progress(self,value,text=None):
        if self._closing:return
        width=(self._progress_right-self._progress_left)*max(0,min(100,value))/100; end=self._progress_left+width
        self.canvas.coords(self.progress_bar,self._progress_left,self._progress_y,end,self._progress_y+10)
        self.canvas.coords(self.progress_glow,max(self._progress_left,end-18),self._progress_y,end,self._progress_y+10)
        self.canvas.itemconfig(self.loading_text,text=text or f"Cargando… {value}%"); self.canvas.itemconfig(self.percent_text,text=f"{value}%"); self.root.update_idletasks()

    def _schedule(self,delay,callback):
        if not self._closing:self._after_ids.append(self.root.after(delay,callback))

    def _animate(self):
        if self._closing:return
        self._tick+=1; offset=2.5 if (self._tick//18)%2==0 else -2.5
        self.canvas.coords(self.logo,self.width//2,self._logo_y+offset)
        for i,ring in enumerate(self._rings):
            self.canvas.itemconfig(ring,outline=self.blue if (self._tick+i*15)%90<18 else self.line)
        for i,node in enumerate(self._nodes):
            self.canvas.itemconfig(node,fill=self.blue if (self._tick+i*5)%70<10 else self.blue_soft)
        for p in self._particles:
            p["x"]+=p["dx"]
            if p["x"]>self.width-75:p["x"]=75
            elif p["x"]<75:p["x"]=self.width-75
            self.canvas.coords(p["id"],p["x"]-2,p["y"]-2,p["x"]+2,p["y"]+2)
        self._schedule(40,self._animate)

    def start_loading(self):
        steps=[(8,"Iniciando núcleo local…"),(22,"Preparando entorno…"),(38,"Inicializando datos locales…"),(54,"Cargando reglas y recursos…"),(70,"Preparando informes y seguimiento…"),(86,"Verificando interfaz…"),(100,"Sistema listo")]
        def step(i=0):
            if self._closing:return
            if i>=len(steps):self._schedule(120,self._finish);return
            p,text=steps[i];self.update_progress(p,text);self._schedule(125 if p<100 else 90,lambda i=i:step(i+1))
        self._animate();step()

    def _finish(self):
        if self._closing:return
        try:
            app=self.on_complete() if self.on_complete else None
            if app is not None and hasattr(app,"root"):
                app.root.deiconify(); app.root.update_idletasks(); app.root.lift(); app.root.focus_force(); self._closing=True
                for aid in self._after_ids:
                    try:self.root.after_cancel(aid)
                    except tk.TclError:pass
                self._after_ids.clear(); self.root.destroy(); app.run(); return
        except Exception:
            self._closing=True; self.root.destroy(); raise
        self._closing=True; self.root.destroy()

    def run(self):self.start_loading();self.root.mainloop()

def show_splash(on_complete=None):SplashScreen(on_complete).run()
