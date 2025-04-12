# AI Dashboard Phase 1

A data analysis and visualization dashboard with AI-powered insights and forecasting capabilities.

## Features

- Data ingestion and preprocessing
- Time series analysis and forecasting using Prophet
- Interactive visualizations using Plotly
- AI-powered insights and anomaly detection
- Chatbot interface for data exploration

## Project Structure

```
ai-dashboard-phase1/
│
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── ingestion.py         # Data ingestion utilities
│   ├── preprocess.py        # Data preprocessing functions
│   ├── insights.py          # Data analysis and insights
│   ├── chatbot.py           # AI chatbot implementation
│   └── utils/
│       ├── file_utils.py    # File handling utilities
│       └── chart_utils.py   # Visualization utilities
│
├── data/
│   └── uploads/             # Directory for uploaded data files
│
├── models/
│   └── prophet_model.py     # Time series forecasting model
│
├── requirements.txt         # Project dependencies
└── README.md               # Project documentation
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

- `GET /`: Welcome message
- `POST /upload`: Upload data files
- `GET /insights`: Get data insights
- `POST /forecast`: Generate time series forecasts
- `POST /chat`: Interact with the data chatbot

## Dependencies

- FastAPI: Web framework
- Pandas: Data manipulation
- Prophet: Time series forecasting
- Plotly: Interactive visualizations
- scikit-learn: Machine learning utilities

## License

MIT License 