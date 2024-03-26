import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

root = tk.Tk()
root.title("Test de síntomas de COVID-19")

tab_control = ttk.Notebook(root)
tab_control.pack(fill='both', expand='yes')

tabs = []

# Calcular nivel de peligro
def calcular_peligro():
    peligro = 0
    
    edad = int(edad_entry.get())
    
    if 1 <= edad < 19:
        peligro = 0
    elif 19 <= edad <= 59:
        peligro += 1
    else:
        enfermedad = enfermedad_var.get()
        if enfermedad in [1, 2, 3, 4]:
            peligro += 2

    for respuesta in respuestas:
        peligro += respuesta.get()
    
    respuesta = int(dolor_cabeza_var.get())
    if respuesta == 1:
        peligro += 0
    elif respuesta == 2:
        peligro += 1
    elif respuesta == 3:
        peligro += 2
    
    duracion_sintomas = duracion_sintomas_var.get()
    peligro += duracion_sintomas - 1
    
    mejoria = mejoria_var.get()
    peligro += 1 if mejoria == 0 else 0
    
    for respuesta in sintomas_generales:
        peligro += respuesta.get()
    
    for respuesta in vacunas:
        peligro += respuesta.get()
    
    if peligro == 0:
        messagebox.showwarning("ADVERTENCIA", "Usten no presenta ningun sintoma aun asi cuidese y visite a su medico familiar")
    elif 8 > peligro >= 2:
        messagebox.showwarning("ADVERTENCIA", "Presenta primeros sintomas, recuera a su medico familiar y tome las precausiones necesarias")
    elif 11 > peligro >= 8:
        messagebox.showwarning("ADVERTENCIA", "Por favor, vaya al hospital. Es necesaria su atención médica.")
    elif 16 >= peligro > 8:
        messagebox.showwarning("ADVERTENCIA", "Urgentemente, vaya al hospital. Es necesaria su atención.")
        



# pestañas
def habilitar_siguiente():
    global paso_actual
    paso_actual += 1
    tab_control.select(paso_actual)  
    if paso_actual == 4: 
        siguiente_button.config(state=tk.DISABLED)
    for widget in tabs[paso_actual - 1].winfo_children():
        widget.configure(state=tk.DISABLED)
    for widget in tabs[paso_actual].winfo_children():
        widget.configure(state=tk.NORMAL)
    if paso_actual == 4:
        root.after(5000, calcular_peligro_auto)  


# Información
for i, tab_name in enumerate(["Información Personal", "Antecedentes Médicos", "Síntomas Respiratorios", "Síntomas Generales", "Historial de Vacunación"]):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text=tab_name)
    tabs.append(tab)

edad_label = tk.Label(tabs[0], text="¿Cuántos años tiene usted?")
edad_label.pack()

edad_entry = tk.Entry(tabs[0])
edad_entry.pack()

enfermedad_label = tk.Label(tabs[0], text="Seleccione su enfermedad si usted es mayor de edad (60 años):")
enfermedad_label.pack()

enfermedad_var = tk.IntVar()
enfermedad_var.set(0)

enfermedad_radios = []
for i, enfermedad_text in enumerate(["Ninguna", "Hipertensión", "Diabetes", "Presión Baja", "Problemas de Corazón"]):
    radio = tk.Radiobutton(tabs[0], text=enfermedad_text, variable=enfermedad_var, value=i)
    radio.pack()

respuestas = [tk.IntVar() for _ in range(4)]

# Preguntas de contacto humano
preguntas = [
    "¿Ha tenido contacto cercano con alguien que haya dado positivo por COVID-19 o que tenga síntomas similares?",
    "¿Ha viajado recientemente a áreas con brotes conocidos de COVID-19 o influenza?",
    "¿Ha recibido alguna vacuna contra la gripe este año?",
    "¿Toma medicamentos que puedan afectar su sistema inmunológico?"
]

for i, pregunta_text in enumerate(preguntas):
    pregunta_label = tk.Label(tabs[1], text=pregunta_text)
    pregunta_label.pack()

    radio1 = tk.Radiobutton(tabs[1], text="Sí", variable=respuestas[i], value=1)
    radio2 = tk.Radiobutton(tabs[1], text="No", variable=respuestas[i], value=0)

    radio1.pack()
    radio2.pack()

dolor_cabeza_label = tk.Label(tabs[2], text="Indique el grado del dolor de cabeza:")
dolor_cabeza_label.pack()

dolor_cabeza_var = tk.IntVar()
dolor_cabeza_var.set(1)

dolor_cabeza_radios = []

for i, dolor_text in enumerate(["Bajo", "Medio", "Alto"]):
    radio = tk.Radiobutton(tabs[2], text=dolor_text, variable=dolor_cabeza_var, value=i + 1)
    radio.pack()

duracion_sintomas_label = tk.Label(tabs[2], text="¿Cuál es la duración de los síntomas?")
duracion_sintomas_label.pack()

duracion_sintomas_var = tk.IntVar()
duracion_sintomas_var.set(1)

duracion_sintomas_radios = []

for i, duracion_text in enumerate(["Ayer", "Dos o tres días", "Cinco días"]):
    radio = tk.Radiobutton(tabs[2], text=duracion_text, variable=duracion_sintomas_var, value=i + 1)
    radio.pack()

mejoria_label = tk.Label(tabs[2], text="¿Ha visto una mejoría?")
mejoria_label.pack()

mejoria_var = tk.IntVar()
mejoria_var.set(1)

mejoria_radios = []

radio1 = tk.Radiobutton(tabs[2], text="Sí", variable=mejoria_var, value=1)
radio2 = tk.Radiobutton(tabs[2], text="No", variable=mejoria_var, value=0)

radio1.pack()
radio2.pack()

# Síntomas del cuerpo
sintomas_generales = [tk.IntVar() for _ in range(5)]

preguntas_sintomas_generales = [
    "¿Ha tenido dolores musculares o corporales?",
    "¿Ha experimentado fatiga o debilidad extrema?",
    "¿Ha tenido dolores de cabeza constantemente?",
    "¿Siente escalofríos o fiebre?",
    "¿Tiene síntomas gastrointestinal?"
]
# Síntomas del cuerpo (continuación)
preguntas_sintomas_generales = [
    "¿Ha tenido dolores musculares o corporales?",
    "¿Ha experimentado fatiga o debilidad extrema?",
    "¿Ha tenido dolor de cabeza?",
    "¿Siente escalofríos o fiebre?",
    "¿Tiene síntomas gastrointestinales como náuseas, vómitos o diarrea?"
]

for i, pregunta_text in enumerate(preguntas_sintomas_generales):
    pregunta_label = tk.Label(tabs[3], text=pregunta_text)
    pregunta_label.pack()

    radio1 = tk.Radiobutton(tabs[3], text="Sí", variable=sintomas_generales[i], value=1)
    radio2 = tk.Radiobutton(tabs[3], text="No", variable=sintomas_generales[i], value=0)
    
    radio1.pack()
    radio2.pack()

# Historial de vacunas 
vacunas = [tk.IntVar() for _ in range(2)]

preguntas_vacunas = [
    "¿Ha recibido la vacuna contra el COVID-19?",
    "¿Ha recibido la vacuna contra la gripe esta temporada?"
]

for i, pregunta_text in enumerate(preguntas_vacunas):
    pregunta_label = tk.Label(tabs[4], text=pregunta_text)
    pregunta_label.pack()

    radio1 = tk.Radiobutton(tabs[4], text="Sí", variable=vacunas[i], value=1)
    radio2 = tk.Radiobutton(tabs[4], text="No", variable=vacunas[i], value=0)
    
    radio1.pack()
    radio2.pack()


# Calcular el peligro del paciente 
def calcular_peligro_auto():
    calcular_peligro()  

# Función para reiniciar el cuestionario
def reiniciar_cuestionario():
    global paso_actual, peligro
    paso_actual = 0
    peligro = 0
    tab_control.select(paso_actual) 
    siguiente_button.config(state=tk.NORMAL) 
    
    # Restablece valores iniciales
    edad_entry.delete(0, tk.END)
    edad_entry.insert(0, "") 
    enfermedad_var.set(0)  
    for var in respuestas:
        var.set(0)  
    dolor_cabeza_var.set(1)  
    duracion_sintomas_var.set(1)  
    mejoria_var.set(1)  
    for var in sintomas_generales:
        var.set(0)  
    for var in vacunas:
        var.set(0) 

siguiente_button = tk.Button(root, text="Siguiente", command=habilitar_siguiente)
siguiente_button.pack()


reiniciar_button = tk.Button(root, text="Reiniciar Cuestionario", command=reiniciar_cuestionario)
reiniciar_button.pack()

paso_actual = 0
peligro = 0

root.mainloop()