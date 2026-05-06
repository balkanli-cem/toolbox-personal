import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from models import ReviewRequest, ReviewResponse, Finding, Severity

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def build_prompt(request: ReviewRequest) -> str:
    focus_note = "all categories" if request.focus == "all" else f"focus on {request.focus}"
    return f"""You are an expert IaC code reviewer specializing in Terraform, Bicep, and ARM templates.
    You are reviewing code for the {request.cloud} cloud environment.

    Review the following code and respond ONLY with valid JSON, no markdown, no explanation outside JSON.

    JSON format:
    {{
    "score": <integer 0-100>,
    "summary": "<2-3 sentence overall assessment>",
    "findings": [
        {{
        "severity": "critical|warning|info|good",
        "category": "Security|Naming|Modularity|Cost|Compliance|Best Practice",
        "title": "<short title>",
        "description": "<explain the issue in 1-2 sentences>",
        "fix": "<concrete fix suggestion>"
        }}
    ]
    }}

    Focus on: {focus_note}. Max 8 findings. Include both problems AND positives.

    Code to review:
    {request.code}"""

def run_review(request: ReviewRequest) -> ReviewResponse:
    prompt = build_prompt(request)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    data = json.loads(raw)

    findings = [Finding(**f) for f in data["findings"]]

    return ReviewResponse(
        score=data["score"],
        summary=data["summary"],
        findings=findings
    )