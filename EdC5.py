from matplotlib import pyplot as plt
import pandas as pd

bd = pd.read_csv('Dados.csv') # Dados da Rede
Rede = [i - i for i in bd['Horas']]
Bateria = [i - i for i in bd['Horas']]
MaxBateria = 4000
HorarioVE = 12

# Controle da Micro Rede
for i in range(96):
    eRest = bd['Carga'][i] - bd['GerSolar'][i] # Energia que sobrará caso vá para bd['Carga']

    if Bateria[i-1] == MaxBateria or bd['GerSolar'][i] < bd['Carga'][i]: # Verifica se a bateria está cheia
        if eRest > 0:
            Bateria[i] = Bateria[i] - bd['CargaVE'][i]
            if Bateria[i-1] == 0:
                Rede[i]= -eRest # Se a bateria estiver sem bd['Carga'], compra energia da rede
            else:
                Bateria[i] = Bateria[i-1] - eRest # Descarrega bateria na bd['Carga']
        else:
            Rede[i] = -eRest # Vende Energia Restante pra Rede
            Bateria[i] = Bateria[i-1]
        if bd['CargaVE'][i] > 0:
            if Bateria[i-1] > 0:
                Bateria[i] = Bateria[i-1] - bd['CargaVE'][i]
            else:
                Rede[i] = -bd['CargaVE'][i] + -eRest
                Bateria[i] = Bateria[i-1]
        else:
            Rede[i] = -eRest # Vende Energia Restante pra Rede
            Bateria[i] = Bateria[i-1]
    else:
        if bd['CargaVE'][i] == 0:
            Bateria[i] = Bateria[i-1] + bd['GerSolar'][i]  # Geração alimenta a bateria
        Rede[i] = -bd['Carga'][i] # Rede alimenta a bd['Carga']

    # Controlador da bateria
    if Bateria[i] > MaxBateria:
        Bateria[i] = MaxBateria # Estado Máximo
    elif Bateria[i] < 0:
        Bateria[i] = 0 # Estado Mínimo


# Plotagem do Gráfico
plt.bar([i for i in range(len(bd['Horas']))], bd['Carga'], label='Carga expandida',width=0.2)
plt.bar([i + 0.2 for i in range(len(bd['Horas']))], bd['GerSolar'], label='Geração expandida', color='limegreen',width=0.2)
plt.bar([i + 0.4 for i in range(len(bd['Horas']))], Rede, label='Rede', color='gold',width=0.2)
plt.bar([i + 0.6 for i in range(len(bd['Horas']))], Bateria, label='Bateria', color='red',width=0.2)
plt.bar([i + 0.8 for i in range(len(bd['Horas']))], bd['CargaVE'], color = 'lightblue', width=0.2)
plt.plot([i for i in range(len(bd['Horas']))], bd['Carga'])
plt.plot([i + 0.2 for i in range(len(bd['Horas']))], bd['GerSolar'], color = 'limegreen')
plt.plot([i + 0.4 for i in range(len(bd['Horas']))], Rede, color = 'gold')
plt.plot([i + 0.6 for i in range(len(bd['Horas']))], Bateria, color = 'red')
plt.plot([i + 0.8 for i in range(len(bd['Horas']))], bd['CargaVE'], color = 'lightblue')
plt.axhline(0, color='black', linestyle='-')
plt.xlabel("bd['Horas']")
plt.ylabel("Energia")
plt.title("Estudo de Caso 2")
plt.grid(color="grey", linestyle="-", linewidth=0.001)
plt.legend()
plt.show()