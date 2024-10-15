# Import things that are needed generically
from langchain.tools import tool
import pymongo
import decimal
from pymongo import MongoClient
from langchain_openai import ChatOpenAI
import os
import logging
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import openai
import re
from vendor_agent import DropShotVendorAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch

# Load environment variables from a .env file if necessary
load_dotenv()

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# MongoDB URI and connection
MONGODB_URI = os.getenv("MONGODB_URI")

###############################
## MongoDB implementation
###############################

def connect_to_mongodb():
    """Establish connection to MongoDB."""
    client = pymongo.MongoClient(MONGODB_URI)
    db = client['drop']
    collection = db['drop-estoque']
    logger.info("Connected to MongoDB collection")
    return collection

# Embedding creation using OpenAI
def get_embedding(text):
    """Generate an embedding for the given text using OpenAI's API."""
    if not text or not isinstance(text, str):
        logger.error("Invalid input text for embedding generation")
        return None

    try:
        logger.info(f"Generating embedding for text: {text}")
        embedding = openai.embeddings.create(input=text, model="text-embedding-ada-002").data[0].embedding
        logger.info(f"Generated embedding: {embedding[:5]}... (truncated)")
        return embedding
    except Exception as e:
        logger.error(f"Error in get_embedding: {e}")
        return None

# Vector search in MongoDB
def vector_search(user_query, collection):
    """Perform vector search in MongoDB based on user query."""
    query_embedding = get_embedding(user_query)

    if query_embedding is None:
        logger.error("Embedding generation failed, skipping vector search.")
        return "Invalid query or embedding generation failed."

    # Log the query embedding for debugging
    logger.info(f"Query embedding: {query_embedding[:5]}... (truncated)")

    # Vector search pipeline
    pipeline = [
    {
        "$vectorSearch": {
            "index": "vector_index",  # Ensure this index exists in your MongoDB
            "queryVector": query_embedding,
            "path": "embedding",  # Use the correct embedding field
            "numCandidates": 10000,
            "limit": 5
        }
    },
    {
        "$project": {
            "Descricao": 1,  # Ensure you're referencing the correct field names
            "Preco": 1,
            "Tipo": 1,
            "Descricao_Complementar": 1,  # Include additional fields if needed
            "score": {"$meta": "vectorSearchScore"}
        }
    }
]

    # Log the pipeline before executing the search
    logger.info(f"Vector search pipeline: {pipeline}")

    # Execute search and return results
    try:
        results = list(collection.aggregate(pipeline))
        if not results:
            logger.warning("No results found during vector search.")
        else:
            logger.info(f"Vector search results: {results}")
        return results
    except Exception as e:
        logger.error(f"Error during vector search: {e}")
        return []

# Format search results into a string
def format_search_results(search_results):
    """Format search results from vector search into a user-friendly string."""
    if not search_results:
        return "No results found."

    formatted_results = "Aqui estão alguns produtos de padel disponíveis:\n\n"
    for result in search_results:
        description = result.get("Descricao", "Descrição indisponível")
        price = result.get("Preco", "Preço indisponível")
        product_type = result.get("Tipo", "Tipo indisponível")

        formatted_results += f"🌟 **{description}**\n- 💲 Preço: {price}\n- 🏷️ Tipo: {product_type}\n\n"

    return formatted_results

# Tool for vector search in Langchain
@tool
def search_items(query: str) -> str:
    """Langchain tool that searches for items in the DropShot MongoDB collection based on vector search."""
    collection = connect_to_mongodb()
    logger.info(f"Performing vector search for user query: {query}")
    search_results = vector_search(query, collection)

    if not search_results:
        return "Nenhum produto encontrado para a consulta realizada."

    # Return the formatted results
    return format_search_results(search_results)


##############################################
## SQL IMPLEMENTATION
##############################################

# # Define the RDS connection URI
# RDS_URI = f"postgresql+psycopg2://{'postgres'}:{'postgres'}@{'dropdb1.c7dhmdz5lx6x.us-east-1.rds.amazonaws.com'}:{5432}/{'dropdb1'}"

# # Create the database connection
# db = SQLDatabase.from_uri(RDS_URI)
# llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.1, verbose=True)

# # Load the SQL toolkit to use the db instance
# toolkit = SQLDatabaseToolkit(db=db, llm=llm)
# tools = toolkit.get_tools()

# # Explicitly tell the LLM about the schema of the table
# schema_prompt = """
# You are interacting with a database called 'dropdb1'. The table you will query is called 'drop_shot_inventory', and it has the following columns:

# - sku (string): The SKU of the product.
# - descricao (string): The name of the product.
# - preco (float): The price of the product.
# - unidade (string): The type of unity 'UN'.
# - estoque_fisico (integer): Available quantity of the product.
# - estoque_disponivel (integer): Available quantity of the product.

# Only write syntactically correct SQL queries. The only table you are allowed to query is 'drop_shot_inventory'. You should always limit results to 100 rows and ensure the query checks against the appropriate columns.

# ### Important Instructions:
# When the user asks for **rackets (raquetes)**, **exclude any accessories** such as racket covers (capa), racket grips (punho), racket bags (bolsa), or any other item related to rackets but **not the racket itself**.

# Focus only on products that are **explicitly rackets** and not accessories.
# """

# query_check_system = """
# You are a SQL expert with a strong attention to detail.
# Double-check the SQL query for common mistakes, including:
# - Using NOT IN with NULL values
# - Data type mismatch in predicates
# - Properly quoting identifiers
# - Using the correct number of arguments for functions
# If there are any mistakes, rewrite the query. If there are no mistakes, reproduce the original query.
# """

# # Query checking (use natural language to check for SQL syntax issues)
# query_check_system = f"{schema_prompt}\n{query_check_system}"

# query_check_prompt = ChatPromptTemplate.from_messages([("system", query_check_system), ("user", "{query}")])
# query_check = query_check_prompt | llm

# @tool
# def check_query_tool(query: str) -> str:
#     """
#     Check if the provided SQL query is valid and free from common mistakes.
#     """
#     try:
#         # Generate query and remove unnecessary content
#         checked_query = query_check.invoke({"query": query}).content

#         # Extract only the SQL query part, removing any additional explanation
#         start_idx = checked_query.find("SELECT")
#         if start_idx == -1:
#             return "Error: No valid SQL query found."
#         end_idx = checked_query.rfind("LIMIT")
#         if end_idx == -1:
#             end_idx = len(checked_query)
        
#         cleaned_query = checked_query[start_idx:end_idx].strip()

#         # Ensure the query has a LIMIT clause
#         if "LIMIT" not in cleaned_query.upper():
#             cleaned_query += " LIMIT 10"

#         logger.info(f"Cleaned SQL query: {cleaned_query}")
#         return cleaned_query

#     except Exception as e:
#         logger.error(f"Error in checking query: {e}")
#         return "Error in checking the query."

# # Add the tool for validating query results
# query_result_check_system = """You are grading the result of a SQL query. 
# - Check that the result is not empty.
# - If it is empty, provide instructions to retry."""

# query_result_check_prompt = ChatPromptTemplate.from_messages([("system", query_result_check_system), ("user", "{query_result}")])
# query_result_check = query_result_check_prompt | llm

# @tool
# def check_result(query_result: str) -> str:
#     """
#     Check the query result to confirm it is not empty or irrelevant.
#     """
#     try:
#         checked_result = query_result_check.invoke({"query_result": query_result}).content
#         return checked_result
#     except Exception as e:
#         logger.error(f"Error in checking result: {e}")
#         return "Error in checking the query result."


# # Function to extract keywords from the user query
# def extract_keywords(user_query: str) -> list:
#     """
#     Extract potential keywords from the user query.
#     This function is a simple example using regex to find words in the query.
#     You can improve this by using NLP techniques to extract relevant product keywords.
#     """
#     # Find all words in the user query
#     words = re.findall(r'\b\w+\b', user_query.lower())
    
#     # Example: You can enhance this by filtering out common words or stopwords
#     # For now, we'll assume all words are relevant
#     return words

# # Function to filter out accessory-related products
# def filter_accessories(results: list) -> list:
#     """
#     Filter out accessory-related products from the query results, 
#     such as grips, covers, or bags, and only return actual rackets.
#     """
#     accessory_keywords = ['grip', 'bag', 'cover', 'capa', 'punho', 'acessorio', 'kit']

#     # Filter out rows where the 'descricao' contains accessory-related keywords
#     filtered_results = [row for row in results if not any(acc in row['descricao'].lower() for acc in accessory_keywords)]

#     # Additionally, ensure that the term 'raquete' is present in the description
#     filtered_results = [row for row in filtered_results if 'raquete' in row['descricao'].lower()]

#     return filtered_results


# # Define the SQL query execution and product search function with proper handling of SQL results.
# @tool
# def search_products(query: str) -> str:
#     """
#     Search for products in the 'drop_shot_inventory' table using a SQL query.
#     """
#     try:
#         # Extract keywords from the user query
#         keywords = extract_keywords(query)

#         if not keywords:
#             return "No valid keywords found in the query."

#         # Create a SQL query using the extracted keywords
#         like_clauses = " OR ".join([f"descricao ILIKE '%{word}%'" for word in keywords])

#         # Ensure query is limited to 100 results
#         sql_query = f"SELECT * FROM drop_shot_inventory WHERE {like_clauses} LIMIT 100"

#         # Check if the query is valid before execution
#         checked_query = check_query_tool(sql_query)
#         if "Error" in checked_query:
#             return checked_query

#         logger.info(f"Executing SQL query: {checked_query}")

#          # Execute the query
#         results = db.run(checked_query)

#         # Log the type and content of the result for debugging
#         logger.info(f"Query Results: {results}")
#         logger.info(f"Results Type: {type(results)}")

#         # Check if results are found
#         if not results:
#             return "No products found for the given query."

#         # Log the first row to examine the format
#         if results:
#             logger.info(f"First row of results: {results[0]}")

#         # Dynamically process the results
#         result_str = "Here are the top products:\n"
#         for row in results:
#             result_str += f"{row}\n"  # Log each row without assumptions

#         return result_str

#     except Exception as e:
#         logger.error(f"Error executing SQL query: {e}")
#         return "There was an error while searching for products."

# DROP_SHOT_ITEMS = [
#     {
#         "name": "Raquete DROP SHOT SPEKTRO 8.0 BT",
#         "category": "Raquete",
#         "price": "R$ 949,90",
#         "description": "Raquete de beach tennis fabricada com Carbono 18K e EVA Tech, ideal para jogadores que buscam controle absoluto e potência em suas jogadas."
#     },
#     {
#         "name": "Raquete DROP SHOT PREMIUM TECH BT",
#         "category": "Raquete",
#         "price": "R$ 1.567,41",
#         "description": "Raquete de beach tennis com Carbono 18K e sistema anti-vibração, perfeita para jogadores avançados que buscam máxima performance."
#     },
#     {
#         "name": "Raquete DROP SHOT CENTAURO 5.0 BT",
#         "category": "Raquete",
#         "price": "R$ 1.662,41",
#         "description": "Raquete de beach tennis equipada com tecnologias de rigidez e controle, ideal para jogadores profissionais."
#     },
#     {
#         "name": "Raquete DROP SHOT AMBITION PRO 2.0",
#         "category": "Raquete",
#         "price": "R$ 1.899,91",
#         "description": "Raquete de alta performance com design inovador e máxima durabilidade, desenvolvida para jogadores que buscam controle e potência."
#     },
#     {
#         "name": "Bola Oficial DROP SHOT Terno",
#         "category": "Bola",
#         "price": "R$ 75,91",
#         "description": "Bola de Beach Tennis aprovada pela ITF, projetada para proporcionar o melhor desempenho nas quadras de areia."
#     },
#     {
#         "name": "Bola de Beach Tennis DROP SHOT Pro",
#         "category": "Bola",
#         "price": "R$ 85,90",
#         "description": "Bola de beach tennis com alta durabilidade e excelente controle, ideal para treinos e competições."
#     },
#     {
#         "name": "Raqueteira DROP SHOT SIBI",
#         "category": "Raqueteira",
#         "price": "R$ 759,91",
#         "description": "Raqueteira com compartimentos ventilados para calçados e raquetes, ideal para transportar seu equipamento com segurança e estilo."
#     },
#     {
#         "name": "Raqueteira DROP SHOT BENTOR LIMA",
#         "category": "Raqueteira",
#         "price": "R$ 997,41",
#         "description": "Projetada com materiais resistentes e compartimentos organizados, oferecendo espaço e proteção para os seus itens."
#     },
#     {
#         "name": "Raqueteira DROP SHOT AIRAM JMD",
#         "category": "Raqueteira",
#         "price": "R$ 1.049,90",
#         "description": "Raqueteira de alta capacidade, com design sofisticado e múltiplos compartimentos para máxima organização e proteção dos equipamentos."
#     },
#     {
#         "name": "Tênis DROP SHOT CAYENNE",
#         "category": "Vestuário",
#         "price": "R$ 569,91",
#         "description": "Tênis com tecnologia de amortecimento e aderência para movimentos ágeis nas quadras, perfeito para jogadores de beach tennis."
#     },
#     {
#         "name": "Tênis DROP SHOT ABIAN CAMPA",
#         "category": "Vestuário",
#         "price": "R$ 999,90",
#         "description": "Usado pelo jogador Lucas Campagnolo, oferece segurança, conforto e estabilidade para máxima performance no padel."
#     },
#     {
#         "name": "Tênis DROP SHOT BENARA LIMA",
#         "category": "Vestuário",
#         "price": "R$ 949,91",
#         "description": "Combina design moderno com tecnologias avançadas de suporte e amortecimento, ideal para intensos jogos de beach tennis."
#     },
#     {
#         "name": "Camiseta DROP SHOT TECH DRY",
#         "category": "Vestuário",
#         "price": "R$ 159,90",
#         "description": "Camiseta com tecnologia de secagem rápida e tecido respirável, proporcionando conforto em treinos e jogos."
#     },
#     {
#         "name": "Shorts DROP SHOT PRO PLAYER",
#         "category": "Vestuário",
#         "price": "R$ 199,90",
#         "description": "Shorts esportivo com ajuste perfeito e tecido leve, ideal para movimentos rápidos e precisos nas quadras."
#     },
#     {
#         "name": "Boné DROP SHOT SUN PROTECT",
#         "category": "Acessório",
#         "price": "R$ 89,90",
#         "description": "Boné com proteção UV e tecido respirável, ideal para proteger durante os treinos ao ar livre."
#     },
#     {
#         "name": "Munhequeira DROP SHOT COMFORT",
#         "category": "Acessório",
#         "price": "R$ 49,90",
#         "description": "Munhequeira com tecido absorvente e ajuste confortável, ideal para oferecer suporte extra durante o jogo."
#     },
#     {
#         "name": "Corda DROP SHOT POWER STRIKE",
#         "category": "Acessório",
#         "price": "R$ 59,90",
#         "description": "Corda de alta durabilidade para raquetes, proporcionando maior potência e controle nos golpes."
#     },
#     {
#         "name": "Mochila DROP SHOT SPORT",
#         "category": "Acessório",
#         "price": "R$ 349,90",
#         "description": "Mochila com múltiplos compartimentos, ideal para transporte de raquetes, roupas e acessórios de forma prática e segura."
#     },
#     {
#         "name": "Bolsa DROP SHOT URBAN",
#         "category": "Acessório",
#         "price": "R$ 299,90",
#         "description": "Bolsa esportiva estilosa com espaço para todos os seus pertences, perfeita para uso dentro e fora das quadras."
#     },
#     {
#         "name": "Grip DROP SHOT TACKY FEEL",
#         "category": "Acessório",
#         "price": "R$ 29,90",
#         "description": "Grip com aderência superior, proporcionando maior conforto e firmeza na pegada durante o jogo."
#     }
# ]

# def connect_to_mongodb():
#     """Establish connection to MongoDB."""
#     client = pymongo.MongoClient(MONGODB_URI)
#     db = client['drop']
#     collection = db['estoque-test']
#     return collection

# @tool
# def item_lookup(query: str, n: int = 10) -> str:
#     """Fetch item details based on the query using vector search."""
#     collection = connect_to_mongodb()

#     # MongoDB vector search configuration
#     db_config = {
#         "collection": collection,
#         "indexName": "vector_index1",
#         "textKey": "embedding_text",
#         "embeddingKey": "embedding",
#     }

#     # Create vector store with OpenAI embeddings
#     vector_store = MongoDBAtlasVectorSearch(
#         OpenAIEmbeddings(),
#         db_config
#     )

#     # Perform similarity search with score
#     results = vector_store.similarity_search_with_score(query, n)

#     return str(results)


# def connect_to_mongodb():
#     client = pymongo.MongoClient(MONGODB_URI)
#     db = client['drop_cluster']
#     collection = db['estoque-test-v1']
#     return collection

# def itens_lookup(query: str, n: int = 5):
#     collection = connect_to_mongodb()
    
#     # Configurations for the vector store (indexing and embedding fields)
#     db_config = {
#         "collection": collection,
#         "indexName": "vector_index",
#         "textKey": "embedding_text",
#         "embeddingKey": "embedding"
#     }
    
#     # Perform vector search using OpenAI embeddings
#     vector_store = MongoDBAtlasVectorSearch(
#         OpenAIEmbeddings(),
#         db_config
#     )
    
#     # Search for results
#     results = vector_store.similarity_search_with_score(query, n)
#     return results

# # Tool for item lookup
# @tool
# def get_itens(query: str) -> str:
#     """
#         Fetches items available for sale on the DropShot website.
#     """
#     results = itens_lookup(query)
#     print(f"Lookup results: {results}")  # Debugging log
#     return f"Results: {results}"

# @tool
# def get_itens() -> str:
#     """
#         Busca os itens disponíveis para a venda no site da DropShot.   
#     """
#     return DROP_SHOT_ITEMS