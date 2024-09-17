import requests
from dotenv import load_dotenv
import os

# Get env vars
load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')


def get_data(endpoint, params=None):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    url = f'{BASE_URL}{endpoint}'
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error {response.status_code}: {response.text}')
        return None
    

def post_data(endpoint, data):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    url = f'{BASE_URL}{endpoint}'
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()
    else:
        print(f'Error {response.status_code}: {response.text}')
        return None


if __name__ == '__main__':
    endpoint = 'your_endpoint_here'
    params = {
        'param1': 'value1',
        'param2': 'value2'
    }
    data = get_data(endpoint, params)

    if data:
        print(data)
