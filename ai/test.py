# Import things that are needed generically
from langchain.tools import tool
import pymongo
import os
from dotenv import load_dotenv
from pymongo import MongoClient
# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings

# Load environment variables from a .env file (if using one)
load_dotenv()

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = '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'

MONGODB_URI = "mongodb+srv://luciano:Gn1hrhRcH5nh3KlM@drop-cluster.uxszu.mongodb.net/?retryWrites=true&w=majority&appName=drop-cluster"

# MongoDB Connection Configuration
def connect_to_mongodb():
    client = pymongo.MongoClient(MONGODB_URI)
    db = client['drop_cluster']
    collection = db['estoque-test-v1']
    return collection

def itens_lookup(query: str, n: int = 5):
    collection = connect_to_mongodb()
    
    # Debug: print the first few documents in the collection
    print("Sample documents from collection:")
    sample_docs = collection.find().limit(5)
    for doc in sample_docs:
        print(doc)
    
    # Configurations for the vector store (indexing and embedding fields)
    db_config = {
        "collection": collection,           # MongoDB collection
        "index_name": "vector_index",       # Index name for vector search
        "text_key": "embedding_text",       # Field in the document for the text
        "embedding_key": "embedding"        # Field in the document for the embedding
    }
    
    # Perform vector search using OpenAI embeddings
    embeddings = OpenAIEmbeddings()
    vector_store = MongoDBAtlasVectorSearch(
        embedding=embeddings,     # Embedding model
        collection=db_config['collection'],  # MongoDB collection
        index_name=db_config['index_name'],  # Index name for vector search
        text_key=db_config['text_key'],      # Field containing the text
        embedding_key=db_config['embedding_key']  # Field containing the embedding
    )
    
    # Search for results
    results = vector_store.similarity_search_with_score(query, n)
    return results

# Test the function with a sample query
def test_itens_lookup():
    query = "raquete"
    try:
        results = itens_lookup(query)
        print(f"Query: {query}")
        print(f"Results: {results}")
    except Exception as e:
        print(f"Error during lookup: {e}")

# Run the test
test_itens_lookup()