from flask import Flask, jsonify
from services.mongo_service import insert_data, get_data
from services.pg_service import insert_message, get_messages
import requests
from bson import ObjectId  # Import this to handle MongoDB ObjectId serialization

# Initialize Flask app
app = Flask(__name__)

# Helper function to serialize MongoDB documents
def serialize_mongo(doc):
    """
    Converts MongoDB's ObjectId to string for JSON serialization.
    """
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc

# Root endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Hello World"})

# POST endpoint to call external API, save data to MongoDB and PostgreSQL
@app.route('/api/hello', methods=['POST'])
def hello_world():
    try:
        # Call an external API
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        api_data = response.json()

        # Insert data into MongoDB
        mongo_id = insert_data("hello_collection", {"api_data": api_data, "message": "Hello from MongoDB!"})

        # Insert data into PostgreSQL
        pg_id = insert_message("Hello from PostgreSQL!")

        return jsonify({
            "message": "Hello, World!",
            "mongo_id": str(mongo_id),
            "postgres_id": pg_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET endpoint to fetch messages from MongoDB and PostgreSQL
@app.route('/api/messages', methods=['GET'])
def get_all_messages():
    try:
        # Retrieve data from MongoDB and serialize
        mongo_docs = get_data("hello_collection")
        serialized_mongo_docs = [serialize_mongo(doc) for doc in mongo_docs]

        # Retrieve data from PostgreSQL
        pg_messages = get_messages()

        return jsonify({
            "mongo_docs": serialized_mongo_docs,
            "postgres_messages": pg_messages
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Main block to run the app
if __name__ == "__main__":
    app.run(debug=True)
