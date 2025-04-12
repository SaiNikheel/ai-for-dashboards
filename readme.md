

# 📊 AI-Powered Dashboard Insights 

Welcome to Phase 1 of the **AI-Powered Dashboard Insight Platform**. This backend service takes uploaded CSV data, detects chart types, performs data analysis, and generates insights via a chatbot interface powered by LLMs.

---

## 🚀 Vision
Build a local backend service to:
- Accept dashboard data (CSV)
- Detect chart types (bar, line, pie)
- Generate statistical + narrative insights
- Provide a chatbot interface for querying insights

This is the foundation for a future open-source AI dashboard assistant.

---

## 🧩 Modules Overview

### 1. **Data Ingestion**
- Upload CSV
- Extract column metadata

### 2. **Chart Detection & Preprocessing**
- Detect suitable chart type
- Clean and process data

### 3. **Insight Engine**
- Detect trends, dips, spikes
- Use Prophet/SciPy for time-series
- Generate LLM-based summaries

### 4. **Chatbot**
- Type questions or auto-generate insights
- Return natural language explanations

### 5. **API Backend (FastAPI)**
- Endpoints for upload, processing, and querying

---

## 🏗️ Architecture
![AI in dashboard phase-1](https://github.com/user-attachments/assets/57d49285-e19c-40d8-b2eb-93d55a74047f)

---

## 📁 Project Structure
```
/ai-dashboard-phase1
│
├── app/
│   ├── main.py
│   ├── ingestion.py
│   ├── preprocess.py
│   ├── insights.py
│   ├── chatbot.py
│   └── utils/
│       ├── file_utils.py
│       └── chart_utils.py
│
├── data/
│   └── uploads/
│
├── models/
│   └── prophet_model.py
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack
- **FastAPI** - Web framework
- **Pandas / SciPy / Prophet** - Data preprocessing & insights
- **LangChain + Gemini/OpenAI** - LLM-based explanation engine
- **Local Storage** - CSV and metadata handling

---

## 📦 Setup Instructions
```bash
TODO
```

---

## 🧪 Example API Flow
1. **POST** `/upload` → Upload CSV
2. **GET** `/analyze` → Trigger chart detection + insight generation
3. **POST** `/chat` → Ask a question or auto-generate summary

---

## 📆 Sprint Tracker (3 Weeks)
- See `sprint_tracker.md` for stories, epics, and tasks.

---

## 🔮 Future Phases
- Phase 2: Source + Domain via vectorDB + LangGraph
- Phase 3: UI & Interactive Dashboard Overlay

---

## 🤝 Contributions
Open to community contributors after Phase 1 completion. Stay tuned!

---

## 📝 License
MIT License

