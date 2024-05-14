from matplotlib import pyplot as plt

def grafico(horas, carga, gerSolar, cargaVE, bateria, rede):
    # Plotagem do Gráfico
    plt.bar([i for i in range(len(horas))], carga, label='Carga expandida',width=0.2)
    plt.bar([i + 0.2 for i in range(len(horas))], gerSolar, label='Geração expandida', color='limegreen',width=0.2)
    plt.bar([i + 0.4 for i in range(len(horas))], rede, label='rede', color='gold',width=0.2)
    plt.bar([i + 0.6 for i in range(len(horas))], bateria, label='bateria', color='red',width=0.2)
    plt.bar([i + 0.8 for i in range(len(horas))], cargaVE, color = 'lightblue', width=0.2)
    plt.plot([i for i in range(len(horas))], carga)
    plt.plot([i + 0.2 for i in range(len(horas))], gerSolar, color = 'limegreen')
    plt.plot([i + 0.4 for i in range(len(horas))], rede, color = 'gold')
    plt.plot([i + 0.6 for i in range(len(horas))], bateria, color = 'red')
    plt.plot([i + 0.8 for i in range(len(horas))], cargaVE, color = 'lightblue')
    plt.axhline(0, color='black', linestyle='-')
    plt.xlabel("horas")
    plt.ylabel("Energia")
    plt.title("Estudo de Caso 2")
    plt.grid(color="grey", linestyle="-", linewidth=0.001)
    plt.legend()
    plt.show()