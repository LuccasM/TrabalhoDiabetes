# Importa as bibliotecas
import pickle
import streamlit as st
import numpy as np
import pandas as pd
import data_handler
import matplotlib.pyplot as plt
import util
import requests
import json

print("Abriu a página")

# verifica se a senha de acesso está correta
if not util.check_password():
    # se a senha estiver errada, para o processamento do app
    print("Usuario não logado")
    st.stop()

print("Carregou a página")    

# primeiro de tudo, carrega os dados da diabete para um dataframe
#dados = data_handler.load_data()

# Carrega o modelo
#model_diabetes = pickle.load(open('modelo/modelo_diabetes.pkl', 'rb'))

API_URL = "http://localhost:8000"

# faz uma requisição da API para obter todos os dados do CSV
response = requests.get(API_URL + "/get_diabete_data") 
dados = None
# verifica se o status de retorno da requisição é 200, que significa sucesso
if response.status_code == 200:
    # se sim, carrega o retorno que está vindo em formato json
    dados_json = json.loads(response.json())
    # transforma o json em um dataframe com todos os dados
    dados = pd.DataFrame(dados_json)
else: 
    print("Erro ao buscar os dados dos pacientes")

# Tpitulo
st.title('Predição de diabetes')

data_analyses_on = st.toggle('Exibir análise dos dados')

if data_analyses_on:
    # essa parte é só um exmplo de que é possível realizar diversas visualizações e plotagens com o streamlit
    st.header('Dados da diabete - Dataframe')
    
    # exibe todo o dataframe dos dados do titanic
    st.dataframe(dados)

    # plota um histograma das idades dos pacientes
    st.header('Histograma das idades')
    fig = plt.figure()
    plt.hist(dados['Age'], bins=10)
    plt.xlabel('Idade')
    plt.ylabel('Quantidade')
    st.pyplot(fig)

    # plota um gráfico de barras com a contagem dos sobreviventes
    st.header('Diabéticos')
    st.bar_chart(dados.Outcome.value_counts())

# Define a primeira linha dos inputs
col1, col2, col3 = st.columns(3)

with col1 :
  Gestacoes = st.number_input('Informe a quantidade de gestações')

with col2 :
  Glicose = st.number_input('Informe a concentração de glicose')
  
with col3 :
  Pressao = st.number_input('Informe a pressão sanguínea')

# Define a segunda linha dos inputs
col1, col2, col3 = st.columns(3)

with col1 :
  EspessuraPele = st.number_input('Informe a espessura da pele (mm)')

with col2 :
  Insulina = st.number_input('Informe a concentração de insulina')

with col3 :
  IMC = st.number_input('Informe o IMC')

# Define a terceira linha dos inputs
col1, col2, col3 = st.columns(3)

with col1 :
  FuncaoDiabate = st.number_input('Informe a função do diabetes')

with col2 :
  Idade = st.number_input('Informe a idade')

with col3 : 
  submit = st.button('Predição')  
  

# Se clicou no botão de predição
if submit or 'diabetes' in st.session_state:
  
  paciente = {
        'Pregnancies': Gestacoes,
        'Glucose': Glicose,
        'BloodPressure': Pressao,
        'SkinThickness': EspessuraPele,
        'Insulin': Insulina,
        'BMI': IMC,
        'DiabetesPedigreeFunction': FuncaoDiabate,
        'Age': Idade
    }

  #values = pd.DataFrame([paciente])
  #print(values) 

  # realiza a predição para saber se o paciente tem ou não diabetes com base nos parâmetros informados
  #results = model_diabetes.predict(values)
  #print(results)

  # converte o dict do paciente em json para enviar para a API
  paciente_json = json.dumps(paciente)

  # realiza um post request para a API, passando o paciente como parametro para realizar a predição de diabetes
  response = requests.post(API_URL + "/predict", json=paciente_json) 
  result = None
  # verifica o status de sucesso da requisição
  if response.status_code == 200:
      # se houve sucesso, quer dizer que a API tem um resultado
      result = response.json()
  else: 
      print("Erro ao chamar a predição")
  
  # verifica se o resultado não é nulo
  if result is not None:
      diabetes = result
      # verifica se o paciente tem ou não diabetes
      if diabetes == 1:
          # se sim, exibe uma mensagem que o paciente tem diabetes
          st.subheader('O paciente tem diabetes! 😢')
          if 'diabetes' not in st.session_state:
              st.snow() 
      else:
          # se não, exibe uma mensagem que o paciente não tem diabetes
          st.subheader('O paciente não tem diabetes 😃🙌🏻')
          if 'diabetes' not in st.session_state:
              st.balloons()
      
      # salva no cache da aplicação se o paciente tem diabetes
      st.session_state['diabetes'] = diabetes

  # verifica se existe um paciente e se já foi verificado se ele é ou não diabético
  if paciente and 'diabetes' in st.session_state:
      # se sim, pergunta ao usuário se a predição está certa e salva essa informação
      st.write("A predição está correta?")
      col1, col2, col3 = st.columns([1,1,5])
      with col1:
          correct_prediction = st.button('👍🏻')
      with col2:
          wrong_prediction = st.button('👎🏻')
      
      # exibe uma mensagem para o usuário agradecendo o feedback
      if correct_prediction or wrong_prediction:
          message = "Muito obrigado pelo feedback"
          if wrong_prediction:
              message += ", iremos usar esses dados para melhorar as predições"
          message += "."
          
          # adiciona no dict do paciente se a predição está correta ou não
          if correct_prediction:
              paciente['CorrectPrediction'] = True
          elif wrong_prediction:
              paciente['CorrectPrediction'] = False
              
          # adiciona no dict do paciente se ele tem ou não diabetes
          paciente['diabetes'] = st.session_state['diabetes']
          
          # escreve a mensagem na tela
          st.write(message)
          
          # salva a predição no JSON para cálculo das métricas de avaliação do sistema
          #data_handler.save_prediction(paciente)

          # converte o dict do paciente para json
          paciente_json = json.dumps(paciente)
          # realiza um post request para a API salvar a predição, passando o json do paciente como parametro
          response = requests.post(API_URL + "/save_prediction", json=paciente_json)
          # verifica o retorno da API
          if response.status_code == 200:
              print("Predição salva")
          else: 
              print("Erro ao salvar predição")

  st.write('')
  # adiciona um botão para permitir o usuário realizar uma nova análise
  col1, col2, col3 = st.columns(3)
  with col2:
      new_test = st.button('Iniciar Nova Análise')
      
      # se o usuário pressionar no botão e já existe um paciente, remove ele do cache
      if new_test and 'diabetes' in st.session_state:
          del st.session_state['diabetes']
          st.rerun()   

# calcula e exibe as métricas de avaliação do modelo
# aqui, somente a acurária está sendo usada
# TODO: adicionar as mesmas métricas utilizadas na disciplina de treinamento e validação do modelo (recall, precision, F1-score)
accuracy_predictions_on = st.toggle('Exibir acurácia')

if accuracy_predictions_on:
    # pega todas as predições salvas no JSON
    #predictions = data_handler.get_all_predictions()

    # envia um get request para pegar todas as predições já salvas na API
    response = requests.get(API_URL + "/get_all_predictions") 
    predictions = None
    # verifica se o status de retorno é de sucesso
    if response.status_code == 200:
        predictions = response.json()
    else: 
        print("Erro ao buscar predições")

    # salva o número total de predições realizadas
    num_total_predictions = len(predictions)
    
    # calcula o número de predições corretas e salva os resultados conforme as predições foram sendo realizadas
    accuracy_hist = [0]
    # salva o numero de predições corretas
    correct_predictions = 0
    # percorre cada uma das predições, salvando o total móvel e o número de predições corretas
    for index, paciente in enumerate(predictions):
        total = index + 1
        if paciente['CorrectPrediction'] == True:
            correct_predictions += 1
            
        # calcula a acurracia movel
        temp_accuracy = correct_predictions / total if total else 0
        # salva o valor na lista de historico de acuracias
        accuracy_hist.append(round(temp_accuracy, 2)) 
    
    # calcula a acuracia atual
    accuracy = correct_predictions / num_total_predictions if num_total_predictions else 0
    
    # exibe a acuracia atual para o usuário
    st.metric(label='Acurácia', value=round(accuracy, 2))
    # TODO: usar o attr delta do st.metric para exibir a diferença na variação da acurácia
    
    # exibe o histórico da acurácia
    st.subheader("Histórico de acurácia")
    st.line_chart(accuracy_hist)               
