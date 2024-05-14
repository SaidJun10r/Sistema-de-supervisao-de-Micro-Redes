def edc1(horas, carga, gerSolar, maxBateria=4000):
    bateria = [i - i for i in horas]
    rede = [i - i for i in horas]
    
    for i in range(len(horas)):
        eRest = carga[i] - gerSolar[i] # Energia que sobra na carga

        if bateria[i-1] == maxBateria or gerSolar[i] < carga[i]:
            if eRest > 0:
                if bateria[i-1] == 0:
                    rede[i] = -eRest
                else:
                    bateria[i] = bateria[i-1] - eRest
            else:
                rede[i] = -eRest
                bateria[i] = bateria[i-1]    
        else:
            bateria[i] = bateria[i-1] + gerSolar[i]
            rede[i] = -carga[i]

        if bateria [i] > maxBateria:
            bateria[i] = maxBateria
        elif bateria[i] < 0:
            bateria[i] = 0

    return bateria, rede

def edc2(horas, carga, gerSolar, maxBateria):
    bateria = [i - i for i in horas]
    rede = [i - i for i in horas]

    for i in range(len(horas)):
        eRest = carga[i] - gerSolar[i] # Energia que sobrará caso vá para carga
        if eRest < 0: # carga atendida
            if bateria[i-1] == maxBateria: # Verifica se a bateria está cheia
                rede[i] = -eRest # Vende energia para a rede
                bateria[i] = bateria[i-1]
            else:
                bateria[i] = bateria[i-1] + -(eRest)  # Geração alimenta a bateria
        else: # carga não foi atendida
            if bateria[i-1] == 0:
                rede[i]= -eRest # Se a bateria estiver sem carga, compra energia da rede
            else:
                bateria[i] = bateria[i-1] - eRest # Descarrega bateria na carga

        # Controlador da bateria
        if bateria[i] > maxBateria:
            bateria[i] = maxBateria # Estado Máximo
        elif bateria[i] < 0:
            bateria[i] = 0 # Estado Mínimo

    return bateria, rede

def edc3(horas, carga, gerSolar, cargaVE, previsao, maxBateria):
    rede = [i - i for i in horas]
    bateria = [i - i for i in horas]
    maxBateria = 4000
    acumulado = 1
    horaDescarga = 0
    divisao = 1

    for i in range(len(horas)):
        if cargaVE[i] != 0 and horaDescarga == 0: # Verifica se há um carregamento
            horaDescarga = i
            horaCarga = i 
    while acumulado <= maxBateria:
        horaCarga -= 1
        acumulado += acumulado*(previsao[horaCarga])/divisao
        divisao += 1
        print(horaCarga, 'Previsão:', previsao[horaCarga], 'Acumulado:', acumulado, 'Divisor:', divisao)
    print(acumulado, horaCarga, horaDescarga)

    for i in range(len(horas)):
        eRest = carga[i] - gerSolar[i] # Energia que sobrará caso vá para carga

        if cargaVE[i]>0: # Horário de descarga
            if bateria[i-1] > 0:
                bateria[i] = bateria[i-1] - cargaVE[i] # Descarrega bateria na carga
                rede[i] = -eRest
                print("ta descarregando bateria", bateria[i-1], i, cargaVE[i])
            else:
                rede[i] = -cargaVE[i] + -eRest
                print('bateria acabou')
                print(eRest, -cargaVE[i], rede[i])
        rede[i] = -eRest # Vende Energia Restante pra rede

        if i >= horaCarga and i < horaDescarga: # Horario de carregamento da bateria
            bateria[i] = bateria[i-1]
            print("ta carregando", i, bateria[i], gerSolar[i])
            bateria[i] = bateria[i-1] + gerSolar[i]  # Geração alimenta a bateria
            rede[i] = -carga[i] # rede alimenta a carga


        # Controlador da bateria
        if bateria[i] > maxBateria:
            bateria[i] = maxBateria
        # Estado Máximo
        elif bateria[i] < 0:
            bateria[i] = 0 # Estado Mínimo

    return bateria, rede

def edc4(horas, carga, gerSolar, cargaVE, previsao, maxBateria):
    rede = [i - i for i in horas]
    bateria = [i - i for i in horas]
    maxBateria = 4000
    acumulado = 1
    horaDescarg = 0

    # Cálculo da hora de carregamento
    for i in range(len(horas)):
        if cargaVE[i] != 0 and horaDescarg == 0: # Verifica se há um carregamento
            horaDescarg = i 
            horaCarg = i 
    while acumulado <= maxBateria:
        horaCarg -= 1
        acumulado += previsao[horaCarg]
        print(horaCarg, acumulado)
    print(acumulado, horaCarg, horaDescarg)

    for i in range(len(horas)):
        eRest = carga[i] - gerSolar[i] # Energia que sobrará caso vá para carga

        if cargaVE[i]>0: # Horário de descarga
            if bateria[i-1] > 0:
                bateria[i] = bateria[i-1] - cargaVE[i] # Descarrega bateria na carga
                rede[i] = -eRest
                print("ta descarregando bateria", bateria[i-1], i, cargaVE[i])
            else:
                rede[i] = -cargaVE[i] + -eRest
                print('bateria acabou')
                print(eRest, -cargaVE[i], rede[i])
        rede[i] = -eRest # Vende Energia Restante pra rede

        if i >= horaCarg and i < horaDescarg: # Horario de carregamento da bateria
            bateria[i] = bateria[i-1]
            print("ta carregando", i, bateria[i], gerSolar[i])
            bateria[i] = bateria[i-1] + gerSolar[i]  # Geração alimenta a bateria
            rede[i] = -carga[i] # rede alimenta a carga


        # Controlador da bateria
        if bateria[i] > maxBateria:
            bateria[i] = maxBateria
        # Estado Máximo
        elif bateria[i] < 0:
            bateria[i] = 0 # Estado Mínimo

    return bateria, rede

def edc5(horas, carga, gerSolar, cargaVE, maxBateria):
    rede = [i - i for i in horas]
    bateria = [i - i for i in horas]
    MaxBateria = 4000

    # Controle da Micro rede
    for i in range(96):
        eRest = carga[i] - gerSolar[i] # Energia que sobrará caso vá para carga

        if bateria[i-1] == maxBateria or gerSolar[i] < carga[i]: # Verifica se a bateria está cheia
            if eRest > 0:
                bateria[i] = bateria[i] - cargaVE[i]
                if bateria[i-1] == 0:
                    rede[i]= -eRest # Se a bateria estiver sem carga, compra energia da rede
                else:
                    bateria[i] = bateria[i-1] - eRest # Descarrega bateria na carga
            else:
                rede[i] = -eRest # Vende Energia Restante pra rede
                bateria[i] = bateria[i-1]
            if cargaVE[i] > 0:
                if bateria[i-1] > 0:
                    bateria[i] = bateria[i-1] - cargaVE[i]
                else:
                    rede[i] = -cargaVE[i] + -eRest
                    bateria[i] = bateria[i-1]
            else:
                rede[i] = -eRest # Vende Energia Restante pra rede
                bateria[i] = bateria[i-1]
        else:
            if cargaVE[i] == 0:
                bateria[i] = bateria[i-1] + gerSolar[i]  # Geração alimenta a bateria
            rede[i] = -carga[i] # rede alimenta a carga

        # Controlador da bateria
        if bateria[i] > maxBateria:
            bateria[i] = maxBateria
        # Estado Máximo
        elif bateria[i] < 0:
            bateria[i] = 0 # Estado Mínimo

    return bateria, rede

