from __future__ import annotations
import json
import streamlit as st

from config import Settings
from llm_client import LLMClient
from registry import list_prompts, load_prompt, render_user
from eval_engine import evaluate_product_copy
from cost import estimate_tokens
from db import log_run

st.set_page_config(page_title="Retail AI Studio", layout="wide")

st.title("Retail AI Studio — GenAI Experimentation & Optimization")
st.caption("Prompt versioning • evaluation • guardrails • cost tracking • agent mode")

settings = Settings()
try:
    llm = LLMClient(settings)
except Exception as e:
    st.error(str(e))
    st.stop()

st.sidebar.header("Controls")
models = st.sidebar.multiselect("Models", ["gpt-4o-mini", "gpt-4o"], default=["gpt-4o-mini"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, float(settings.temperature), 0.05)
mode = st.sidebar.radio("Mode", ["Single Run", "Agent Mode (auto-pick best)"])

versions = list_prompts(task="product_copy")
if not versions:
    st.sidebar.error("No prompt templates found.")
    st.stop()

st.subheader("Input Product JSON")
default_payload = {
    "name": "Organic Cotton Oxford Shirt",
    "material": "100% organic cotton (oxford weave)",
    "fit": "Regular fit",
    "color": "Light blue",
    "sustainability": "Organic cotton; designed for durability",
    "additional_details": "Button-down collar, subtle embroidered logo, machine washable"
}
payload_text = st.text_area("Product payload", value=json.dumps(default_payload, ensure_ascii=False, indent=2), height=220)

try:
    payload = json.loads(payload_text)
except Exception:
    st.error("Invalid JSON in input.")
    st.stop()

colA, colB = st.columns([1, 1])

if mode == "Single Run":
    prompt_version = st.sidebar.selectbox("Prompt version", versions, index=0)

    if st.button("Run"):
        p = load_prompt(task="product_copy", version=prompt_version)
        user = render_user(p.user_template, payload)
        model = models[0] if models else settings.default_model

        out = llm.chat(system=p.system, user=user, model=model, temperature=temperature)
        ev, normalized_json, guardrail_passed = evaluate_product_copy(
        out,
        sustainability_provided=bool(str(payload.get("sustainability","")).strip()),
        payload=payload)
        tok = estimate_tokens(model, user, out)

        log_run(
            task="product_copy",
            model=model,
            prompt_version=prompt_version,
            temperature=temperature,
            input_json=payload_text,
            prompt_text=user,
            output_text=out,
            score=ev.score,
            guardrail_passed=guardrail_passed,
            guardrail_warnings="; ".join([r for r in ev.reasons if "pattern" in r or "hallucination" in r]),
            tokens=tok.__dict__,
        )

        with colA:
            st.markdown("### Output (raw)")
            st.code(out, language="json")
            st.markdown("### Normalized JSON (parsed)")
            st.code(normalized_json or "N/A", language="json")

        with colB:
            st.markdown("### Evaluation")
            st.metric("Score", f"{ev.score:.2f}")
            st.write(ev.reasons)
            st.markdown("### Token estimate")
            st.json(tok.__dict__)

else:
    chosen_versions = st.sidebar.multiselect("Prompt versions", versions, default=versions[:2] if len(versions) >= 2 else versions)

    if st.button("Run Agent Mode"):
        from agent import run_agent_product_copy
        best, all_cands = run_agent_product_copy(
            llm=llm,
            payload=payload,
            prompt_versions=chosen_versions,
            models=models if models else [settings.default_model],
            temperature=temperature,
        )

        st.success(f"Best: prompt={best.prompt_version} • model={best.model} • score={best.score:.2f}")

        with colA:
            st.markdown("### Best output (raw)")
            st.code(best.output_text, language="json")

        with colB:
            st.markdown("### Best evaluation")
            st.metric("Score", f"{best.score:.2f}")
            st.write(best.reasons)
            st.markdown("### Token estimate (best)")
            st.json(best.tokens)

        st.markdown("---")
        st.subheader("All candidates")
        rows = [
            {"prompt_version": c.prompt_version, "model": c.model, "score": c.score, "total_tokens": c.tokens.get("total_tokens", None)}
            for c in all_cands
        ]
        st.dataframe(rows, use_container_width=True)

        log_run(
            task="product_copy",
            model=best.model,
            prompt_version=best.prompt_version,
            temperature=temperature,
            input_json=payload_text,
            prompt_text="(agent_mode)",
            output_text=best.output_text,
            score=best.score,
            guardrail_passed=True,
            guardrail_warnings="",
            tokens=best.tokens,
        )
