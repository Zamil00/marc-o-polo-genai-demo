import numpy as np
from embeddings import embed_text

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query, faq_data, faq_embeddings, top_k=1):
    query_embedding = embed_text(query)
    similarities = [
        cosine_similarity(query_embedding, emb)
        for emb in faq_embeddings
    ]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [faq_data[i] for i in top_indices]
