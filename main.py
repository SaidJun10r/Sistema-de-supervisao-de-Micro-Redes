from leitor import leitorcsv
import modelos
from grafico import grafico
import tkinter, customtkinter

dados = 'Dados.csv'

horas, carga, gerSolar, cargaVE, previsao = leitorcsv(dados)
bateria, rede = modelos.edc2(horas, carga, gerSolar, 4000)
print(bateria, rede)
#grafico(horas, carga, gerSolar, cargaVE==None, bateria, rede)

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")
app.title("TCC II")

app.grid_columnconfigure((0), weight=1)
app.grid_columnconfigure((1), weight=4)
app.grid_rowconfigure((0), weight=4)
app.grid_rowconfigure((1), weight=1)


def button_function():
    grafico(horas, carga, gerSolar, cargaVE==None, bateria, rede)

# Botão
button = customtkinter.CTkButton(master=app, text="Estudo de Caso 2", command=button_function)
button.grid(row=0, column=1, padx=20, pady=10, sticky="news")

# Botão
button2 = customtkinter.CTkButton(master=app, text="Estudo de Caso 2", command=button_function)
button2.grid(row=0, column=0, padx=20, pady=10, sticky="news")

# Botão
button3 = customtkinter.CTkButton(master=app, text="Estudo de Caso 2", command=button_function)
button3.grid(row=1, column=1, padx=20, pady=10, sticky="news")

# Botão
button4 = customtkinter.CTkButton(master=app, text="Estudo de Caso 2", command=button_function)
button4.grid(row=1, column=0, padx=20, pady=10, sticky="news")

app.mainloop()