export type NotificationType =
  | "REFLECTION_NUDGE"
  | "OPPORTUNITY"
  | "MAP_EXPANSION"
  | "PEER_PROMPT";

export interface Notification {
  id: string;
  studentId: string;
  type: NotificationType;
  title: string;
  body: string;
  relatedNodeId?: string;
  deliveredAt?: Date;
  readAt?: Date;
  actedOn: boolean;
  createdAt: Date;
}

export interface NotificationPreferences {
  studentId: string;
  maxPerWeek: number;
  reflectionNudges: boolean;
  opportunityAlerts: boolean;
  mapExpansions: boolean;
  peerPrompts: boolean;
  quietHoursStart: string; // "21:00"
  quietHoursEnd: string;   // "08:00"
}

export interface QStashJobPayload {
  type:
    | "WEEKLY_NUDGE_SWEEP"
    | "OPPORTUNITY_SWEEP"
    | "POST_SESSION_SYNTHESIS";
  data: Record<string, unknown>;
  triggeredAt: string;
}

export interface GenerateNotificationRequest {
  studentId: string;
  triggerType: NotificationType;
  triggerData?: Record<string, unknown>;
}

export interface GenerateNotificationResponse {
  title: string;
  body: string;
}
