from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
# from google.generativeai import GenerativeModel
import os
import numpy as np
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Load embedding model
device = "cpu"
model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

# Initialize Pinecone

pc = Pinecone(api_key="YOUR_API_KEY")
index_name = "course-details-search"
index = pc.Index(index_name)

# Initialize Memory to Store Chat History
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

gemini_api_key = "YOUR_API_KEY"
genai.configure(api_key=gemini_api_key)

llm = genai.GenerativeModel(model_name="gemini-1.5-flash-002")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get JSON input
        data = request.json
        user_query = data.get("query", "").strip()
        if not user_query:
            return jsonify({"error": "Query is required"}), 400

        # Convert query to embedding
        query_embedding = model.encode([user_query], normalize_embeddings=True)

        # Search in Pinecone
        query_results = index.query(vector=query_embedding.tolist(), top_k=5, include_metadata=True)

        # Extract retrieved course data
        retrieved_data = "\n".join([
            f"Title: {match['metadata'].get('title', 'N/A')}\n"
            f"Description: {match['metadata'].get('description', 'N/A')}\n"
            f"Price: {match['metadata'].get('Price Per Session', 'N/A')}\n"
            f"Lessons: {match['metadata'].get('Lessons', 'N/A')}\n"
            f"Total Cost: {match['metadata'].get('Total Cost', 'N/A')}\n"
            for match in query_results["matches"]
        ])

        # Generate response using Gemini with context
        prompt = f"You are an AI assistant for course recommendations. Answer based on the following course data:\n\n{retrieved_data}\n\nUser: {user_query}\nAssistant:"
        response = llm.generate_content(prompt)
        response_text = response.text if response else "Sorry, I couldn't generate a response."

        # Store conversation in memory
        memory.save_context({"input": user_query}, {"output": response_text})

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "API is running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
