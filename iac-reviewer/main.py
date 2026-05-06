import os
from urllib import response
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models import ReviewRequest, ReviewResponse
from reviewer import run_review

app = FastAPI(title="IaC Reviewer")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

@app.post("/review", response_model=ReviewResponse)
def review(request: ReviewRequest):
    try:
        result = run_review(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))