import requests
from dotenv import load_dotenv
import os

# Get env vars
load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

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
    product = 'Agasalho DROP SHOT AIRAM JMD'
    endpoint = 'produtos.pesquisa.php'
    
    params = {
    'formato': 'JSON',
    'pesquisa': product
    }

    result = get_data(endpoint, params)

    breakpoint()
    if result:
        print(result)
