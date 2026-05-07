import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models import AnalyzeRequest, GenerateRequest
from styler import analyze_style, load_profile
from writer import generate_content

app = FastAPI(title="Writing Assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

@app.get("/profile")
def get_profile():
    profile = load_profile()
    if profile is None:
        return {"exists": False}
    return {"exists": True, "profile": profile.model_dump()}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    try:
        profile = analyze_style(request)
        return {"success": True, "profile": profile.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/generate")
def generate(request: GenerateRequest):
    try:
        profile = load_profile()
        if profile is None:
            raise HTTPException(status_code=400, detail="No style found. Please analyze writing samples first.")
        result = generate_content(request, profile)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))