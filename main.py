from leitor import leitorcsv
import modelos
from grafico import grafico
import customtkinter
from customtkinter import filedialog

def button_function(dados_csv, bateria, rede):
    horas, carga, gerSolar, cargaVE, previsao = dados_csv
    calculo(dados_csv)
    grafico(horas, carga, gerSolar, cargaVE==None, bateria, rede)

def file_path():
    file_path = filedialog.askopenfilename()
    return file_path

def dados_csv():
    dados_csv = leitorcsv(file_path())
    return dados_csv

def calculo(dados_csv):
    horas, carga, gerSolar, cargaVE, previsao = dados_csv
    bateria, rede = modelos.edc2(horas, carga, gerSolar, 4000)
    print(bateria, rede)
#grafico(horas, carga, gerSolar, cargaVE==None, bateria, rede)

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("540x360")
app.title("TCC II")

app.grid_columnconfigure((0), weight=1)
app.grid_columnconfigure((1), weight=4)
app.grid_rowconfigure((0), weight=4)
app.grid_rowconfigure((1), weight=1)

# Botão
button = customtkinter.CTkButton(master=app, text="Selecionar CSV", command=dados_csv)
button.grid(row=0, column=1, padx=20, pady=10, sticky="news")

# Botão
button2 = customtkinter.CTkButton(master=app, text="Selecionar CSV", command=dados_csv)
button2.grid(row=0, column=0, padx=20, pady=10, sticky="news")

# Botão
button3 = customtkinter.CTkButton(master=app, text="Estudo de Caso 2", command=button_function)
button3.grid(row=1, column=1, padx=20, pady=10, sticky="news")

# Botão
button4 = customtkinter.CTkButton(master=app, text="Estudo de Caso 2", command=button_function)
button4.grid(row=1, column=0, padx=20, pady=10, sticky="news")

app.mainloop()