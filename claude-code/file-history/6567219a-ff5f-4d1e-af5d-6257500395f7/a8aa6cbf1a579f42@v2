import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import { UserButton } from "@clerk/nextjs";
import { SignalBadge } from "@compass/ui";
import PrivacySettingsPanel from "@/components/PrivacySettingsPanel";

interface InterestCluster {
  id: string;
  label: string;
  strength: "strong" | "moderate" | "emerging";
  evidenceCount: number;
}

interface CharacterSignal {
  trait: string;
  description: string;
  confidence: "high" | "medium" | "low";
}

export default async function ProfilePage() {
  const student = await requireStudent();

  const [signalProfile, privacySettings, sessionsCount] = await Promise.all([
    prisma.signalProfile.findFirst({
      where: { studentId: student.id },
      orderBy: { createdAt: "desc" },
    }),
    prisma.studentPrivacySettings.findUnique({
      where: { studentId: student.id },
    }),
    prisma.reflectionSession.count({
      where: { studentId: student.id, completedAt: { not: null } },
    }),
  ]);

  const clusters = (signalProfile?.interestClusters as InterestCluster[]) ?? [];
  const characterSignals =
    (signalProfile?.characterSignals as CharacterSignal[]) ?? [];

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="pt-2 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-[#1A1A2E]">
            {student.firstName} {student.lastName}
          </h1>
          <p className="text-sm text-[#6B7280]">
            Grade {student.gradeLevel ?? "?"} · {sessionsCount} reflection
            {sessionsCount !== 1 ? "s" : ""}
          </p>
        </div>
        <UserButton afterSignOutUrl="/sign-in" />
      </div>

      {/* Signal Profile */}
      {signalProfile ? (
        <>
          {/* Compressed Summary */}
          {signalProfile.compressedSummary && (
            <div className="glass-card p-5">
              <h2 className="font-semibold text-[#1A1A2E] mb-3">
                Your Signal Profile
              </h2>
              <p className="text-sm text-[#6B7280] leading-relaxed">
                {signalProfile.compressedSummary}
              </p>
            </div>
          )}

          {/* Interest Clusters */}
          {clusters.length > 0 && (
            <div className="glass-card p-5">
              <h2 className="font-semibold text-[#1A1A2E] mb-3">
                Interest Clusters
              </h2>
              <div className="flex flex-wrap gap-2">
                {clusters.map((cluster) => (
                  <SignalBadge
                    key={cluster.id}
                    label={cluster.label}
                    strength={cluster.strength}
                  />
                ))}
              </div>
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
                      className={`mt-0.5 w-2 h-2 rounded-full flex-shrink-0 ${
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
                      <p className="text-xs text-[#6B7280] mt-0.5">
                        {signal.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Breadth Score */}
          <div className="glass-card p-5">
            <div className="flex items-center justify-between mb-2">
              <h2 className="font-semibold text-[#1A1A2E]">
                Exploration Breadth
              </h2>
              <span className="text-sm font-bold text-[#3B82F6]">
                {Math.round(signalProfile.breadthScore)}/100
              </span>
            </div>
            <div className="h-2 bg-gray-200/60 rounded-full overflow-hidden">
              <div
                className="h-full bg-[#3B82F6] rounded-full transition-all duration-500"
                style={{ width: `${signalProfile.breadthScore}%` }}
              />
            </div>
          </div>
        </>
      ) : (
        <div className="glass-card p-8 text-center">
          <div className="text-4xl mb-3">🔭</div>
          <h3 className="font-semibold text-[#1A1A2E] mb-1">
            Your profile is building
          </h3>
          <p className="text-sm text-[#6B7280]">
            Complete your first reflection to see your signal profile here.
          </p>
        </div>
      )}

      {/* Privacy Settings */}
      <PrivacySettingsPanel settings={privacySettings} />

      {/* Data Export */}
      <div className="glass-card p-5">
        <h2 className="font-semibold text-[#1A1A2E] mb-2">Your Data</h2>
        <div className="flex gap-3">
          <a
            href="/api/export"
            download
            className="text-sm text-[#3B82F6] font-medium hover:underline"
          >
            Export all data
          </a>
          <span className="text-[#9CA3AF]">·</span>
          <span className="text-sm text-[#9CA3AF]">
            GDPR deletion available on request
          </span>
        </div>
      </div>
    </div>
  );
}
