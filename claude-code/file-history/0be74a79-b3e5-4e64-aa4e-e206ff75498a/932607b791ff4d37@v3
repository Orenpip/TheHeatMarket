import { NextResponse } from "next/server";
import { requireCounselor, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { redis, CACHE_KEYS, CACHE_TTL, rateLimiters } from "@/lib/redis";
import { aiService } from "@/lib/ai-service";

export const maxDuration = 60;

export async function GET(
  _req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const counselor = await requireCounselor();
    const { id: studentId } = await params;

    const { success } = await rateLimiters.counselorMeetingPrep.limit(counselor.id);
    if (!success) {
      return NextResponse.json({ error: "Too many requests" }, { status: 429 });
    }

    // Check cache
    const cacheKey = CACHE_KEYS.meetingPrep(studentId, counselor.id);
    const cached = await redis.get(cacheKey);
    if (cached) {
      return NextResponse.json(cached);
    }

    // Get student data (privacy filtered)
    const student = await prisma.student.findFirst({
      where: { id: studentId, schoolId: counselor.schoolId },
      include: {
        privacySettings: true,
        signalProfiles: {
          orderBy: { createdAt: "desc" },
          take: 1,
        },
        sessions: {
          take: 3,
          orderBy: { createdAt: "desc" },
          include: {
            reflections: {
              where: { isSharedWithCounselor: true },
              select: {
                promptText: true,
                responseText: true,
                promptType: true,
              },
            },
          },
        },
      },
    });

    if (!student) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    const privacy = student.privacySettings;
    const profile = student.signalProfiles[0];

    const filteredProfile = profile
      ? {
          interestClusters:
            privacy?.shareInterestClusters !== false
              ? profile.interestClusters
              : [],
          characterSignals:
            privacy?.shareCharacterSignals !== false
              ? profile.characterSignals
              : [],
          trajectoryShifts:
            privacy?.shareTrajectoryShifts !== false
              ? profile.trajectoryShifts
              : [],
          breadthScore:
            privacy?.shareBreadthScore !== false ? profile.breadthScore : null,
          compressedSummary:
            privacy?.shareSummary !== false
              ? profile.compressedSummary
              : null,
        }
      : null;

    const sharedReflections = student.sessions.flatMap((s) =>
      s.reflections.map((r) => ({
        ...r,
        monthKey: s.monthKey,
      }))
    );

    const result = await aiService.getMeetingPrep({
      studentId: student.id,
      counselorId: counselor.id,
      signalProfile: filteredProfile,
      sharedReflections,
    });

    // Cache for 24 hours
    await redis.setex(cacheKey, CACHE_TTL.meetingPrep, result);

    return NextResponse.json(result);
  } catch (error) {
    return apiError(error);
  }
}
