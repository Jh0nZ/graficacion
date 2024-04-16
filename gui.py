import math
import os
from pathlib import Path
import subprocess
import time
from tkinter import NW, Menu, Tk, Canvas, Entry, Text, Button, colorchooser, StringVar, filedialog, ttk, Frame, Scrollbar, RIGHT
from PIL import Image, ImageTk, ImageDraw
from shape.Circulo import Circulo
from shape.Triangulo import Triangulo

def is_number(char):
    try:
        float(char)
        return True
    except ValueError:
        return False

def validate_number(text):
    if text == "":
        return True
    return is_number(text)

def hex_to_rgb(hex_color):
    # Eliminar el caracter '#' si está presente
    hex_color = hex_color.lstrip('#')
    
    # Verificar si el color es un formato válido de 3 o 6 caracteres
    if len(hex_color) == 3:
        r = int(hex_color[0] * 2, 16)
        g = int(hex_color[1] * 2, 16)
        b = int(hex_color[2] * 2, 16)
    elif len(hex_color) == 6:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    else:
        raise ValueError("Formato de color hexadecimal inválido.")
    
    return (r, g, b)

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])



def clearImage():
    for x in range(700):
        for y in range(700):
            imagen.putpixel((x, y), (200, 200, 200))

window = Tk()
window.geometry("980x720")
window.configure(bg = "#FFFFFF")
window.title("Figuras")
window.resizable(False, False)





canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 980,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

# ------------------------variables------------------------
lastType = "New"
figuraSeleccionada = Circulo((100, 100), 25, (0, 80, 220), (31, 31, 31), 6, "Segmented")
button_texts = []


shapes = ["Triangle", "Circle"]
selected_shape = StringVar(window)
selected_shape.set(shapes[0])

fillColorVar = StringVar(window)
fillColorVar.set("#ff00ff")

borderColorVar = StringVar(window)
borderColorVar.set("#000000")

line_styles = ["Continuous", "Segmented"]
selected_style = StringVar(window)
selected_style.set(line_styles[0])

grosorBordeVar = StringVar(window)
grosorBordeVar.set("1")

positionXVar = StringVar(window)
positionXVar.set("100")

positionYVar = StringVar(window)
positionYVar.set("100")

sizeRadioVar = StringVar(window)
sizeRadioVar.set("25")

scaleVar = StringVar(window)
scaleVar.set("1")

rotationVar = StringVar(window)
rotationVar.set("0")

# ------------------------variables------------------------
def change_color(colorVar, button):
    color = colorchooser.askcolor(title="Select a color")
    if color[1]:  # Si se selecciona un color y no se cancela
        colorVar.set(color[1])
        button.config(bg=color[1])

def shape_selected(event):
    selected_shape = shape_dropdown.get()
    if (selected_shape == "Circle"):
        canvas.itemconfig(radioSizeText, text="Radio")
    else:
        canvas.itemconfig(radioSizeText, text="Size")
    print("Shape selected:", selected_shape)
    window.focus_set()

def style_selected(event):
    selected_style = style_dropdown.get()
    print("Style selected:", selected_style)
    window.focus_set()

canvas.create_text(
    16.0,
    70.0,
    anchor="nw",
    text="Fill color:",
    fill="#000000",
    font=("RobotoRoman Regular", 24 * -1)
)

canvas.create_text(
    16.0,
    28.0,
    anchor="nw",
    text="Shape:",
    fill="#000000",
    font=("RobotoRoman Regular", 24 * -1)
)

canvas.create_text(
    16.0,
    112.0,
    anchor="nw",
    text="Border color:",
    fill="#000000",
    font=("RobotoRoman Regular", 24 * -1)
)

canvas.create_text(
    16.0,
    154.0,
    anchor="nw",
    text="Border style:",
    fill="#000000",
    font=("RobotoRoman Regular", 24 * -1)
)

canvas.create_text(
    16.0,
    196.0,
    anchor="nw",
    text="Border width:",
    fill="#000000",
    font=("RobotoRoman Regular", 24 * -1)
)
# ------------------------position-x---------------------------
canvas.create_text(
    16.0,
    196.0+42,
    anchor="nw",
    text="Position x:",
    fill="#000000",
    font=("RobotoRoman Regular", 24 * -1)
)
positionXEntry = Entry(
    bd=0,
    bg="#d9d9d9",
    fg="#000716",
    highlightthickness=0,
    font=("Roboto", 12),
    validate="key",
    validatecommand=(window.register(validate_number), "%S"),
    textvariable=positionXVar
)
positionXEntry.bind("<Return>", lambda e:window.focus_set())  # Llamar a quitar_focus con Enter
positionXEntry.bind("<FocusOut>", lambda e:window.focus_set())
positionXEntry.place(
    x=169.0,
    y=196.0+42,
    width=90.0,
    height=35.0
)

# ------------------------position-y---------------------------
canvas.create_text(
    16.0,
    196.0+42+42,
    anchor="nw",
    text="Position y:",
    fill="#000000",
    font=("RobotoRoman Regular", 24 * -1)
)
positionYEntry = Entry(
    bd=0,
    bg="#d9d9d9",
    fg="#000716",
    highlightthickness=0,
    font=("Roboto", 12),
    validate="key",
    validatecommand=(window.register(validate_number), "%S"),
    textvariable=positionYVar
)
positionYEntry.bind("<Return>", lambda e:window.focus_set())
positionYEntry.bind("<FocusOut>", lambda e:window.focus_set())
positionYEntry.place(
    x=169.0,
    y=196.0+42+42,
    width=90.0,
    height=35.0
)

# --------------------------size-------------------------------
radioSizeText = canvas.create_text(
    16.0,
    196.0+42+42+42,
    anchor="nw",
    text="Size:",
    fill="#000000",
    font=("RobotoRoman Regular", 24 * -1)
)
sizeRadioEntry = Entry(
    bd=0,
    bg="#d9d9d9",
    fg="#000716",
    highlightthickness=0,
    font=("Roboto", 12),
    validate="key",
    validatecommand=(window.register(validate_number), "%S"),
    textvariable=sizeRadioVar
)
sizeRadioEntry.bind("<Return>", lambda e:window.focus_set())  # Llamar a quitar_focus con Enter
sizeRadioEntry.bind("<FocusOut>", lambda e:window.focus_set())
sizeRadioEntry.place(
    x=169.0,
    y=196.0+42+42+42,
    width=90.0,
    height=35.0
)
# --------------------------scale------------------------------
canvas.create_text(
    16.0,
    196.0+42+42+42+42,
    anchor="nw",
    text="Scale:",
    fill="#000000",
    font=("RobotoRoman Regular", 24 * -1)
)
scaleEntry= Entry(
    bd=0,
    bg="#d9d9d9",
    fg="#000716",
    highlightthickness=0,
    font=("Roboto", 12),
    validate="key",
    validatecommand=(window.register(validate_number), "%S"),
    textvariable=scaleVar
)
scaleEntry.bind("<Return>", lambda e:window.focus_set())
scaleEntry.bind("<FocusOut>", lambda e:window.focus_set())
scaleEntry.place(
    x=169.0,
    y=196.0+42+42+42+42,
    width=90.0,
    height=35.0
)
# --------------------------rotation---------------------------
canvas.create_text(
    16.0,
    196.0+42+42+42+42+42,
    anchor="nw",
    text="Rotation:",
    fill="#000000",
    font=("RobotoRoman Regular", 24 * -1)
)
rotationEntry = Entry(
    bd=0,
    bg="#d9d9d9",
    fg="#000716",
    highlightthickness=0,
    font=("Roboto", 12),
    validate="key",
    validatecommand=(window.register(validate_number), "%S"),
    textvariable=rotationVar
)
rotationEntry.bind("<Return>", lambda e:window.focus_set())
rotationEntry.bind("<FocusOut>", lambda e:window.focus_set())
rotationEntry.place(
    x=169.0,
    y=196.0+42+42+42+42+42,
    width=90.0,
    height=35.0
)

# ------------------------ Lista Scrolleable de Botones ------------------------
# Frame para contener la lista de botones
button_list_frame = Frame(window, bg="#FFFFFF")
button_list_frame.place(x=16.0, y=196.0+42+42+42+42+42+60+42)
# Canvas para la lista de botones con scrollbar
canvas_buttons = Canvas(button_list_frame, bg="#FFFFFF", width=235, height=200, bd=0, highlightthickness=0)
scrollbar_buttons = Scrollbar(button_list_frame, orient="vertical", command=canvas_buttons.yview)
scrollbar_buttons.pack(side=RIGHT, fill="y")
canvas_buttons.pack(side="left", fill="both", expand=True)
canvas_buttons.configure(yscrollcommand=scrollbar_buttons.set)
# Frame para el scroll de botones
button_list_inner = Frame(canvas_buttons, bg="#FFFFFF")
button_list_inner_id = canvas_buttons.create_window((0, 0), window=button_list_inner, anchor="nw")
# scroll
def configure_scroll(event):
    canvas_buttons.configure(scrollregion=canvas_buttons.bbox("all"))
button_list_inner.bind("<Configure>", configure_scroll)
def on_canvas_configure(event):
    canvas_buttons.itemconfig(button_list_inner_id, width=canvas_buttons.winfo_width())
canvas_buttons.bind("<Configure>", on_canvas_configure)
# Función para manejar el scroll con la rueda del ratón
def on_mousewheel(event):
    canvas_buttons.yview_scroll(int(-1 * (event.delta / 120)), "units")
canvas_buttons.bind_all("<MouseWheel>", on_mousewheel)
# Destruye todos los botones dentro del scroll
def limpiar_frame():
    for widget in button_list_inner.winfo_children():
        widget.destroy()
# ------------------------ Fin de la Lista Scrolleable de Botones ------------------------

# ------------------------ Botones importantes ------------------------
# ------------------------ New ------------------------

def newFuntion():
    global figuraSeleccionada, button_texts
    clearImage()
    for figura in button_texts:
        figura.dibujar(imagen)
    figuraSeleccionada = Circulo( 
        (300,300), 
        100, 
        (200,0,200), 
        (31,31,31), 
        3, 
        "Continuous",
    )

    selected_style.set(figuraSeleccionada.estilo_borde)
    style_dropdown.config(textvariable=selected_style)

    fillColorVar.set(rgb_to_hex(figuraSeleccionada.color_relleno))
    button_fill_color.config(bg=fillColorVar.get())

    grosorBordeVar.set(figuraSeleccionada.ancho_borde)
    grosorBordeEntry.config(textvariable=grosorBordeVar)

    borderColorVar.set(rgb_to_hex(figuraSeleccionada.color_borde))
    button_border_color.config(bg=borderColorVar.get())

    positionXVar.set(figuraSeleccionada.x)
    positionXEntry.config(textvariable=positionXVar)

    positionYVar.set(figuraSeleccionada.y)
    positionYEntry.config(textvariable=positionYVar)

    sizeRadioVar.set(figuraSeleccionada.radio)
    sizeRadioEntry.config(textvariable=sizeRadioVar)

    scaleVar.set(figuraSeleccionada.scale)
    scaleEntry.config(textvariable=scaleVar)

    rotationVar.set("0")
    rotationEntry.config(textvariable=rotationVar)

    imagen_tk.paste(imagen)
    canvas.update()

button_New = Button(
    text="    🗑️",
    bg="#0077ee",
    fg="#eeeeee",
    font=("Roboto", 16),
    borderwidth=0,
    highlightthickness=0,
    command=newFuntion,
    relief="flat"
)
button_New.place(
    x=10.0,
    y=450.0,
    width=60.0,
    height=40.0
)
# ------------------------ New ------------------------

# ------------------------ Delete ------------------------
def eliminarFuntion():
    global button_texts, figuraSeleccionada
    print(figuraSeleccionada.name)
    if (figuraSeleccionada.name != "New"):
        for figuraEliminar in button_texts:
            if figuraEliminar.name == figuraSeleccionada.name:
                button_texts.remove(figuraEliminar)
                print(f"Círculo con nombre '{figuraSeleccionada.name}' eliminado.")
                #figuraSeleccionada = Circulo((100, 100), 25, (0, 80, 220), (31, 31, 31), 6, "Segmented")
                limpiar_frame()
                clearImage()
                for figuraaaa in button_texts:
                    def figuraCallBack(figuraButton):
                        def aaa():
                            global figuraSeleccionada
                            figuraSeleccionada = figuraButton
                            print(figuraButton.name, " se presiono")
                            if isinstance(figuraButton, Circulo):
                                selected_shape.set(shapes[1])
                                canvas.itemconfig(radioSizeText, text="Radio")
                            else:
                                selected_shape.set(shapes[0])
                                canvas.itemconfig(radioSizeText, text="Size")
                            
                            shape_dropdown.config(textvariable=selected_shape)
                            selected_style.set(figuraButton.estilo_borde)
                            style_dropdown.config(textvariable=selected_style)

                            fillColorVar.set(rgb_to_hex(figuraButton.color_relleno))
                            button_fill_color.config(bg=fillColorVar.get())

                            grosorBordeVar.set(figuraButton.ancho_borde)
                            grosorBordeEntry.config(textvariable=grosorBordeVar)

                            borderColorVar.set(rgb_to_hex(figuraButton.color_borde))
                            button_border_color.config(bg=borderColorVar.get())

                            positionXVar.set(figuraButton.x)
                            positionXEntry.config(textvariable=positionXVar)

                            positionYVar.set(figuraButton.y)
                            positionYEntry.config(textvariable=positionYVar)

                            sizeRadioVar.set(figuraButton.radio)
                            sizeRadioEntry.config(textvariable=sizeRadioVar)

                            scaleVar.set(figuraButton.scale)
                            scaleEntry.config(textvariable=scaleVar)

                            rotationVar.set(figuraButton.rotation)
                            rotationEntry.config(textvariable=rotationVar)
                        return aaa
                    
                    nuevo_boton = Button(
                        button_list_inner, 
                        text=figuraaaa.name, 
                        width=20, 
                        height=2, 
                        bg="#0077ee", 
                        fg="#eeeeee", 
                        font=("Roboto", 12), 
                        borderwidth=0, 
                        highlightthickness=0, 
                        command=figuraCallBack(figuraaaa)
                    )
                    nuevo_boton.pack(pady=5)
                    figuraaaa.dibujar(imagen)
                configure_scroll(None)
                imagen_tk.paste(imagen)
                canvas.update()
                return
        print(f"Círculo con nombre '{figuraSeleccionada.name}' no encontrado.")
    else:
        print(f"Círculo con nombre '{figuraSeleccionada.name}' es nuevo.")

button_Delete = Button(
    text="Delete",
    bg="#0077ee",
    fg="#eeeeee",
    font=("Roboto", 16),
    borderwidth=0,
    highlightthickness=0,
    command=eliminarFuntion,
    relief="flat"
)
button_Delete.place(
    x=10+60+5,
    y=450.0,
    width=80.0,
    height=40.0
)
# ------------------------ Delete ------------------------

# ------------------------ Save ------------------------
def agregar_boton():
    global figuraSeleccionada, button_texts
    # Función para agregar un nuevo botón a la lista scrolleable
    if figuraSeleccionada.name != "New":
        for figura in button_texts:
            if figura.name == figuraSeleccionada.name:
                figura.cambiar_punto_control((int(positionXVar.get()), int(positionYVar.get())))
                figura.radio = int(sizeRadioVar.get())
                figura.color_relleno = hex_to_rgb(fillColorVar.get())
                figura.color_borde = hex_to_rgb(borderColorVar.get())
                figura.ancho_borde = int(grosorBordeVar.get())
                figura.estilo_borde = selected_style.get()
                figura.rotation = int(rotationVar.get())
                figura.scale = int(scaleVar.get())
                figuraSeleccionada = Circulo((100, 100), 25, (0, 80, 220), (31, 31, 31), 6, "Segmented")
                break
    else:
        nuevo_texto = "Circle {}".format(len(button_texts) + 1) if isinstance(figuraSeleccionada, Circulo) else "Triangle {}".format(len(button_texts) + 1)
        figuraSeleccionada.name = nuevo_texto
        button_texts.append(figuraSeleccionada)
        copiaFigura = figuraSeleccionada

        def aaa():
            global figuraSeleccionada
            print(nuevo_texto, "se presiono")
            figuraSeleccionada = copiaFigura

            if isinstance(figuraSeleccionada, Circulo):
                selected_shape.set(shapes[1])
                canvas.itemconfig(radioSizeText, text="Radio")
            else:
                selected_shape.set(shapes[0])
                canvas.itemconfig(radioSizeText, text="Size")
            
            shape_dropdown.config(textvariable=selected_shape)
            selected_style.set(figuraSeleccionada.estilo_borde)
            style_dropdown.config(textvariable=selected_style)

            fillColorVar.set(rgb_to_hex(figuraSeleccionada.color_relleno))
            button_fill_color.config(bg=fillColorVar.get())

            grosorBordeVar.set(figuraSeleccionada.ancho_borde)
            grosorBordeEntry.config(textvariable=grosorBordeVar)

            borderColorVar.set(rgb_to_hex(figuraSeleccionada.color_borde))
            button_border_color.config(bg=borderColorVar.get())

            positionXVar.set(figuraSeleccionada.x)
            positionXEntry.config(textvariable=positionXVar)

            positionYVar.set(figuraSeleccionada.y)
            positionYEntry.config(textvariable=positionYVar)

            sizeRadioVar.set(figuraSeleccionada.radio)
            sizeRadioEntry.config(textvariable=sizeRadioVar)

            scaleVar.set(figuraSeleccionada.scale)
            scaleEntry.config(textvariable=scaleVar)

            rotationVar.set(figuraSeleccionada.rotation)
            rotationEntry.config(textvariable=rotationVar)
            
        nuevo_boton = Button(
            button_list_inner, 
            text=nuevo_texto, 
            width=20, 
            height=2, 
            bg="#0077ee", 
            fg="#eeeeee", 
            font=("Roboto", 12), 
            borderwidth=0, 
            highlightthickness=0, 
            command=aaa
        )
        nuevo_boton.pack(pady=5)
        figuraSeleccionada = Circulo((100, 100), 25, (0, 80, 220), (31, 31, 31), 6, "Segmented")

        selected_style.set(figuraSeleccionada.estilo_borde)
        style_dropdown.config(textvariable=selected_style)

        fillColorVar.set(rgb_to_hex(figuraSeleccionada.color_relleno))
        button_fill_color.config(bg=fillColorVar.get())

        grosorBordeVar.set(figuraSeleccionada.ancho_borde)
        grosorBordeEntry.config(textvariable=grosorBordeVar)

        borderColorVar.set(rgb_to_hex(figuraSeleccionada.color_borde))
        button_border_color.config(bg=borderColorVar.get())

        positionXVar.set(figuraSeleccionada.x)
        positionXEntry.config(textvariable=positionXVar)

        positionYVar.set(figuraSeleccionada.y)
        positionYEntry.config(textvariable=positionYVar)

        sizeRadioVar.set(figuraSeleccionada.radio)
        sizeRadioEntry.config(textvariable=sizeRadioVar)

        scaleVar.set(figuraSeleccionada.scale)
        scaleEntry.config(textvariable=scaleVar)

        rotationVar.set("0")
        rotationEntry.config(textvariable=rotationVar)
    clearImage()
    for figura in button_texts:
        figura.dibujar(imagen)
    imagen_tk.paste(imagen)
    canvas.update()
    # Configurar el scroll para la nueva lista de botones
    configure_scroll(None)

button_Save= Button(
    text="Save",
    bg="#0077ee",
    fg="#eeeeee",
    font=("Roboto", 16),
    borderwidth=0,
    highlightthickness=0,
    command=agregar_boton,
    relief="flat"
)
button_Save.place(
    x=10+60+5+80+5,
    y=450.0,
    width=60.0,
    height=40.0
)
# ------------------------ Save ------------------------

# ------------------------ show ------------------------
def showFunction():
    global figuraSeleccionada, button_texts
    clearImage()
    for figura in button_texts:
        if figuraSeleccionada.name == figura.name:
            continue
        figura.dibujar(imagen)
    
    if selected_shape.get() == "Circle":
        figuraSeleccionada = Circulo(
            (int(positionXVar.get()), int(positionYVar.get())), 
            int(sizeRadioVar.get()), 
            hex_to_rgb(fillColorVar.get()), 
            hex_to_rgb(borderColorVar.get()), 
            int(grosorBordeVar.get()), 
            selected_style.get(),
            figuraSeleccionada.name,
            int(scaleVar.get()),
            int(rotationVar.get())
        )
    else:
        figuraSeleccionada = Triangulo(
            (int(positionXVar.get()), int(positionYVar.get())), 
            int(sizeRadioVar.get()), 
            hex_to_rgb(fillColorVar.get()), 
            hex_to_rgb(borderColorVar.get()), 
            int(grosorBordeVar.get()), 
            selected_style.get(),
            figuraSeleccionada.name,
            int(scaleVar.get()),
            int(rotationVar.get())
        )
    figuraSeleccionada.dibujar(imagen)
    imagen_tk.paste(imagen)
    canvas.update()

button_Show= Button(
    text="     👁️",
    bg="#0077ee",
    fg="#eeeeee",
    font=("Roboto", 16),
    borderwidth=0,
    highlightthickness=0,
    command=showFunction,
    relief="flat"
)
button_Show.place(
    x=10+60+5+80+5+60+5,
    y=450.0,
    width=40.0,
    height=40.0
)
# ------------------------ show ------------------------
button_fill_color = Button(
    bg=fillColorVar.get(),
    borderwidth=0,
    highlightthickness=0,
    command=lambda: change_color(fillColorVar, button_fill_color),
    relief="flat"
)
button_fill_color.place(
    x=169.0,
    y=66.0,
    width=90.0,
    height=35.0
)

button_border_color = Button(
    bg=borderColorVar.get(),
    borderwidth=0,
    highlightthickness=0,
    command=lambda: change_color(borderColorVar, button_border_color),
    relief="flat"
)
button_border_color.place(
    x=169.0,
    y=108.0,
    width=90.0,
    height=35.0
)

# shape combobox
shape_dropdown = ttk.Combobox(window, textvariable=selected_shape, values=shapes, state="readonly")
shape_dropdown.bind("<<ComboboxSelected>>", shape_selected)
shape_dropdown.current(0)
shape_dropdown.place(x=139.0+30, y=25.0, width=90.0, height=35.0)

# estilo borde
style_dropdown = ttk.Combobox(window, textvariable=selected_style, values=line_styles, state="readonly")
style_dropdown.bind("<<ComboboxSelected>>", style_selected)
style_dropdown.current(0)
style_dropdown.place(x=169.0, y=151.0, width=90.0, height=35.0)

grosorBordeEntry = Entry(
    bd=0,
    bg="#d9d9d9",
    fg="#000716",
    highlightthickness=0,
    font=("Roboto", 12),
    validate="key",
    validatecommand=(window.register(validate_number), "%S"),
    textvariable=grosorBordeVar
)

grosorBordeEntry.bind("<Return>", lambda e:window.focus_set())  # Llamar a quitar_focus con Enter
grosorBordeEntry.bind("<FocusOut>", lambda e:window.focus_set())
grosorBordeEntry.place(
    x=169.0,
    y=192.0,
    width=90.0,
    height=35.0
)

# imagen donde dibujamos todo
imagen = Image.new("RGB", (700, 700), color=(200, 200, 200))
imagen_tk = ImageTk.PhotoImage(imagen)
draw = ImageDraw.Draw(imagen)

def guardarImagen():
    global imagen
    ruta = filedialog.asksaveasfilename(defaultextension=".png",
                                        filetypes=[("PNG files", "*.png")])
    if ruta:
        # Convertir la imagen a RGB si es necesario
        if imagen.mode != "RGB":
            imagen = imagen.convert("RGB")
        
        # Guardar la imagen en formato JPG
        imagen.save(ruta, format="PNG")
        print("Imagen guardada en:", ruta)
        rutaCorregida = os.path.normpath(ruta)
        print("Imagen guardada en carpeta:", rutaCorregida)
        subprocess.Popen(f'explorer /select,"{rutaCorregida}"')


menu_bar = Menu(window)
menu_bar.add_command(label="Save Image 💾", command=guardarImagen)
window.config(menu=menu_bar)

canvasContenido = Canvas(window, width=700, height=700)
canvasContenido.pack()

canvasContenido.create_image(0, 0, anchor=NW, image=imagen_tk)
canvasContenido.place(x=270, y=10)

#triangulo = Triangulo(100, 100, 50, (240,0,240), (31,31,31), 1, "Continuous")
#triangulo.dibujar(imagen)

imagen_tk.paste(imagen)
canvas.update()

window.mainloop()