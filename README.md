# 🤖 PersonaBot - Multi-Personality AI Chatbot

An interactive multi-personality conversational AI web application built with **LangChain**, **Groq LLM (`openai/gpt-oss-20b`)**, and **Streamlit**.

Users can dynamically switch between different AI personalities (Angry, Funny, Sad), and the chatbot retains conversation context with short-term memory using LangChain's message schema.

---

## ✨ Features

- 🎭 **Multiple AI Personalities:**
  - 😡 **Angry Mode:** Impatient, aggressive, and grumpy persona.
  - 😂 **Funny Mode:** Humorous, witty, and joke-telling assistant.
  - 😢 **Sad Mode:** Emotional, melancholic, and sensitive persona.
- ⚡ **Ultra-Fast Inference:** Powered by **Groq Cloud API** (`openai/gpt-oss-20b`) for lightning-fast responses.
- 🧠 **Context & Memory:** Retains chat history in `st.session_state` using `HumanMessage`, `AIMessage`, and dynamic `SystemMessage`.
- 🎨 **Modern Dark UI:** Custom styled Streamlit interface.
- 🗑️ **Conversation Reset:** Clear conversation button or typing `0` to instantly reset.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **LangChain & LangChain-Groq**
- **Groq Cloud API**
- **Streamlit**

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-Personality-Chatbot.git
cd AI-Personality-Chatbot
```

### 2. Create a virtual environment & install dependencies
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Setup your Groq API Key
1. Get a free API key from [Groq Console](https://console.groq.com/keys).
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Add your key inside `.env`:
   ```env
   GROQ_API_KEY=gsk_your_groq_api_key_here
   ```

### 4. Run the chatbot
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
AI-Personality-Chatbot/
├── app.py               # Main multi-personality chatbot app
├── simple_chatbot.py    # Single-persona funny chatbot variant
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template for users
├── .gitignore           # Keeps API keys and .venv safe from git
└── README.md            # Documentation
```

---

