import pandas as pd
import numpy as np
import json
import pickle

# método para realizar a predição se o paciente tem ou não diabetes
def paciente_predictor(paciente):
    
    # transforma o dict do paciente em um dataframe
    values = pd.DataFrame([paciente])
    
    # carrega o modelo de predição de diabetes
    model = pickle.load(open('./modelo/modelo_diabetes.pkl', 'rb')) 

    # realiza a predição com base no modelo carregado e nos dados recebidos como parametro da API
    results = model.predict(values)
     
    result = None
    
    # se existir somente um resultado, já o transforma em inteiro e retorna
    if len(results) == 1:
        result = int(results[0])
    
    return result

# realiza a carga dos dados do arquivo CSV da diabetes para um dataframe pandas
def load_data():
    # faz a leitura do conjunto de dados
    dados = pd.read_csv('./dados/diabetes.csv')
    return dados

# retorna todos os dados já armazenados das predições realizadas e validadas pelo usuário
# TODO: verificar se o arquivo existe antes de abrir
def get_all_predictions():
    data = None
    with open('predictions.json', 'r') as f:
        data = json.load(f)
        
    return data

# salva as predições em um arquivo JSON
# TODO: verificar se já não está salvo no arquivo antes de salvar de novo
def save_prediction(paciente):
    try:
        # le todos as predições
        data = get_all_predictions()

        # adiciona a nova predição nos dados já armazenados
        data.append(paciente)

        # salva todas as predições no arquivo json
        with open('predictions.json', 'w') as f:
            json.dump(data, f)

        return True 
    
    except Exception as e:
        print(f'Exception during save_prediction: {e}')
        return False   