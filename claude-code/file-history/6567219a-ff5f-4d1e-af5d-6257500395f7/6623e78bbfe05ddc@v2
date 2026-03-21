from fastapi import APIRouter, HTTPException
import anthropic
import json
from app.models.requests import ReflectionPromptsRequest, ReflectionPromptsResponse, ReflectionPrompt, PromptType
from app.prompts.reflection import build_reflection_prompt, REFLECTION_SYSTEM_PROMPT
from app.config import get_settings

router = APIRouter()


@router.post("/reflection-prompts", response_model=ReflectionPromptsResponse)
async def get_reflection_prompts(request: ReflectionPromptsRequest) -> ReflectionPromptsResponse:
    settings = get_settings()
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    user_prompt = build_reflection_prompt(
        compressed_summary=request.compressedSummary,
        recent_activities=request.recentActivities,
        recent_reflections=request.recentReflections,
        previous_prompts=request.previousPrompts,
    )

    try:
        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            system=REFLECTION_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )

        content = message.content[0].text.strip()

        # Parse JSON response
        prompts_data = json.loads(content)

        prompts = [
            ReflectionPrompt(
                promptText=p["promptText"],
                promptType=PromptType(p["promptType"]),
            )
            for p in prompts_data
        ]

        return ReflectionPromptsResponse(prompts=prompts)

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse AI response: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(e)}"
        )
