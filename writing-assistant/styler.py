import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from models import AnalyzeRequest, StyleProfile

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

PROFILE_PATH = "style_profile.json"

def analyze_style(request: AnalyzeRequest) -> StyleProfile:
    samples_text = "\n\n---\n\n".join(request.samples)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="""You are an expert writing analyst. Your job is to extract a person's unique writing style from provided samples. 
        Respond only with valid JSON, no markdown, no explanation outside JSON.""",
        messages=[
            {
                "role": "user",
                "content": f"""Analyze the writing style from these samples and return a JSON object with exactly these fields:
                {{
                "personality": "<describe tone, warmth, directness, humor>",
                "structure": "<describe how they open, close, use paragraphs or bullets>",
                "language": "<describe vocabulary level, technical vs plain, recurring phrases>",
                "narrative_style": "<story-driven, fact-driven, or opinion-driven — explain>"
                }}

                Writing samples:
                {samples_text}"""
                }
            ]
        )
    raw = message.content[0].text
    data = json.loads(raw)
    profile = StyleProfile(**data)
    save_profile(profile)
    return profile

def save_profile(profile: StyleProfile) -> None:
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile.model_dump(), f, indent=2)

def load_profile() -> StyleProfile | None:
    if not os.path.exists(PROFILE_PATH):
        return None
    with open(PROFILE_PATH, "r") as f:
        content = f.read().strip()
        if not content:
            return None
        data = json.loads(content)
    return StyleProfile(**data)