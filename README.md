# 🧠 Course Chatbot - AI-Powered Course Assistant
An interactive chatbot using **LangChain, Pinecone, and Gemini AI**, designed to help users explore courses, get pricing, and receive AI-generated recommendations.

## 🚀 Features
✅ **Web-based chatbot UI** (Flask + HTML)  
✅ **AI-powered responses using Google Gemini**  
✅ **Context-aware chat with Pinecone vector search**  
✅ **Web scraping for live course data**  

---

## 🛠️ Installation & Setup
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/Course-Chatbot.git
cd Course-Chatbot
```

### **2️⃣ Set Up Virtual Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Configure API Keys**
- **Gemini API Key:** Set in `config.py`
- **Pinecone API Key:** Also set in `config.py`
- Example `config.py`:
```python
import os
os.environ["GEMINI_API_KEY"] = "your-gemini-api-key"
os.environ["PINECONE_API_KEY"] = "your-pinecone-api-key"
```

### **5️⃣ Run Flask Server**
```bash
python Flask_API.py
```
📍 Now open `http://127.0.0.1:5001/` in your browser.

---

## 🏗️ Project Structure
📦 **Course-Chatbot**  
├── 📂 `data/` → Cleaned course data  
├── 📂 `templates/` → Chat UI (`index.html`)  
├── 📂 `scripts/` → Web scraping (`webscraping.py`)  
├── `Flask_API.py` → Main API backend  
├── `requirements.txt` → Python dependencies  
└── `README.md` → Documentation  

---

## 📌 Technologies Used
- **Flask** (Backend API)
- **LangChain** (AI-powered conversation)
- **Pinecone** (Vector storage)
- **Gemini AI** (LLM for response generation)
- **BeautifulSoup** (Web scraping)

---

## 🤝 Contributing
Want to improve this chatbot? Feel free to **fork** this repo and submit a **pull request**.  

🔗 **GitHub Repo:** [Course-Chatbot](https://github.com/RAHULJOGI-CODE/LangChain/)  

