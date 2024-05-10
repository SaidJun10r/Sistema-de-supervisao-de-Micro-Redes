from matplotlib import pyplot as plt
import pandas as pd

bd = pd.read_csv('Dados.csv') # Dados da Rede
Rede = [i - i for i in bd['Horas']]
Bateria = [i - i for i in bd['Horas']]
MaxBateria = 4000
HorarioVE = 12
acumulado = 0
horaDescarg = 0

# Cálculo da hora de carregamento
for i in range(96):
    if bd['CargaVE'][i] != 0 and horaDescarg == 0: # Verifica se há um carregamento
        horaDescarg = i 
        horaCarg = i 
while acumulado <= MaxBateria:
    horaCarg -= 1
    acumulado += bd['Previsao'][horaCarg]
    print(horaCarg, acumulado)
print(acumulado, horaCarg, horaDescarg)

tempoCarregamento = [i-i for i in range(horaCarg, horaDescarg)]

# Contrle da Micro Rede
for i in range(96):
    eRest = bd['Carga'][i] - bd['GerSolar'][i] # Energia que sobrará caso vá para bd['Carga']

    if bd['CargaVE'][i]>0: # Horário de descarga
        if Bateria[i-1] > 0:
            Bateria[i] = Bateria[i-1] - bd['CargaVE'][i] # Descarrega bateria na bd['Carga']
            Rede[i] = -eRest
            print("ta descarregando bateria", Bateria[i-1], i, bd['CargaVE'][i])
        else:
            Rede[i] = -bd['CargaVE'][i] + -eRest
            print('Bateria acabou')
            print(eRest, -bd['CargaVE'][i], Rede[i])
    Rede[i] = -eRest # Vende Energia Restante pra Rede

    if i >= horaCarg and i < horaDescarg: # Horario de carregamento da bateria
        Bateria[i] = Bateria[i-1]
        print("ta carregando", i, Bateria[i], bd['GerSolar'][i])
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