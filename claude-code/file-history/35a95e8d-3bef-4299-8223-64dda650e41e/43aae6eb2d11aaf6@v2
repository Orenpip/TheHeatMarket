import { NextResponse } from "next/server";
import { requireAdmin, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { synthesizeProfile } from "@/lib/synthesize";
import { redis, CACHE_KEYS } from "@/lib/redis";

export const maxDuration = 60;

// POST /api/admin/retrigger-synthesis
// Body: { studentId: string } — re-runs synthesis for the student's latest completed session
export async function POST(req: Request) {
  try {
    await requireAdmin();

    const { studentId } = (await req.json()) as { studentId?: string };
    if (!studentId) {
      return NextResponse.json({ error: "studentId required" }, { status: 400 });
    }

    // Find latest completed session
    const session = await prisma.reflectionSession.findFirst({
      where: { studentId, completedAt: { not: null } },
      orderBy: { completedAt: "desc" },
    });

    if (!session) {
      return NextResponse.json({ error: "No completed session found" }, { status: 404 });
    }

    const [activities, reflections, previousProfile] = await Promise.all([
      prisma.activity.findMany({
        where: { studentId },
        orderBy: { createdAt: "asc" },
      }),
      prisma.reflection.findMany({
        where: { studentId },
        orderBy: { createdAt: "asc" },
      }),
      prisma.signalProfile.findFirst({
        where: { studentId, sessionId: { not: session.id } },
        orderBy: { createdAt: "desc" },
      }),
    ]);

    const synthesis = await synthesizeProfile({
      studentId,
      sessionId: session.id,
      activities: activities.map((a) => ({
        ...a,
        hoursPerWeek: a.hoursPerWeek ? Number(a.hoursPerWeek) : null,
      })),
      reflections,
      previousProfile,
    });

    await prisma.signalProfile.upsert({
      where: { studentId_sessionId: { studentId, sessionId: session.id } },
      create: {
        studentId,
        sessionId: session.id,
        interestClusters: synthesis.interestClusters,
        characterSignals: synthesis.characterSignals,
        trajectoryShifts: synthesis.trajectoryShifts,
        gapDetection: synthesis.gapDetection,
        breadthScore: synthesis.breadthScore,
        compressedSummary: synthesis.compressedSummary,
        lastSynthesizedAt: new Date(),
      },
      update: {
        interestClusters: synthesis.interestClusters,
        characterSignals: synthesis.characterSignals,
        trajectoryShifts: synthesis.trajectoryShifts,
        gapDetection: synthesis.gapDetection,
        breadthScore: synthesis.breadthScore,
        compressedSummary: synthesis.compressedSummary,
        lastSynthesizedAt: new Date(),
      },
    });

    await Promise.all([
      redis.del(CACHE_KEYS.signalProfile(studentId)),
      redis.del(CACHE_KEYS.personalizedMap(studentId)),
      redis.del(CACHE_KEYS.exploreFeed(studentId)),
    ]).catch(() => {});

    return NextResponse.json({
      success: true,
      sessionId: session.id,
      breadthScore: synthesis.breadthScore,
      summary: synthesis.compressedSummary.slice(0, 100) + "...",
    });
  } catch (error) {
    return apiError(error);
  }
}
