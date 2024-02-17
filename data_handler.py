import pandas as pd
import numpy as np
import json

# retorna todos os dados já armazenados das predições realizadas e validadas pelo usuário
# TODO: verificar se o arquivo existe antes de abrir
def get_all_predictions():
    data = None
    with open('predictions.json', 'r') as f:
        data = json.load(f)
        
    return data

# salva as predições em um arquivo JSON
# TODO: verificar se já não está salvo no arquivo antes de salvar de novo
def save_prediction(passageiro):
    # le todos as predições
    data = get_all_predictions()
    # adiciona a nova predição nos dados já armazenados
    data.append(passageiro)
    # salva todas as predições no arquivo json
    with open('predictions.json', 'w') as f:
        json.dump(data, f)