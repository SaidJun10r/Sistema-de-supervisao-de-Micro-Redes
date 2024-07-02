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

def grafMicro(): 

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
    maxminDados(dadosMR)
    dadosMon(dadosMR)

    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, master = tabview.tab("Gráfico da Micro Rede"))   
    canvas.draw() 

    #PUXANDO GERXPREV
    grafGerPrev()
    grafRedCarg()
  
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="news") 

def grafGerPrev():
    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = calBatRede(leitorcsv)

    # the figure that will contain the plot 
    fig = Figure(figsize = (2, 2), 
                 dpi = 100) 
    
    grafControle = fig.add_subplot(111)
    
    grafControle.plot([i for i in range(len(horas))], previsao, color = 'violet')
    grafControle.plot([i + 0.2 for i in range(len(horas))], gerSolar, color = 'limegreen')

    grafControle.bar([i for i in range(len(horas))], previsao, label='Previsão', color = 'violet', width=0.2)
    grafControle.bar([i + 0.2 for i in range(len(horas))], gerSolar, label='Geração', color='limegreen', width=0.2)

    grafControle.set_xlabel('Horas')
    grafControle.set_ylabel("Energia")
    grafControle.axhline(0, color='black', linestyle='-')
    grafControle.set_title("Geração x Previsão")
    grafControle.grid(color="grey", linestyle="-", linewidth=0.001)
    grafControle.legend()

    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, master = tabview.tab("Previsão x Geração"))   
    canvas.draw() 
  
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="news") 

def grafRedCarg():
    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = calBatRede(leitorcsv)

    # the figure that will contain the plot 
    fig = Figure(figsize = (2, 2), 
                 dpi = 100) 
    
    grafControle = fig.add_subplot(111)
    
    grafControle.plot([i for i in range(len(horas))], carga, color = 'violet')
    grafControle.plot([i + 0.2 for i in range(len(horas))], rede, color = 'limegreen')

    grafControle.bar([i for i in range(len(horas))], carga, label='Previsão', color = 'violet', width=0.2)
    grafControle.bar([i + 0.2 for i in range(len(horas))], rede, label='Geração', color='limegreen', width=0.2)

    grafControle.set_xlabel('Horas')
    grafControle.set_ylabel("Energia")
    grafControle.axhline(0, color='black', linestyle='-')
    grafControle.set_title("Geração x Previsão")
    grafControle.grid(color="grey", linestyle="-", linewidth=0.001)
    grafControle.legend()

    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, master = tabview.tab("Rede x Carga"))   
    canvas.draw() 
  
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="news") 

def dadosDinamicos(dadosMR):
    # Potência Máxima
    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = dadosMR
    somCarga, somgerSolar, somBateria, somRede = 0, 0, 0, 0
    for i in range(len(horas)):
        somCarga += carga[i]
        somgerSolar += gerSolar[i]
        somBateria += bateria[i]
        somRede += rede[i]
    somaMR = f"Soma Carga: {somCarga:.2f}\nSoma Geração Solar: {somgerSolar:.2f}\nSoma Bateria: {somBateria:.2f}\nSoma Rede: {somRede:.2f}"
    label = customtkinter.CTkLabel(master = tabviewinfo.tab("Total - Média"),
                                text=f'{somaMR}',
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
    somaMR = f"Média Carga: {medCarga:.2f}\nMédia Geração Solar: {medgerSolar:.2f}\nMédia Bateria: {medBateria:.2f}\nMédia Rede: {medRede:.2f}"
    label = customtkinter.CTkLabel(master = tabviewinfo.tab("Total - Média"),
                                text=f"{somaMR}",
                                font= ('Roboto', 20, 'bold'),
                                width=200,
                                height=25,
                                corner_radius=8)
    label.grid(row = 0, column=1, padx=20, pady=10, sticky="news")

def maxminDados(dadosMR):
    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = dadosMR

    # Máximo dos dados
    maxCarga = max(carga)
    maxgerSolar = max(gerSolar)
    maxBateria = max(bateria)
    maxRede = max(rede)
    maxMR = f"Maxima Carga: {maxCarga:.2f}\nMaxima Geração Solar: {maxgerSolar:.2f}\nMaxima Bateria: {maxBateria:.2f}\nMaxima Rede: {maxRede:.2f}"
    label = customtkinter.CTkLabel(master = tabviewinfo.tab("Máximos - Minímos"),
                                text=f"{maxMR}",
                                font= ('Roboto', 20, 'bold'),
                                width=200,
                                height=25,
                                corner_radius=8)
    label.grid(row=0, column=0, padx=20, pady=10, sticky="news")

    # Minimo dos dados
    minCarga = min(carga)
    mingerSolar = min(gerSolar)
    minBateria = min(bateria)
    minRede = min(rede)
    minMR = f"Maxima Carga: {minCarga:.2f}\nMaxima Geração Solar: {mingerSolar:.2f}\nMaxima Bateria: {minBateria:.2f}\nMaxima Rede: {minRede:.2f}"
    label = customtkinter.CTkLabel(master = tabviewinfo.tab("Máximos - Minímos"),
                                text=f"{minMR}",
                                font= ('Roboto', 20, 'bold'),
                                width=200,
                                height=25,
                                corner_radius=8)
    label.grid(row = 0, column=1, padx=20, pady=10, sticky="news")

def dadosMon(dadosMR):
    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = dadosMR

    # Placeholder um
    label = customtkinter.CTkLabel(master = tabviewinfo.tab("Monetário"),
                                text="Placeholder",
                                font= ('Roboto', 20, 'bold'),
                                width=200,
                                height=25,
                                corner_radius=8)
    label.grid(row=0, column=0, padx=20, pady=10, sticky="news")

    # Placeholder dois
    label = customtkinter.CTkLabel(master = tabviewinfo.tab("Monetário"),
                                text="Placeholder2",
                                font= ('Roboto', 20, 'bold'),
                                width=200,
                                height=25,
                                corner_radius=8)
    label.grid(row = 0, column=1, padx=20, pady=10, sticky="news")

def saidaControle():
    pass

def gerPDF():
    pass

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
app.geometry("1250x860")
app.title("TCC II")


app.grid_columnconfigure((0, 1), weight=1)
app.grid_columnconfigure((2), weight=10)
app.grid_rowconfigure((0, 1, 2, 3), weight=1)


# Frames
frame_botoes = customtkinter.CTkFrame(app)
frame_botoes.grid(row=0, column=0, rowspan=3, padx=(20, 20), pady=(20, 10), sticky="nsew")
frame_graf = customtkinter.CTkFrame(app)
frame_graf.grid(row=0, rowspan=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="news")
frame_graf.grid_columnconfigure((0), weight=1)
frame_graf.grid_rowconfigure((0), weight=1)
frame_dados = customtkinter.CTkFrame(app)
frame_dados.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="news")
frame_dados.grid_columnconfigure((0, 1), weight=1)
frame_dados.grid_rowconfigure(0, weight=1)
frame_logo = customtkinter.CTkFrame(app)
frame_logo.grid(row=3, column=0, padx=(20, 20), pady=(20, 10), sticky="news")

# Tab View do Gráfico
tabview = customtkinter.CTkTabview(frame_graf, width=250)
tabview.grid(row=0, column=0, padx=(20, 20), pady=(0, 20), sticky="nsew")
tabview.add("Gráfico da Micro Rede")
tabview.add("Previsão x Geração")
tabview.add("Rede x Carga")
tabview.tab("Gráfico da Micro Rede").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
tabview.tab("Gráfico da Micro Rede").grid_rowconfigure(0, weight=1)
tabview.tab("Previsão x Geração").grid_columnconfigure(0, weight=1)
tabview.tab("Previsão x Geração").grid_rowconfigure(0, weight=1)
tabview.tab("Rede x Carga").grid_columnconfigure(0, weight=1)

# Tab View das informações
tabviewinfo = customtkinter.CTkTabview(frame_dados, width=250)
tabviewinfo.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(0, 20), sticky="nsew")
tabviewinfo.add("Total - Média")
tabviewinfo.add("Máximos - Minímos")
tabviewinfo.add("Monetário")
tabviewinfo.tab("Total - Média").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
tabviewinfo.tab("Total - Média").grid_rowconfigure(0, weight=1)
tabviewinfo.tab("Máximos - Minímos").grid_columnconfigure(0, weight=1)
tabviewinfo.tab("Máximos - Minímos").grid_rowconfigure(0, weight=1)
tabviewinfo.tab("Monetário").grid_columnconfigure(0, weight=1)

# Logo UFSM
try:
    logo_ufsm = customtkinter.CTkImage(light_image=Image.open('images/Dístico.png'), dark_image=Image.open('images/Dístico.png'), size=(200, 200))
    ufsm_label = customtkinter.CTkLabel(app, text='', image=logo_ufsm, bg_color='#e5e5e5')
    ufsm_label.grid(row=3, column=0, pady=10)
except:
    print('Não carregou')

# Botão
button2 = customtkinter.CTkButton(master=frame_botoes, 
                                  text="Selecionar CSV", 
                                  font=fonte_escrita,
                                  command= leitorcsv)
button2.grid(row=0, column=0, padx=(60, 20), pady=20, sticky="nsew")

# Tipo de controle aplicado na microrede
optionmenu_1 = customtkinter.CTkOptionMenu(master=frame_botoes, 
                                           dynamic_resizing=True, 
                                           font=fonte_escrita,
                                           values=["Método de controle 1", 
                                                   "Método de controle 2",
                                                   "Método de controle 3",
                                                   "Método de controle 4",
                                                   "Método de controle 5"])
optionmenu_1.grid(row=1, column=0, padx=(60, 20), pady=20, sticky="nsew")

# Botão para plotar o gráfico
button2 = customtkinter.CTkButton(master=frame_botoes, 
                                  text="Plotar Gráfico", 
                                  font=fonte_escrita,
                                  command=grafMicro)
button2.grid(row=2, column=0, padx=(60, 20), pady=20, sticky="nsew")

# Local de saída
button3 = customtkinter.CTkButton(master=frame_botoes, 
                                  text="Saída do controle", 
                                  font=fonte_escrita,
                                  command=saidaControle)
button3.grid(row=3, column=0, padx=(60, 20), pady=20, sticky="nsew")

# Gerar PDF
button4 = customtkinter.CTkButton(master=frame_botoes, 
                                  text="Gerar relatório", 
                                  font=fonte_escrita,
                                  command=gerPDF)
button4.grid(row=4, column=0, padx=(60, 20), pady=20, sticky="nsew")

try:
    app.iconbitmap('images/ufsm.ico')
except:
    print('ícone não carregado')


app.mainloop()