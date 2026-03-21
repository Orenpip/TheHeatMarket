import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";
import { Client } from "@upstash/qstash";
import { redis, CACHE_KEYS, rateLimiters } from "@/lib/redis";
import { synthesizeProfile } from "@/lib/synthesize";

export const maxDuration = 60;

function getQStash() {
  return new Client({ token: process.env.QSTASH_TOKEN! });
}

export async function POST(
  _req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const student = await requireStudent();
    const { id } = await params;

    const { success } = await rateLimiters.sessionSubmit.limit(student.id);
    if (!success) {
      return NextResponse.json({ error: "Too many requests" }, { status: 429 });
    }

    const session = await prisma.reflectionSession.findFirst({
      where: { id, studentId: student.id },
    });

    if (!session) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    if (session.completedAt) {
      return NextResponse.json({ error: "Session already submitted" }, { status: 400 });
    }

    // Mark session as complete
    const now = new Date();
    const durationSeconds = Math.floor(
      (now.getTime() - session.createdAt.getTime()) / 1000
    );

    await prisma.reflectionSession.update({
      where: { id },
      data: { completedAt: now, durationSeconds },
    });

    // Run synthesis directly (primary path — no external service dependency)
    try {
      const [activities, reflections, previousProfile] = await Promise.all([
        prisma.activity.findMany({
          where: { studentId: student.id },
          orderBy: { createdAt: "asc" },
        }),
        prisma.reflection.findMany({
          where: { studentId: student.id },
          orderBy: { createdAt: "asc" },
        }),
        prisma.signalProfile.findFirst({
          where: { studentId: student.id },
          orderBy: { createdAt: "desc" },
        }),
      ]);

      const synthesis = await synthesizeProfile({
        studentId: student.id,
        sessionId: id,
        activities: activities.map((a) => ({
          ...a,
          hoursPerWeek: a.hoursPerWeek ? Number(a.hoursPerWeek) : null,
        })),
        reflections,
        previousProfile,
      });

      await prisma.signalProfile.upsert({
        where: { studentId_sessionId: { studentId: student.id, sessionId: id } },
        create: {
          studentId: student.id,
          sessionId: id,
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
        redis.del(CACHE_KEYS.signalProfile(student.id)),
        redis.del(CACHE_KEYS.personalizedMap(student.id)),
      ]).catch(() => {});
    } catch (e) {
      console.error("Direct synthesis failed:", e);
      // Enqueue QStash as fallback so synthesis retries asynchronously
      if (process.env.QSTASH_TOKEN) {
        try {
          const appUrl = process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000";
          await getQStash().publishJSON({
            url: `${appUrl}/api/webhooks/qstash`,
            body: {
              type: "POST_SESSION_SYNTHESIS",
              data: { studentId: student.id, sessionId: id },
              triggeredAt: now.toISOString(),
            },
            delay: 10,
          });
        } catch (qe) {
          console.error("QStash fallback also failed:", qe);
        }
      }
    }

    return NextResponse.json({ success: true, completedAt: now });
  } catch (error) {
    return apiError(error);
  }
}
