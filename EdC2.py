from matplotlib import pyplot as plt
import numpy as np

Horas = [i for i in np.linspace(0, 23.75, 96)]
Carga = [0, 0, 0, 0, 0, 0, 10, 100, 500, 100, 10, 1000, 2000, 1000, 100, 10, 10, 10, 100, 500, 1000, 2000, 500, 10]
GerSolar = [0, 0, 0, 0, 0, 0, 5, 10, 100, 1000, 2000, 3000, 5000, 4000, 3000, 2000, 1000, 1000, 100, 5, 0, 0, 0, 0]
Rede = [i - i for i in Horas]
Bateria = [i - i for i in Horas]
MaxBateria = 4000

# Interpolação
Carga = np.interp(np.linspace(0, len(Carga) - 1, 96), range(len(Carga)), Carga)
GerSolar = np.interp(np.linspace(0, len(GerSolar) - 1, 96), range(len(GerSolar)), GerSolar)

# Controle da Micro Rede
for i in range(96):
    eRest = Carga[i] - GerSolar[i] # Energia que sobrará caso vá para carga
    if eRest < 0: # Carga atendida
        if Bateria[i-1] == MaxBateria: # Verifica se a bateria está cheia
            Rede[i] = -eRest # Vende energia para a rede
            Bateria[i] = Bateria[i-1]
        else:
            Bateria[i] = Bateria[i-1] + -(eRest)  # Geração alimenta a bateria
    else: # Carga não foi atendida
        if Bateria[i-1] == 0:
            Rede[i]= -eRest # Se a bateria estiver sem carga, compra energia da rede
        else:
            Bateria[i] = Bateria[i-1] - eRest # Descarrega bateria na carga

    # Controlador da bateria
    if Bateria[i] > MaxBateria:
        Bateria[i] = MaxBateria # Estado Máximo
    elif Bateria[i] < 0:
        Bateria[i] = 0 # Estado Mínimo

# Plotagem do Gráfico
plt.bar([i for i in range(len(Horas))], Carga, label='Carga expandida',width=0.25)
plt.bar([i + 0.25 for i in range(len(Horas))], GerSolar, label='Geração expandida', color='limegreen',width=0.25)
plt.bar([i + 0.5 for i in range(len(Horas))], Rede, label='Rede', color='gold',width=0.25)
plt.bar([i + 0.75 for i in range(len(Horas))], Bateria, label='Bateria', color='red',width=0.25)
plt.plot([i for i in range(len(Horas))], Carga)
plt.plot([i + 0.25 for i in range(len(Horas))], GerSolar, color = 'limegreen')
plt.plot([i + 0.5 for i in range(len(Horas))], Rede, color = 'gold')
plt.plot([i + 0.75 for i in range(len(Horas))], Bateria, color = 'red')
plt.axhline(0, color='black', linestyle='-')
plt.xlabel("Horas")
plt.ylabel("Energia")
plt.title("Estudo de Caso 2")
plt.grid(color="grey", linestyle="-", linewidth=0.001)
plt.legend()
plt.show()