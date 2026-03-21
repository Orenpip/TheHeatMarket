import { Redis } from "@upstash/redis";

export const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

export const CACHE_KEYS = {
  signalProfile: (studentId: string) => `signal:${studentId}`,
  personalizedMap: (studentId: string) => `map:personalized:${studentId}`,
  meetingPrep: (studentId: string, counselorId: string) =>
    `meeting-prep:${studentId}:${counselorId}`,
  notificationCount: (studentId: string, weekKey: string) =>
    `notif-count:${studentId}:${weekKey}`,
} as const;

export const CACHE_TTL = {
  signalProfile: 60 * 60,        // 1 hour
  personalizedMap: 60 * 60,       // 1 hour
  meetingPrep: 60 * 60 * 24,      // 24 hours
  notificationCount: 60 * 60 * 24 * 7, // 1 week
} as const;
