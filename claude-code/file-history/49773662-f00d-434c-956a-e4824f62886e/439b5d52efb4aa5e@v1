import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import { Client } from "@upstash/qstash";
import { aiService } from "@/lib/ai-service";
import { redis, CACHE_KEYS } from "@/lib/redis";

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
      data: {
        completedAt: now,
        durationSeconds,
      },
    });

    // Try QStash first, fall back to inline synthesis
    let synthesisQueued = false;
    try {
      if (process.env.QSTASH_TOKEN) {
        const appUrl = process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000";
        await getQStash().publishJSON({
          url: `${appUrl}/api/webhooks/qstash`,
          body: {
            type: "POST_SESSION_SYNTHESIS",
            data: {
              studentId: student.id,
              sessionId: id,
            },
            triggeredAt: now.toISOString(),
          },
          delay: 30,
        });
        synthesisQueued = true;
      }
    } catch (e) {
      console.error("Failed to enqueue synthesis job:", e);
    }

    // Inline synthesis fallback if QStash unavailable
    if (!synthesisQueued) {
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

        const synthesis = await aiService.synthesizeProfile({
          studentId: student.id,
          sessionId: id,
          activities,
          reflections,
          previousProfile,
        });

        await prisma.signalProfile.create({
          data: {
            studentId: student.id,
            interestClusters: synthesis.interestClusters as object[],
            characterSignals: synthesis.characterSignals as object[],
            trajectoryShifts: synthesis.trajectoryShifts as object[],
            gapDetection: synthesis.gapDetection as object,
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
        console.error("Inline synthesis failed:", e);
      }
    }

    return NextResponse.json({ success: true, completedAt: now });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
