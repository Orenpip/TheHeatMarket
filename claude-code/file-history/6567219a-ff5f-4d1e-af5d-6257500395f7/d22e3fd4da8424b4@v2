from fastapi import APIRouter, HTTPException
import anthropic
import json
from app.models.requests import NotificationRequest, NotificationResponse
from app.prompts.notifications import build_notification_prompt, NOTIFICATION_SYSTEM_PROMPT
from app.config import get_settings

router = APIRouter()


@router.post("/generate-notification", response_model=NotificationResponse)
async def generate_notification(request: NotificationRequest) -> NotificationResponse:
    settings = get_settings()
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    user_prompt = build_notification_prompt(
        trigger_type=request.triggerType,
        compressed_summary=request.compressedSummary,
        trigger_data=request.triggerData,
    )

    try:
        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=256,
            system=NOTIFICATION_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )

        content = message.content[0].text.strip()
        data = json.loads(content)

        # Enforce length constraints
        title = data.get("title", "Check in with COMPASS")[:60]
        body = data.get("body", "Your monthly reflection is ready.")[:300]

        return NotificationResponse(title=title, body=body)

    except json.JSONDecodeError as e:
        # Fallback notification
        return NotificationResponse(
            title="Your monthly reflection awaits",
            body="Take 10 minutes to capture what's been on your mind this month.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Notification generation error: {str(e)}"
        )
