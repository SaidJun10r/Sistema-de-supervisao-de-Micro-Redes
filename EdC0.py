# Bibliotecas
from matplotlib import pyplot as plt
import csv

# Matrizes Inicias
horas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
GerSolar = [0, 0, 0, 0, 0, 0, 5, 10, 100, 1000, 2000, 3000, 5000, 4000, 3000, 2000, 1000, 1000, 100, 5, 0, 0, 0, 0]
Carga = [0, 0, 0, 0, 0, 0, 10, 100, 500, 100, 10, 1000, 2000, 1000, 100, 10, 10, 10, 100, 500, 1000, 2000, 500, 10]
Rede = [i - i for i in horas]
#Rede = [0, 0, 0, 0, 0, 0, -10, -100, -500, -100, -10, 2000, 3000, 3000, 2900, 1990, 990, 990, 0, 0, 0, -495, -500, -10]

# Controle da Micro Rede
for i in range(24):
    eRestante = Carga[i] - GerSolar[i]
    Rede[i] = -eRestante

print('Rede', Rede)

# Plotagem do Gráfico
plt.bar(horas, GerSolar, label='Geração', width=.25)
plt.bar([i + 0.33 for i in horas], Carga, label='Carga', color='limegreen',width=.33)
plt.bar([i + 0.66 for i in horas], Rede, label='Rede', color='gold',width=.33)
plt.xticks(range(min(horas), max(horas)+1))
plt.yticks(range(min(Rede), max(max(GerSolar), max(Carga), max(Rede))+1, 500))
plt.axis([0, 24, min(Rede), max(max(GerSolar), max(Carga), max(Rede))])
plt.legend()
plt.axhline(0, color='black', linestyle='-')
plt.xlabel("Horas")
plt.ylabel("Energia")
plt.title("Estudo de Caso 1")
plt.grid(color="grey", linestyle="-", linewidth=0.1)
plt.show()