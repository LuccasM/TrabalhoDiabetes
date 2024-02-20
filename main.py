from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Union, Any
import data_handler
import json
import pandas as pd
 
api = FastAPI()

# Método simples de exemplo para verificar se a API está rodando e funcionando
@api.get("/hello_world")
async def root():
    return {"message": "Hello World"}

# método especifico para realizar a predição se um paciente tem ou não diabetes
# recebe um json com as informações do paciente
@api.post("/predict")
def predict(paciente_json: Any = Body(None)):
    # carrega o json em um python dict
    paciente = json.loads(paciente_json)
    # chama o método para realizar a predição passando o dict do paciente 
    result = data_handler.paciente_predictor(paciente)
    # retorna o resultado
    return result

# método para retornar todos os dados dos pacientes
@api.get("/get_diabete_data")
async def get_diabete_data(): 
    # carrega os dados
    dados = data_handler.load_data()
    # transforma os dados em json
    dados_json = dados.to_json(orient='records')
    # retorna o json para ser enviado via API
    return dados_json

# método para salvar a predição
# recebe como parametro um json com todas as informações do paciente e do resultado da predição
@api.post("/save_prediction")
async def save_prediction(paciente_json: Any = Body(None)):
    # transforma o json em um python dict
    paciente = json.loads(paciente_json)
    # salva a predição no arquivo já existente de predições realizadas
    result = data_handler.save_prediction(paciente)
    # retorna o resultado
    return result

# método para retornar todas as predições já realizadas e salvas
@api.get("/get_all_predictions")
async def get_all_predictions():
    # carrega a lista de predições
    all_predictions = data_handler.get_all_predictions()
    # retorna essa lista
    return all_predictions
