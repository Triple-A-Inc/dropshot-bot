import pandas as pd
import requests
from dotenv import load_dotenv
import os
import time

# Get env vars
load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

# df = pd.read_csv('estoque_drop_clean.csv')

def get_data(endpoint: str, data: dict, headers={}):
    url = f'{BASE_URL}{endpoint}'
    data['token'] = API_KEY

    try:
        response = requests.post(url, data=data, headers=headers)
        
        # Raise an error if the request failed
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"Problema com {url}, {str(e)}")
    

if __name__ == '__main__':
    df = pd.read_csv(r'tiny\description_scrapper\estoque_drop_clean.csv')
    # product_list = df['codigo'].to_list()
    product_list = df['codigo'].head(200).to_list()

    endpoint = 'produto.obter.php'
    # product_code = 'TXP240020227'
    format_return = 'JSON'

    params = {
        'token': API_KEY,
        'formato': format_return
    }

    status_list = []
    correct_products = 0

    for idx, product_code in enumerate(product_list):
        params['id'] = product_code

        response = get_data(endpoint, params)

        status = (response['retorno']['status'])

        print(f'Analisando produto {idx}: {product_code} -> STATUS: {status}')
        if status == 'Erro':
            print(response['retorno']['erros'][0]['erro'])

        if 'API Bloqueada' in status:
            print(f'\tAPI BLOQUEADA\n{status}')
            print(f'\tREQUISICAO NUMERO: {idx}')
            breakpoint()
        # elif status == 'Erro':
        #     status_list.append(response['retorno']['erros'][0]['erro'])
        if status != 'Erro':
            print('PRODUTO ENCONTRADO')
            print(response)
            correct_products += 1

        time.sleep(1)



    breakpoint()