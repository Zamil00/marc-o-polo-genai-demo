# 🚀 Generative AI Prototypes – Fashion Retail Use Cases

A set of practical Generative AI prototypes inspired by modern fashion retail workflows (e.g., Marc O’Polo context).

The focus is on **real business value**, combining:

- Retrieval-Augmented Generation (RAG)
- Structured Prompt Engineering
- Automation-ready AI integration
- Governance & measurable KPIs

---

## ✅ Modules Overview

- **Module 1 — RAG Fashion Support Assistant**
- **Module 2 — Product Description Generator (DE/EN, SEO, JSON)**
- **Module 3 — Automation Workflow Concept**

---

# Module 1 — RAG Fashion Support Assistant

## 🎯 Use Case

AI-powered customer support assistant for fashion retail.

The system:

- Embeds internal FAQ knowledge  
- Performs semantic similarity search  
- Injects context into LLM prompts  
- Generates brand-consistent responses  
- Supports cost-efficient embedding caching  

## 🧠 Architecture

1. FAQ Embedding (`text-embedding-3-small`)
2. Cosine Similarity Retrieval
3. Context Injection
4. LLM Response Generation (`gpt-4o-mini`)
5. Optional Embedding Cache (NumPy)

## 💼 Business Impact

- ⚡ Faster customer response time  
- 🎯 Context-aware and accurate answers  
- 🧠 Consistent brand tone  
- 📈 Scalable for multilingual expansion  
- 🔄 Ready for internal ChatGPT integration  
- 💰 Reduced manual workload in support teams  

## ▶️ Demo Example

**Customer:**  
HOW LONG DOES SHIPPING TAKE IN GERMANY?

**Assistant:**  
Shipping within Germany typically takes 2–4 business days.

---

# Module 2 — Product Description Generator (LLM)

A structured prompt pipeline generating **brand-consistent, SEO-ready product copy** in **DE/EN** with strict JSON output validation.

## Generates

- Short description (≤ 60 words)  
- SEO description (~150 words)  
- 5 feature bullets  
- Meta title (≤ 60 characters)  
- Meta description (≤ 155 characters)  

## Example Output Structure

```json
{
  "short_description": "...",
  "seo_description": "...",
  "features": ["...", "...", "...", "...", "..."],
  "meta_title": "...",
  "meta_description": "..."
}

## Run (from repo root)

```bash
python3 product_generator/cli.py --input product_generator/sample_products.json --lang DE
python3 product_generator/cli.py --input product_generator/sample_products.json --lang EN
```

Outputs:

- `product_generator/out/generated_copy_DE.json`
- `product_generator/out/generated_copy_EN.json`

---

# Module 3 — Automation Workflow Concept

A practical GenAI automation architecture for product workflows.

## Flow Overview

New product created  
→ LLM generates copy (DE/EN)  
→ Content routed to Notion / CMS draft  
→ Slack notification sent  
→ Human approval  
→ Publish + audit logging  

## Included

- `automation_concept/workflow.md`
- `automation_concept/architecture.png`

## Governance & Reliability

- Prompt versioning  
- Model logging  
- Output validation  
- Human-in-the-loop approval  
- KPI tracking  

## KPIs (Measurable Impact)

- Time-to-market reduction  
- % of manual edits required  
- SEO performance uplift  
- Copy consistency metrics  
- Operational workload reduction  

---

# 🛠 Tech Stack

- Python  
- OpenAI API  
- NumPy  
- python-dotenv  
- Modular architecture design  
- Structured JSON validation  

---

# ⚙️ Setup (All Modules)

## 1️⃣ Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

## 3️⃣ Create `.env` file in repo root

```bash
OPENAI_API_KEY=your_api_key_here
```

---

# ▶️ Run

## Module 1

```bash
cd rag_support
python3 main.py
```

## Module 2

```bash
python3 product_generator/cli.py --input product_generator/sample_products.json --lang DE
```

---

# 🎯 Positioning

These prototypes demonstrate:

- Practical RAG implementation  
- Structured LLM prompting  
- Multilingual generation  
- Business-oriented AI automation thinking  
- Governance-aware AI integration  

Designed as a realistic showcase of how Generative AI can be embedded into fashion retail operations.