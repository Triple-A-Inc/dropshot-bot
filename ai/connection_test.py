import pymongo

MONGODB_URI = "mongodb+srv://luciano:Gn1hrhRcH5nh3KlM@drop-cluster.uxszu.mongodb.net/?retryWrites=true&w=majority&appName=drop-cluster"


def test_mongodb_connection():
    try:
        client = pymongo.MongoClient(MONGODB_URI)
        db = client['drop_cluster']
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

test_mongodb_connection()