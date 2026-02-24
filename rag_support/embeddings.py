import json
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_faq(path):
    with open(path, "r") as f:
        return json.load(f)

def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)

def build_embedding_index(faq_data):
    embeddings = []
    for item in faq_data:
        combined = item["question"] + " " + item["answer"]
        emb = embed_text(combined)
        embeddings.append(emb)
    return np.vstack(embeddings)
