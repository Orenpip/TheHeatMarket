from datetime import datetime


def build_synthesis_prompt(
    activities: list[dict],
    reflections: list[dict],
    previous_profile: dict | None,
) -> str:
    activities_text = ""
    if activities:
        activity_lines = [
            f"- {a.get('name')} [{a.get('category')}]: "
            f"excitement {a.get('excitement', '?')}/5, "
            f"{a.get('hoursPerWeek', '?')} hrs/wk, "
            f"ongoing={a.get('isOngoing', True)}"
            for a in activities
        ]
        activities_text = "ALL ACTIVITIES:\n" + "\n".join(activity_lines)

    reflections_text = ""
    if reflections:
        reflection_lines = []
        for r in reflections:
            if r.get("responseText"):
                reflection_lines.append(
                    f"[{r.get('promptType')}] Q: {r.get('promptText', '')[:100]}\n"
                    f"A: {r.get('responseText', '')[:400]}"
                )
        reflections_text = "REFLECTION HISTORY:\n\n".join(reflection_lines[:15])

    prev_profile_text = ""
    if previous_profile:
        prev_profile_text = f"""
PREVIOUS SIGNAL PROFILE (for comparison/continuity):
Breadth Score: {previous_profile.get('breadthScore', 0)}
Interest Clusters: {[c.get('label') for c in previous_profile.get('interestClusters', [])]}
Previous summary: {previous_profile.get('compressedSummary', '')[:300]}
"""

    today = datetime.now().strftime("%Y-%m-%d")

    return f"""You are a longitudinal student analyst for COMPASS, an educational tool for high school students.
Analyze this student's complete history to synthesize a signal profile.

Date: {today}

{activities_text}

{reflections_text}

{prev_profile_text}

Synthesize a comprehensive signal profile. Your analysis must be:
1. Evidence-based — cite specific activities/reflections
2. Non-prescriptive — frame interests as "emerging" or "strong," never as fixed destiny
3. Cross-domain aware — notice when technical + creative + social interests overlap
4. Breadth-aware — score 0-100 based on domain diversity (not just number of activities)

Breadth Score guidelines:
- 0-20: Very narrow (1-2 domains)
- 21-40: Developing breadth (3 domains)
- 41-60: Moderate breadth (4-5 domains)
- 61-80: Broad (6-7 diverse domains)
- 81-100: Highly interdisciplinary (8+ domains with deep engagement)

Respond with ONLY valid JSON matching this exact schema:
{{
  "interestClusters": [
    {{
      "id": "cluster-1",
      "label": "Descriptive label (e.g., 'Systems Thinking & Design')",
      "strength": "strong | moderate | emerging",
      "evidenceCount": 3,
      "domains": ["Technology", "Design"],
      "lastSeen": "2025-11",
      "trend": "rising | stable | declining"
    }}
  ],
  "characterSignals": [
    {{
      "trait": "Trait name (e.g., 'Analytical Curiosity')",
      "description": "2-3 sentence description with specific evidence",
      "evidenceExamples": ["Example 1 from their data", "Example 2"],
      "confidence": "high | medium | low"
    }}
  ],
  "trajectoryShifts": [
    {{
      "fromArea": "Previous area of focus",
      "toArea": "New area of interest",
      "detectedAt": "2025-11",
      "description": "What changed and potential significance (1-2 sentences)",
      "isSignificant": true
    }}
  ],
  "gapDetection": {{
    "underexploredAreas": ["Area 1", "Area 2"],
    "suggestedExpansions": ["Natural next step 1", "Natural next step 2"],
    "lastUpdated": "{today}"
  }},
  "breadthScore": 45,
  "compressedSummary": "A 300-400 word narrative summary of this student's signal profile. Write in third person. Cover: their strongest interest clusters, key character traits, any trajectory shifts, and breadth assessment. Frame everything as observations and emerging patterns, never as fixed attributes or prescriptions."
}}"""


SYNTHESIS_SYSTEM_PROMPT = """You are a longitudinal student analyst. You identify patterns in students' interests, activities, and reflections to help them understand themselves better.
Always respond with valid JSON only. Never prescribe what students should do."""
