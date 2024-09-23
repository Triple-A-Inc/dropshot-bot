import requests
from dotenv import load_dotenv
import os

from models import ParamSearchProduct, ParamGetSupply, SupplyReturnObject, GetProductReturnObject

# Get env vars
load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

ReturnType = SupplyReturnObject | GetProductReturnObject

class TinyConsultant:
    def __init__(self, token: str, return_format: str = 'JSON'):
        self.token = token
        self.return_format = return_format

    def search_products(self, params: ParamSearchProduct) -> GetProductReturnObject:
        # TODO
        # return_obj = _parse_return(...)
        # return return_obj
        pass

    def get_supply(self, params: ParamGetSupply) -> SupplyReturnObject:
        # TODO
        # return_obj = _parse_return(...)
        # return return_obj
        pass

    def _parse_return(self, function_called: str, ) -> ReturnType:
        # Acts in between the get function and its real return.
        # TODO
        pass



if __name__ == '__main__':
    pass