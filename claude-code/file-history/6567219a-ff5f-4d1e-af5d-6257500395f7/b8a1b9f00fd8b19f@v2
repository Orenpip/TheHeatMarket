export type Role = "STUDENT" | "COUNSELOR" | "ADMIN";

export interface Student {
  id: string;
  clerkId: string;
  email: string;
  firstName: string;
  lastName: string;
  gradeLevel?: number; // 9-12
  schoolId?: string;
  onboardingCompleted: boolean;
  createdAt: Date;
  updatedAt: Date;
  school?: School;
}

export interface Counselor {
  id: string;
  clerkId: string;
  email: string;
  firstName: string;
  lastName: string;
  schoolId: string;
  createdAt: Date;
  school: School;
}

export interface School {
  id: string;
  name: string;
  district?: string;
  state?: string;
  tier: "free" | "licensed";
  licenseExpires?: Date;
  createdAt: Date;
}

export interface StudentPrivacySettings {
  studentId: string;
  shareInterestClusters: boolean;
  shareBreadthScore: boolean;
  shareTrajectoryShifts: boolean;
  shareCharacterSignals: boolean;
  updatedAt: Date;
}

export interface StudentWithStats extends Student {
  breadthScore?: number;
  topInterests?: string[];
  lastSessionDate?: Date;
  engagementStatus?: "active" | "warning" | "inactive";
  sessionsCount?: number;
}
