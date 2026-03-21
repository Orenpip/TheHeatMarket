export interface InterestCluster {
  id: string;
  label: string;
  strength: "strong" | "moderate" | "emerging";
  evidenceCount: number;
  domains: string[];
  lastSeen: string; // ISO date
  trend: "rising" | "stable" | "declining";
}

export interface CharacterSignal {
  trait: string;
  description: string;
  evidenceExamples: string[];
  confidence: "high" | "medium" | "low";
}

export interface TrajectoryShift {
  fromArea: string;
  toArea: string;
  detectedAt: string; // ISO date
  description: string;
  isSignificant: boolean;
}

export interface GapDetection {
  underexploredAreas: string[];
  suggestedExpansions: string[];
  lastUpdated: string;
}

export interface SignalProfile {
  id: string;
  studentId: string;
  interestClusters: InterestCluster[];
  characterSignals: CharacterSignal[];
  trajectoryShifts: TrajectoryShift[];
  gapDetection: GapDetection;
  breadthScore: number; // 0-100
  compressedSummary?: string;
  lastSynthesizedAt?: Date;
  synthesisVersion: number;
  createdAt: Date;
}

export interface ReflectionPrompt {
  promptText: string;
  promptType: "PATTERN" | "EXPLORATION" | "IDENTITY" | "CHALLENGE";
}

export interface SynthesisRequest {
  studentId: string;
  sessionId?: string;
}

export interface SynthesisResponse {
  interestClusters: InterestCluster[];
  characterSignals: CharacterSignal[];
  trajectoryShifts: TrajectoryShift[];
  gapDetection: GapDetection;
  breadthScore: number;
  compressedSummary: string;
}
