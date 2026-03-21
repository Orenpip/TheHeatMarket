from datetime import datetime


def build_meeting_prep_prompt(
    signal_profile: dict | None,
    shared_reflections: list[dict],
) -> str:
    profile_text = ""
    if signal_profile:
        clusters = signal_profile.get("interestClusters", [])
        traits = signal_profile.get("characterSignals", [])
        shifts = signal_profile.get("trajectoryShifts", [])
        breadth = signal_profile.get("breadthScore")
        summary = signal_profile.get("compressedSummary", "")

        profile_text = f"""SYNTHESIZED PROFILE:
Breadth Score: {breadth}/100
Interest Clusters: {', '.join(c.get('label', '') for c in clusters[:3])}
Key Character Traits: {', '.join(t.get('trait', '') for t in traits[:3])}
Trajectory Shifts: {len(shifts)} detected
Profile Summary: {summary[:400] if summary else "Not available"}"""

    reflections_text = ""
    if shared_reflections:
        shared = [r for r in shared_reflections if r.get("responseText")][:5]
        if shared:
            reflection_lines = [
                f"[{r.get('promptType')}]: {r.get('responseText', '')[:200]}"
                for r in shared
            ]
            reflections_text = "SHARED REFLECTIONS (student-consented):\n" + "\n\n".join(reflection_lines)

    today = datetime.now().strftime("%B %Y")

    return f"""You are a counselor support assistant for COMPASS.
Prepare a meeting brief for a school counselor about to meet with a student.
Date: {today}

{profile_text}

{reflections_text}

CRITICAL INSTRUCTIONS:
- This output goes to a COUNSELOR, not the student
- Write professional but warm language
- NEVER include raw reflection text — synthesize and paraphrase
- Flag things that might need counselor attention (disengagement, narrow interests, stress signals)
- Suggest 2-3 open-ended conversation starters that won't feel scripted
- Maximum 300 words total
- Respect student privacy — this is synthesized data only

Respond with ONLY this JSON:
{{
  "summary": "2-3 paragraph synthesized summary of where the student is developmentally",
  "conversationStarters": [
    "Open-ended question 1",
    "Open-ended question 2",
    "Open-ended question 3"
  ],
  "flags": [
    "Any concerns to note — or empty array if none"
  ]
}}"""


COUNSELOR_SYSTEM_PROMPT = """You are a counselor support assistant. You help school counselors understand their students' developmental trajectories.
Always synthesize, never quote raw student data. Maintain professional warmth.
Respond with valid JSON only."""
