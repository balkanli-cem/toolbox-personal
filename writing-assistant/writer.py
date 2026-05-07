import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from models import GenerateRequest, GenerateResponse, StyleProfile

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def build_system_prompt(profile: StyleProfile) -> str:
    return f"""You are a professional ghostwriter. You write content that 
        sounds exactly like the person described below. Match their style precisely.

        THEIR WRITING STYLE:
        - Personality: {profile.personality}
        - Structure: {profile.structure}
        - Language: {profile.language}
        - Narrative style: {profile.narrative_style}

        Always write in first person. Never sound like generic AI output.
        Respond ONLY with valid JSON, no markdown, no explanation outside JSON."""

def generate_content(request: GenerateRequest, profile: StyleProfile) -> GenerateResponse:
    is_email = request.content_type == "email"

    format_instructions = """Return JSON in this format:
        {
        "subject": "<email subject line>",
        "draft": "<full email body>"
        }""" if is_email else """Return JSON in this format:
        {
        "draft": "<full LinkedIn post>"
        }"""

    extra = f"\nExtra instructions: {request.extra_instructions}" if request.extra_instructions else ""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=build_system_prompt(profile),
        messages=[
            {
                "role": "user",
                "content": f"""Write a {request.content_type} about the following topic:

                {request.topic}{extra}

                {format_instructions}"""
            }
        ]
    )

    raw = message.content[0].text
    data = json.loads(raw)

    return GenerateResponse(
        draft=data["draft"],
        subject=data.get("subject")
    )