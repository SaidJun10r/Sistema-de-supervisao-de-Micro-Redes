import modelos
import customtkinter
from customtkinter import filedialog
from tkinter import * 
from matplotlib import pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import pandas as pd
from PIL import Image

def leitorcsv():
    file_path = filedialog.askopenfilename()
    bd = pd.read_csv(file_path) # Dados da rede
    horas = bd['Horas']
    carga = bd['Carga']
    gerSolar = bd['GerSolar']
    cargaVE = bd['CargaVE']
    previsao = bd['Previsao']

    return horas, carga, gerSolar, cargaVE, previsao

def calBatRede(leitorcsv):
    horas, carga, gerSolar, cargaVE, previsao = leitorcsv()

    numMetodo = optionmenu_1.get()

    match numMetodo:
        case "Método de controle 1":
            bateria, rede = modelos.edc1(horas, carga, gerSolar, 4000)
        case "Método de controle 2":
            bateria, rede = modelos.edc2(horas, carga, gerSolar, 4000)
        case "Método de controle 3":
            bateria, rede = modelos.edc3(horas, carga, gerSolar, cargaVE, previsao, 4000) 
        case "Método de controle 4":
            bateria, rede = modelos.edc4(horas, carga, gerSolar, cargaVE, previsao, 4000)
        case "Método de controle 5":     
            bateria, rede = modelos.edc5(horas, carga, gerSolar, cargaVE, previsao, 4000)

    return horas, carga, gerSolar, cargaVE, previsao, bateria, rede

def plot(): 

    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = calBatRede(leitorcsv)

    # the figure that will contain the plot 
    fig = Figure(figsize = (2, 2), 
                 dpi = 100) 
    
    grafControle = fig.add_subplot(111)
    grafControle.plot([i for i in range(len(horas))], carga)
    
    grafControle.plot([i + 0.2 for i in range(len(horas))], gerSolar, color = 'limegreen')
    grafControle.plot([i + 0.4 for i in range(len(horas))], rede, color = 'gold')
    grafControle.plot([i + 0.6 for i in range(len(horas))], bateria, color = 'red')

    # Verifica se tem carga de VE
    if optionmenu_1.get() == "Método de controle 3" or optionmenu_1.get() == "Método de controle 4" or optionmenu_1.get() == "Método de controle 5":
        grafControle.plot([i + 0.8 for i in range(len(horas))], cargaVE, color = 'lightblue')

    grafControle.bar([i for i in range(len(horas))], carga, label='Carga expandida',width=0.2)
    grafControle.bar([i + 0.2 for i in range(len(horas))], gerSolar, label='Geração expandida', color='limegreen',width=0.2)
    grafControle.bar([i + 0.4 for i in range(len(horas))], rede, label='Rede', color='gold',width=0.2)
    grafControle.bar([i + 0.6 for i in range(len(horas))], bateria, label='Bateria', color='red',width=0.2)

    # Verifica se tem carga de VE
    if optionmenu_1.get() == "Método de controle 3" or optionmenu_1.get() == "Método de controle 4" or optionmenu_1.get() == "Método de controle 5":
        grafControle.bar([i + 0.8 for i in range(len(horas))], cargaVE, label='Carga do VE',color = 'lightblue', width=0.2)
  
    grafControle.set_xlabel('Horas')
    grafControle.set_ylabel("Energia")
    grafControle.axhline(0, color='black', linestyle='-')
    grafControle.set_title("Gráfico da Micro Rede")
    grafControle.grid(color="grey", linestyle="-", linewidth=0.001)
    grafControle.legend()

    # Dados dinamicos mostrados
    dadosMR = calBatRede(leitorcsv)
    dadosDinamicos(dadosMR)
    mediaDados(dadosMR)


    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, master = app)   
    canvas.draw() 
  
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().grid(row=0, rowspan=3, column=1, columnspan=2, padx=(30, 30), pady=(30, 20), sticky="news") 

def dadosDinamicos(dadosMR):
    # Potência Máxima
    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = dadosMR
    somCarga, somgerSolar, somBateria, somRede = 0, 0, 0, 0
    for i in range(len(horas)):
        somCarga += carga[i]
        somgerSolar += gerSolar[i]
        somBateria += bateria[i]
        somRede += rede[i]
    somaMR = f"Soma Carga: {somCarga}\nSoma Geração Solar: {somgerSolar}\nSoma Bateria: {somBateria}\nSoma Rede: {somRede}"
    label = customtkinter.CTkLabel(master=frame_dados,
                                text=f"{somaMR}",
                                font= ('Roboto', 20, 'bold'),
                                width=200,
                                height=25,
                                corner_radius=8)
    label.grid(row=0, column=0, padx=20, pady=10, sticky="news")

def mediaDados(dadosMR):
    # Potência Máxima
    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = dadosMR
    medCarga, medgerSolar, medBateria, medRede = 1, 1, 1, 1
    for i in range(len(horas)):
        medCarga += carga[i]/medCarga
        medgerSolar += gerSolar[i]/medgerSolar
        medBateria += bateria[i]/medBateria
        medRede += rede[i]/medRede
    somaMR = f"Média Carga: {medCarga}\nMédia Geração Solar: {medgerSolar}\nMédia Bateria: {medBateria}\nMédia Rede: {medRede}"
    label = customtkinter.CTkLabel(master=frame_dados,
                                text=f"{somaMR}",
                                font= ('Roboto', 20, 'bold'),
                                width=200,
                                height=25,
                                corner_radius=8)
    label.grid(row = 0, column=1, padx=20, pady=10, sticky="news")



# Dados Estaticos
somaMR = 0

# Customizar TKinter
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
# Fonte do programa
fonte_escrita = 'Roboto', 12, 'bold'

# Cria a janela e os parametros
app = customtkinter.CTk()  # create CTk window like you do with the Tk window
# app.attributes("-fullscreen", True)
app.geometry("1070x670")
app.iconbitmap('images/Dístico.png')
app.title("TCC II")

app.grid_columnconfigure((0, 1), weight=1)
app.grid_columnconfigure((2), weight=1)
app.grid_rowconfigure((0, 1, 2, 3), weight=1)


# Frames
frame_botoes = customtkinter.CTkFrame(app)
frame_botoes.grid(row=0, column=0, rowspan=3, padx=(20, 20), pady=(20, 10), sticky="nsew")
frame_graf = customtkinter.CTkFrame(app)
frame_graf.grid(row=0, rowspan=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="news")
frame_dados = customtkinter.CTkFrame(app)
frame_dados.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="news")
frame_dados.grid_columnconfigure((0, 1), weight=1)
frame_dados.grid_rowconfigure(0, weight=1)
frame_logo = customtkinter.CTkFrame(app)
frame_logo.grid(row=3, column=0, padx=(20, 20), pady=(20, 10), sticky="news")

# Logo UFSM
logo_ufsm = customtkinter.CTkImage(light_image=Image.open('images/Dístico.png'), dark_image=Image.open('images/Dístico.png'), size=(200, 200))
ufsm_label = customtkinter.CTkLabel(app, text='', image=logo_ufsm, bg_color='transparent')
ufsm_label.grid(row=3, column=0, pady=10)

# Botão
button2 = customtkinter.CTkButton(master=app, 
                                  text="Selecionar CSV", 
                                  font=fonte_escrita,
                                  command= leitorcsv)
button2.grid(row=0, column=0)


optionmenu_1 = customtkinter.CTkOptionMenu(app, 
                                           dynamic_resizing=True, 
                                           font=fonte_escrita,
                                           values=["Método de controle 1", 
                                                   "Método de controle 2",
                                                   "Método de controle 3",
                                                   "Método de controle 4",
                                                   "Método de controle 5"])
optionmenu_1.grid(row=1, column=0)



button2 = customtkinter.CTkButton(master=app, 
                                  text="Plotar Gráfico", 
                                  font=fonte_escrita,
                                  command=plot)
button2.grid(row=2, column=0)

app.mainloop()