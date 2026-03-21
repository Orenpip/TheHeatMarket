import { NextResponse } from "next/server";
import { requireStudent, apiError } from "@/lib/auth";
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
        shareSummary: false,
      },
      create: {
        studentId: student.id,
        shareInterestClusters: false,
        shareBreadthScore: false,
        shareTrajectoryShifts: false,
        shareCharacterSignals: false,
        shareSummary: false,
      },
    });

    // Also set all reflections to private
    await prisma.reflection.updateMany({
      where: { studentId: student.id },
      data: { isSharedWithCounselor: false },
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    return apiError(error);
  }
}
