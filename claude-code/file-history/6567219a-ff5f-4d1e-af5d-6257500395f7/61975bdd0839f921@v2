"use client";

import { useState, useEffect, useRef } from "react";
import { Button } from "@compass/ui";

interface Reflection {
  id: string;
  promptText: string;
  responseText: string | null;
  promptType: string;
  isSharedWithCounselor: boolean;
}

interface Session {
  id: string;
  reflections: Reflection[];
  activities: unknown[];
}

interface Prompt {
  promptText: string;
  promptType: string;
}

export default function ReflectionPromptsStep({
  session,
  onNext,
  onBack,
}: {
  session: Session;
  onNext: (reflections: Reflection[]) => void;
  onBack: () => void;
}) {
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [responses, setResponses] = useState<Record<number, string>>({});
  const [savedIds, setSavedIds] = useState<Record<number, string>>({});
  const [loadingPrompts, setLoadingPrompts] = useState(true);
  const [saving, setSaving] = useState(false);
  const autoSaveTimers = useRef<Record<number, NodeJS.Timeout>>({});

  useEffect(() => {
    async function fetchPrompts() {
      try {
        const res = await fetch("/api/sessions/prompts", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ sessionId: session.id }),
        });

        if (res.ok) {
          const data = await res.json() as { prompts: Prompt[] };
          setPrompts(data.prompts);
        }
      } catch {
        // Fallback prompts
        setPrompts([
          {
            promptText:
              "What activity from this month felt most alive or energizing to you?",
            promptType: "PATTERN",
          },
          {
            promptText:
              "What have you been curious about lately that you haven't had time to explore?",
            promptType: "EXPLORATION",
          },
        ]);
      } finally {
        setLoadingPrompts(false);
      }
    }

    fetchPrompts();
  }, [session.id]);

  function handleResponseChange(index: number, value: string) {
    setResponses((prev) => ({ ...prev, [index]: value }));

    // Auto-save with debounce
    if (autoSaveTimers.current[index]) {
      clearTimeout(autoSaveTimers.current[index]);
    }
    autoSaveTimers.current[index] = setTimeout(() => {
      autoSave(index, value);
    }, 3000);
  }

  async function autoSave(index: number, text: string) {
    if (!prompts[index] || !text.trim()) return;

    const prompt = prompts[index]!;

    if (savedIds[index]) {
      // Update existing reflection
      await fetch(`/api/reflections/${savedIds[index]}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ responseText: text }),
      });
    } else {
      // Create new reflection
      const res = await fetch("/api/reflections", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sessionId: session.id,
          promptText: prompt.promptText,
          responseText: text,
          promptType: prompt.promptType,
          isSharedWithCounselor: false,
        }),
      });

      if (res.ok) {
        const reflection = await res.json() as { id: string };
        setSavedIds((prev) => ({ ...prev, [index]: reflection.id }));
      }
    }
  }

  async function handleNext() {
    setSaving(true);
    // Save any unsaved responses
    for (let i = 0; i < prompts.length; i++) {
      const response = responses[i];
      if (response?.trim() && !savedIds[i]) {
        await autoSave(i, response);
      }
    }

    // Fetch updated reflections
    const res = await fetch(`/api/sessions/${session.id}`);
    if (res.ok) {
      const updated = await res.json() as { reflections: Reflection[] };
      onNext(updated.reflections);
    } else {
      onNext([]);
    }
    setSaving(false);
  }

  function wordCount(text: string): number {
    return text.trim().split(/\s+/).filter(Boolean).length;
  }

  if (loadingPrompts) {
    return (
      <div className="glass-card p-8 text-center">
        <div className="text-4xl mb-3 animate-pulse">✨</div>
        <p className="text-[#6B7280] text-sm">
          Generating personalized reflection prompts...
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="glass-card p-5">
        <h2 className="text-xl font-bold text-[#1A1A2E] mb-1">
          Time to reflect
        </h2>
        <p className="text-sm text-[#6B7280] mb-5">
          Answer as much or as little as feels right. No right or wrong.
          Auto-saves as you type.
        </p>

        <div className="space-y-6">
          {prompts.map((prompt, i) => (
            <div key={i} className="space-y-2">
              <div className="flex items-start gap-2">
                <span className="flex-shrink-0 w-6 h-6 bg-[#3B82F6] text-white text-xs rounded-full flex items-center justify-center font-medium">
                  {i + 1}
                </span>
                <p className="text-sm font-medium text-[#1A1A2E]">
                  {prompt.promptText}
                </p>
              </div>
              <div className="relative">
                <textarea
                  value={responses[i] ?? ""}
                  onChange={(e) => handleResponseChange(i, e.target.value)}
                  placeholder="Take your time..."
                  rows={4}
                  className="w-full px-4 py-3 bg-white/60 border border-gray-200/60 rounded-xl text-sm text-[#1A1A2E] placeholder-[#9CA3AF] focus:outline-none focus:ring-2 focus:ring-blue-500/40 resize-none"
                />
                <div className="absolute bottom-2 right-3 text-[10px] text-[#9CA3AF]">
                  {wordCount(responses[i] ?? "")} words
                  {savedIds[i] && (
                    <span className="ml-2 text-emerald-500">✓ saved</span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex gap-3">
        <Button onClick={onBack} variant="ghost" size="lg">
          Back
        </Button>
        <Button
          onClick={handleNext}
          loading={saving}
          variant="primary"
          size="lg"
          fullWidth
        >
          Continue →
        </Button>
      </div>
    </div>
  );
}
