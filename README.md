# EventFlow

Interactive chatbot for collecting and managing event data, powered by **LangGraph**, **FastAPI**, **PostgreSQL**, and **Google Drive** storage.

## 🚀 Overview
EventFlow is designed to help collect and manage event information (concerts, conferences, workshops, etc.) in a structured way.  
The chatbot interacts with users, stores checkpoints and long-term memory in PostgreSQL, and saves generated files and media in Google Drive.

## 🛠 Tech Stack
- [LangGraph](https://github.com/langchain-ai/langgraph) – interactive chatbot workflows
- [FastAPI](https://fastapi.tiangolo.com/) – API framework
- PostgreSQL – memory & checkpoints
- Google Drive API – media & file storage

## 📂 Project Structure
```
eventflow/
├── app/
│ ├── agents/           # LangGraph chatbot logic
│ ├── core/             # Config, database, logger
│ ├── helper/           # Google Drive & file utilities
│ ├── routers/          # FastAPI routes
│ ├── schemas/          # Pydantic models
│ └── tests/            # Unit tests
├── main.py             # FastAPI entry point
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── README.md              
└── CONTRIBUTING.md       
```

## ⚙️ Setup
1. Clone the repository
```bash
git clone https://github.com/adama444/eventflow.git
cd eventflow
```

2. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

3. Copy .env.example to .env and fill in your values
```bash
cp .env.example .env
```

4. Run the API
```bash
uvicorn main:app --reload
```