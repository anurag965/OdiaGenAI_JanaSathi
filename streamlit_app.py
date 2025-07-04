import streamlit as st
from model import OdiaEGovernanceBot
import os
import glob

st.set_page_config(page_title="Odia E-Governance Bot", page_icon="🤖", layout="centered")

st.title("🤖 Odisha E-Governance Assistant")
st.write("Get easy-to-understand information about Odisha Government Schemes in **English** and **Odia**.")

CURRENT_DIR = os.getcwd()
pdf_paths = glob.glob(os.path.join(CURRENT_DIR, "*.pdf"))

API_KEY = "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"
bot = OdiaEGovernanceBot(API_KEY)

if pdf_paths:
    with st.spinner("Processing government documents..."):
        bot.process_pdfs(pdf_paths)
    st.success(f"Loaded {len(pdf_paths)} PDF(s) successfully. You can now ask questions.")
else:
    st.warning("No PDFs found in the current directory. Please place your PDFs alongside this script.")

if bot.documents:
    user_query = st.text_input("Ask your question about Odisha Government schemes:")

    if st.button("Get Answer") and user_query.strip():
        with st.spinner("Generating response..."):
            response = bot.chat(user_query)
        st.markdown("---")
        st.subheader("Bot's Response:")

        if "ENGLISH RESPONSE" in response and "ODIA TRANSLATION" in response:
            en_part, odia_part = response.split("ODIA TRANSLATION:")
            st.markdown(f"**English:**\n\n{en_part.split('ENGLISH RESPONSE:')[1].strip()}")
            st.markdown(f"**Odia:**\n\n{odia_part.strip()}")
        else:
            st.write(response)
else:
    st.info("PDFs need to be processed to enable question answering.")
