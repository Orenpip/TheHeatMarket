"use client";

import { useState } from "react";
import { PrivacyToggle } from "@compass/ui";

interface PrivacySettings {
  studentId: string;
  shareInterestClusters: boolean;
  shareBreadthScore: boolean;
  shareTrajectoryShifts: boolean;
  shareCharacterSignals: boolean;
}

export default function PrivacySettingsPanel({
  settings,
}: {
  settings: PrivacySettings | null;
}) {
  const [prefs, setPrefs] = useState({
    shareInterestClusters: settings?.shareInterestClusters ?? true,
    shareBreadthScore: settings?.shareBreadthScore ?? true,
    shareTrajectoryShifts: settings?.shareTrajectoryShifts ?? true,
    shareCharacterSignals: settings?.shareCharacterSignals ?? true,
  });
  const [saving, setSaving] = useState(false);

  async function handleToggle(
    key: keyof typeof prefs,
    value: boolean
  ) {
    const updated = { ...prefs, [key]: value };
    setPrefs(updated);
    setSaving(true);

    try {
      await fetch("/api/privacy", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ [key]: value }),
      });
    } finally {
      setSaving(false);
    }
  }

  async function makeAllPrivate() {
    await fetch("/api/privacy/reset", { method: "POST" });
    setPrefs({
      shareInterestClusters: false,
      shareBreadthScore: false,
      shareTrajectoryShifts: false,
      shareCharacterSignals: false,
    });
  }

  return (
    <div className="glass-card p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-semibold text-[#1A1A2E]">
          Counselor Sharing
        </h2>
        {saving && (
          <span className="text-xs text-[#9CA3AF]">Saving...</span>
        )}
      </div>

      <div className="space-y-4">
        <PrivacyToggle
          enabled={prefs.shareInterestClusters}
          onChange={(v) => handleToggle("shareInterestClusters", v)}
          label="Interest Clusters"
          description="Your identified areas of interest and passion"
        />
        <PrivacyToggle
          enabled={prefs.shareBreadthScore}
          onChange={(v) => handleToggle("shareBreadthScore", v)}
          label="Exploration Breadth Score"
          description="How broadly you&apos;ve been exploring different fields"
        />
        <PrivacyToggle
          enabled={prefs.shareTrajectoryShifts}
          onChange={(v) => handleToggle("shareTrajectoryShifts", v)}
          label="Interest Shifts"
          description="Changes in your interests over time"
        />
        <PrivacyToggle
          enabled={prefs.shareCharacterSignals}
          onChange={(v) => handleToggle("shareCharacterSignals", v)}
          label="Character Signals"
          description="Patterns in how you approach challenges and work"
        />
      </div>

      <button
        onClick={makeAllPrivate}
        className="mt-4 text-xs text-red-500 hover:underline"
      >
        Make everything private
      </button>

      <p className="mt-3 text-[10px] text-[#9CA3AF]">
        Individual reflections are always private unless you explicitly share them.
      </p>
    </div>
  );
}
