"use client";

import { useState } from "react";
import { Button, PrivacyToggle } from "@compass/ui";

interface Reflection {
  id: string;
  promptText: string;
  responseText: string | null;
  isSharedWithCounselor: boolean;
}

interface Session {
  id: string;
  reflections: Reflection[];
}

export default function PrivacyReviewStep({
  session,
  onSubmit,
  onBack,
  submitting,
}: {
  session: Session;
  onSubmit: () => void;
  onBack: () => void;
  submitting: boolean;
}) {
  const [shareSignals, setShareSignals] = useState(true);
  const [sharedReflections, setSharedReflections] = useState<
    Record<string, boolean>
  >({});

  function toggleReflection(id: string, shared: boolean) {
    setSharedReflections((prev) => ({ ...prev, [id]: shared }));

    // Update in DB
    fetch(`/api/reflections/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ isSharedWithCounselor: shared }),
    }).catch(console.error);
  }

  return (
    <div className="space-y-4">
      <div className="glass-card p-5">
        <h2 className="text-xl font-bold text-[#1A1A2E] mb-1">
          Privacy Review
        </h2>
        <p className="text-sm text-[#6B7280] mb-5">
          Choose what your counselor can see. Your reflections are always
          private by default — you decide what to share.
        </p>

        {/* Signal Data Sharing */}
        <div className="space-y-3 mb-5">
          <h3 className="text-sm font-semibold text-[#1A1A2E]">
            Signal Data
          </h3>
          <PrivacyToggle
            enabled={shareSignals}
            onChange={setShareSignals}
            label="Share interest signals with counselor"
            description="Includes interest clusters, breadth score, and trajectory patterns"
          />
        </div>

        {/* Reflection Sharing */}
        {session.reflections.filter((r) => r.responseText).length > 0 && (
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-[#1A1A2E]">
              Reflections (default private)
            </h3>
            {session.reflections
              .filter((r) => r.responseText)
              .map((reflection) => (
                <div
                  key={reflection.id}
                  className="p-3 bg-white/50 rounded-xl border border-gray-200/40"
                >
                  <PrivacyToggle
                    enabled={
                      sharedReflections[reflection.id] ??
                      reflection.isSharedWithCounselor
                    }
                    onChange={(shared) =>
                      toggleReflection(reflection.id, shared)
                    }
                    label={reflection.promptText.slice(0, 60) + "..."}
                    description="Share this specific response with your counselor"
                  />
                </div>
              ))}
          </div>
        )}

        {/* Preview of what counselor sees */}
        <div className="mt-5 p-4 bg-gray-50/60 rounded-xl border border-gray-200/40">
          <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wide mb-2">
            What your counselor will see:
          </h3>
          <ul className="space-y-1">
            {shareSignals ? (
              <>
                <li className="text-xs text-[#1A1A2E] flex items-center gap-1.5">
                  <span className="text-emerald-500">✓</span>
                  Interest clusters and patterns
                </li>
                <li className="text-xs text-[#1A1A2E] flex items-center gap-1.5">
                  <span className="text-emerald-500">✓</span>
                  Exploration breadth score
                </li>
              </>
            ) : (
              <li className="text-xs text-[#6B7280] flex items-center gap-1.5">
                <span>—</span>
                Signal data is private
              </li>
            )}
            {Object.values(sharedReflections).some((v) => v) ? (
              <li className="text-xs text-[#1A1A2E] flex items-center gap-1.5">
                <span className="text-emerald-500">✓</span>
                {Object.values(sharedReflections).filter((v) => v).length} reflection
                {Object.values(sharedReflections).filter((v) => v).length !== 1
                  ? "s"
                  : ""}
              </li>
            ) : (
              <li className="text-xs text-[#6B7280] flex items-center gap-1.5">
                <span>—</span>
                No reflections shared
              </li>
            )}
          </ul>
        </div>
      </div>

      <div className="flex gap-3">
        <Button onClick={onBack} variant="ghost" size="lg">
          Back
        </Button>
        <Button
          onClick={onSubmit}
          loading={submitting}
          variant="primary"
          size="lg"
          fullWidth
        >
          Submit Reflection ✓
        </Button>
      </div>
    </div>
  );
}
