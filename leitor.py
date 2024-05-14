import pandas as pd

def leitorcsv(dados: str):
    bd = pd.read_csv(dados) # Dados da rede
    horas = bd['Horas']
    carga = bd['Carga']
    gerSolar = bd['GerSolar']
    cargaVE = bd['CargaVE']
    previsao = bd['Previsao']

    return horas, carga, gerSolar, cargaVE, previsao