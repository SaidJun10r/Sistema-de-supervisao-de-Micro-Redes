from matplotlib import pyplot as plt
import numpy as np
import csv

Horas = [i for i in np.linspace(0, 23.75, 96)]
Agendamento = np.zeros((96,), dtype=int)
Carga = [0, 0, 0, 0, 0, 0, 10, 100, 500, 100, 10, 1000, 2000, 1000, 100, 10, 10, 10, 100, 500, 1000, 2000, 500, 10]
GerSolar = [0, 0, 0, 0, 0, 0, 5, 10, 100, 1000, 2000, 3000, 5000, 4000, 3000, 2000, 1000, 1000, 100, 5, 0, 0, 0, 0]
Rede = [i - i for i in Horas]

# Interpolação
expanded_carga = np.interp(np.linspace(0, len(Carga) - 1, 96), range(len(Carga)), Carga)
expanded_geracao = np.interp(np.linspace(0, len(GerSolar) - 1, 96), range(len(GerSolar)), GerSolar)

def write_vectors_to_csv(Horas, expanded_carga , expanded_geracao, filename):
    # Verificar se o tamanho dos vetores é o mesmo
    if len(expanded_carga) != len(expanded_geracao):
        raise ValueError("TAMANHOS DOS VETORES DIFERENTES!")

    # juntar vetores
    rows = zip(Horas, expanded_carga, expanded_geracao, Agendamento)

    # Grava no arquivo csv
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Horas', 'Carga', 'Geracao', 'Agendamento'])  # Escrever cabecalhos
        writer.writerows(rows)

# Nome do arquivo
filename = 'Dados.csv'

# Insere vetores no arquivo CSV
write_vectors_to_csv(Horas, expanded_carga, expanded_geracao, filename)

print(f"Vetores inseridos no arquivo '{filename}' com sucesso.")
print(len(Horas))

for i in range(96):
    eRestante = expanded_carga[i] - expanded_geracao[i]
    Rede[i] = -eRestante


plt.bar([i for i in range(len(Horas))], expanded_carga, label='Carga expandida',width=0.33)
plt.bar([i + 0.33 for i in range(len(Horas))], expanded_geracao, label='Geração expandida', color='limegreen',width=0.33)
plt.bar([i + 0.66 for i in range(len(Horas))], Rede, label='Rede', color='gold',width=0.33)
plt.axhline(0, color='black', linestyle='-')
plt.xlabel("Horas")
plt.ylabel("Energia")
plt.title("Estudo de Caso 1")
plt.grid(color="grey", linestyle="-", linewidth=0.1)
plt.legend()
plt.show()