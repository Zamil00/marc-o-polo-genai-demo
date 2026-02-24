from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(query, retrieved_docs):
    context = "\n".join([doc["answer"] for doc in retrieved_docs])

    prompt = f"""
You are a customer support assistant for a premium Scandinavian fashion brand.

Use the context below to answer professionally and clearly.

Context:
{context}

Customer question:
{query}

Respond in a helpful and brand-consistent tone.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
