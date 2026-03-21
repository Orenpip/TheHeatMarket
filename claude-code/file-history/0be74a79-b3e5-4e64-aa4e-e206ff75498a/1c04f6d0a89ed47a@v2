"use client";

import { useState, useEffect } from "react";
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
  error,
}: {
  session: Session;
  onSubmit: () => void;
  onBack: () => void;
  submitting: boolean;
  error?: string | null;
}) {
  const [shareSignals, setShareSignals] = useState(true);
  const [shareSummary, setShareSummary] = useState(true);
  const [shareFullText, setShareFullText] = useState(false);

  // Load current settings so the UI reflects what's already saved
  useEffect(() => {
    fetch("/api/privacy")
      .then((r) => r.json())
      .then((s: { shareSignals?: boolean; shareSummary?: boolean }) => {
        if (typeof s.shareSignals === "boolean") setShareSignals(s.shareSignals);
        if (typeof s.shareSummary === "boolean") setShareSummary(s.shareSummary);
      })
      .catch(() => {});
  }, []);

  function persistPrivacy(patch: { shareSignals?: boolean; shareSummary?: boolean }) {
    fetch("/api/privacy", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(patch),
    }).catch(console.error);
  }
  const [sharedReflections, setSharedReflections] = useState<
    Record<string, boolean>
  >({});

  const answeredReflections = session.reflections.filter((r) => r.responseText);

  function toggleReflection(id: string, shared: boolean) {
    setSharedReflections((prev) => ({ ...prev, [id]: shared }));

    fetch(`/api/reflections/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ isSharedWithCounselor: shared }),
    }).catch(console.error);
  }

  function handleFullTextToggle(enabled: boolean) {
    setShareFullText(enabled);
    if (!enabled) {
      for (const r of answeredReflections) {
        if (sharedReflections[r.id] ?? r.isSharedWithCounselor) {
          toggleReflection(r.id, false);
        }
      }
      setSharedReflections({});
    }
  }

  const sharedCount = Object.values(sharedReflections).filter((v) => v).length;

  return (
    <div className="space-y-4">
      <div className="glass-card p-5">
        <h2 className="text-xl font-bold text-[#1A1A2E] mb-1">
          Privacy Review
        </h2>
        <p className="text-sm text-[#6B7280] mb-5">
          Choose what your counselor can see. Everything is private by
          default &mdash; you decide what to share.
        </p>

        {/* Signal Data Sharing */}
        <div className="space-y-3 mb-5">
          <h3 className="text-sm font-semibold text-[#1A1A2E]">
            Signal Data
          </h3>
          <PrivacyToggle
            enabled={shareSignals}
            onChange={(val) => {
              setShareSignals(val);
              persistPrivacy({ shareSignals: val });
            }}
            label="Share interest signals with counselor"
            description="AI-generated interest clusters, breadth score, and trajectory patterns"
          />
        </div>

        {/* Summary sharing (default on) */}
        <div className="space-y-3 mb-5">
          <h3 className="text-sm font-semibold text-[#1A1A2E]">
            Reflection Summary
          </h3>
          <PrivacyToggle
            enabled={shareSummary}
            onChange={(val) => {
              setShareSummary(val);
              persistPrivacy({ shareSummary: val });
            }}
            label="Share AI-generated summary"
            description="A brief overview of themes from your reflections &mdash; not the full text"
          />
        </div>

        {/* Full reflection text (opt-in) */}
        {answeredReflections.length > 0 && (
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-[#1A1A2E]">
              Full Reflection Text (optional)
            </h3>
            <PrivacyToggle
              enabled={shareFullText}
              onChange={handleFullTextToggle}
              label="Let me choose specific reflections to share"
              description="Share your exact responses &mdash; off by default"
            />

            {shareFullText && (
              <div className="space-y-2 mt-2 pl-1">
                {answeredReflections.map((reflection) => (
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
                      label={
                        reflection.promptText.length > 55
                          ? reflection.promptText.slice(0, 55) + "..."
                          : reflection.promptText
                      }
                      description="Share this response with your counselor"
                    />
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Preview */}
        <div className="mt-5 p-4 bg-gray-50/60 rounded-xl border border-gray-200/40">
          <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wide mb-2">
            What your counselor will see:
          </h3>
          <ul className="space-y-1">
            {shareSignals ? (
              <li className="text-xs text-[#1A1A2E] flex items-center gap-1.5">
                <span className="text-emerald-500">&#10003;</span>
                Interest clusters, breadth score, trajectory
              </li>
            ) : (
              <li className="text-xs text-[#6B7280] flex items-center gap-1.5">
                <span>&mdash;</span>
                Signal data is private
              </li>
            )}
            {shareSummary ? (
              <li className="text-xs text-[#1A1A2E] flex items-center gap-1.5">
                <span className="text-emerald-500">&#10003;</span>
                AI-generated reflection summary
              </li>
            ) : (
              <li className="text-xs text-[#6B7280] flex items-center gap-1.5">
                <span>&mdash;</span>
                Reflection summary is private
              </li>
            )}
            {shareFullText && sharedCount > 0 ? (
              <li className="text-xs text-[#1A1A2E] flex items-center gap-1.5">
                <span className="text-emerald-500">&#10003;</span>
                {sharedCount} full reflection
                {sharedCount !== 1 ? "s" : ""}
              </li>
            ) : (
              <li className="text-xs text-[#6B7280] flex items-center gap-1.5">
                <span>&mdash;</span>
                Full reflection text is private
              </li>
            )}
          </ul>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-xl">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

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
          Submit Reflection
        </Button>
      </div>
    </div>
  );
}
