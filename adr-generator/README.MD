# ADR Generator

AI-powered Architecture Decision Record generator. Takes your raw architecture thinking and turns it into professional documentation ready to share with clients or commit to a repo.

## What it does

- Takes your title, context, options, and decision as input
- Claude elaborates the context and decision into professional language
- Generates pros/cons for each option you considered
- Produces consequences you might not have thought of
- Outputs a clean markdown ADR you can copy or download as a `.md` file

## Setup

1. Clone the repo
2. Navigate to the `adr-generator` folder
3. Create a virtual environment:
```bash
   python -m venv .venv
```
4. Activate it:
```bash
   # Windows
   .venv\Scripts\activate

   # Mac/Linux
   source .venv/bin/activate
```
5. Install dependencies:
```bash
   python -m pip install -r requirements.txt
```
6. Create a `.env` file with your Anthropic API key

7. Run the server:
```bash
   python -m uvicorn main:app --reload
```
8. Open `http://localhost:8000`

## Project structure

adr-generator/
─ main.py          # FastAPI routes
─ generator.py     # Claude logic and markdown assembly
─ models.py        # Pydantic request and response models
─ requirements.txt
─ static/
    ─ index.html   # Frontend

## Stack

- **Backend** — Python, FastAPI, Uvicorn
- **AI** — Anthropic Claude Sonnet via Python SDK
- **Frontend** — Plain HTML, CSS, JavaScript

## Notes

- Each generated ADR can be copied as markdown or downloaded as a `.md` file
- The `status` field accepts: `Proposed`, `Accepted`, `Deprecated`