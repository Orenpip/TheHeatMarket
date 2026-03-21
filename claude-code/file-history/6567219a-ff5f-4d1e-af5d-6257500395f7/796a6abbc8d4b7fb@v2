import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";

export async function GET() {
  try {
    const student = await requireStudent();

    // Return a history of what data the counselor has been able to see
    const [privacySettings, sharedReflections, sessions] = await Promise.all([
      prisma.studentPrivacySettings.findUnique({
        where: { studentId: student.id },
      }),
      prisma.reflection.findMany({
        where: { studentId: student.id, isSharedWithCounselor: true },
        select: {
          id: true,
          promptType: true,
          wordCount: true,
          createdAt: true,
          session: { select: { monthKey: true } },
        },
        orderBy: { createdAt: "desc" },
      }),
      prisma.reflectionSession.count({
        where: { studentId: student.id, completedAt: { not: null } },
      }),
    ]);

    return NextResponse.json({
      currentSettings: privacySettings ?? {
        shareInterestClusters: true,
        shareBreadthScore: true,
        shareTrajectoryShifts: true,
        shareCharacterSignals: true,
      },
      sharedReflectionsCount: sharedReflections.length,
      sharedReflections: sharedReflections.map((r) => ({
        id: r.id,
        promptType: r.promptType,
        wordCount: r.wordCount,
        monthKey: r.session.monthKey,
        sharedAt: r.createdAt,
      })),
      totalSessionsCompleted: sessions,
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
