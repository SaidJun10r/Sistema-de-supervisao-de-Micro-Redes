from leitor import leitorcsv
import modelos
from grafico import grafico
import customtkinter

dados = 'Dados.csv'

horas, carga, gerSolar, cargaVE, previsao = leitorcsv(dados)
bateria, rede = modelos.edc2(horas, carga, gerSolar, 4000)
print(bateria, rede)
#grafico(horas, carga, gerSolar, cargaVE==None, bateria, rede)

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")

def button_function():
    grafico(horas, carga, gerSolar, cargaVE==None, bateria, rede)

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, text="Estudo de Caso 2", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

app.mainloop()