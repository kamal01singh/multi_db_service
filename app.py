from flask import Flask, jsonify
from services.mongo_service import insert_data, get_data
from services.pg_service import insert_message, get_messages
import requests
from bson import ObjectId  

app = Flask(__name__)

def serialize_mongo(doc):
    """
    Converts MongoDB's ObjectId to string for JSON serialization.
    """
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Hello World"})

@app.route('/api/hello', methods=['POST'])
def hello_world():
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        api_data = response.json()

        mongo_id = insert_data("hello_collection", {"api_data": api_data, "message": "Hello from MongoDB!"})

        pg_id = insert_message("Hello from PostgreSQL!")

        return jsonify({
            "message": "Hello, World!",
            "mongo_id": str(mongo_id),
            "postgres_id": pg_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/messages', methods=['GET'])
def get_all_messages():
    try:
        mongo_docs = get_data("hello_collection")
        serialized_mongo_docs = [serialize_mongo(doc) for doc in mongo_docs]

        pg_messages = get_messages()

        return jsonify({
            "mongo_docs": serialized_mongo_docs,
            "postgres_messages": pg_messages
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
