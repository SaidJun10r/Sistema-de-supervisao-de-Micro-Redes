import pandas as pd

def leitorcsv(file_path: str):
    bd = pd.read_csv(file_path) # Dados da rede
    horas = bd['Horas']
    carga = bd['Carga']
    gerSolar = bd['GerSolar']
    cargaVE = bd['CargaVE']
    previsao = bd['Previsao']

    return horas, carga, gerSolar, cargaVE, previsao