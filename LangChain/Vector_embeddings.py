import json
import os
from pinecone import Pinecone
from pinecone import Pinecone, ServerlessSpec

with open("cleaned_courses.json", "r", encoding="utf-8") as f:
    courses = json.load(f)

# text for embeddings
texts = [
    f"{course['title']} {course['description']} Price: {course.get('Price Per Session', 'N/A')}, "
    f"Lessons: {course.get('Lessons', 'N/A')}, Total Cost: {course.get('Total Cost', 'N/A')}"
    for course in courses
]

from sentence_transformers import SentenceTransformer

# embedding model
device = "cpu"
model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
embeddings = model.encode(texts, normalize_embeddings=True) # generating embeddings

pc = Pinecone(api_key="pcsk_5juGvg_KyoP7ij5FaZLLvSFtuKhmapdJfzdfKarDZULmLzcZU1kXD51iNqtN9SrBELTiJc")
index_name = "course-details-search"

# i am deleting the previous index , cz i faced errors with dimensions mismatch error

if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)

# creating index with the correct dimension (384) as i was using all-MiniLM-L6-v2 model , which gives only 384 dimension vectors
# intially , i created 1024 dimensions , so i got the dimensions mismatch error, so i changed it to 384
pc.create_index(
    name=index_name,
    dimension=384,  # Matches the embedding model output
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)

index = pc.Index(index_name)
vectors = [(str(i), embeddings[i].tolist(), courses[i]) for i in range(len(courses))]
index.upsert(vectors)

print("Embeddings stored in Pinecone successfully!")