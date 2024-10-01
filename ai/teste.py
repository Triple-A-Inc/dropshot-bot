import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import pymongo

# Load environment variables from a .env file
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

# Check MongoDB Documents for required fields
def check_mongodb_documents():
    collection = connect_to_mongodb()
    
    # Check a sample of documents
    print("Checking MongoDB Documents...")
    sample_docs = collection.find().limit(5)
    for idx, doc in enumerate(sample_docs):
        print(f"\nDocument {idx+1}:")
        print(f"ID: {doc.get('_id')}")
        print(f"Text: {doc.get('embedding_text', 'Field missing')}")
        print(f"Embedding: {doc.get('embedding', 'Field missing')}")
    
    print("\nEnsure that 'embedding_text' and 'embedding' fields are present and valid.")

# Generate an embedding and compare with stored ones in MongoDB
def check_embedding_consistency(query: str):
    collection = connect_to_mongodb()
    
    # Generate an embedding for the query
    embeddings = OpenAIEmbeddings()
    query_embedding = embeddings.embed_query(query)
    print(f"\nGenerated Embedding for Query '{query}': {query_embedding[:5]}... (truncated)")

    # Retrieve a document's embedding from MongoDB for comparison
    sample_doc = collection.find_one({'embedding_text': {'$exists': True}})
    
    if sample_doc:
        stored_embedding = sample_doc.get('embedding', None)
        if stored_embedding:
            print(f"\nStored Embedding in MongoDB for Document '{sample_doc.get('_id')}': {stored_embedding[:5]}... (truncated)")
            
            # You could calculate similarity between generated embedding and stored embedding
            from numpy import dot
            from numpy.linalg import norm

            similarity = dot(query_embedding, stored_embedding) / (norm(query_embedding) * norm(stored_embedding))
            print(f"Similarity between query embedding and stored embedding: {similarity}")
        else:
            print("Error: No embedding field found in the retrieved document.")
    else:
        print("Error: No documents with 'embedding_text' found in MongoDB.")

# Run the tests
def run_tests():
    # Check MongoDB documents
    check_mongodb_documents()

    # Test embedding consistency
    query = "beach tennis raquete"
    check_embedding_consistency(query)

# Run the tests
if __name__ == "__main__":
    run_tests()