# Module 3 — AI Automation Workflow (Concept)

## Use case
**New product created** in the Product Information Management (PIM) system triggers an automated GenAI workflow to generate:
- Product description (DE/EN)
- SEO metadata (meta title/description)
- Feature bullets
- Optional creative prompts for image generation (for Marketing/Design)

Then routes results to the right tools and people for review & publishing.

---

## End-to-end flow (example)

1. **Trigger (PIM / CMS)**
   - Event: *New product created* or *Product updated*
   - Payload: `product_id, name, material, fit, color, sustainability, details, category`

2. **Validation / Data Hygiene**
   - Ensure required fields exist
   - Normalize text (trim, remove HTML)
   - If missing critical fields → create task for merch team

3. **GenAI Step 1 — Product Copy (LLM)**
   - Structured prompt (JSON output)
   - Outputs: short + SEO description, 5 bullets, meta title/description
   - Language: DE & EN
   - Guardrails: no invented certifications/claims

4. **GenAI Step 2 — Optional Creative Prompt Pack**
   - “Prompt recipes” for Midjourney / DALL·E use
   - Includes style, lighting, composition constraints
   - Output stored for marketing, not auto-published

5. **Routing**
   - Save copy to **Notion** (content hub) or CMS draft
   - Attach product_id + version + timestamp
   - Notify **Slack** channel (Marketing / E-Com)
   - Create **email draft** for merch review if needed

6. **Human-in-the-loop Review**
   - Reviewer edits in Notion/CMS
   - Approve / Reject
   - If rejected: feedback stored for prompt iteration

7. **Publish**
   - Approved copy pushed to CMS/PIM
   - Audit log updated (who approved, when, what changed)

---

## Tools (example options)
- **Automation Orchestrator:** Make.com or Zapier
- **Content Hub:** Notion
- **Messaging:** Slack / MS Teams
- **LLM:** OpenAI / Claude (API)
- **Image Gen:** Midjourney / DALL·E (human-operated step)

---

## Data contract (minimal)
```json
{
  "product_id": "string",
  "name": "string",
  "material": "string",
  "fit": "string",
  "color": "string",
  "sustainability": "string",
  "additional_details": "string"
}
```

---

## Reliability & Governance
- **Versioning:** store `prompt_version` + `model` + `timestamp`
- **Logging:** input payload hash + output JSON
- **PII:** do not include customer PII in prompts
- **Safety:** reject outputs containing banned claims (e.g., certifications not provided)
- **Fallbacks:** if LLM fails → create task + notify

---

## KPIs (measurable impact)
- Time-to-market for new products (minutes saved per product)
- % of copy requiring edits (quality)
- SEO metrics uplift (CTR, dwell time)
- Support reduction (fewer questions due to clearer copy)
- Consistency score (tone/style checks)

---

## Next step for production
- Connect to real PIM/CMS webhooks
- Add approval UI + role-based permissions
- Add brand tone checks (embedding similarity to reference copy)
- Add A/B testing for generated copy variants
