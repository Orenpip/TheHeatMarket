import { NextResponse } from "next/server";
import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";

export async function POST() {
  try {
    const student = await requireStudent();

    // Make everything private
    await prisma.studentPrivacySettings.upsert({
      where: { studentId: student.id },
      update: {
        shareInterestClusters: false,
        shareBreadthScore: false,
        shareTrajectoryShifts: false,
        shareCharacterSignals: false,
      },
      create: {
        studentId: student.id,
        shareInterestClusters: false,
        shareBreadthScore: false,
        shareTrajectoryShifts: false,
        shareCharacterSignals: false,
      },
    });

    // Also set all reflections to private
    await prisma.reflection.updateMany({
      where: { studentId: student.id },
      data: { isSharedWithCounselor: false },
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
