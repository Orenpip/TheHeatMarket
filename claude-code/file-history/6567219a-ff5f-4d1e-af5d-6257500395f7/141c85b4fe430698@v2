import { requireCounselor } from "@/lib/auth";
import { prisma } from "@compass/db";
import Link from "next/link";

const FLAG_LABELS: Record<string, { label: string; color: string; description: string }> = {
  never_onboarded: {
    label: "Never Onboarded",
    color: "text-red-600 bg-red-50 border-red-200",
    description: "Has not completed the onboarding flow",
  },
  never_reflected: {
    label: "Never Reflected",
    color: "text-orange-600 bg-orange-50 border-orange-200",
    description: "Completed onboarding but never submitted a reflection",
  },
  disengaged: {
    label: "Disengaged",
    color: "text-amber-600 bg-amber-50 border-amber-200",
    description: "No completed reflection in 90+ days",
  },
  narrow_interests: {
    label: "Narrow Interests",
    color: "text-violet-600 bg-violet-50 border-violet-200",
    description: "Breadth score below 20 — very focused on 1-2 areas",
  },
};

export default async function FlagsPage() {
  const counselor = await requireCounselor();

  const students = await prisma.student.findMany({
    where: { schoolId: counselor.schoolId },
    include: {
      signalProfiles: {
        orderBy: { createdAt: "desc" },
        take: 1,
        select: { breadthScore: true },
      },
      sessions: {
        orderBy: { createdAt: "desc" },
        take: 1,
        select: { completedAt: true },
      },
      privacySettings: true,
    },
  });

  const now = new Date();
  const flaggedStudents: Array<{
    id: string;
    firstName: string;
    lastName: string;
    gradeLevel: number | null;
    flags: string[];
    breadthScore: number | null;
    lastSessionDate: Date | null;
  }> = [];

  for (const student of students) {
    const flags: string[] = [];
    const lastSession = student.sessions[0];
    const profile = student.signalProfiles[0];

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
            ? profile?.breadthScore ?? null
            : null,
        lastSessionDate: lastSession?.completedAt ?? null,
      });
    }
  }

  // Sort: most flags first
  flaggedStudents.sort((a, b) => b.flags.length - a.flags.length);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-[#1A1A2E]">Needs Attention</h1>
        <p className="text-[#6B7280] mt-1">
          {flaggedStudents.length} student
          {flaggedStudents.length !== 1 ? "s" : ""} flagged across your school
        </p>
      </div>

      {/* Legend */}
      <div className="glass-card p-4">
        <h2 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wide mb-3">
          Flag Types
        </h2>
        <div className="grid grid-cols-2 gap-2">
          {Object.entries(FLAG_LABELS).map(([key, val]) => (
            <div key={key} className="flex items-start gap-2">
              <span
                className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${val.color}`}
              >
                {val.label}
              </span>
              <p className="text-[10px] text-[#9CA3AF]">{val.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Flagged Students */}
      {flaggedStudents.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <div className="text-4xl mb-3">✅</div>
          <h3 className="font-semibold text-[#1A1A2E] mb-1">All clear!</h3>
          <p className="text-sm text-[#6B7280]">
            No students currently need attention.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {flaggedStudents.map((student) => (
            <div key={student.id} className="glass-card p-5">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="font-semibold text-[#1A1A2E]">
                      {student.firstName} {student.lastName}
                    </h3>
                    {student.gradeLevel && (
                      <span className="text-xs text-[#9CA3AF]">
                        Grade {student.gradeLevel}
                      </span>
                    )}
                  </div>

                  <div className="flex flex-wrap gap-1.5 mb-2">
                    {student.flags.map((flag) => {
                      const flagInfo = FLAG_LABELS[flag];
                      if (!flagInfo) return null;
                      return (
                        <span
                          key={flag}
                          className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${flagInfo.color}`}
                        >
                          {flagInfo.label}
                        </span>
                      );
                    })}
                  </div>

                  <div className="flex gap-4 text-xs text-[#9CA3AF]">
                    {student.lastSessionDate ? (
                      <span>
                        Last reflected{" "}
                        {new Date(student.lastSessionDate).toLocaleDateString(
                          "en-US",
                          { month: "short", day: "numeric", year: "numeric" }
                        )}
                      </span>
                    ) : (
                      <span>Never reflected</span>
                    )}
                    {student.breadthScore !== null && (
                      <span>Breadth: {Math.round(student.breadthScore)}/100</span>
                    )}
                  </div>
                </div>

                <Link
                  href={`/students/${student.id}`}
                  className="text-sm text-[#3B82F6] font-medium hover:underline ml-4 flex-shrink-0"
                >
                  View profile →
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
