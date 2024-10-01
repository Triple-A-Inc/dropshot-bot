import os
from dotenv import load_dotenv
import openai
import pymongo
from openai import OpenAI
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch

# Load environment variables from a .env file
load_dotenv()

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = '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'

MONGODB_URI = "mongodb+srv://luciano:Gn1hrhRcH5nh3KlM@drop-cluster.uxszu.mongodb.net/?retryWrites=true&w=majority&appName=drop-cluster"

openai_client = OpenAI()

# Initialize MongoDB client
client = MongoClient(MONGODB_URI)
db = client["drop"]
collection = db["estoque-test"]

# Function to generate embedding using OpenAI
def generate_embedding(text):
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    # Check the structure of the response object
    print(response)  # To understand the structure of the response

    # Assuming the data is accessed as an attribute, not as a dictionary
    embedding_data = response.data[0].embedding  # Corrected access pattern
    return embedding_data

# Function to update documents with embedding_text and embedding fields
def update_documents():
    documents = collection.find()  # Find all documents
    total_docs = collection.count_documents({})
    print(f"Found {total_docs} documents in the collection.")

    if total_docs == 0:
        print("No documents to update.")
        return
    
    for doc in documents:
        descricao = doc.get("descricao")
        if descricao:
            print(f"Processing document with _id: {doc['_id']} and descricao: {descricao}")

            # Generate embedding for 'descricao'
            embedding = generate_embedding(descricao)

            # Create new fields to be added to the document
            update_data = {
                "embedding_text": descricao,
                "embedding": embedding
            }

            # Update the document with the new fields
            result = collection.update_one(
                {"_id": doc["_id"]},
                {"$set": update_data}
            )

            if result.modified_count > 0:
                print(f"Successfully updated document ID {doc['_id']}.")
            else:
                print(f"Document ID {doc['_id']} was not updated.")
        else:
            print(f"Document ID {doc['_id']} has no 'descricao' field.")

# Run the update
update_documents()