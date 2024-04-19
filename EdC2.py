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

# Contrle da Micro Rede
for i in range(96):
    # Enviar energia gerada para a carga
    EnergRest = GerSolar[i] - Carga[i]
    print(EnergRest)
    # Carga está sendo atendida?
    if EnergRest < 0 :
        # Descarregar energia da bateria na carga
        print("Bateria-1 = ", Bateria[i-1])
        EnergRest = Bateria[i-1] - EnergRest
        # Carga está sendo atendida?
        if EnergRest < 0:
            # Comprar energia da rede para a carga
            Rede[i] = EnergRest
        else:
            continue
    else:
        # Bateria está cheia?
        if Bateria[i-1] >= MaxBateria:
            # Vender energia restante na rede
            Rede[i] = EnergRest
        else:
            # Envia energia gerada para bateria
            Bateria[i] = Bateria[i-1] + EnergRest

    # Controlador da bateria
    if Bateria[i] > MaxBateria:
        Bateria[i] = MaxBateria
        
print('Bateria = ', Bateria, "\n")
print('Rde = ', Rede)

plt.plot(Horas, Bateria)
plt.show()
# Plotagem do Gráfico
plt.bar([i for i in range(len(Horas))], Carga, label='Carga expandida',width=0.25)
plt.bar([i + 0.25 for i in range(len(Horas))], GerSolar, label='Geração expandida', color='limegreen',width=0.25)
plt.bar([i + 0.5 for i in range(len(Horas))], Rede, label='Rede', color='gold',width=0.25)
plt.bar([i + 0.75 for i in range(len(Horas))], Bateria, label='Bateria', color='red',width=0.25)
plt.axhline(0, color='black', linestyle='-')
plt.xlabel("Horas")
plt.ylabel("Energia")
plt.title("Estudo de Caso 1")
plt.grid(color="grey", linestyle="-", linewidth=0.1)
plt.legend()
plt.show()