import os
import json
from typing import List, Dict, Any, Optional
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
from io import BytesIO
import re
import logging
from datetime import datetime
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OdiaEGovernanceBot:
    def __init__(self, openrouter_api_key: str):
        """
        Initialize the Odia E-Governance Bot with RAG capabilities
        """
        self.api_key = openrouter_api_key
        self.model_name = "thedrummer/valkyrie-49b-v1"
        self.translation_model = "cohere/command-r-plus"
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

        # Initialize sentence transformer for embeddings
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

        # Storage for processed documents
        self.documents = []
        self.embeddings = np.array([])
        self.metadata = []

        logger.info("Odia E-Governance Bot initialized successfully!")

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            return ""

    def preprocess_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'[^\w\s.,!?()-]', '', text)
        return text

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        return chunks

    def process_pdfs(self, pdf_paths: List[str]) -> None:
        logger.info("Processing PDF files...")
        for pdf_path in pdf_paths:
            if not os.path.exists(pdf_path):
                logger.warning(f"PDF file not found: {pdf_path}")
                continue
            text = self.extract_text_from_pdf(pdf_path)
            if not text:
                logger.warning(f"No text extracted from {pdf_path}")
                continue
            cleaned_text = self.preprocess_text(text)
            chunks = self.chunk_text(cleaned_text)
            for i, chunk in enumerate(chunks):
                self.documents.append(chunk)
                self.metadata.append({
                    'source': pdf_path,
                    'chunk_id': i,
                    'length': len(chunk),
                    'timestamp': datetime.now().isoformat()
                })
        if self.documents:
            logger.info(f"Creating embeddings for {len(self.documents)} document chunks...")
            self.embeddings = np.array(self.embedder.encode(self.documents))
            logger.info("PDF processing completed successfully!")
        else:
            logger.warning("No documents were processed!")

    def retrieve_relevant_docs(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if len(self.embeddings) == 0:
            logger.warning("No embeddings available. Please process PDFs first.")
            return []
        query_embedding = self.embedder.encode([query])
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        relevant_docs = []
        for idx in top_indices:
            if similarities[idx] > 0.1:
                relevant_docs.append({
                    'content': self.documents[idx],
                    'similarity': float(similarities[idx]),
                    'metadata': self.metadata[idx]
                })
        return relevant_docs

    def get_system_prompt(self) -> str:
          """
          Get the system prompt for the Odisha E-Governance Bot
          """
          return """You are an expert Odisha E-Governance Assistant specializing in Odisha Government schemes and programs. Your role is to:

  CORE RESPONSIBILITIES:
  1. Explain government schemes in simple, conversational English
  2. Provide accurate information about eligibility, benefits, and application processes
  3. Focus on three main schemes: KALIA Yojana, Biju Swasthya Kalyan Yojana, and Mission Shakti
  4. Make complex bureaucratic information accessible to common citizens

  COMMUNICATION STYLE:
  - Use simple, everyday English (avoid complex bureaucratic jargon)
  - Break down complex procedures into easy-to-follow steps
  - Provide practical examples and real-life scenarios
  - Be empathetic and understanding of common citizen concerns
  - Explain technical terms in plain language

  RESPONSE FORMAT:
  - Start with a brief, clear answer
  - Provide step-by-step guidance when relevant
  - Include eligibility criteria clearly
  - Mention required documents
  - Add helpful tips or common pitfalls to avoid
  - End with encouragement or next steps

  STRUCTURE YOUR RESPONSES:
  For scheme-related queries, organize information as:
  - Brief scheme overview
  - Who can apply (eligibility criteria)
  - What benefits are provided
  - How to apply (step-by-step process)
  - Required documents
  - Helpful tips and important notes

  ACCURACY REQUIREMENTS:
  - Base all responses on provided document context
  - If information is unclear, ask for clarification
  - Never provide incorrect eligibility or benefit information
  - Clearly state when information is not available in the documents
  - Always mention official sources when possible

  Remember: You are helping everyday citizens understand their rights and access government benefits. Be patient, clear, and supportive in your explanations."""

    def get_user_prompt(self, query: str, relevant_docs: List[Dict[str, Any]]) -> str:
          """
          Generate user prompt with query and relevant context
          """
          context = "\n\n".join([doc['content'] for doc in relevant_docs])

          prompt = f"""Based on the following official government documents about Odisha schemes:

  CONTEXT:
  {context}

  USER QUERY: {query}

  Please provide a helpful response in clear, simple English following these guidelines:
  1. Focus on practical, actionable information
  2. Use simple language that any citizen can understand
  3. Include specific steps, eligibility, and requirements when relevant
  4. If the query is about a specific scheme, structure your response with:
    - Brief scheme overview
    - Who can apply (eligibility)
    - What benefits are provided
    - How to apply (step-by-step)
    - Required documents
    - Helpful tips

  If the information is not available in the provided context, please say so clearly and suggest how the user might find this information."""

          return prompt


    def call_openrouter_api(self, messages: List[Dict[str, str]], model_override: Optional[str] = None) -> Optional[str]:
        from httpx import post
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_override if model_override else self.model_name,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1500,
            "top_p": 0.9
        }
        try:
            response = post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            logger.debug(f"API Raw Response: {result}")
            return result['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"API call failed: {e}")
            return None

    def translate_to_odia(self, english_text: str) -> Optional[str]:
        paragraphs = [p for p in english_text.split('\n') if p.strip()]
        translations = []
        for para in paragraphs:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an Odia translation engine. Translate ONLY the user's input from English to Odia. "
                        "Do NOT add explanations, comments, or intermediate thoughts. Return Odia translation only, using Odia script."
                    )
                },
                {"role": "user", "content": para}
            ]
            translation = self.call_openrouter_api(messages, model_override=self.translation_model)
            if translation:
                translation = translation.strip()
                translation = re.sub(r"(translation:?|ଅନୁବାଦ:?|here is the translation|let me translate.*)", "", translation, flags=re.IGNORECASE).strip()
                translations.append(translation)
            else:
                translations.append("[Translation unavailable]")

        return "\n".join(translations)

    def chat(self, query: str) -> str:
        relevant_docs = self.retrieve_relevant_docs(query)
        if not relevant_docs:
            return "I'm sorry, I couldn't find relevant information. Please ask a more specific question."
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": self.get_user_prompt(query, relevant_docs)}
        ]
        response_en = self.call_openrouter_api(messages)
        if not response_en:
            return "I'm sorry, there's a technical issue right now. Please try again later."
        response_odia = self.translate_to_odia(response_en)
        combined_response = (f"\nENGLISH RESPONSE:\n{response_en}\n\nODIA TRANSLATION:\n{response_odia if response_odia else 'Translation unavailable.'}")
        return combined_response

# Example usage
def main():
    API_KEY = "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"
    bot = OdiaEGovernanceBot(API_KEY)
    pdf_paths = ["ODISHA-GOVT-SCHEMES.pdf", "SCHEMES.pdf"]
    bot.process_pdfs(pdf_paths)
    print("Odisha E-Governance Bot Ready!")

    while True:
        user_input = input("\nYour Question: ")
        if user_input.lower() in ["exit", "quit", "stop"]:
            print("Thank you for using the bot!")
            break
        if user_input.strip():
            response = bot.chat(user_input)
            print(response)

if __name__ == "__main__":
    main()
