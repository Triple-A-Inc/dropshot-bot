import requests
from dotenv import load_dotenv, find_dotenv
import os

from models import ParamSearchProduct, ParamGetSupply, SupplyReturnObject, GetProductReturnObject

class TinyConsultant:
    def __init__(self, token: str, return_format: str = 'JSON', base_url: str = 'https://api.tiny.com.br/api2/'):
        self.token = token
        self.return_format = return_format
        self.base_url = base_url

        self.search_product_url = f'{self.base_url}produtos.pesquisa.php'
        self.get_stock_url = f'{self.base_url}produtos.pesquisa.php'

    def search_product(self, params: ParamSearchProduct, headers={}) -> GetProductReturnObject:
        url = self.search_product_url
        
        breakpoint()
        try:
            response = requests.post(url, data=params.model_dump_json(), headers=headers)
            
            breakpoint()
            # Raise an error if the request failed
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Problema com {url}, {str(e)}")
        

        breakpoint()
        # TODO
        # return_obj = _parse_return(...)
        # return return_obj
        pass

    def get_supply(self, params: ParamGetSupply, headers={}) -> SupplyReturnObject:
        # TODO
        # return_obj = _parse_return(...)
        # return return_obj
        pass

    def _parse_return(self, function_called: str) -> SupplyReturnObject | GetProductReturnObject:
        # Acts in between the get function and its real return.
        # TODO
        pass



if __name__ == '__main__':
    # Get env vars
    load_dotenv(find_dotenv())

    API_KEY = os.getenv('API_KEY')
    BASE_URL = os.getenv('BASE_URL')

    Consultant = TinyConsultant(API_KEY)

    product_name = 'Agasalho DROP SHOT AIRAM JMD'
    product_info = Consultant.search_product(
        ParamSearchProduct(
            token=Consultant.token,
            formato=Consultant.return_format,
            pesquisa=product_name
        )
    )


    # endpoint = 'produtos.pesquisa.php'
    
    # params = {
    # 'formato': 'JSON',
    # 'pesquisa': product
    # }

    # result = get_data(endpoint, params)
    # if result:
    #     print(result)
    # pass