import { requireCounselor } from "@/lib/auth";
import { prisma } from "@compass/db";
import Link from "next/link";

interface StudentRow {
  id: string;
  firstName: string;
  lastName: string;
  gradeLevel: number | null;
  onboardingCompleted: boolean;
  engagementStatus: "active" | "warning" | "inactive";
  breadthScore: number | null;
  topInterests: string[] | null;
  lastSessionDate: Date | null;
}

function EngagementDot({
  status,
}: {
  status: "active" | "warning" | "inactive";
}) {
  const colors = {
    active: "bg-emerald-500",
    warning: "bg-amber-500",
    inactive: "bg-red-500",
  };

  return (
    <div
      className={`w-2.5 h-2.5 rounded-full ${colors[status]} flex-shrink-0`}
      title={status}
    />
  );
}

export default async function CounselorDashboard() {
  const counselor = await requireCounselor();

  // Fetch students via API (applies privacy filtering)
  const studentsRes = await fetch(
    `${process.env.NEXT_PUBLIC_APP_URL}/api/counselor/students`,
    {
      headers: {
        // Internal server-to-server call — auth via service key
        "x-internal": "true",
      },
      cache: "no-store",
    }
  );

  let students: StudentRow[] = [];

  // Fallback: direct DB query
  const rawStudents = await prisma.student.findMany({
    where: { schoolId: counselor.schoolId },
    include: {
      signalProfiles: {
        orderBy: { createdAt: "desc" },
        take: 1,
        select: { breadthScore: true, interestClusters: true },
      },
      sessions: {
        orderBy: { createdAt: "desc" },
        take: 1,
        select: { completedAt: true },
      },
      privacySettings: true,
    },
    orderBy: { lastName: "asc" },
  });

  const now = new Date();

  students = rawStudents.map((s) => {
    const profile = s.signalProfiles[0];
    const lastSession = s.sessions[0];
    const privacy = s.privacySettings;

    let engagementStatus: "active" | "warning" | "inactive" = "inactive";
    if (lastSession?.completedAt) {
      const daysSince = Math.floor(
        (now.getTime() - new Date(lastSession.completedAt).getTime()) /
          (1000 * 60 * 60 * 24)
      );
      if (daysSince <= 45) engagementStatus = "active";
      else if (daysSince <= 90) engagementStatus = "warning";
    }

    const clusters = profile?.interestClusters;
    return {
      id: s.id,
      firstName: s.firstName,
      lastName: s.lastName,
      gradeLevel: s.gradeLevel,
      onboardingCompleted: s.onboardingCompleted,
      engagementStatus,
      breadthScore:
        privacy?.shareBreadthScore !== false ? profile?.breadthScore ?? null : null,
      topInterests:
        privacy?.shareInterestClusters !== false && Array.isArray(clusters)
          ? (clusters as Array<{ label: string }>).slice(0, 2).map((c) => c.label)
          : null,
      lastSessionDate: lastSession?.completedAt ?? null,
    };
  });

  const activeCount = students.filter((s) => s.engagementStatus === "active").length;
  const needsAttentionCount = students.filter(
    (s) => s.engagementStatus !== "active"
  ).length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-[#1A1A2E]">
          Student Dashboard
        </h1>
        <p className="text-[#6B7280] mt-1">
          {students.length} students · {activeCount} active ·{" "}
          {needsAttentionCount} may need attention
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        <div className="glass-card p-4">
          <p className="text-2xl font-bold text-[#1A1A2E]">{students.length}</p>
          <p className="text-sm text-[#6B7280]">Total Students</p>
        </div>
        <div className="glass-card p-4">
          <p className="text-2xl font-bold text-emerald-600">{activeCount}</p>
          <p className="text-sm text-[#6B7280]">Actively Reflecting</p>
        </div>
        <div className="glass-card p-4">
          <p className="text-2xl font-bold text-amber-600">
            {needsAttentionCount}
          </p>
          <p className="text-sm text-[#6B7280]">Need Attention</p>
        </div>
      </div>

      {/* Student Grid */}
      <div className="glass-card overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200/40">
              <th className="text-left px-6 py-4 text-xs font-semibold text-[#6B7280] uppercase tracking-wide">
                Student
              </th>
              <th className="text-left px-4 py-4 text-xs font-semibold text-[#6B7280] uppercase tracking-wide">
                Grade
              </th>
              <th className="text-left px-4 py-4 text-xs font-semibold text-[#6B7280] uppercase tracking-wide">
                Top Interests
              </th>
              <th className="text-left px-4 py-4 text-xs font-semibold text-[#6B7280] uppercase tracking-wide">
                Breadth
              </th>
              <th className="text-left px-4 py-4 text-xs font-semibold text-[#6B7280] uppercase tracking-wide">
                Status
              </th>
              <th className="px-4 py-4" />
            </tr>
          </thead>
          <tbody>
            {students.map((student) => (
              <tr
                key={student.id}
                className="border-b border-gray-200/20 hover:bg-white/30 transition-colors"
              >
                <td className="px-6 py-4">
                  <p className="text-sm font-medium text-[#1A1A2E]">
                    {student.firstName} {student.lastName}
                  </p>
                </td>
                <td className="px-4 py-4">
                  <span className="text-sm text-[#6B7280]">
                    {student.gradeLevel ? `${student.gradeLevel}th` : "—"}
                  </span>
                </td>
                <td className="px-4 py-4">
                  {student.topInterests && student.topInterests.length > 0 ? (
                    <div className="flex flex-wrap gap-1">
                      {student.topInterests.map((interest) => (
                        <span
                          key={interest}
                          className="text-[10px] px-2 py-0.5 bg-blue-50 text-blue-700 rounded-full"
                        >
                          {interest}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <span className="text-xs text-[#9CA3AF]">Private</span>
                  )}
                </td>
                <td className="px-4 py-4">
                  {student.breadthScore !== null ? (
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-[#3B82F6] rounded-full"
                          style={{ width: `${student.breadthScore}%` }}
                        />
                      </div>
                      <span className="text-xs text-[#6B7280]">
                        {Math.round(student.breadthScore)}
                      </span>
                    </div>
                  ) : (
                    <span className="text-xs text-[#9CA3AF]">—</span>
                  )}
                </td>
                <td className="px-4 py-4">
                  <div className="flex items-center gap-2">
                    <EngagementDot status={student.engagementStatus} />
                    <span className="text-xs text-[#6B7280] capitalize">
                      {student.engagementStatus}
                    </span>
                  </div>
                </td>
                <td className="px-4 py-4">
                  <Link
                    href={`/students/${student.id}`}
                    className="text-xs text-[#3B82F6] font-medium hover:underline"
                  >
                    View →
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {students.length === 0 && (
          <div className="py-12 text-center text-[#9CA3AF] text-sm">
            No students found for this school.
          </div>
        )}
      </div>
    </div>
  );
}
