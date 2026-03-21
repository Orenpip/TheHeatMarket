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
        },
        sessions: {
          orderBy: { createdAt: "desc" },
          take: 1,
          select: {
            id: true,
            completedAt: true,
            createdAt: true,
          },
        },
        privacySettings: true,
      },
      orderBy: { lastName: "asc" },
    });

    const now = new Date();

    const result = students.map((student) => {
      const latestProfile = student.signalProfiles[0];
      const lastSession = student.sessions[0];

      // Calculate engagement status
      let engagementStatus: "active" | "warning" | "inactive" = "inactive";
      if (lastSession?.completedAt) {
        const daysSince = Math.floor(
          (now.getTime() - new Date(lastSession.completedAt).getTime()) /
            (1000 * 60 * 60 * 24)
        );
        if (daysSince <= 45) engagementStatus = "active";
        else if (daysSince <= 90) engagementStatus = "warning";
      }

      // Only expose privacy-allowed data
      const privacy = student.privacySettings;
      const clusters = latestProfile?.interestClusters;

      return {
        id: student.id,
        firstName: student.firstName,
        lastName: student.lastName,
        gradeLevel: student.gradeLevel,
        email: student.email,
        onboardingCompleted: student.onboardingCompleted,
        lastSessionDate: lastSession?.completedAt,
        engagementStatus,
        breadthScore:
          privacy?.shareBreadthScore !== false
            ? latestProfile?.breadthScore
            : null,
        topInterests:
          privacy?.shareInterestClusters !== false && Array.isArray(clusters)
            ? (clusters as Array<{ label: string }>)
                .slice(0, 2)
                .map((c) => c.label)
            : null,
        hasSignalProfile: !!latestProfile,
      };
    });

    return NextResponse.json(result);
  } catch (error) {
    return apiError(error);
  }
}
