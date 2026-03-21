from fastapi import APIRouter, HTTPException
import anthropic
import json
from datetime import datetime
from app.models.requests import SynthesisRequest, SynthesisResponse, InterestCluster, CharacterSignal, TrajectoryShift, GapDetection
from app.prompts.synthesis import build_synthesis_prompt, SYNTHESIS_SYSTEM_PROMPT
from app.config import get_settings

router = APIRouter()


@router.post("/synthesize-profile", response_model=SynthesisResponse)
async def synthesize_profile(request: SynthesisRequest) -> SynthesisResponse:
    settings = get_settings()
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    user_prompt = build_synthesis_prompt(
        activities=request.activities,
        reflections=request.reflections,
        previous_profile=request.previousProfile,
    )

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYNTHESIS_SYSTEM_PROMPT,
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

        today = datetime.now().strftime("%Y-%m-%d")

        return SynthesisResponse(
            interestClusters=[
                InterestCluster(**cluster)
                for cluster in data.get("interestClusters", [])
            ],
            characterSignals=[
                CharacterSignal(**signal)
                for signal in data.get("characterSignals", [])
            ],
            trajectoryShifts=[
                TrajectoryShift(**shift)
                for shift in data.get("trajectoryShifts", [])
            ],
            gapDetection=GapDetection(
                **{
                    **data.get("gapDetection", {}),
                    "lastUpdated": data.get("gapDetection", {}).get("lastUpdated", today),
                }
            ),
            breadthScore=float(data.get("breadthScore", 0)),
            compressedSummary=data.get("compressedSummary", ""),
        )

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse synthesis response: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Synthesis error: {str(e)}"
        )
