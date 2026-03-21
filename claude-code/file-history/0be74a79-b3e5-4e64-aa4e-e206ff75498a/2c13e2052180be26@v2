import { NextResponse } from "next/server";
import { requireCounselor, apiError } from "@/lib/auth";
import { prisma } from "@compass/db";

export async function GET() {
  try {
    const counselor = await requireCounselor();

    const students = await prisma.student.findMany({
      where: { schoolId: counselor.schoolId },
      include: {
        signalProfiles: {
          orderBy: { createdAt: "desc" },
          take: 1,
          select: { breadthScore: true, gapDetection: true },
        },
        sessions: {
          orderBy: { createdAt: "desc" },
          take: 1,
          select: { completedAt: true, createdAt: true },
        },
        privacySettings: true,
      },
    });

    const now = new Date();
    const flaggedStudents = [];

    for (const student of students) {
      const flags: string[] = [];
      const lastSession = student.sessions[0];
      const profile = student.signalProfiles[0];

      // Disengagement flag: no session in 90+ days (or never)
      if (!lastSession?.completedAt) {
        if (!student.onboardingCompleted) {
          flags.push("never_onboarded");
        } else {
          flags.push("never_reflected");
        }
      } else {
        const daysSince = Math.floor(
          (now.getTime() - new Date(lastSession.completedAt).getTime()) /
            (1000 * 60 * 60 * 24)
        );
        if (daysSince > 90) {
          flags.push("disengaged");
        }
      }

      // Narrow interest flag: breadthScore < 20
      if (
        student.privacySettings?.shareBreadthScore !== false &&
        profile?.breadthScore !== undefined &&
        profile.breadthScore < 20
      ) {
        flags.push("narrow_interests");
      }

      if (flags.length > 0) {
        flaggedStudents.push({
          id: student.id,
          firstName: student.firstName,
          lastName: student.lastName,
          gradeLevel: student.gradeLevel,
          flags,
          breadthScore:
            student.privacySettings?.shareBreadthScore !== false
              ? profile?.breadthScore
              : null,
          lastSessionDate: lastSession?.completedAt,
        });
      }
    }

    return NextResponse.json(flaggedStudents);
  } catch (error) {
    return apiError(error);
  }
}
