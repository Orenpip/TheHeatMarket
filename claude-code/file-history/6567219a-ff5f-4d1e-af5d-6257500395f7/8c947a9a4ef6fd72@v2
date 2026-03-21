"use client";

import { SignalBadge } from "@compass/ui";

interface SignalProfile {
  interestClusters: unknown;
  characterSignals: unknown;
  trajectoryShifts: unknown;
  breadthScore: number;
  lastSynthesizedAt: Date | null;
}

interface InterestCluster {
  id: string;
  label: string;
  strength: "strong" | "moderate" | "emerging";
  trend: "rising" | "stable" | "declining";
  evidenceCount: number;
}

export default function SignalSummary({ profile }: { profile: SignalProfile }) {
  const clusters = (profile.interestClusters as InterestCluster[]) ?? [];
  const topClusters = clusters.slice(0, 5);

  return (
    <div className="glass-card p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-semibold text-[#1A1A2E]">Your Interest Signals</h2>
        {profile.lastSynthesizedAt && (
          <span className="text-xs text-[#9CA3AF]">
            Updated{" "}
            {new Date(profile.lastSynthesizedAt).toLocaleDateString("en-US", {
              month: "short",
              day: "numeric",
            })}
          </span>
        )}
      </div>

      {topClusters.length > 0 ? (
        <div className="space-y-3">
          {topClusters.map((cluster) => (
            <div key={cluster.id} className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <SignalBadge
                  label={cluster.label}
                  strength={cluster.strength}
                />
                {cluster.trend === "rising" && (
                  <span className="text-[10px] text-emerald-600 font-medium">
                    ↑ rising
                  </span>
                )}
                {cluster.trend === "declining" && (
                  <span className="text-[10px] text-amber-600 font-medium">
                    ↓ shifting
                  </span>
                )}
              </div>
              <span className="text-xs text-[#9CA3AF]">
                {cluster.evidenceCount} signal{cluster.evidenceCount !== 1 ? "s" : ""}
              </span>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm text-[#6B7280]">
          No interest clusters detected yet. Complete more reflections to see patterns.
        </p>
      )}
    </div>
  );
}
