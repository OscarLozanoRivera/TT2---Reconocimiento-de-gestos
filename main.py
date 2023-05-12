from tkinter import *
from tkinter import filedialog
from datetime import date
from tkinter.ttk import Button, Label, Style , Combobox , Treeview
import tkinter as tk
from tkinter import Label as Label2
from tkinter import Button as Button2
from PIL import ImageTk, Image
from os import listdir

colorFondo = "#60656F"
colorFuente = "#F7F7FF"
tercerColor = "#279AF1"
cuartoColor = "#C49991"
nombreEscenario = ""
rutaEscenario = ""

class RoundedButton(tk.Canvas):

    def __init__(self, master=None, text:str="", radius=30, btnforeground=colorFuente, btnbackground=colorFondo, clicked=None, *args, **kwargs):
        super(RoundedButton, self).__init__(master, *args, **kwargs)
        self.config(bg=self.master["bg"])
        self.btnbackground = btnbackground
        self.clicked = clicked
        
        self.radius = radius        
        self['height']=50                   #Tamaño alto
        self['width']=240                   #Tamaño largo
        self['highlightthickness'] = 0      #Quitar margen canvas
        
        self.rect = self.round_rectangle(0, 0, 0, 0, tags="button", radius=radius, fill=btnbackground)
        self.text = self.create_text(0, 0, text=text, tags="button", fill=btnforeground, font=("Century Gothic", 16), justify="center")

        self.tag_bind("button", "<ButtonPress>", self.border)
        self.tag_bind("button", "<ButtonRelease>", self.border)
        self.bind("<Configure>", self.resize)
        
        text_rect = self.bbox(self.text)
        if int(self["width"]) < text_rect[2]-text_rect[0]:
            self["width"] = (text_rect[2]-text_rect[0]) + 10
        
        if int(self["height"]) < text_rect[3]-text_rect[1]:
            self["height"] = (text_rect[3]-text_rect[1]) + 10
          
    def round_rectangle(self, x1, y1, x2, y2, radius=25, update=False, **kwargs): # if update is False a new rounded rectangle's id will be returned else updates existing rounded rect.
        # source: https://stackoverflow.com/a/44100075/15993687
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]

        if not update:
            return self.create_polygon(points, **kwargs, smooth=True)
        
        else:
            self.coords(self.rect, points)

    def resize(self, event):
        text_bbox = self.bbox(self.text)

        if self.radius > event.width or self.radius > event.height:
            radius = min((event.width, event.height))

        else:
            radius = self.radius

        width, height = event.width, event.height

        if event.width < text_bbox[2]-text_bbox[0]:
            width = text_bbox[2]-text_bbox[0] + 30
        
        if event.height < text_bbox[3]-text_bbox[1]:  
            height = text_bbox[3]-text_bbox[1] + 30
        
        self.round_rectangle(5, 5, width-5, height-5, radius, update=True)

        bbox = self.bbox(self.rect)

        x = ((bbox[2]-bbox[0])/2) - ((text_bbox[2]-text_bbox[0])/2)
        y = ((bbox[3]-bbox[1])/2) - ((text_bbox[3]-text_bbox[1])/2)

        self.moveto(self.text, x, y)

    def border(self, event):
        if event.type == "4":
            self.itemconfig(self.rect, fill=cuartoColor)
            if self.clicked is not None:
                self.clicked()
        else:
            self.itemconfig(self.rect, fill=self.btnbackground)


# Crear la root
root = Tk()
# Icono Aplicación
anchoVentana = 580         #Definir medidas de ventana
altoVentana = 420
xVentana = root.winfo_screenwidth() // 2 - anchoVentana // 2  #Definir posición de laventana
yVentana = root.winfo_screenheight() // 2 - altoVentana // 2
posicion = str(anchoVentana) + "x" + str(altoVentana) + \
    "+" + str(xVentana) + "+" + str(yVentana)
root.geometry(posicion)
root.resizable(False, False)    #La ventana no se puede alargar ni ensanchar
root.title("RGM OPMA") # Reconocimiento de gestos manuales para la organización y presentación de material audiovisual

# Crear menu superior
barraMenu = Menu(root)
escenarioMenu = Menu(barraMenu, tearoff=0)
ayudaMenu = Menu(barraMenu, tearoff=0)
root.config(bg=colorFondo, menu=barraMenu)

escenarioMenu.add_command(label="Nuevo")
escenarioMenu.add_command(label="Abrir")
escenarioMenu.add_command(label="Editar")
escenarioMenu.add_command(label="Eliminar")
escenarioMenu.add_separator()
escenarioMenu.add_command(label="Salir", command=root.quit)

#ayudaMenu.add_command(label="Ayuda")

barraMenu.add_cascade(label="Escenarios", menu=escenarioMenu)
#barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

# Crear funciones
def nuevaVentana():            # Plantilla para nuevas ventanas
    # root.withdraw()
    top2 = Toplevel()
    anchoVentana = 580         #Definir medidas de ventana
    altoVentana = 420
    xVentana = root.winfo_screenwidth() // 2 - anchoVentana // 2  #Definir posición de la ventana
    yVentana = root.winfo_screenheight() // 2 - altoVentana // 2
    posicion = str(anchoVentana) + "x" + str(altoVentana) + \
        "+" + str(xVentana) + "+" + str(yVentana)
    top2.title("root nueva")
    top2.geometry(posicion)
    button = Button(top2, text="OK", command=top2.destroy).pack()

def windowRoot():           # Ventana principal
    pass

def siguienteImagen():
    print("Imagen siguiente")

def anteriorImagen():
    print("Imagen anterior")

def ventanaAyuda():           # Ventana de ayuda
    top = Toplevel()
    top.overrideredirect(True) # Quitar barra de título
    anchoVentana = 800         #Definir medidas de ventana
    altoVentana = 600
    xVentana = root.winfo_screenwidth() // 2 - anchoVentana // 2  #Definir posición de la ventana
    yVentana = root.winfo_screenheight() // 2 - altoVentana // 2
    posicion = str(anchoVentana) + "x" + str(altoVentana) + \
        "+" + str(xVentana) + "+" + str(yVentana)
    top.geometry(posicion)
    top.config(bg=colorFondo)
    top.title("Ayuda")
    Label(top, text="Ayuda", style="Label.TLabel" ).grid(row=0, column=0, pady=30)
    Label(top, text="Aqui debe aparecer texto o imagenes con ayuda", style="Label2.TLabel" ).grid(row=1, column=0, columnspan=3)
    RoundedButton(top,text="<", radius=40, btnbackground=colorFondo, btnforeground=cuartoColor, clicked=anteriorImagen).grid(row=2, column=0)
    canv = Canvas(top, width=300, height=300, bg=colorFondo)
    canv.grid(row=2, column=1)
    img = ImageTk.PhotoImage(Image.open("img/gestos/2.png"))  # PIL solution
    canv.create_image(20,20, anchor=NW, image=img)
    RoundedButton(top,text=">", radius=40, btnbackground=colorFondo, btnforeground=cuartoColor, clicked=siguienteImagen).grid(row=2, column=2)
    RoundedButton(top,text="Cerrar Ayuda", radius=40, btnbackground=tercerColor, btnforeground=colorFuente, clicked=top.destroy).grid(row=4, column=2, pady=50)


def configurarEscenario():    # Ventana de configuracion de escenario
    top = Toplevel()
    root.geometry(posicion)
    top.config(bg=colorFondo)
    top.title("Configura tu escenario")

def crearEscenario():
    # root.withdraw()
    top = Toplevel()
    anchoVentana = 580         #Definir medidas de ventana
    altoVentana = 420
    xVentana = root.winfo_screenwidth() // 2 - anchoVentana // 2  #Definir posición de la ventana
    yVentana = root.winfo_screenheight() // 2 - altoVentana // 2
    posicion = str(anchoVentana) + "x" + str(altoVentana) + \
        "+" + str(xVentana) + "+" + str(yVentana)
    top.title("root nueva")
    top.geometry(posicion)
    top.config(bg=colorFondo)
    top.title("Crear escenario")
    Label(top, text="Datos del escenario", style="Label.TLabel").grid(row=0, column=0,pady=20,padx=20)
    # frame2 = Frame(top, bd=5, relief="sunken", padx=20, pady=20).pack()
    Label(top, 
                     text="Nombre:", 
                     style="Label2.TLabel").grid(row=1, column=0, padx=50, pady=20)
    Label(top,
                     text="Fecha de creacion:", 
                     style="Label2.TLabel").grid(row=2,column=0, padx=50, pady=20)

    nombreEscenario = StringVar()
    Entry(top, textvariable=nombreEscenario).grid(row=1, column=1)
    Label(top, text=date.today(), style="Label2.TLabel").grid(row=2, column=1)
    RoundedButton(top,text="Crear escenario", radius=40, btnbackground=tercerColor, btnforeground=colorFuente, clicked=top.destroy).grid(row=3, column=1,pady=40)

def abrirEscenario():
    # root.withdraw()
    top = Toplevel()
    anchoVentana = 900         #Definir medidas de ventana
    altoVentana = 450
    xVentana = root.winfo_screenwidth() // 2 - anchoVentana // 2  #Definir posición de la ventana
    yVentana = root.winfo_screenheight() // 2 - altoVentana // 2
    posicion = str(anchoVentana) + "x" + str(altoVentana) + \
        "+" + str(xVentana) + "+" + str(yVentana)
    top.geometry(posicion)
    top.config(bg=colorFondo)
    top.title("Listado de escenarios")
    Label(top, text="Abrir Escenario", style="Label.TLabel").grid(row=0, column=0,pady=20,padx=20)
    # frame2 = Frame(top, bd=5, relief="sunken", padx=20, pady=20).pack()
    nombreEscenario = StringVar()
    origen = StringVar()
    origenDesplegar = "img/gestos"
    origenDatos = listdir(origenDesplegar)

    tabla = Treeview(top,columns=2)
    tabla.grid(row=2, column=0,padx=80, rowspan=3)
    tabla.heading("#0",text = "Fecha")
    tabla.heading("#1",text = "Nombre")
    for escenario in origenDatos:
        tabla.insert("",0,text="Fecha",values=escenario[:-4])

    Combobox (top, values = origenDatos, textvariable = origen,style="Combobox.TCombobox")
    RoundedButton(top,text="Cambiar Origen", radius=40, btnbackground=colorFuente, btnforeground=colorFondo, clicked=top.destroy).grid(row=5, column=0,pady=10)
    RoundedButton(top,text="Abrir", radius=40, btnbackground=tercerColor, btnforeground=colorFuente, clicked=top.destroy).grid(row=2, column=2,pady=10)
    RoundedButton(top,text="Editar", radius=40, btnbackground=cuartoColor, btnforeground=colorFuente, clicked=editarEscenario).grid(row=3, column=2,pady=10)
    RoundedButton(top,text="Eliminar", radius=40, btnbackground="red", btnforeground=colorFuente, clicked=top.destroy).grid(row=4, column=2,pady=10)

s2 = Style()
s2.configure('Combobox.TCombobox',
        background = colorFondo,
        foreground = colorFuente,
        font=('Century Gothic', 16))

def editarEscenario():
    # root.withdraw()

    def agregarAccion():
        pass

    top = Toplevel()
    anchoVentana = 860     #Definir medidas de ventana
    altoVentana = 550
    xVentana = root.winfo_screenwidth() // 2 - anchoVentana // 2  #Definir posición de la ventana
    yVentana = root.winfo_screenheight() // 2 - altoVentana // 2
    posicion = str(anchoVentana) + "x" + str(altoVentana) + \
        "+" + str(xVentana) + "+" + str(yVentana)
    top.geometry(posicion)
    top.config(bg=colorFondo)
    top.title("Configurar Escenario")
    Label(top, text="Configurar Escenario", style="Label.TLabel").grid(row=0, column=0,pady=20,padx=60)

    # frame2 = Frame(top, bd=5, relief="sunken", padx=20, pady=20).pack()
    
    
    lblFrame = LabelFrame(top, text=" ",background=colorFondo)
    lblFrame.grid(row=2, column=0,padx=80, columnspan=3,sticky=EW)
    Label(lblFrame, text="Gesto",background=colorFondo,width=20).grid(row=0, column=0)
    Label(lblFrame, text="Acción",background=colorFondo,width=40).grid(row=0, column=1)
    Label(lblFrame, text="Material",background=colorFondo,width=40).grid(row=0, column=2)

    lblFramen = LabelFrame(lblFrame, text=" ",background=cuartoColor,border=0)
    lblFramen.grid(row=1, column=0,columnspan=3)

    def actualizarImagen(self):
        print(gestocbb.get())
        img = ImageTk.PhotoImage(Image.open("img/gestos/"+gestocbb.get()+".png"))  # PIL solution
        canv.create_image(40,40, anchor=NW, image=img)    
        pass


    #Gesto

    gestocbb = StringVar()
    accioncbb = StringVar()
    cbbGesto = Combobox(lblFramen, textvariable=gestocbb,width=20)
    cbbGesto['values'] = ('1', '2', '3')
    cbbGesto.grid(row=0, column=0)
    cbbGesto.bind("<<ComboboxSelected>>", actualizarImagen)
    canv = Canvas(lblFramen, width=50, height=50, bg=colorFondo)
    canv.grid(row=1)
    img = ImageTk.PhotoImage(Image.open("img/gestos/1.png"))  # PIL solution
    canv.create_image(40,40, anchor=NW, image=img)

    #Acción

    cbbAccion = Combobox(lblFramen, textvariable=accioncbb,width=40)
    cbbAccion['values'] = ('a', 'b', 'c')
    cbbAccion.grid(row=0, column=1)
    cbbAccion.bind("<<ComboboxSelected>>", actualizarImagen)

    #Material
    def selec():
        pass

    opcion = IntVar() # Como StrinVar pero en entero

    Radiobutton(lblFramen, text="Archivo", variable=opcion, 
                value=0, command=selec).grid(row=0,column=2)
    Radiobutton(lblFramen, text="Enlace", variable=opcion,
                value=1, command=selec).grid(row=1,column=2)
    RoundedButton(lblFramen,text="Seleccionar", radius=40, btnbackground=cuartoColor, btnforeground=colorFuente, clicked=abrirEscenario2).grid(row=0, column=3, rowspan=2)





    origen = StringVar()
    origenDesplegar = "img/gestos"
    origenDatos = listdir(origenDesplegar)
    combo = Combobox (top, values = origenDatos, textvariable = origen,style="Combobox.TCombobox")
    RoundedButton(top,text="Agregar Acción",        radius=40, btnbackground=colorFuente, btnforeground=colorFondo, clicked=agregarAccion).grid(row=3, column=1,pady=10)
    RoundedButton(top,text="Guardar", radius=40, btnbackground=tercerColor, btnforeground=colorFuente, clicked=top.destroy).grid(row=4, column=0,pady=40)
    RoundedButton(top,text="Abrir",                 radius=40, btnbackground=tercerColor, btnforeground=colorFuente, clicked=top.destroy).grid(row=4, column=1,pady=10)
    RoundedButton(top,text="Regresar",              radius=40, btnbackground="red", btnforeground=colorFuente,       clicked=top.destroy).grid(row=4, column=2,pady=10)
    



def abrirEscenario2():
    try:
        path = filedialog.askopenfilename(
            title="Abrir escenario",
            filetypes=(
                ("Archivos de texto", "*.txt"),
                ("Archivos RGM", "*.rgm"),
            ))
        file = open(path, 'r')
        print (file.read())
    except:
        print("No se abrió nada")




# Crear un contenido principal
Label(root, text="Menú principal", style="Label.TLabel").grid(row=0, column=0,pady=20,padx=20)
#label2 = Label(root, text="Abre o crea un nuevo escenario para continuar:", bg=colorFondo, fg=colorFuente).grid(row=1, column=1)

#Estilos
s = Style()
s.configure('Label.TLabel',
        background = colorFondo,
        foreground = colorFuente,
        font=('Century Gothic', 16))

s2 = Style()
s2.configure('Label2.TLabel',
        background = colorFondo,
        foreground = colorFuente,
        font=('Century Gothic', 12))


# button1 = Button(root, text="Otra root", command=nuevaVentana).pack()
RoundedButton(root,text="Abrir/Editar Escenario", radius=40, btnbackground=tercerColor, btnforeground=colorFuente, clicked=abrirEscenario).grid(row=2, column=1,pady=40)
RoundedButton(root,text="Nuevo Escenario", radius=40, btnbackground=tercerColor, btnforeground=colorFuente, clicked=crearEscenario).grid(row=3, column=1)

#b4 = Button(root, text="Configuración", command=configurarEscenario, style="Boton.TButton").grid(row=4, column=1, pady=6)

#Label2(root, bitmap="question", background=colorFondo, foreground='white').grid(row=0, column=2,sticky=E,padx=60)

b5 = RoundedButton(root, text="?", radius=40,btnbackground=colorFondo, btnforeground=colorFuente, clicked=ventanaAyuda).grid(row=0, column=2)

root.mainloop()