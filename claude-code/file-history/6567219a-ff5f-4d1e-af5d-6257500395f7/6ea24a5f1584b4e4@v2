export type ActivityCategory =
  | "ACADEMIC"
  | "EXTRACURRICULAR"
  | "READING"
  | "PROJECT"
  | "WORK"
  | "VOLUNTEER"
  | "HOBBY";

export type PromptType =
  | "PATTERN"
  | "EXPLORATION"
  | "IDENTITY"
  | "CHALLENGE";

export interface ReflectionSession {
  id: string;
  studentId: string;
  monthKey: string; // "2025-03" format
  pulseScore?: number; // 1-10
  pulseNote?: string;
  completedAt?: Date;
  durationSeconds?: number;
  createdAt: Date;
  activities?: Activity[];
  reflections?: Reflection[];
}

export interface Activity {
  id: string;
  studentId: string;
  sessionId?: string;
  category: ActivityCategory;
  name: string;
  description?: string;
  hoursPerWeek?: number;
  excitement?: number; // 1-5
  isOngoing: boolean;
  startDate?: Date;
  endDate?: Date;
  createdAt: Date;
}

export interface Reflection {
  id: string;
  studentId: string;
  sessionId: string;
  promptText: string;
  responseText?: string;
  promptType: PromptType;
  isSharedWithCounselor: boolean;
  wordCount?: number;
  createdAt: Date;
}

export interface SessionWizardState {
  sessionId: string;
  currentStep: 1 | 2 | 3 | 4 | 5;
  pulseScore?: number;
  pulseNote?: string;
  activities: Activity[];
  reflections: Reflection[];
  privacySelections: Record<string, boolean>;
}

export interface CreateSessionInput {
  monthKey?: string;
}

export interface CreateActivityInput {
  sessionId?: string;
  category: ActivityCategory;
  name: string;
  description?: string;
  hoursPerWeek?: number;
  excitement?: number;
  isOngoing?: boolean;
  startDate?: string;
  endDate?: string;
}

export interface SaveReflectionInput {
  sessionId: string;
  promptText: string;
  responseText?: string;
  promptType: PromptType;
  isSharedWithCounselor?: boolean;
}
