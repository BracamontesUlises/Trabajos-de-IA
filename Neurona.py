import tkinter as tk

entradas = []

def generar_entradas():
    num_entradas = int(entrada_num_entradas.get())
    # Borra cualquier entrada de pesos anterior
    for widget in frame_entradas.winfo_children():
        widget.destroy()


    entradas.clear()

    for i in range(num_entradas):
        etiqueta_entrada = tk.Label(frame_entradas, text=f"entrada {i + 1}:")
        etiqueta_entrada.pack()
        entrada_entrada = tk.Entry(frame_entradas)
        entrada_entrada.pack()
        entradas.append(entrada_entrada)

def calcular():
    num_entradas = int(entrada_num_entradas.get())
    umbral = float(entrada_umbral.get())
    resultados = "Tabla de entradas y resultado\n"

    for entrada in entradas:
        resultados += f"X{entradas.index(entrada) + 1}\t"
    resultados += "Y\n"

    for i in range(2 ** num_entradas):
        entradas_bin = format(i, f'0{num_entradas}b')
        entradas_vals = [int(bit) for bit in entradas_bin]
        suma = sum(entradas_vals[j] * float(entrada.get()) for j, entrada in enumerate(entradas))
        resultado = 1 if suma > umbral else 0
        fila = entradas_vals + [resultado]
        resultados += "\t".join([str(fila[j]) for j in range(num_entradas + 1)]) + "\n"

    resultado_texto.config(state='normal')
    resultado_texto.delete('1.0', tk.END)
    resultado_texto.insert('1.0', resultados)
    resultado_texto.config(state='disabled')

def limpiar_datos():
    for entrada in entradas:
        entrada.delete(0, tk.END)
    resultado_texto.config(state='normal')
    resultado_texto.delete('1.0', tk.END)
    resultado_texto.config(state='disabled')

app = tk.Tk()
app.title("Calculadora de Tabla de Entradas")
app.geometry("800x600")

frame_entradas = tk.Frame(app)
frame_entradas.pack()

etiqueta_num_entradas = tk.Label(app, text="Número de entradas:")
etiqueta_num_entradas.pack()
entrada_num_entradas = tk.Entry(app)
entrada_num_entradas.pack()

boton_generar_entradas = tk.Button(app, text="Generar Entradas", command=generar_entradas)
boton_generar_entradas.pack()

etiqueta_umbral = tk.Label(app, text="Valor umbral:")
etiqueta_umbral.pack()
entrada_umbral = tk.Entry(app)
entrada_umbral.pack()

boton_calcular = tk.Button(app, text="Calcular", command=calcular)
boton_calcular.pack()

boton_limpiar = tk.Button(app, text="Limpiar Datos", command=limpiar_datos)
boton_limpiar.pack()

resultado_texto = tk.Text(app, wrap=tk.WORD, state='disabled', height=10, width=40)
resultado_texto.pack()

app.mainloop()

# Programa Creado en Equpio por:
# Bracamontes Ordoñez Ulises
# Robert González Jesús Israel
# ESIME-ZACATENCO ICE, Especialidad computacion 