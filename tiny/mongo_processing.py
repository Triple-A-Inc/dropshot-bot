from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

uri = "mongodb+srv://luciano:Gn1hrhRcH5nh3KlM@drop-cluster.uxszu.mongodb.net/?retryWrites=true&w=majority&appName=drop-cluster"

client = MongoClient(uri, server_api=ServerApi('1'))

df = pd.read_csv('/Users/beylouni/Downloads/vendasdropestoque - Página2.csv')

data = df.to_dict(orient='records')

collections = [
    "estoque-test-v1",
    "estoque-test"
]

db = client['drop']
collection = db[collections[0]]

try:
    collection.insert_many(data)
    print("Data inserted successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()