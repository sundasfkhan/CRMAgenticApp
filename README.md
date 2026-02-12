# CRM Agentic App

A LangChain-powered agent for interacting with Microsoft Dynamics 365 CRM cases.

## Features

- Retrieve customer cases from Dataverse using natural language
- Interactive chat interface
- LangChain v1 agent with OpenAI integration

## Setup

1. **Clone the repository**

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your actual values:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DATAVERSE_RESOURCE_URL`: Your Dynamics 365 environment URL

## Usage

Run the application:
```bash
python main.py
```

This will start an interactive chat session. You can ask questions like:
- "Get me all cases for customer Trey Research"
- "What cases does John Smith have?"

Type `exit` or `quit` to end the session.

## Project Structure

```
CRMAgenticApp/
├── main.py              # Entry point
├── crm_case_agent.py    # LangChain agent implementation
├── utility.py           # Helper functions for Dataverse queries
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── .env                 # Your local environment variables (not tracked)
└── .gitignore           # Git ignore rules
```

## Requirements

- Python 3.9+
- Microsoft Dynamics 365 / Dataverse access
- OpenAI API key

