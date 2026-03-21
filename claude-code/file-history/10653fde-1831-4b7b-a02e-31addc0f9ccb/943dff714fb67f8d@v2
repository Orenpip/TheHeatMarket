import { requireCounselor } from "@/lib/auth";
import { prisma } from "@compass/db";
import { notFound } from "next/navigation";
import { SignalBadge } from "@compass/ui";
import MeetingPrepPanel from "@/components/counselor/MeetingPrepPanel";

interface InterestCluster {
  id: string;
  label: string;
  strength: "strong" | "moderate" | "emerging";
  trend: "rising" | "stable" | "declining";
}

interface CharacterSignal {
  trait: string;
  description: string;
  confidence: "high" | "medium" | "low";
}

interface TrajectoryShift {
  fromArea: string;
  toArea: string;
  detectedAt: string;
  description: string;
  isSignificant: boolean;
}

export default async function StudentDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const counselor = await requireCounselor();
  const { id } = await params;

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
        take: 5,
        select: {
          id: true,
          monthKey: true,
          completedAt: true,
          activities: { select: { id: true } },
          reflections: {
            where: { isSharedWithCounselor: true },
            select: {
              id: true,
              promptText: true,
              responseText: true,
              promptType: true,
            },
          },
        },
      },
    },
  });

  if (!student) notFound();

  const profile = student.signalProfiles[0];
  const privacy = student.privacySettings;

  const clusters = privacy?.shareInterestClusters !== false
    ? ((profile?.interestClusters as unknown as InterestCluster[]) ?? [])
    : [];
  const characterSignals = privacy?.shareCharacterSignals !== false
    ? ((profile?.characterSignals as unknown as CharacterSignal[]) ?? [])
    : [];
  const trajectoryShifts = privacy?.shareTrajectoryShifts !== false
    ? ((profile?.trajectoryShifts as unknown as TrajectoryShift[]) ?? [])
    : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-[#1A1A2E]">
            {student.firstName} {student.lastName}
          </h1>
          <p className="text-[#6B7280] mt-1">
            Grade {student.gradeLevel ?? "?"} ·{" "}
            {student.sessions.filter((s) => s.completedAt).length} completed
            sessions
          </p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="col-span-2 space-y-5">
          {/* Interest Clusters */}
          {clusters.length > 0 ? (
            <div className="glass-card p-5">
              <h2 className="font-semibold text-[#1A1A2E] mb-3">
                Interest Signals
              </h2>
              <div className="flex flex-wrap gap-2 mb-4">
                {clusters.map((cluster) => (
                  <SignalBadge
                    key={cluster.id}
                    label={cluster.label}
                    strength={cluster.strength}
                  />
                ))}
              </div>
              {trajectoryShifts.length > 0 && (
                <div className="border-t border-gray-200/40 pt-3 mt-3">
                  <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wide mb-2">
                    Interest Shifts
                  </h3>
                  {trajectoryShifts.map((shift, i) => (
                    <div key={i} className="flex items-center gap-2 text-sm text-[#6B7280]">
                      <span>{shift.fromArea}</span>
                      <span className="text-[#3B82F6]">→</span>
                      <span className="text-[#1A1A2E] font-medium">{shift.toArea}</span>
                      {shift.isSignificant && (
                        <span className="text-xs text-amber-600">Notable shift</span>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className="glass-card p-5 text-center text-[#9CA3AF] text-sm">
              Signal data is private or not yet available
            </div>
          )}

          {/* Character Signals */}
          {characterSignals.length > 0 && (
            <div className="glass-card p-5">
              <h2 className="font-semibold text-[#1A1A2E] mb-3">
                Character Signals
              </h2>
              <div className="space-y-3">
                {characterSignals.map((signal, i) => (
                  <div key={i} className="flex items-start gap-3">
                    <div
                      className={`mt-1 w-2 h-2 rounded-full flex-shrink-0 ${
                        signal.confidence === "high"
                          ? "bg-emerald-500"
                          : signal.confidence === "medium"
                          ? "bg-amber-500"
                          : "bg-gray-400"
                      }`}
                    />
                    <div>
                      <p className="text-sm font-medium text-[#1A1A2E]">
                        {signal.trait}
                      </p>
                      <p className="text-xs text-[#6B7280]">
                        {signal.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Breadth Score */}
          {privacy?.shareBreadthScore !== false && profile && (
            <div className="glass-card p-5">
              <div className="flex items-center justify-between mb-2">
                <h2 className="font-semibold text-[#1A1A2E]">
                  Exploration Breadth
                </h2>
                <span className="text-sm font-bold text-[#3B82F6]">
                  {Math.round(profile.breadthScore)}/100
                </span>
              </div>
              <div className="h-2 bg-gray-200/60 rounded-full overflow-hidden">
                <div
                  className="h-full bg-[#3B82F6] rounded-full"
                  style={{ width: `${profile.breadthScore}%` }}
                />
              </div>
              <p className="text-xs text-[#9CA3AF] mt-1">
                Measures interest diversity across domains
              </p>
            </div>
          )}

          {/* Shared Reflections */}
          {student.sessions.some((s) => s.reflections.length > 0) && (
            <div className="glass-card p-5">
              <h2 className="font-semibold text-[#1A1A2E] mb-3">
                Shared Reflections
              </h2>
              <div className="space-y-4">
                {student.sessions.flatMap((session) =>
                  session.reflections.map((r) => (
                    <div
                      key={r.id}
                      className="p-3 bg-white/50 rounded-xl border border-gray-200/40"
                    >
                      <p className="text-xs font-medium text-[#6B7280] mb-1">
                        {session.monthKey} · {r.promptType}
                      </p>
                      <p className="text-xs text-[#1A1A2E] font-medium mb-1">
                        {r.promptText}
                      </p>
                      <p className="text-sm text-[#6B7280]">{r.responseText}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar: Meeting Prep */}
        <div className="col-span-1">
          <MeetingPrepPanel
            studentId={student.id}
            counselorId={counselor.id}
          />
        </div>
      </div>
    </div>
  );
}
