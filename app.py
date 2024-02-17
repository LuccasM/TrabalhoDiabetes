# importing Important Liberaries
import pickle
import streamlit as st
import numpy as np
import pandas as pd
import data_handler

# Load model
model_diabetes = pickle.load(open('modelo/modelo_diabetes.pkl', 'rb'))

# Web Title
st.title('Predição de diabetes')

# Split Columns
col1, col2, col3 = st.columns(3)

with col1 :
  Gestacoes = st.number_input('Informe a quantidade de gestações')

with col2 :
  Glicose = st.number_input('Informe a concentração de glicose')
  
with col3 :
  Pressao = st.number_input('Informe a pressão sanguínea')

# define a linha 2 de inputs, também com 3 colunas
col1, col2, col3 = st.columns(3)

with col1 :
  EspessuraPele = st.number_input('Informe a espessura da pele (mm)')

with col2 :
  Insulina = st.number_input('Informe a concentração de insulina')

with col3 :
  IMC = st.number_input('Informe o IMC')

# define a linha 2 de inputs, também com 3 colunas
col1, col2, col3 = st.columns(3)

with col1 :
  FuncaoDiabate = st.number_input('Informe a função do diabetes')

with col2 :
  Idade = st.number_input('Informe a idade')

with col3 : 
  submit = st.button('Predição')  
  
# Prediction
#diabetes_diagnostico = ''

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
  print(paciente)

  values = pd.DataFrame([paciente])
  print(values) 

  # realiza a predição de sobrevivência do passageiro com base nos dados inseridos pelo usuário
  results = model_diabetes.predict(values)
  print(results)

  # o modelo foi treinado para retornar uma lista com 0 ou 1, onde cada posição da lista indica se o passageiro sobreviveu (1) ou não (0)
  # como estamos realizando a predição de somente um passageiro por vez, o modelo deverá retornar somente um elemento na lista
  if len(results) == 1:
      # converte o valor retornado para inteiro
      diabetes = int(results[0])
      
      # verifica se o passageiro sobreviveu
      if diabetes == 1:
          # se sim, exibe uma mensagem que o passageiro sobreviveu
          st.subheader('O paciente não tem diabetes 😃🙌🏻')
          if 'diabetes' not in st.session_state:
              st.balloons()
      else:
          # se não, exibe uma mensagem que o passageiro não sobreviveu
          st.subheader('O paciente tem diabetes! 😢')
          if 'diabetes' not in st.session_state:
              st.snow()
      
      # salva no cache da aplicação se o passageiro sobreviveu
      st.session_state['diabetes'] = diabetes

  # verifica se existe um passageiro e se já foi verificado se ele sobreviveu ou não
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
          
          # adiciona no dict do passageiro se a predição está correta ou não
          if correct_prediction:
              paciente['CorrectPrediction'] = True
          elif wrong_prediction:
              paciente['CorrectPrediction'] = False
              
          # adiciona no dict do passageiro se ele sobreviveu ou não
          paciente['diabetes'] = st.session_state['diabetes']
          
          # escreve a mensagem na tela
          st.write(message)
          print(message)
          
          # salva a predição no JSON para cálculo das métricas de avaliação do sistema
          data_handler.save_prediction(paciente)    

  st.write('')
  # adiciona um botão para permitir o usuário realizar uma nova análise
  col1, col2, col3 = st.columns(3)
  with col2:
      new_test = st.button('Iniciar Nova Análise')
      
      # se o usuário pressionar no botão e já existe um passageiro, remove ele do cache
      if new_test and 'diabetes' in st.session_state:
          del st.session_state['diabetes']
          st.rerun()   

# calcula e exibe as métricas de avaliação do modelo
# aqui, somente a acurária está sendo usada
# TODO: adicionar as mesmas métricas utilizadas na disciplina de treinamento e validação do modelo (recall, precision, F1-score)
accuracy_predictions_on = st.toggle('Exibir acurácia')

if accuracy_predictions_on:
    # pega todas as predições salvas no JSON
    predictions = data_handler.get_all_predictions()
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
