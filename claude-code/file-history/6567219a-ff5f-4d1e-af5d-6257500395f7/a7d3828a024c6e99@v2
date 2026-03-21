"use client";

import { useState, useEffect } from "react";

interface MeetingPrepResult {
  summary: string;
  conversationStarters: string[];
  flags: string[];
}

export default function MeetingPrepPanel({
  studentId,
  counselorId: _counselorId,
}: {
  studentId: string;
  counselorId: string;
}) {
  const [prep, setPrep] = useState<MeetingPrepResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [fetched, setFetched] = useState(false);

  async function fetchPrep() {
    setLoading(true);
    try {
      const res = await fetch(
        `/api/counselor/students/${studentId}/meeting-prep`
      );
      if (res.ok) {
        const data = await res.json() as MeetingPrepResult;
        setPrep(data);
      }
    } finally {
      setLoading(false);
      setFetched(true);
    }
  }

  return (
    <div className="glass-card p-5 sticky top-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-semibold text-[#1A1A2E]">Meeting Prep</h2>
        <span className="text-[10px] text-[#9CA3AF] bg-gray-100 px-2 py-0.5 rounded-full">
          AI generated
        </span>
      </div>

      {!fetched && !loading && (
        <div className="text-center py-4">
          <p className="text-xs text-[#6B7280] mb-3">
            Generate a personalized meeting brief based on this student's
            privacy-filtered signals.
          </p>
          <button
            onClick={fetchPrep}
            className="btn-primary text-sm py-2 px-4"
          >
            Generate Brief
          </button>
        </div>
      )}

      {loading && (
        <div className="text-center py-6">
          <div className="text-2xl animate-spin mb-2">✨</div>
          <p className="text-xs text-[#6B7280]">Generating meeting brief...</p>
        </div>
      )}

      {prep && !loading && (
        <div className="space-y-4">
          {/* Summary */}
          <div>
            <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wide mb-2">
              Overview
            </h3>
            <p className="text-sm text-[#1A1A2E] leading-relaxed whitespace-pre-wrap">
              {prep.summary}
            </p>
          </div>

          {/* Conversation Starters */}
          {prep.conversationStarters.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wide mb-2">
                Conversation Starters
              </h3>
              <div className="space-y-2">
                {prep.conversationStarters.map((starter, i) => (
                  <div
                    key={i}
                    className="text-xs text-[#1A1A2E] p-2.5 bg-blue-50/60 rounded-lg border border-blue-100"
                  >
                    "{starter}"
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Flags */}
          {prep.flags.length > 0 && prep.flags[0] !== "" && (
            <div>
              <h3 className="text-xs font-semibold text-amber-600 uppercase tracking-wide mb-2">
                ⚑ Flags
              </h3>
              <div className="space-y-1">
                {prep.flags.map((flag, i) => (
                  <p key={i} className="text-xs text-amber-800 bg-amber-50 p-2 rounded-lg">
                    {flag}
                  </p>
                ))}
              </div>
            </div>
          )}

          <button
            onClick={fetchPrep}
            className="text-xs text-[#9CA3AF] hover:text-[#6B7280] transition-colors"
          >
            Regenerate
          </button>
        </div>
      )}

      <p className="mt-4 text-[10px] text-[#9CA3AF] border-t border-gray-200/40 pt-3">
        Only shows student-consented data. Raw reflections are never included.
      </p>
    </div>
  );
}
