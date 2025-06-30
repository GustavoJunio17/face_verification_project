import chromadb
from chromadb.config import Settings
import os

persist_dir = os.path.abspath("chroma_db")
client = chromadb.Client(Settings(persist_directory=persist_dir, is_persistent=True))
collection = client.get_or_create_collection(name="faces")

def get_all_users():
    return collection.get(include=["metadatas", "embeddings"])

def add_user_to_collection(user_id, embedding, metadata):
    collection.add(ids=[user_id], embeddings=[embedding], metadatas=[metadata])