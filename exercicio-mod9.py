import os
import json
import time
from random import random
from datetime import datetime
from sys import argv

import seaborn as sns
import pandas as pd
import requests

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'



# Captando a taxa CDI do site do BCB

def get_cdi():
  try:
    response = requests.get(URL)
    response.raise_for_status()
  except requests.HTTPError as exc:
    print("Dado não encontrado, continuando.")
    cdi = None
  except Exception as exc:
    print("Erro, parando a execução.")
    raise exc
  else:
    return json.loads(response.text)[-1]['valor']

dado = get_cdi()
contador = 0  
while contador < 10:

  # Criando a variável data e hora

  data_e_hora = datetime.now()
  data = datetime.strftime(data_e_hora, '%Y/%m/%d')
  hora = datetime.strftime(data_e_hora, '%H:%M:%S')

  cdi = round(float(dado) + (random() - 0.5), 2)

  # Verificando se o arquivo "taxa-cdi.csv" existe

  if os.path.exists('./taxa-cdi.csv') == False:

    with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
      fp.write('data,hora,taxa\n')
    print('Criando cabeçalho')
    # Salvando dados no arquivo "taxa-cdi.csv"

  with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
    fp.write(f'{data},{hora},{cdi}\n')
  print(f'Linha {contador + 1} adicionada')
  time.sleep(1)

  contador += 1
print("Sucesso")


df = pd.read_csv('./taxa-cdi.csv')

grafico = sns.lineplot(x= df['hora'], y= df['taxa'])
grafico.get_figure().savefig(f"{argv[1]}.png")
