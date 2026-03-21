import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

export interface SynthesisInput {
  studentId: string;
  sessionId?: string;
  activities: {
    name: string;
    category: string;
    excitement?: number | null;
    hoursPerWeek?: number | null;
    isOngoing?: boolean;
  }[];
  reflections: {
    promptText: string;
    responseText?: string | null;
    promptType: string;
  }[];
  previousProfile?: {
    breadthScore: number;
    interestClusters: unknown;
    compressedSummary?: string | null;
  } | null;
}

export interface SynthesisResult {
  interestClusters: object[];
  characterSignals: object[];
  trajectoryShifts: object[];
  gapDetection: object;
  breadthScore: number;
  compressedSummary: string;
}

function buildPrompt(input: SynthesisInput): string {
  const today = new Date().toISOString().split("T")[0]!;

  let activitiesText = "";
  if (input.activities.length > 0) {
    const lines = input.activities.map(
      (a) =>
        `- ${a.name} [${a.category}]: excitement ${a.excitement ?? "?"}/5, ${a.hoursPerWeek ?? "?"} hrs/wk, ongoing=${a.isOngoing ?? true}`
    );
    activitiesText = "ALL ACTIVITIES:\n" + lines.join("\n");
  }

  let reflectionsText = "";
  if (input.reflections.length > 0) {
    const lines = input.reflections
      .filter((r) => r.responseText)
      .slice(0, 15)
      .map(
        (r) =>
          `[${r.promptType}] Q: ${r.promptText.slice(0, 100)}\nA: ${r.responseText!.slice(0, 400)}`
      );
    reflectionsText = "REFLECTION HISTORY:\n\n" + lines.join("\n\n");
  }

  let prevProfileText = "";
  if (input.previousProfile) {
    const clusters = Array.isArray(input.previousProfile.interestClusters)
      ? (input.previousProfile.interestClusters as { label?: string }[]).map(
          (c) => c.label
        )
      : [];
    prevProfileText = `
PREVIOUS SIGNAL PROFILE (for comparison/continuity):
Breadth Score: ${input.previousProfile.breadthScore}
Interest Clusters: ${JSON.stringify(clusters)}
Previous summary: ${(input.previousProfile.compressedSummary ?? "").slice(0, 300)}
`;
  }

  return `You are a longitudinal student analyst for COMPASS, an educational tool for high school students.
Analyze this student's complete history to synthesize a signal profile.

Date: ${today}

${activitiesText}

${reflectionsText}

${prevProfileText}

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
{
  "interestClusters": [
    {
      "id": "cluster-1",
      "label": "Descriptive label",
      "strength": "strong | moderate | emerging",
      "evidenceCount": 3,
      "domains": ["Technology"],
      "lastSeen": "${today.slice(0, 7)}",
      "trend": "rising | stable | declining"
    }
  ],
  "characterSignals": [
    {
      "trait": "Trait name",
      "description": "2-3 sentence description with specific evidence",
      "evidenceExamples": ["Example 1", "Example 2"],
      "confidence": "high | medium | low"
    }
  ],
  "trajectoryShifts": [],
  "gapDetection": {
    "underexploredAreas": ["Area 1"],
    "suggestedExpansions": ["Next step 1"],
    "lastUpdated": "${today}"
  },
  "breadthScore": 45,
  "compressedSummary": "300-400 word narrative summary in third person."
}`;
}

export interface ReflectionPrompt {
  promptText: string;
  promptType: "PATTERN" | "EXPLORATION" | "IDENTITY" | "CHALLENGE";
}

export async function generateReflectionPrompts(input: {
  compressedSummary?: string;
  recentActivities: { name: string; category: string; excitement?: number | null; hoursPerWeek?: number | null }[];
  recentReflections: { promptText: string; responseText?: string | null; promptType: string }[];
  previousPrompts: string[];
}): Promise<ReflectionPrompt[]> {
  const today = new Date().toLocaleString("default", { month: "long", year: "numeric" });

  const activityLines = input.recentActivities.slice(0, 10).map(
    (a) => `- ${a.name} (${a.category}): excitement ${a.excitement ?? "?"}/5, ~${a.hoursPerWeek ?? "?"} hrs/week`
  );
  const activityText = activityLines.length
    ? "Recent activities:\n" + activityLines.join("\n")
    : "";

  const recentAnswered = input.recentReflections
    .filter((r) => r.responseText)
    .slice(-3)
    .map((r) => `[${r.promptType}] ${r.responseText!.slice(0, 200)}`);
  const reflectionText = recentAnswered.length
    ? "Recent reflection excerpts:\n" + recentAnswered.join("\n")
    : "";

  const prevPromptsText = input.previousPrompts.length
    ? "Previously asked prompts (DO NOT repeat):\n" +
      input.previousPrompts.slice(-10).map((p) => `- ${p}`).join("\n")
    : "";

  const profileText = input.compressedSummary
    ? `Student signal profile:\n${input.compressedSummary}`
    : "";

  const prompt = `You are COMPASS, a reflection companion for high school students.
Your role is to help students notice patterns in their own interests and expand their awareness — never to direct or prescribe.

Current month: ${today}

${profileText}

${activityText}

${reflectionText}

${prevPromptsText}

Generate 2-3 thoughtful reflection questions for this student.

STRICT RULES:
- Each question must be under 30 words
- Never tell the student what they should do or pursue
- Connect cross-domain interests when you see them
- No repeats of previous prompts
- Frame everything as curiosity and exploration, never judgment

Question types: PATTERN, EXPLORATION, IDENTITY, CHALLENGE

Respond with ONLY a JSON array:
[{"promptText": "...", "promptType": "PATTERN"}, ...]`;

  const message = await client.messages.create({
    model: "claude-haiku-4-5-20251001",
    max_tokens: 1024,
    system:
      "You are COMPASS, a reflection companion for high school students. Always respond with valid JSON only.",
    messages: [{ role: "user", content: prompt }],
  });

  const firstBlock = message.content[0];
  if (!firstBlock || firstBlock.type !== "text") {
    throw new Error("Unexpected AI response format from generateReflectionPrompts");
  }
  let content = firstBlock.text.trim();
  content = content.replace(/^```(?:json)?\s*/i, "").replace(/\s*```\s*$/, "").trim();
  let data: { promptText: string; promptType: string }[];
  try {
    data = JSON.parse(content) as { promptText: string; promptType: string }[];
  } catch {
    throw new Error("Failed to parse AI response as JSON in generateReflectionPrompts");
  }
  return data.map((p) => ({
    promptText: p.promptText,
    promptType: p.promptType as ReflectionPrompt["promptType"],
  }));
}

export async function synthesizeProfile(
  input: SynthesisInput
): Promise<SynthesisResult> {
  const message = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 4096,
    system:
      "You are a longitudinal student analyst. You identify patterns in students' interests, activities, and reflections to help them understand themselves better. Always respond with valid JSON only. Never prescribe what students should do.",
    messages: [{ role: "user", content: buildPrompt(input) }],
  });

  const firstBlock = message.content[0];
  if (!firstBlock || firstBlock.type !== "text") {
    throw new Error("Unexpected AI response format from synthesizeProfile");
  }
  let content = firstBlock.text.trim();
  content = content.replace(/^```(?:json)?\s*/i, "").replace(/\s*```\s*$/, "").trim();
  let data: Record<string, unknown>;
  try {
    data = JSON.parse(content) as Record<string, unknown>;
  } catch {
    throw new Error("Failed to parse AI response as JSON in synthesizeProfile");
  }

  return {
    interestClusters: (data.interestClusters as object[]) ?? [],
    characterSignals: (data.characterSignals as object[]) ?? [],
    trajectoryShifts: (data.trajectoryShifts as object[]) ?? [],
    gapDetection: (data.gapDetection as object) ?? {},
    breadthScore: typeof data.breadthScore === "number" ? data.breadthScore : 0,
    compressedSummary:
      typeof data.compressedSummary === "string" ? data.compressedSummary : "",
  };
}
