"use client";

import { useState } from "react";
import { Button } from "@compass/ui";

interface PulseCheckStepProps {
  session: { id: string; pulseScore: number | null; pulseNote: string | null };
  student: { firstName: string };
  onNext: (data: { pulseScore: number; pulseNote: string }) => void;
}

const energyLabels: Record<number, string> = {
  1: "Really drained",
  2: "Low energy",
  3: "A bit tired",
  4: "Okay",
  5: "Neutral",
  6: "Decent",
  7: "Pretty good",
  8: "Good energy",
  9: "High energy",
  10: "Thriving",
};

export default function PulseCheckStep({
  session,
  student,
  onNext,
}: PulseCheckStepProps) {
  const [pulseScore, setPulseScore] = useState(session.pulseScore ?? 5);
  const [pulseNote, setPulseNote] = useState(session.pulseNote ?? "");
  const [saving, setSaving] = useState(false);

  async function handleNext() {
    setSaving(true);
    try {
      await fetch(`/api/sessions/${session.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pulseScore, pulseNote: pulseNote || undefined }),
      });
      onNext({ pulseScore, pulseNote });
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="glass-card p-6">
        <h2 className="text-xl font-bold text-[#1A1A2E] mb-1">
          Hey {student.firstName}, how&apos;s your energy?
        </h2>
        <p className="text-sm text-[#6B7280] mb-6">
          This isn&apos;t a mood tracker — just context for your reflection.
          No right or wrong answer.
        </p>

        {/* Energy Slider */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-[#6B7280]">Low energy</span>
            <span className="text-3xl font-bold text-[#1A1A2E]">
              {pulseScore}
            </span>
            <span className="text-sm text-[#6B7280]">High energy</span>
          </div>

          <input
            type="range"
            min={1}
            max={10}
            value={pulseScore}
            onChange={(e) => setPulseScore(parseInt(e.target.value))}
            className="w-full h-3 accent-[#3B82F6] cursor-pointer"
          />

          <div className="text-center">
            <span className="inline-block px-4 py-1.5 bg-blue-50 text-[#3B82F6] text-sm font-medium rounded-full">
              {energyLabels[pulseScore] ?? ""}
            </span>
          </div>
        </div>

        {/* Optional note */}
        <div className="mt-6">
          <label className="text-sm text-[#6B7280] mb-2 block">
            What&apos;s been on your mind lately? (optional)
          </label>
          <textarea
            value={pulseNote}
            onChange={(e) => setPulseNote(e.target.value)}
            placeholder="Anything you want to set context with — no need to elaborate..."
            rows={3}
            className="w-full px-4 py-3 bg-white/60 border border-gray-200/60 rounded-xl text-sm text-[#1A1A2E] placeholder-[#9CA3AF] focus:outline-none focus:ring-2 focus:ring-blue-500/40 resize-none"
          />
        </div>
      </div>

      <Button onClick={handleNext} loading={saving} fullWidth size="lg">
        Continue to Activities →
      </Button>
    </div>
  );
}
