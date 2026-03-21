def build_notification_prompt(
    trigger_type: str,
    compressed_summary: str | None,
    trigger_data: dict | None = None,
) -> str:
    profile_context = (
        f"Student profile summary:\n{compressed_summary}"
        if compressed_summary
        else "No profile available yet."
    )

    type_instructions = {
        "REFLECTION_NUDGE": """Generate a reflection nudge notification.
Goal: Invite the student to complete their monthly reflection.
Tone: Warm, curious, never urgent or guilt-inducing.
Reference something specific from their profile if available.""",

        "OPPORTUNITY": """Generate an opportunity notification.
Goal: Surface a relevant program, competition, or experience adjacent to their interests.
Tone: Excited but low-pressure. "You might find this interesting" not "Don't miss this!"
Be specific about why it connects to their interests.""",

        "MAP_EXPANSION": """Generate a map expansion notification.
Goal: Show the student that their interests connect to something they may not have considered.
Tone: Curious, expansive. "Did you know that..." energy.""",

        "PEER_PROMPT": """Generate a peer interaction prompt.
Goal: Encourage the student to explore with a peer who has similar interests.
Tone: Social, low-stakes. Never pushy.""",
    }

    instructions = type_instructions.get(
        trigger_type,
        "Generate a helpful notification for this student."
    )

    return f"""You are COMPASS, generating a push notification for a high school student.

{profile_context}

{instructions}

STRICT CONSTRAINTS:
- Title: 8 words maximum, action-oriented
- Body: 50 words maximum, specific and personal
- NEVER: urgency language, FOMO, "don't miss", "last chance", "you should"
- ALWAYS: specific to their interests, warm and curious tone
- Reference their actual interests, not generic educational content

Respond with ONLY this JSON:
{{"title": "Short title here", "body": "Body text here."}}"""


NOTIFICATION_SYSTEM_PROMPT = """You generate warm, personalized notifications for high school students using COMPASS.
Never use urgency, pressure, or guilt. Always be specific to the student's interests.
Respond with valid JSON only."""
