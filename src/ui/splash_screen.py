"""Pantalla de inicio profesional con transición continua a la aplicación."""
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
WHITE="#FFFFFF"; BLUE="#0e98d6"; DARK="#111111"; LIGHT="#E7F5FB"; MUTED="#66717A"
class SplashScreen:
 def __init__(self,on_complete=None):
  self.on_complete=on_complete; self.root=tk.Tk(); self.root.overrideredirect(True); self.root.configure(bg=WHITE); sw,sh=self.root.winfo_screenwidth(),self.root.winfo_screenheight(); self.width,self.height=sw,sh; self.root.geometry(f"{sw}x{sh}+0+0")
  self.canvas=tk.Canvas(self.root,width=sw,height=sh,bg=WHITE,highlightthickness=0);self.canvas.pack(fill="both",expand=True);self._particles=[];self._nodes=[];self._rings=[];self._after_ids=[];self._closing=False;self._tick=0;self._logo_y=int(sh*.39);self._draw_background();self._load_logo();self._draw_content();self._create_progress()
 def _draw_background(self):
  m=18;right=self.width-m;bottom=self.height-m;self.canvas.create_rectangle(m,m,right,bottom,outline=LIGHT,width=2);self.canvas.create_rectangle(m+16,m+16,right-16,bottom-16,outline="#F4FAFD",width=1)
  for y,direction in ((42,1),(bottom-40,-1)):
   self.canvas.create_line(40,y,right-40,y,fill=LIGHT,width=2)
   for x in range(55,right-50,65):self.canvas.create_line(x,y,x+28*direction,y,fill=BLUE,width=1);node=self.canvas.create_oval(x-3,y-3,x+3,y+3,fill=LIGHT,outline="");self._nodes.append(node)
  branches=[(55,42,55,105),(150,42,150,88),(255,42,255,120),(right-255,42,right-255,105),(right-150,42,right-150,88),(right-55,42,right-55,120)]
  for x1,y1,x2,y2 in branches:self.canvas.create_line(x1,y1,x2,y2,fill=BLUE,width=1);self.canvas.create_oval(x2-4,y2-4,x2+4,y2+4,fill=BLUE,outline="")
  for x,sgn in ((55,1),(right-55,-1)):
   for i in range(4):y=170+i*75;end=x+sgn*55;self.canvas.create_line(x,y,end,y,fill=LIGHT,width=2);self.canvas.create_line(end,y,end,y+22,fill=BLUE,width=1)
  for r in (92,108,124):self._rings.append(self.canvas.create_oval(self.width//2-r,self._logo_y-r,self.width//2+r,self._logo_y+r,outline=LIGHT,width=1))
  for i in range(16):p=self.canvas.create_oval(0,0,6,6,fill=BLUE,outline="");self._particles.append({"id":p,"x":55+(i*53)%(right-110),"y":100+(i*29)%(bottom-190),"dx":.65 if i%2 else -.5})
 def _load_logo(self):
  paths=[Path(__file__).parent.parent.parent/"assets"/"logo.png",Path(__file__).parent.parent.parent/"assets"/"logo_g.png",Path("assets/logo.png"),Path("assets/logo_g.png")]
  for path in paths:
   if path.exists():img=Image.open(path).convert("RGBA");img.thumbnail((190,190));self.logo_img=ImageTk.PhotoImage(img);self.logo=self.canvas.create_image(self.width//2,self._logo_y,image=self.logo_img);return
  self.logo=self.canvas.create_text(self.width//2,self._logo_y,text="A",font=("Helvetica",82,"bold"),fill=BLUE)
 def _draw_content(self):
  cx=self.width//2;self.canvas.create_text(cx,int(self.height*.64),text="ASISTENTE ONG",font=("Helvetica",30,"bold"),fill=DARK);self.canvas.create_text(cx,int(self.height*.70),text="Triaje y Canalización",font=("Helvetica",14),fill=MUTED);self.canvas.create_text(cx,int(self.height*.745),text="TECNOLOGÍA LOCAL  ·  PRIVACIDAD  ·  OFFLINE",font=("Helvetica",9,"bold"),fill=BLUE);self.loading_text=self.canvas.create_text(cx,int(self.height*.805),text="Preparando entorno local...",font=("Helvetica",10),fill=MUTED);self.percent_text=self.canvas.create_text(cx,int(self.height*.845),text="0%",font=("Helvetica",9,"bold"),fill=BLUE);self.canvas.create_text(cx,self.height-28,text="NubiWorks · Tecnología con impacto social",font=("Helvetica",8),fill=MUTED)
 def _create_progress(self):
  left=self.width*.20;right=self.width*.80;y=self.height*.87;self._progress_left=left;self._progress_right=right;self._progress_y=y;self.canvas.create_rectangle(left,y,right,y+12,fill=LIGHT,outline="");self.progress_bar=self.canvas.create_rectangle(left,y,left,y+12,fill=BLUE,outline="");self.progress_glow=self.canvas.create_rectangle(left,y,left,y+12,fill="#57BCE7",outline="")
 def update_progress(self,value,text=None):
  if self._closing:return
  width=(self._progress_right-self._progress_left)*max(0,min(100,value))/100;self.canvas.coords(self.progress_bar,self._progress_left,self._progress_y,self._progress_left+width,self._progress_y+12);self.canvas.coords(self.progress_glow,max(self._progress_left,self._progress_left+width-14),self._progress_y,self._progress_left+width,self._progress_y+12);self.canvas.itemconfig(self.loading_text,text=text or f"Cargando... {value}%");self.canvas.itemconfig(self.percent_text,text=f"{value}%");self.root.update_idletasks()
 def _schedule(self,delay,callback):
  if not self._closing:self._after_ids.append(self.root.after(delay,callback))
 def _animate(self):
  if self._closing:return
  self._tick+=1;offset=3 if (self._tick//20)%2==0 else -3;self.canvas.coords(self.logo,self.width//2,self._logo_y+offset)
  for i,node in enumerate(self._nodes):self.canvas.itemconfig(node,fill=BLUE if (self._tick+i*4)%50<12 else LIGHT)
  for i,r in enumerate(self._rings):self.canvas.itemconfig(r,outline=BLUE if (self._tick+i*11)%70<12 else LIGHT)
  for p in self._particles:
   p["x"]+=p["dx"]
   if p["x"]>self.width-55:p["x"]=55
   if p["x"]<55:p["x"]=self.width-55
   self.canvas.coords(p["id"],p["x"]-3,p["y"]-3,p["x"]+3,p["y"]+3)
  self._schedule(45,self._animate)
 def start_loading(self):
  steps=[(10,"Iniciando Asistente ONG..."),(25,"Preparando entorno local..."),(40,"Inicializando datos locales..."),(55,"Cargando reglas y recursos..."),(70,"Preparando informes y seguimiento..."),(85,"Verificando interfaz..."),(100,"Sistema listo")]
  def step(i=0):
   if self._closing:return
   if i>=len(steps):self._schedule(100,self._finish);return
   p,t=steps[i];self.update_progress(p,t);self._schedule(130 if p<100 else 100,lambda i=i:step(i+1))
  self._animate();step()
 def _finish(self):
  if self._closing:return
  try:
   app=self.on_complete() if self.on_complete else None
   if app is not None and hasattr(app,"root"):
    app.root.deiconify();app.root.update_idletasks();app.root.lift();app.root.focus_force();self._closing=True
    for aid in self._after_ids:
     try:self.root.after_cancel(aid)
     except tk.TclError:pass
    self._after_ids.clear();self.root.destroy();app.run();return
  except Exception:self._closing=True;self.root.destroy();raise
  self._closing=True;self.root.destroy()
 def run(self):self.start_loading();self.root.mainloop()
def show_splash(on_complete=None):SplashScreen(on_complete).run()
