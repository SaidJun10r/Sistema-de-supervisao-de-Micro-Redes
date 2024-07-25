from tkinter import messagebox

def gravacaoSaida(comControle):
    # Criando arquivo de controle da microrede
    try:
        with open("inputs/out.txt", 'r') as caminho:
            # Lendo todas as linhas do arquivo e armazenando em uma lista
            local_arquivo = caminho.readlines()
    except:
        messagebox.showwarning("Local da saída invalído!", "O local do documento de controle não foi selecionado ou é inválido!")
        return
    # Abrindo o arquivo em modo de escrita ('w' para write)
    with open(f"{str(local_arquivo[0])}/controleMR.txt", 'w') as controle:
        # Escrevendo cada linha dos dados no arquivo
        for j in range(len(comControle)):
            controle.write(f"[{comControle[j]}]\n")  # Adiciona uma quebra de linha ao final de cada linha

def edc1(horas, carga, gerSolar, maxBateria=4000):
    bateria = [i - i for i in horas]
    rede = [i - i for i in horas]
    comControle = []

    for i in range(len(horas)):
        eRest = carga[i] - gerSolar[i] # Energia que sobra na carga

        if bateria[i-1] == maxBateria or gerSolar[i] < carga[i]:
            if eRest > 0:
                if bateria[i-1] == 0:
                    rede[i] = -eRest
                    comControle .append(str(i) + "| carga - gersolar | carga - rede")
                else:
                    bateria[i] = bateria[i-1] - eRest
                    comControle .append(str(i) + " | carga - gersolar |  carga - bateria")
            else:
                rede[i] = -eRest
                bateria[i] = bateria[i-1]    
                comControle .append(str(i) + " | carga - gersolar | rede - gersolar")
        else:
            bateria[i] = bateria[i-1] + gerSolar[i]
            rede[i] = -carga[i]
            comControle .append(str(i) + " | carga - rede | bateria - gersolar")

        if bateria [i] > maxBateria:
            bateria[i] = maxBateria
        elif bateria[i] < 0:
            bateria[i] = 0

    gravacaoSaida(comControle)

    return bateria, rede

def edc2(horas, carga, gerSolar, maxBateria=4000):
    bateria = [i - i for i in horas]
    rede = [i - i for i in horas]
    comControle = []

    for i in range(len(horas)):
        eRest = carga[i] - gerSolar[i] # Energia que sobrará caso vá para carga
        if eRest < 0: # carga atendida
            if bateria[i-1] == maxBateria: # Verifica se a bateria está cheia
                rede[i] = -eRest # Vende energia para a rede
                bateria[i] = bateria[i-1]
                comControle .append(str(i) + " | carga - gersolar | rede - gersolar")
            else:
                bateria[i] = bateria[i-1] + -(eRest)  # Geração alimenta a bateria
                comControle .append(str(i) + " | carga - gersolar | bateria - gersolar")
        else: # carga não foi atendida
            if bateria[i-1] == 0:
                rede[i]= -eRest # Se a bateria estiver sem carga, compra energia da rede
                comControle .append(str(i) + " | carga - gersolar | carga - rede")
            else:
                bateria[i] = bateria[i-1] - eRest # Descarrega bateria na carga
                comControle .append(str(i) + " | carga - gersolar | carga - bateria")


        # Controlador da bateria
        if bateria[i] > maxBateria:
            bateria[i] = maxBateria # Estado Máximo
        elif bateria[i] < 0:
            bateria[i] = 0 # Estado Mínimo

    gravacaoSaida(comControle)

    return bateria, rede

def edc3(horas, carga, gerSolar, cargaVE, previsao, maxBateria=4000):
    rede = [i - i for i in horas]
    bateria = [i - i for i in horas]
    acumulado = 1
    horaDescarga = 0
    divisao = 1
    comControle = []

    for i in range(len(horas)):
        if cargaVE[i] != 0 and horaDescarga == 0: # Verifica se há um carregamento
            horaDescarga = i
            horaCarga = i 
    while acumulado <= maxBateria:
        horaCarga -= 1
        acumulado += acumulado*(previsao[horaCarga])/divisao
        divisao += 1

    for i in range(len(horas)):
        eRest = carga[i] - gerSolar[i] # Energia que sobrará caso vá para carga

        if cargaVE[i]>0: # Horário de descarga
            if bateria[i-1] > 0:
                bateria[i] = bateria[i-1] - cargaVE[i] # Descarrega bateria na carga
                rede[i] = -eRest
                comControle .append(str(i) + " | carga - gersolar | carga - rede | cargave - bateria")
            else:
                rede[i] = -cargaVE[i] + -eRest
                comControle .append(str(i) + " | carga - gersolar | cargave - rede")
        else:  
            rede[i] = -eRest # Vende Energia Restante pra rede
            comControle .append(str(i) + " | carga - gersolar | rede - gersolar")


        if i >= horaCarga and i < horaDescarga: # Horario de carregamento da bateria
            bateria[i] = bateria[i-1]
            bateria[i] = bateria[i-1] + gerSolar[i]  # Geração alimenta a bateria
            rede[i] = -carga[i] # rede alimenta a carga
            comControle .append(str(i) + " | carga - rede | bateria - gersolar")



        # Controlador da bateria
        if bateria[i] > maxBateria:
            bateria[i] = maxBateria
        # Estado Máximo
        elif bateria[i] < 0:
            bateria[i] = 0 # Estado Mínimo

    gravacaoSaida(comControle)

    return bateria, rede

def edc4(horas, carga, gerSolar, cargaVE, previsao, maxBateria=4000):
    rede = [i - i for i in horas]
    bateria = [i - i for i in horas]
    acumulado = 1
    horaDescarg = 0
    comControle = []

    # Cálculo da hora de carregamento
    for i in range(len(horas)):
        if cargaVE[i] != 0 and horaDescarg == 0: # Verifica se há um carregamento
            horaDescarg = i 
            horaCarg = i 
    while acumulado <= maxBateria:
        horaCarg -= 1
        acumulado += previsao[horaCarg]

    for i in range(len(horas)):
        eRest = carga[i] - gerSolar[i] # Energia que sobrará caso vá para carga

        if cargaVE[i]>0: # Horário de descarga
            if bateria[i-1] > 0:
                bateria[i] = bateria[i-1] - cargaVE[i] # Descarrega bateria na carga
                rede[i] = -eRest
                comControle .append(str(i) + " | carga - gersolar | carga - rede | cargave - bateria")
            else:
                rede[i] = -cargaVE[i] + -eRest
                comControle .append(str(i) + " | carga - gersolar | cargave - rede")
        else:  
            rede[i] = -eRest # Vende Energia Restante pra rede
            comControle .append(str(i) + " | carga - gersolar | rede - gersolar")

        if i >= horaCarg and i < horaDescarg: # Horario de carregamento da bateria
            bateria[i] = bateria[i-1]
            bateria[i] = bateria[i-1] + gerSolar[i]  # Geração alimenta a bateria
            rede[i] = -carga[i] # rede alimenta a carga
            comControle .append(str(i) + " | carga - rede | bateria - gersolar")


        # Controlador da bateria
        if bateria[i] > maxBateria:
            bateria[i] = maxBateria
        # Estado Máximo
        elif bateria[i] < 0:
            bateria[i] = 0 # Estado Mínimo

    gravacaoSaida(comControle)

    return bateria, rede

def edc5(horas, carga, gerSolar, cargaVE, maxBateria=4000):
    rede = [i - i for i in horas]
    bateria = [i - i for i in horas]
    comControle = []

    # Controle da Micro rede
    for i in range(len(horas)):
        eRest = carga[i] - gerSolar[i] # Energia que sobrará caso vá para carga

        if bateria[i-1] == maxBateria or gerSolar[i] < carga[i]: # Verifica se a bateria está cheia
            if eRest > 0:
                bateria[i] = bateria[i] - cargaVE[i]
                if bateria[i-1] == 0:
                    rede[i]= -eRest # Se a bateria estiver sem carga, compra energia da rede
                    comControle.append(str(i) + " |  | ")
                else:
                    bateria[i] = bateria[i-1] - eRest # Descarrega bateria na carga
                    comControle .append(str(i) + " | carga - gersolar | carga - bateria")
            else:
                rede[i] = -eRest # Vende Energia Restante pra rede
                bateria[i] = bateria[i-1]
                comControle.append(str(i) + " |  | ")

            if cargaVE[i] > 0:
                if bateria[i-1] > 0:
                    bateria[i] = bateria[i-1] - cargaVE[i]
                    comControle.append(str(i) + " |  | ")
                else:
                    rede[i] = -cargaVE[i] + -eRest
                    bateria[i] = bateria[i-1]
                    comControle.append(str(i) + " |  | ")
            else:
                rede[i] = -eRest # Vende Energia Restante pra rede
                bateria[i] = bateria[i-1]
                comControle.append(str(i) + " |  | ")
        else:
            if cargaVE[i] == 0:
                bateria[i] = bateria[i-1] + gerSolar[i]  # Geração alimenta a bateria
            rede[i] = -carga[i] # rede alimenta a carga
            comControle.append(str(i) + " |  | ")


        # Controlador da bateria
        if bateria[i] > maxBateria:
            bateria[i] = maxBateria
        # Estado Máximo
        elif bateria[i] < 0:
            bateria[i] = 0 # Estado Mínimo

    gravacaoSaida(comControle)

    return bateria, rede

