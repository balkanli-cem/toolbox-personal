import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse
from models import ADRRequest, ADRResponse
from generator import generate_adr

app = FastAPI(title="ADR Generator")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

@app.post("/generate", response_model=ADRResponse)
def generate(request: ADRRequest):
    try:
        result = generate_adr(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download")
def download(title: str, markdown: str):
    filename = title.lower().replace(" ", "-") + ".md"
    return PlainTextResponse(
        content=markdown,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )