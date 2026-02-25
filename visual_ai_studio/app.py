from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import streamlit as st

from prompts import PROMPT_V1, PROMPT_V2, render_prompt
from utils import run_image_generation

st.set_page_config(page_title="Visual AI Studio", page_icon="🖼️", layout="wide")

st.title("🖼️ Visual AI Studio — Product Image Prompting + Generation")
st.caption("Module 5 — Text-to-Image demo for fashion retail (prompt versions + basic governance).")

left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("Input Product JSON")
    default_json = (Path(__file__).parent / "sample_product.json").read_text(encoding="utf-8")
    product_json_text = st.text_area("Paste product JSON:", value=default_json, height=260)

    st.subheader("Controls")
    llm_model = st.selectbox("Prompt LLM model", ["gpt-4o-mini", "gpt-4o"], index=0)
    image_model = st.selectbox("Image model", ["gpt-image-1.5", "gpt-image-1", "gpt-image-1-mini", "dall-e-3"], index=0)
    size = st.selectbox("Size", ["1024x1024", "1536x1024", "1024x1536"], index=0)
    quality = st.selectbox("Quality", ["auto", "high", "medium", "low", "hd", "standard"], index=0)
    n = st.slider("Number of images", min_value=1, max_value=4, value=2, step=1)
    prompt_version = st.radio("Prompt version", ["v1", "v2"], horizontal=True)

    run_btn = st.button("Run (generate images)", type="primary")

with right:
    st.subheader("Output")

    if run_btn:
        try:
            product: Dict[str, Any] = json.loads(product_json_text)
        except Exception as e:
            st.error(f"Invalid JSON: {e}")
            st.stop()

        template = PROMPT_V1 if prompt_version == "v1" else PROMPT_V2
        rendered = render_prompt(template, product)

        out_dir = Path(__file__).parent / "out"

        with st.spinner("Generating prompt and images..."):
            result = run_image_generation(
                product,
                prompt_version=prompt_version,
                rendered_prompt=rendered,
                llm_model=llm_model,
                image_model=image_model,
                n=n,
                size=size,
                quality=quality,
                out_dir=out_dir,
            )

        st.markdown("### Governance")
        st.write(f"Input score: **{result.score:.2f}**")
        if result.reasons:
            st.warning("\n".join(result.reasons))
        else:
            st.success("No risky input claims detected.")

        st.markdown("### Generated prompt")
        st.code(result.prompt, language="text")

        if not result.image_paths:
            st.info("No base64 images returned. Check the saved *_meta.json in visual_ai_studio/out/.")
        else:
            st.markdown("### Images")
            for p in result.image_paths:
                st.image(str(p), caption=p.name, use_container_width=True)
                st.download_button(
                    label=f"Download {p.name}",
                    data=p.read_bytes(),
                    file_name=p.name,
                    mime="image/png",
                    key=f"dl_{p.name}",
                )

        st.markdown("### Saved artifacts")
        st.write(f"Output directory: `{out_dir}`")
