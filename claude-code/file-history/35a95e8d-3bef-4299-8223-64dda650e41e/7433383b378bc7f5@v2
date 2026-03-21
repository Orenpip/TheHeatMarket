from fastapi import APIRouter, HTTPException
import anthropic
import json
from app.models.requests import ExplainMatchRequest, ExplainMatchResponse, OpportunityExplanation
from app.config import get_settings

router = APIRouter()

SYSTEM_PROMPT = """You are a college counselor assistant. Given a student's interest profile and a list of opportunities, write a 1-sentence explanation for why each opportunity matches this student. Be specific, warm, and actionable. Focus on the connection between the student's interests and what the opportunity offers.

Respond with a JSON array. Each object must have "id" (the opportunity id) and "reason" (the explanation sentence). Do not include any other text."""


@router.post("/explain-match", response_model=ExplainMatchResponse)
async def explain_match(request: ExplainMatchRequest) -> ExplainMatchResponse:
    settings = get_settings()
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    if not request.opportunities:
        return ExplainMatchResponse(explanations=[])

    opportunities_text = "\n".join(
        f"- id: {opp.id}, title: {opp.title}, category: {opp.category}, description: {opp.description[:200]}"
        for opp in request.opportunities
    )

    user_prompt = f"""Student profile summary:
{request.studentSummary}

Opportunities to explain:
{opportunities_text}

Return a JSON array with one object per opportunity, each with "id" and "reason" fields."""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )

        content = message.content[0].text.strip()

        # Strip markdown code fences if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        data = json.loads(content)
        explanations = [
            OpportunityExplanation(id=item["id"], reason=item["reason"])
            for item in data
            if isinstance(item, dict) and "id" in item and "reason" in item
        ]
        return ExplainMatchResponse(explanations=explanations)

    except json.JSONDecodeError:
        # Return empty explanations rather than failing the whole explore request
        return ExplainMatchResponse(explanations=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explain match error: {str(e)}")
