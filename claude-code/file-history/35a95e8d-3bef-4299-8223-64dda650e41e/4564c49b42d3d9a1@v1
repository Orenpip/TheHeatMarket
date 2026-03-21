import { Redis } from "@upstash/redis";
import { Ratelimit } from "@upstash/ratelimit";

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

export const rateLimiters = {
  sessionCreate: new Ratelimit({
    redis,
    limiter: Ratelimit.slidingWindow(10, "1 h"),
    prefix: "rl:session-create",
  }),
  sessionSubmit: new Ratelimit({
    redis,
    limiter: Ratelimit.slidingWindow(5, "1 h"),
    prefix: "rl:session-submit",
  }),
  personalizedMap: new Ratelimit({
    redis,
    limiter: Ratelimit.slidingWindow(20, "1 m"),
    prefix: "rl:map-personalized",
  }),
  reflectionsCreate: new Ratelimit({
    redis,
    limiter: Ratelimit.slidingWindow(30, "1 h"),
    prefix: "rl:reflections-create",
  }),
  activitiesCreate: new Ratelimit({
    redis,
    limiter: Ratelimit.slidingWindow(30, "1 h"),
    prefix: "rl:activities-create",
  }),
  counselorMeetingPrep: new Ratelimit({
    redis,
    limiter: Ratelimit.slidingWindow(10, "1 h"),
    prefix: "rl:counselor-meeting-prep",
  }),
};

export const CACHE_TTL = {
  signalProfile: 60 * 60,        // 1 hour
  personalizedMap: 60 * 60,       // 1 hour
  meetingPrep: 60 * 60 * 24,      // 24 hours
  notificationCount: 60 * 60 * 24 * 7, // 1 week
} as const;
