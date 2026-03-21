import { NextResponse } from "next/server";
import { requireCounselor } from "@/lib/auth";
import { prisma } from "@compass/db";

export async function GET(
  _req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const counselor = await requireCounselor();
    const { id } = await params;

    // Verify student is in counselor's school
    const student = await prisma.student.findFirst({
      where: { id, schoolId: counselor.schoolId },
      include: {
        privacySettings: true,
        signalProfiles: {
          orderBy: { createdAt: "desc" },
          take: 1,
        },
        sessions: {
          orderBy: { createdAt: "desc" },
          include: {
            reflections: {
              where: { isSharedWithCounselor: true },
              select: {
                promptText: true,
                responseText: true,
                promptType: true,
                createdAt: true,
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

    // Build privacy-filtered response
    const summary = {
      studentId: student.id,
      firstName: student.firstName,
      lastName: student.lastName,
      gradeLevel: student.gradeLevel,
      // Signal data (filtered by privacy settings)
      interestClusters:
        privacy?.shareInterestClusters !== false
          ? profile?.interestClusters
          : null,
      characterSignals:
        privacy?.shareCharacterSignals !== false
          ? profile?.characterSignals
          : null,
      trajectoryShifts:
        privacy?.shareTrajectoryShifts !== false
          ? profile?.trajectoryShifts
          : null,
      breadthScore:
        privacy?.shareBreadthScore !== false ? profile?.breadthScore : null,
      gapDetection:
        privacy?.shareInterestClusters !== false ? profile?.gapDetection : null,
      // Shared reflections only
      sharedReflections: student.sessions.flatMap((s) =>
        s.reflections.map((r) => ({
          ...r,
          monthKey: s.monthKey,
        }))
      ),
      sessionsCount: student.sessions.length,
      lastSynthesizedAt: profile?.lastSynthesizedAt,
    };

    return NextResponse.json(summary);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
