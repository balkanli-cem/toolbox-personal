## Setup

1. Clone the repo
2. Create a virtual environment: `python -m venv .venv`
3. Activate it: `.venv\Scripts\activate`
4. Install dependencies: `python -m pip install -r requirements.txt`
5. Create a `.env` file with your key:
ANTHROPIC_API_KEY=sk-ant-your-key-here
6. Run: `python -m uvicorn main:app --reload`
7. Open: `http://localhost:8000`