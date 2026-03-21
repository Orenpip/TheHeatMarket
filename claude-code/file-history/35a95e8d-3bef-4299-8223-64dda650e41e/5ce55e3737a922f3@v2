from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum


class PromptType(str, Enum):
    PATTERN = "PATTERN"
    EXPLORATION = "EXPLORATION"
    IDENTITY = "IDENTITY"
    CHALLENGE = "CHALLENGE"


class ReflectionPrompt(BaseModel):
    promptText: str
    promptType: PromptType


class ReflectionPromptsRequest(BaseModel):
    studentId: str
    compressedSummary: Optional[str] = None
    recentActivities: list[dict[str, Any]] = []
    recentReflections: list[dict[str, Any]] = []
    previousPrompts: list[str] = []


class ReflectionPromptsResponse(BaseModel):
    prompts: list[ReflectionPrompt]


class SynthesisRequest(BaseModel):
    studentId: str
    sessionId: Optional[str] = None
    activities: list[dict[str, Any]] = []
    reflections: list[dict[str, Any]] = []
    previousProfile: Optional[dict[str, Any]] = None


class InterestCluster(BaseModel):
    id: str
    label: str
    strength: str  # strong | moderate | emerging
    evidenceCount: int
    domains: list[str]
    lastSeen: str
    trend: str  # rising | stable | declining


class CharacterSignal(BaseModel):
    trait: str
    description: str
    evidenceExamples: list[str]
    confidence: str  # high | medium | low


class TrajectoryShift(BaseModel):
    fromArea: str
    toArea: str
    detectedAt: str
    description: str
    isSignificant: bool


class GapDetection(BaseModel):
    underexploredAreas: list[str]
    suggestedExpansions: list[str]
    lastUpdated: str


class SynthesisResponse(BaseModel):
    interestClusters: list[InterestCluster]
    characterSignals: list[CharacterSignal]
    trajectoryShifts: list[TrajectoryShift]
    gapDetection: GapDetection
    breadthScore: float
    compressedSummary: str


class NotificationRequest(BaseModel):
    studentId: str
    triggerType: str
    triggerData: Optional[dict[str, Any]] = None
    compressedSummary: Optional[str] = None


class NotificationResponse(BaseModel):
    title: str
    body: str


class MeetingPrepRequest(BaseModel):
    studentId: str
    counselorId: str
    signalProfile: Optional[dict[str, Any]] = None
    sharedReflections: list[dict[str, Any]] = []


class MeetingPrepResponse(BaseModel):
    summary: str
    conversationStarters: list[str]
    flags: list[str]


class EmbedRequest(BaseModel):
    text: str


class EmbedResponse(BaseModel):
    embedding: list[float]


class OpportunityForExplanation(BaseModel):
    id: str
    title: str
    description: str
    category: str


class ExplainMatchRequest(BaseModel):
    studentSummary: str
    opportunities: list[OpportunityForExplanation]


class OpportunityExplanation(BaseModel):
    id: str
    reason: str


class ExplainMatchResponse(BaseModel):
    explanations: list[OpportunityExplanation]
