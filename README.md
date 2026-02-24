# 🚀 Generative AI Prototype – Fashion Retail RAG Assistant

This project demonstrates how Generative AI can be embedded into a fashion retail environment to create measurable business value.

Built as a practical prototype inspired by Marc O’Polo’s Generative AI use cases, the system implements a Retrieval-Augmented Generation (RAG) architecture combining semantic search with LLM-based response generation to ensure accurate and brand-consistent answers.

---

## 🎯 Use Case

AI-powered customer support assistant for fashion retail.

The system:
- Embeds internal FAQ knowledge
- Performs semantic retrieval
- Generates context-aware responses using an LLM
- Maintains consistent brand tone

---

## 🧠 Architecture

1. FAQ Embedding (text-embedding-3-small)
2. Semantic Similarity Search (Cosine Similarity)
3. Context Injection
4. GPT-4o-mini Response Generation
5. Optional Embedding Caching for cost efficiency

---

## 💼 Business Impact

- ⚡ Faster customer response time
- 🎯 Context-aware and accurate answers
- 🧠 Brand-consistent communication
- 📈 Scalable architecture for multilingual expansion
- 🔄 Ready to integrate into internal ChatGPT systems
- 💰 Reduced manual workload in support teams

---

## 🛠 Tech Stack

- Python
- OpenAI API
- NumPy
- python-dotenv
- Modular RAG Architecture

---

## ▶️ Demo Example

**Customer:**  
HOW LONG DOES SHIPPING TAKE IN GERMANY?

**Assistant:**  
Shipping within Germany typically takes 2–4 business days. If you have any further questions or need assistance with your order, please feel free to reach out.

---

## ⚙️ Setup

1. Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate   # Mac
