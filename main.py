from leitor import leitorcsv
import modelos
from grafico import grafico

dados = 'Dados.csv'

horas, carga, gerSolar, cargaVE, previsao = leitorcsv(dados)
bateria, rede = modelos.edc2(horas, carga, gerSolar, 4000)
print(bateria, rede)
grafico(horas, carga, gerSolar, cargaVE==None, bateria, rede)