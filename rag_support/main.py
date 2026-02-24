from embeddings import load_faq, build_embedding_index
from retriever import retrieve
from generator import generate_response

faq_data = load_faq("faq_data.json")
faq_embeddings = build_embedding_index(faq_data)

print("AI Fashion Support Assistant (type 'exit' to quit)")

while True:
    query = input("\nCustomer question: ")
    if query.lower() == "exit":
        break

    retrieved = retrieve(query, faq_data, faq_embeddings)
    answer = generate_response(query, retrieved)

    print("\nAI Response:\n")
    print(answer)
    print("\n" + "-"*50 + "\n")
