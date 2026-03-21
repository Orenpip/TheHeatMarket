from fastapi import APIRouter, HTTPException
import anthropic
import json
from app.models.requests import MeetingPrepRequest, MeetingPrepResponse
from app.prompts.counselor import build_meeting_prep_prompt, COUNSELOR_SYSTEM_PROMPT
from app.config import get_settings

router = APIRouter()


@router.post("/meeting-prep", response_model=MeetingPrepResponse)
async def get_meeting_prep(request: MeetingPrepRequest) -> MeetingPrepResponse:
    settings = get_settings()
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    user_prompt = build_meeting_prep_prompt(
        signal_profile=request.signalProfile,
        shared_reflections=request.sharedReflections,
    )

    try:
        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            system=COUNSELOR_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )

        content = message.content[0].text.strip()
        data = json.loads(content)

        return MeetingPrepResponse(
            summary=data.get("summary", ""),
            conversationStarters=data.get("conversationStarters", []),
            flags=data.get("flags", []),
        )

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse meeting prep response: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Meeting prep error: {str(e)}"
        )
