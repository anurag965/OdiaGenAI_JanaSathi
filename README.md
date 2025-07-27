
# 🗣️ JanaSathi: Odia E-Governance Chatbot

**JanaSathi** is a bilingual AI chatbot that helps users understand and access Odisha Government schemes. It uses a **Retrieval-Augmented Generation (RAG)** architecture to retrieve relevant content from official documents and generate responses in **English and Odia**.

---

## 🤖 Features

- ✅ Answers queries about government schemes like KALIA Yojana, Mission Shakti, and Biju Swasthya Kalyan Yojana
- 📄 Reads and processes official government PDF documents
- 🌐 Uses Large Language Models via OpenRouter API
- 🔍 Retrieves relevant information using semantic search (MiniLM)
- 🧠 Generates responses in English and translates to Odia
- 🖥️ Streamlit frontend for interactive usage

---

## 🛠️ Tech Stack

- Python 3.10+
- Streamlit
- Sentence-Transformers (`all-MiniLM-L6-v2`)
- OpenAI-compatible LLMs via OpenRouter
- Cohere models for Odia translation
- PyPDF2 for PDF parsing
- scikit-learn for cosine similarity

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/odia-e-gov-chatbot.git
cd odia-e-gov-chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add government scheme PDFs
Place your scheme-related PDFs in the project root directory.

### 4. Run the chatbot
```bash
streamlit run streamlit_app.py
```

---

## 💡 How It Works

- PDF documents are processed and chunked into smaller sections.
- Embeddings are generated using `all-MiniLM-L6-v2`.
- The chatbot retrieves top relevant chunks using cosine similarity.
- Uses a 49B LLM to generate responses in English.
- Translates the responses into Odia using Cohere’s LLM.
- Presents both responses through a clean Streamlit interface.

---

## 📷 Demo

![Streamlit UI](samples/ui_screenshot.png)

---

## 📌 To Do

- Improve document chunking for regional formatting
- Add document upload feature in the UI
- Support voice-based queries and responses
- Log chat history for audit and learning

---

## 🙋‍♂️ Author

**Anurag Pradhan**  
📧 [anuragpradhancb@gmail.com](mailto:anuragpradhancb@gmail.com)  
🔗 [LinkedIn](https://linkedin.com/in/anurag-pradhan-0340bb288) • [GitHub](https://github.com/anurag965)

---

## 📄 License

This project is licensed under the MIT License.

