from matplotlib import pyplot as plt
import numpy as np

Horas = [i for i in np.linspace(0, 23.75, 96)]
Carga = [0, 0, 0, 0, 0, 0, 10, 100, 500, 100, 10, 1000, 2000, 1000, 100, 10, 10, 10, 100, 500, 1000, 2000, 500, 10]
GerSolar = [0, 0, 0, 0, 0, 0, 5, 10, 100, 1000, 2000, 3000, 5000, 4000, 3000, 2000, 1000, 1000, 100, 5, 0, 0, 0, 0]
CargaVE =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5000, 0, 0, 0, 0, 0, 0, 5000, 0, 0, 0, 0]
previsao = [0, 0, 0, 0, 0, 0, 0, -90, -400, 900, 1990, 0, 0, 3000, -100, 990, 990, -1010, 0, -495, -1000, -2000, -500, -10]
Rede = [i - i for i in Horas]
Bateria = [i - i for i in Horas]
MaxBateria = 4000
HorarioVE = 12
acumulado = 1
horaDescarga = 0
divisao = 1

# Interpolação
Carga = np.interp(np.linspace(0, len(Carga) - 1, 96), range(len(Carga)), Carga)
GerSolar = np.interp(np.linspace(0, len(GerSolar) - 1, 96), range(len(GerSolar)), GerSolar)
CargaVE = np.interp(np.linspace(0, len(CargaVE) - 1, 96), range(len(CargaVE)), CargaVE)
previsao = np.interp(np.linspace(0, len(previsao) - 1, 96), range(len(previsao)), previsao)

# Cálculo da hora de carregamento
for i in range(96):
    if CargaVE[i] != 0 and horaDescarga == 0: # Verifica se há um carregamento
        horaDescarga = i
        horaCarga = i 
while acumulado <= MaxBateria:
    horaCarga -= 1
    print(previsao[horaCarga], divisao)
    acumulado = acumulado*(previsao[horaCarga]) / divisao
    divisao += 1
    print(horaCarga, acumulado)
print(acumulado, horaCarga, horaDescarga)

tempoCarregamento = [i-i for i in range(horaCarga, horaDescarga)]

# Contrle da Micro Rede
for i in range(96):
    eRest = Carga[i] - GerSolar[i] # Energia que sobrará caso vá para carga

    if CargaVE[i]>0: # Horário de descarga
        if Bateria[i-1] > 0:
            Bateria[i] = Bateria[i-1] - CargaVE[i] # Descarrega bateria na carga
            Rede[i] = -eRest
            print("ta descarregando bateria", Bateria[i-1], i, CargaVE[i])
        else:
            Rede[i] = -CargaVE[i] + -eRest
            print('Bateria acabou')
            print(eRest, -CargaVE[i], Rede[i])
    Rede[i] = -eRest # Vende Energia Restante pra Rede

    if i >= horaCarga and i < horaDescarga: # Horario de carregamento da bateria
        Bateria[i] = Bateria[i-1]
        print("ta carregando", i, Bateria[i], GerSolar[i])
        Bateria[i] = Bateria[i-1] + GerSolar[i]  # Geração alimenta a bateria
        Rede[i] = -Carga[i] # Rede alimenta a carga


    # Controlador da bateria
    if Bateria[i] > MaxBateria:
        Bateria[i] = MaxBateria # Estado Máximo
    elif Bateria[i] < 0:
        Bateria[i] = 0 # Estado Mínimo


# Plotagem do Gráfico
plt.bar([i for i in range(len(Horas))], Carga, label='Carga expandida',width=0.2)
plt.bar([i + 0.2 for i in range(len(Horas))], GerSolar, label='Geração expandida', color='limegreen',width=0.2)
plt.bar([i + 0.4 for i in range(len(Horas))], Rede, label='Rede', color='gold',width=0.2)
plt.bar([i + 0.6 for i in range(len(Horas))], Bateria, label='Bateria', color='red',width=0.2)
plt.bar([i + 0.8 for i in range(len(Horas))], CargaVE, color = 'lightblue', width=0.2)
plt.plot([i for i in range(len(Horas))], Carga)
plt.plot([i + 0.2 for i in range(len(Horas))], GerSolar, color = 'limegreen')
plt.plot([i + 0.4 for i in range(len(Horas))], Rede, color = 'gold')
plt.plot([i + 0.6 for i in range(len(Horas))], Bateria, color = 'red')
plt.plot([i + 0.8 for i in range(len(Horas))], CargaVE, color = 'lightblue')
plt.axhline(0, color='black', linestyle='-')
plt.xlabel("Horas")
plt.ylabel("Energia")
plt.title("Estudo de Caso 2")
plt.grid(color="grey", linestyle="-", linewidth=0.001)
plt.legend()
plt.show()