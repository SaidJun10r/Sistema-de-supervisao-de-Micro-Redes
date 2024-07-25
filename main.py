import modelos
import customtkinter
from customtkinter import filedialog
from tkinter import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import pandas as pd
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import time

def leitorcsv():
    # Janela de busca de arquivos pelo Usúario
    file_path = filedialog.askopenfilename()

    # Abrindo o arquivo em modo de escrita ('w' para write)
    with open("inputs/in.txt", 'w') as caminho:
        # Escrevendo cada linha dos dados no arquivo
        caminho.write(file_path)  # Adiciona uma quebra de linha ao final de cada linha

def calBatRede():
    # Abrindo o arquivo em modo de leitura ('r' para read)
    with open("inputs/in.txt", 'r') as caminho:
        # Lendo todas as linhas do arquivo e armazenando em uma lista
        file_path = caminho.readlines()
    
    # Leitura do banco de dados
    bd = pd.read_csv(file_path[0]) # Dados da rede
    horas = bd['Horas']
    carga = bd['Carga']
    gerSolar =  bd['GerSolar']
    cargaVE = bd['CargaVE']
    previsao = bd['Previsao']

    numMetodo = optionmenu_1.get()

#################################################

    # MÁXIMO DA BATERIA
    maxBateria = 4000

#################################################

    match numMetodo:
        case "Método de controle 1":
            bateria, rede = modelos.edc1(horas, carga, gerSolar, maxBateria)
        case "Método de controle 2":
            bateria, rede = modelos.edc2(horas, carga, gerSolar, maxBateria)
        case "Método de controle 3":
            bateria, rede = modelos.edc3(horas, carga, gerSolar, cargaVE, previsao, maxBateria) 
        case "Método de controle 4":
            bateria, rede = modelos.edc4(horas, carga, gerSolar, cargaVE, previsao, maxBateria)
        case "Método de controle 5":     
            bateria, rede = modelos.edc5(horas, carga, gerSolar, cargaVE, maxBateria)

    return horas, carga, gerSolar, cargaVE, previsao, bateria, rede

def grafMicro(): 

    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = calBatRede()

    # the figure that will contain the plot 
    fig = Figure(figsize = (8, 4), 
                 dpi = 100) 
    
    grafControle = fig.add_subplot(111)
    grafControle.plot([i for i in range(len(horas))], carga)
    
    grafControle.plot([i + 0.2 for i in range(len(horas))], gerSolar, color = 'limegreen')
    grafControle.plot([i + 0.4 for i in range(len(horas))], rede, color = 'gold')
    grafControle.plot([i + 0.6 for i in range(len(horas))], bateria, color = 'red')

    # Verifica se tem carga de VE
    if optionmenu_1.get() == "Método de controle 3" or optionmenu_1.get() == "Método de controle 4" or optionmenu_1.get() == "Método de controle 5":
        grafControle.plot([i + 0.8 for i in range(len(horas))], cargaVE, color = 'lightblue')

    grafControle.bar([i for i in range(len(horas))], carga, label='Carga',width=0.2)
    grafControle.bar([i + 0.2 for i in range(len(horas))], gerSolar, label='Geração', color='limegreen',width=0.2)
    grafControle.bar([i + 0.4 for i in range(len(horas))], rede, label='Rede', color='gold',width=0.2)
    grafControle.bar([i + 0.6 for i in range(len(horas))], bateria, label='Bateria', color='red',width=0.2)

    # Verifica se tem carga de VE
    if optionmenu_1.get() == "Método de controle 3" or optionmenu_1.get() == "Método de controle 4" or optionmenu_1.get() == "Método de controle 5":
        grafControle.bar([i + 0.8 for i in range(len(horas))], cargaVE, label='Carga do VE',color = 'lightblue', width=0.2)
  
    grafControle.set_xlabel('Pontos')
    grafControle.set_ylabel("Energia")
    grafControle.axhline(0, color='black', linestyle='-')
    grafControle.set_title("Gráfico da Micro Rede")
    grafControle.grid(color="grey", linestyle="-", linewidth=0.001)
    grafControle.legend()

    # Salvando Gráfico em PNG
    fig.savefig('graficos/grafMR.png')

    # Dados dinamicos mostrados
    dadosMR = calBatRede()
    somaMR = dadosDinamicos(dadosMR)
    mediaMR = mediaDados(dadosMR)
    maxMR, minMR = maxminDados(dadosMR)
    preco_final, preco_carga, preco_max, preco_min = dadosMon(dadosMR)
    gerPDF(somaMR, mediaMR, maxMR, minMR, preco_final, preco_carga, preco_max, preco_min)


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
    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = calBatRede()

    # the figure that will contain the plot 
    fig = Figure(figsize = (8, 4), 
                 dpi = 100) 
    
    grafControle = fig.add_subplot(111)
    
    grafControle.plot([i for i in range(len(horas))], previsao, color = 'violet')
    grafControle.plot([i + 0.2 for i in range(len(horas))], gerSolar, color = 'limegreen')

    grafControle.bar([i for i in range(len(horas))], previsao, label='Previsão', color = 'violet', width=0.2)
    grafControle.bar([i + 0.2 for i in range(len(horas))], gerSolar, label='Geração', color='limegreen', width=0.2)

    grafControle.set_xlabel('Pontos')
    grafControle.set_ylabel("Energia")
    grafControle.axhline(0, color='black', linestyle='-')
    grafControle.set_title("Gráfico da Geração x Previsão")
    grafControle.grid(color="grey", linestyle="-", linewidth=0.001)
    grafControle.legend()

    # Salvando Gráfico em PNG
    fig.savefig('graficos/grafGerPrev.png')

    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, master = tabview.tab("Previsão x Geração"))   
    canvas.draw() 
  
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="news") 

def grafRedCarg():
    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = calBatRede()

    # the figure that will contain the plot 
    fig = Figure(figsize = (8, 4), 
                 dpi = 100) 
    
    grafControle = fig.add_subplot(111)
    
    grafControle.plot([i for i in range(len(horas))], carga, color = 'violet')
    grafControle.plot([i + 0.2 for i in range(len(horas))], rede, color = 'limegreen')

    grafControle.bar([i for i in range(len(horas))], carga, label='Carga', color = 'violet', width=0.2)
    grafControle.bar([i + 0.2 for i in range(len(horas))], rede, label='Rede', color='limegreen', width=0.2)

    grafControle.set_xlabel('Pontos')
    grafControle.set_ylabel("Energia")
    grafControle.axhline(0, color='black', linestyle='-')
    grafControle.set_title("Gráfico da Rede x Carga")
    grafControle.grid(color="grey", linestyle="-", linewidth=0.001)
    grafControle.legend()

    # Salvando Gráfico em PNG
    fig.savefig('graficos/grafRedCarg.png')

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
    # Listas das somas de MR
    somaMR = [somCarga, somgerSolar, somBateria, somRede]
    
    ssomaMR = f"Soma Carga: {somCarga:.2f} W\nSoma Geração Solar: {somgerSolar:.2f} W\nSoma Bateria: {somBateria:.2f} W\nSoma Rede: {somRede:.2f} W"
    
    label = customtkinter.CTkLabel(master = tabviewinfo.tab("Total - Média"),
                                text=f'{ssomaMR}',
                                font= ('Roboto', 20, 'bold'),
                                width=150,
                                height=25,
                                corner_radius=2)
    label.grid(row=0, column=0, padx=(60, 20), pady=10, sticky="nws")

    return somaMR

def mediaDados(dadosMR):
    # Potência Máxima
    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = dadosMR
    medCarga, medgerSolar, medBateria, medRede = 1, 1, 1, 1
    for i in range(len(horas)):
        medCarga += carga[i]/medCarga
        medgerSolar += gerSolar[i]/medgerSolar
        medBateria += bateria[i]/medBateria
        medRede += rede[i]/medRede
    # Lista com todas as médias
    mediaMR = [medCarga, medgerSolar, medBateria, medRede]
    
    smediaMR = f"Média Carga: {medCarga:.2f} W\nMédia Geração Solar: {medgerSolar:.2f} W\nMédia Bateria: {medBateria:.2f} W\nMédia Rede: {medRede:.2f} W"
    
    label = customtkinter.CTkLabel(master = tabviewinfo.tab("Total - Média"),
                                text=f"{smediaMR}",
                                font= ('Roboto', 20, 'bold'),
                                width=150,
                                height=25,
                                corner_radius=2)
    label.grid(row = 0, column=1, padx=(20,60), pady=10, sticky="news")

    return mediaMR

def maxminDados(dadosMR):
    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = dadosMR

    # Máximo dos dados
    maxCarga = max(carga)
    maxgerSolar = max(gerSolar)
    maxBateria = max(bateria)
    maxRede = max(rede)
    # Lista com máximos da MR
    maxMR = [maxCarga, maxgerSolar, maxBateria, maxRede]
    
    smaxMR = f"Maxima Carga: {maxCarga:.2f} W\nMaxima Geração Solar: {maxgerSolar:.2f} W\nMaxima Bateria: {maxBateria:.2f} W\nMaxima Rede: {maxRede:.2f} W"
    
    label = customtkinter.CTkLabel(master = tabviewinfo.tab("Máximos - Minímos"),
                                text=f"{smaxMR}",
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
    # Lista com minímos das MR
    minMR = [minCarga, mingerSolar, minBateria, minRede]
    
    sminMR = f"Maxima Carga: {minCarga:.2f} W\nMaxima Geração Solar: {mingerSolar:.2f} W\nMaxima Bateria: {minBateria:.2f} W\nMaxima Rede: {minRede:.2f} W"
    
    label = customtkinter.CTkLabel(master = tabviewinfo.tab("Máximos - Minímos"),
                                text=f"{sminMR}",
                                font= ('Roboto', 20, 'bold'),
                                width=200,
                                height=25,
                                corner_radius=8)
    label.grid(row = 0, column=1, padx=20, pady=10, sticky="news")

    return maxMR, minMR

def dadosMon(dadosMR):
    horas, carga, gerSolar, cargaVE, previsao, bateria, rede = dadosMR

######################## Preço da energia ###################################
    preco_energia = 0.17

    # Quanto foi pago    
    preco_final=0
    for i in range(len(rede)):
        preco_final += rede[i] * preco_energia

    # Quanto pagaria só comprando da rede
    preco_carga = 0
    for i in range(len(carga)):
        preco_carga += carga[i] * preco_energia


    preco = f"\nPreço final: R$ {preco_final:.2f}\n\nPreço com carga exclusivamente\nalimentada pela rede: R$ {preco_carga:.2f}"

    # Quanto foi pago no horario de máxima compra
    preco_max = max(rede) * preco_energia

    # Quanto foi pago o horário de minima compra
    preco_min = min(rede) * preco_energia

    precominmax = f"\nPreço no horário de\nmaior consumo: R$ {preco_max:.2f}\n\nPreço do horário de\nmenor consumo: R$ {preco_min:.2f}"

    # Preço da rede inteira
    label = customtkinter.CTkLabel(master = tabviewinfo.tab("Monetário"),
                                text=f"{preco}",
                                font= ('Roboto', 20, 'bold'),
                                width=200,
                                height=25,
                                corner_radius=8)
    label.grid(row=0, column=0, padx=20, pady=10, sticky="news")

    # Preço 
    label = customtkinter.CTkLabel(master = tabviewinfo.tab("Monetário"),
                                text=f"{precominmax}",
                                font= ('Roboto', 20, 'bold'),
                                width=200,
                                height=25,
                                corner_radius=8)
    label.grid(row = 0, column=1, padx=20, pady=10, sticky="news")

    return preco_final, preco_carga, preco_max, preco_min

def saidaControle():
    # Janela de busca de arquivos pelo Usúario
    file_path = filedialog.askdirectory()

    # Abrindo o arquivo em modo de escrita ('w' para write)
    with open("inputs/out.txt", 'w') as caminho:
        # Escrevendo cada linha dos dados no arquivo
        caminho.write(file_path)  # Adiciona uma quebra de linha ao final de cada linha

def gerPDF(somaMR, mediaMR, maxMR, minMR, preco_final, preco_carga, preco_max, preco_min):
    # Criando PDF
    cnv = canvas.Canvas("outputs/relatorio_MR.pdf", pagesize=A4)

    # Inserindo a fonte no pdf
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

######################################Página 1#######################################  
    # Fonte do Título
    cnv.setFont('Arial', 18)
    
    # Título do documento
    cnv.drawString(100, 800, "Relátorio da analíse dos dados da Micro Rede")

    # Inserir imagem do modelo da Micro Rede

    # Mudança de fonte
    cnv.setFont('Arial', 12)

############################### Dados do Usuário ####################################

    cnv.drawString(30, 770, "Usuário: Said Ernandes de Moura Júnior")

    cnv.drawString(30, 750, "Objetivo da simulação: Minimo uso da rede centralizada")

    cnv.drawString(30, 730, "Máximo da Bateria: 4000")

#####################################################################################

    # Desenho da microrrede
    cnv.drawImage("images/Microrrede.png", 380, 720, width=100, height=70)

    # Desenhando a soma PDF
    margem = 30
    cnv.drawString(margem, 700, "Soma das medições dos pontos")
    eixo = 685
    x = 0
    for i in somaMR:
        match x:
            case 0:
                cnv.drawString(margem, eixo, f"Carga: {i:.2f} W")
            case 1:
                cnv.drawString(margem, eixo, f"Geração Solar: {i:.2f} W")
            case 2:
                cnv.drawString(margem, eixo, f"Rede: {i:.2f} W")
            case 3:
                cnv.drawString(margem, eixo, f"Bateria: {i:.2f} W")
        eixo -= 15
        x += 1

    # Desenhando a max PDF
    margem = 30
    cnv.drawString(margem, 600, "Valor máximo das medições dos pontos")
    eixo = 585
    x = 0
    for i in maxMR:
        match x:
            case 0:
                cnv.drawString(margem, eixo, f"Carga: {i:.2f} W")
            case 1:
                cnv.drawString(margem, eixo, f"Geração Solar: {i:.2f} W")
            case 2:
                cnv.drawString(margem, eixo, f"Rede: {i:.2f} W")
            case 3:
                cnv.drawString(margem, eixo, f"Bateria: {i:.2f} W")
        eixo -= 15
        x += 1

    # Desenhando média microrrede
    margem = 260
    cnv.drawString(margem, 700, "Médias das medições dos pontos")
    eixo = 685
    x = 0
    for i in mediaMR:
        match x:
            case 0:
                cnv.drawString(margem, eixo, f"Carga: {i:.2f} W")
            case 1:
                cnv.drawString(margem, eixo, f"Geração Solar: {i:.2f} W")
            case 2:
                cnv.drawString(margem, eixo, f"Rede: {i:.2f} W")
            case 3:
                cnv.drawString(margem, eixo, f"Bateria: {i:.2f} W")
        eixo -= 15
        x += 1

    # Desenhando a min PDF
    margem = 260
    cnv.drawString(margem, 600, "Valor mínimo das medições dos pontos")
    eixo = 585
    x = 0
    for i in minMR:
        match x:
            case 0:
                cnv.drawString(margem, eixo, f"Carga: {i:.2f} W")
            case 1:
                cnv.drawString(margem, eixo, f"Geração Solar: {i:.2f} W")
            case 2:
                cnv.drawString(margem, eixo, f"Rede: {i:.2f} W")
            case 3:
                cnv.drawString(margem, eixo, f"Bateria: {i:.2f} W")
        eixo -= 15
        x += 1

    # Desenhando preço total da micro
    cnv.drawString(30, 510, "Preço final:")
    cnv.drawString(350, 510, f"R$ {preco_final:.2f}")

    # Desenhando preço compra exclusiva microrrede
    cnv.drawString(30, 490, "Preço com carga exclusivamente alimentada pela rede:")
    cnv.drawString(350, 490, f"R$ {preco_carga:.2f}")

    # Desenhando preço total da micro
    cnv.drawString(30, 470, "Preço no horário de maior consumo:")
    cnv.drawString(350, 470, f"R$ {preco_max:.2f}")

    # Desenhando preço total da micro
    cnv.drawString(30, 450, "Preço do horário de menor consumo:")
    cnv.drawString(350, 450, f"R$ {preco_min:.2f}")

    # Escolhendo o fluxograma do método de controle escolhido
    numMetodo = optionmenu_1.get()
    match numMetodo:
        case "Método de controle 1":
            cnv.drawImage("fluxogramas/flu1.png", 150, 75, width=300, height=330)
        case "Método de controle 2":
            cnv.drawImage("fluxogramas/flu2.png", 150, 75, width=300, height=330)
        case "Método de controle 3":
            cnv.drawImage("fluxogramas/flu3.png", 125, 75, width=350, height=330)
        case "Método de controle 4":
            cnv.drawImage("fluxogramas/flu4.png", 150, 75, width=300, height=330)
        case "Método de controle 5":     
            cnv.drawImage("fluxogramas/flu5.png", 125, 75, width=375, height=330)

    # Rodapé
    cnv.drawString(10, 25, "Controle, Supervisão e Automação de Microredes")
    cnv.drawString(10, 10, "Said Ernandes de Moura Júnior")

######################################Página 2#######################################  

    # Cria nova página PDF
    cnv.showPage()

    # Gráfico MR
    cnv.drawImage("graficos/grafMR.png", 30, 555, width=550, height=250)

    # Gráfico Geração x Previsão
    cnv.drawImage("graficos/grafGerPrev.png", 30, 305, width=550, height=250)

    # Gráfico Rede x Carga
    cnv.drawImage("graficos/grafRedCarg.png", 30, 55, width=550, height=250)

    # Roda pé
    cnv.drawString(10, 25, "Controle, Supervisão e Automação de Microredes")
    cnv.drawString(10, 10, "Said Ernandes de Moura Júnior")

    cnv.save()

def funcaoLoop():
    
    # Escolhe por quanto tempo o loop rodara
    tempLoop = optionmenu_2.get()
    match tempLoop:
        case "30 minutos":
            tempo_total = 1800
        case "1 hora":
            tempo_total = 3600
        case "4 horas":
            tempo_total = 14400
        case "8 horas":
            tempo_total = 28800
        case "12 horas":     
            tempo_total = 43200
        case "24 horas":     
            tempo_total = 86400

    # Escolhe o tempo de intervalo do loop
    tempIntervalo = optionmenu_3.get()
    match tempIntervalo:
        case "5 segundos":
            intervalo = 5
        case "15 segundos":
            intervalo = 15
        case "30 segundos":
            intervalo = 30
        case "1 minuto":
            intervalo = 60
        case "5 minutos":     
            intervalo = 300
        case "15 minutos":     
            intervalo = 900

    inicio = time.time() # Inicia o timer
    app.attributes("-fullscreen", "True") # Coloca o modo supervisorio em tela cheia

    # Loop do modo de supervisão
    while time.time() - inicio < tempo_total:
        grafMicro()
        app.update()
        time.sleep(intervalo)
        app.update()
    
    app.attributes("-fullscreen", "False") # Tira do modo tela cheia após o loop

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
app.geometry("1350x940")
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
tabview.tab("Rede x Carga").grid_rowconfigure(0, weight=1)

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
    label = customtkinter.CTkLabel(master=app,
                                text=f" TCC II\nSaid Ernandes de Moura Junior",
                                font= ('Roboto', 14, 'bold'),
                                bg_color='#e5e5e5')
    label.grid(row=3, column=0, pady=(10, 20), sticky="s")
except:
    print('Não carregou')

# Botões da interface
padx = (60, 20) # Tamanho botões

# Botão
button2 = customtkinter.CTkButton(master=frame_botoes, 
                                  text="Selecionar CSV", 
                                  font=fonte_escrita,
                                  command= leitorcsv)
button2.grid(row=0, column=0, padx=padx, pady=20, sticky="nsew")

# Tipo de controle aplicado na microrede
optionmenu_1 = customtkinter.CTkOptionMenu(master=frame_botoes, 
                                           dynamic_resizing=True, 
                                           font=fonte_escrita,
                                           values=["Método de controle 1", 
                                                   "Método de controle 2",
                                                   "Método de controle 3",
                                                   "Método de controle 4",
                                                   "Método de controle 5"])
optionmenu_1.grid(row=1, column=0, padx=padx, pady=20, sticky="nsew")

# Botão para plotar o gráfico
button2 = customtkinter.CTkButton(master=frame_botoes, 
                                  text="Plotar Gráfico", 
                                  font=fonte_escrita,
                                  command=grafMicro)
button2.grid(row=2, column=0, padx=padx, pady=20, sticky="news")

# Local de saída
button3 = customtkinter.CTkButton(master=frame_botoes, 
                                  text="Saída do controle", 
                                  font=fonte_escrita,
                                  command=saidaControle)
button3.grid(row=3, column=0, padx=padx, pady=20, sticky="news")

# Gerar PDF
button4 = customtkinter.CTkButton(master=frame_botoes, 
                                  text="Gerar relatório", 
                                  font=fonte_escrita,
                                  command=gerPDF)
button4.grid(row=4, column=0, padx=padx, pady=(20, 20), sticky="nsew")

# Titulo botões
label = customtkinter.CTkLabel(master=frame_botoes,
                                text=f"Tempo de supervisão:",
                                font= ('Roboto', 14, 'bold'))
label.grid(row=5, column=0, padx=padx, pady=(0, 0), sticky="nsew")

# Tempo do Loop
optionmenu_2 = customtkinter.CTkOptionMenu(master=frame_botoes, 
                                           dynamic_resizing=True, 
                                           font=fonte_escrita,
                                           values=["30 minutos", 
                                                   "1 hora",
                                                   "4 horas",
                                                   "8 horas",
                                                   "12 horas",
                                                   "24 horas"])
optionmenu_2.grid(row=6, column=0, padx=padx, pady=(5, 20), sticky="nsew")

label = customtkinter.CTkLabel(master=frame_botoes,
                                text=f"Intervalo de atualização:",
                                font= ('Roboto', 14, 'bold'))
label.grid(row=7, column=0, padx=padx, pady=(0, 0), sticky="nsew")

# Intervalo do loop do Loop
optionmenu_3 = customtkinter.CTkOptionMenu(master=frame_botoes, 
                                           dynamic_resizing=True, 
                                           font=fonte_escrita,
                                           values=["5 segundos", 
                                                   "15 segundos",
                                                   "30 segundos",
                                                   "1 minuto",
                                                   "5 minutos",
                                                   "15 minutos"])
optionmenu_3.grid(row=8, column=0, padx=padx, pady=(5, 20), sticky="nsew")

# Loop
button4 = customtkinter.CTkButton(master=frame_botoes, 
                                  text="Iniciar modo de supervisão", 
                                  font=fonte_escrita,
                                  command=funcaoLoop)
button4.grid(row=9, column=0, padx=padx, pady=20, sticky="nsew")

try:
    app.iconbitmap('images/ufsm.ico')
except:
    print('ícone não carregado')

app.mainloop()