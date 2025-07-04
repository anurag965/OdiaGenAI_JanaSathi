# OdiaGenAI_Hackathon
An AI-Powered Chatbot to Help Citizens Understand Odisha Government Welfare Schemes in Simple English & Odia

📌 Project Overview
The Odisha E-Governance Assistant is a Retrieval-Augmented Generation (RAG) based chatbot that provides easy-to-understand information about various Odisha Government schemes such as:

✅ KALIA Yojana
✅ Biju Swasthya Kalyan Yojana
✅ Mission Shakti
✅ Subhadra Yojana (or any other scheme documents provided)

The bot extracts information from official government documents and answers user queries in both English and Odia, making bureaucratic information accessible to common citizens.

🚀 Key Features
✔️ Provides bilingual responses (English & Odia)
✔️ AI-generated, citizen-friendly explanations of schemes
✔️ Covers eligibility criteria, benefits, application process, and required documents
✔️ Retrieves verified information from official PDFs
✔️ Simple, intuitive Streamlit interface

🏗️ Technology Stack
Component	Technology Used
Embedding Model	Sentence Transformers (all-MiniLM-L6-v2)
RAG Model	OpenRouter AI (thedrummer/valkyrie-49b-v1)
Translation	Cohere Command-R-Plus (English to Odia)
PDF Processing	PyPDF2, Regex
Similarity Search	Cosine Similarity
Web Interface	Streamlit
Language	Python 3.x

📂 Project Structure
bash
Copy
Edit
├── model.py              # Core chatbot logic and RAG pipeline
├── streamlit_app.py      # Streamlit web interface
├── requirements.txt      # Project dependencies
├── *.pdf                 # Official scheme documents (place here)
├── README.md             # Project documentation
⚙️ Installation & Setup
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/odisha-e-governance-bot.git
cd odisha-e-governance-bot
2️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Place Scheme Documents
Add official PDF documents containing scheme details in the same directory as the code files.

4️⃣ Add API Key
Obtain your OpenRouter API key from OpenRouter.ai

Replace the placeholder API key in model.py and streamlit_app.py with your actual key.

5️⃣ Run the Application
bash
Copy
Edit
streamlit run streamlit_app.py
💡 Usage Example
Launch the app

Upload your PDFs if not already placed

Enter your query like:

"What are the benefits of the KALIA Yojana?"

The bot will respond with:
✅ Simplified English explanation
✅ Accurate Odia translation

📊 Future Enhancements
Expand coverage to more schemes and departments

Odia voice input/output support

Mobile and WhatsApp integration

Real-time document updates

🤝 Contributing
Contributions, ideas, and feedback are welcome!
Please open issues or submit pull requests to collaborate.

📄 License
This project is for educational and proof-of-concept purposes. For production deployment, ensure compliance with Odisha Government data policies.
