import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from models import ADRRequest, ADRResponse

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def build_options_text(request: ADRRequest) -> str:
    return "\n".join([f"- {opt.name}: {opt.description}" for opt in request.options])

def generate_adr(request: ADRRequest) -> ADRResponse:
    options_text = build_options_text(request)
    extra = f"\nExtra instructions: {request.extra_instructions}" if request.extra_instructions else ""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system="""You are a senior solution architect helping document
architecture decisions in a clear, professional format.
You elaborate raw input into well-structured ADR documents.
Respond ONLY with valid JSON, no markdown, no explanation outside JSON.""",
        messages=[
            {
                "role": "user",
                "content": f"""Generate a complete Architecture Decision Record from this input.
Title: {request.title}
Status: {request.status.value}
Context (raw): {request.context}
Options considered:
{options_text}
Decision (raw): {request.decision}{extra}

Return JSON in this exact format:
{{
  "context": "<elaborate the context into 2-3 professional sentences>",
  "options_analysis": "<for each option, provide pros and cons in markdown format>",
  "decision_rationale": "<elaborate why this decision was made in 2-3 sentences>",
  "consequences": "<list positive and negative consequences of this decision in markdown format>"
}}"""
            }
        ]
    )

    raw = message.content[0].text
    data = json.loads(raw)

    markdown = build_markdown(request, data)

    return ADRResponse(
        title=request.title,
        status=request.status.value,
        markdown=markdown
    )


def build_markdown(request: ADRRequest, data: dict) -> str:
    return f"""# ADR: {request.title}

**Status:** {request.status.value}

## Context

{data['context']}

## Options Considered

{data['options_analysis']}

## Decision

{request.decision}

{data['decision_rationale']}

## Consequences

{data['consequences']}
"""