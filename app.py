import streamlit as st
import subprocess
import os

# --- Configuration ---
MODEL_NAME = "qwen2.5-coder:1.5b"
THINK_MODE = False
LLM_API_BASE = "http://localhost:11434/v1"
LLM_API_KEY = "ollama"
STRIX_LLM = f"openai/{MODEL_NAME}"
# ---------------------

st.set_page_config(page_title="Strix Visual Explorer", page_icon="🦉", layout="centered")

st.title("🦉 Strix Visual Explorer")
st.markdown("A visual interface for Strix, the AI pentesting tool. Powered by local Ollama.")

st.info(f"**Current LLM**: `{MODEL_NAME}` (Thinking/Reasoning: `{THINK_MODE}`)")

target = st.text_input("Target URL or Local Directory", value="./dummy_app")

if st.button("Start Pentest Scan"):
    with st.spinner("Initializing Strix agents..."):
        env = os.environ.copy()
        env["STRIX_LLM"] = STRIX_LLM
        env["LLM_API_BASE"] = LLM_API_BASE
        env["LLM_API_KEY"] = LLM_API_KEY
        env["STRIX_REASONING_EFFORT"] = "low"
        
        try:
            # We run Strix in non-interactive mode
            cmd = ["strix", "-n", "--target", target, "--scan-mode", "quick"]
            
            result = subprocess.run(
                cmd, 
                env=env,
                capture_output=True, 
                text=True, 
                check=False
            )
            
            st.subheader("Scan Results")
            if result.stdout:
                st.code(result.stdout, language="markdown")
                
                # Save the output to output.md
                import re
                clean_text = re.sub(r'\x1b\[[0-9;]*m', '', result.stdout)
                with open("output.md", "w", encoding="utf-8") as f:
                    f.write(clean_text)
                st.success("Report successfully saved to `output.md`")
                
            if result.stderr:
                st.error("Errors/Warnings:")
                st.code(result.stderr, language="text")
                
            if result.returncode == 0:
                st.success("Scan completed successfully. No vulnerabilities found.")
            else:
                st.warning("Scan completed. Vulnerabilities detected or scan failed.")
                
        except Exception as e:
            st.error(f"Error running Strix: {str(e)}")
            st.info("Did you install strix-agent? Try running: pip install strix-agent")
