const AI_SERVICE_URL = process.env.AI_SERVICE_URL!;
const AI_SERVICE_SECRET_KEY = process.env.AI_SERVICE_SECRET_KEY!;

async function aiServiceFetch<T>(
  path: string,
  body: unknown
): Promise<T> {
  const response = await fetch(`${AI_SERVICE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Service-Key": AI_SERVICE_SECRET_KEY,
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`AI service error ${response.status}: ${text}`);
  }

  return response.json() as Promise<T>;
}

export interface ReflectionPrompt {
  promptText: string;
  promptType: "PATTERN" | "EXPLORATION" | "IDENTITY" | "CHALLENGE";
}

export interface SynthesisResult {
  interestClusters: unknown[];
  characterSignals: unknown[];
  trajectoryShifts: unknown[];
  gapDetection: unknown;
  breadthScore: number;
  compressedSummary: string;
}

export interface NotificationContent {
  title: string;
  body: string;
}

export interface MeetingPrepResult {
  summary: string;
  conversationStarters: string[];
  flags: string[];
}

export const aiService = {
  getReflectionPrompts: (data: {
    studentId: string;
    compressedSummary?: string;
    recentActivities: unknown[];
    recentReflections: unknown[];
    previousPrompts: string[];
  }) =>
    aiServiceFetch<{ prompts: ReflectionPrompt[] }>(
      "/reflection-prompts",
      data
    ),

  synthesizeProfile: (data: {
    studentId: string;
    sessionId?: string;
    activities: unknown[];
    reflections: unknown[];
    previousProfile?: unknown;
  }) =>
    aiServiceFetch<SynthesisResult>("/synthesize-profile", data),

  generateNotification: (data: {
    studentId: string;
    triggerType: string;
    triggerData?: unknown;
    compressedSummary?: string;
  }) =>
    aiServiceFetch<NotificationContent>("/generate-notification", data),

  getMeetingPrep: (data: {
    studentId: string;
    counselorId: string;
    signalProfile: unknown;
    sharedReflections: unknown[];
  }) =>
    aiServiceFetch<MeetingPrepResult>("/meeting-prep", data),
};
