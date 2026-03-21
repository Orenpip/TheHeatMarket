"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@compass/ui";
import { fadeUpVariant, staggerContainer } from "@compass/ui";

// Step components
import PulseCheckStep from "./steps/PulseCheckStep";
import ActivityLoggerStep from "./steps/ActivityLoggerStep";
import ReflectionPromptsStep from "./steps/ReflectionPromptsStep";
import MapMomentStep from "./steps/MapMomentStep";
import PrivacyReviewStep from "./steps/PrivacyReviewStep";

interface Session {
  id: string;
  monthKey?: string | null;
  sessionNumber?: number | null;
  template?: { title: string; orderNum: number } | null;
  pulseScore: number | null;
  pulseNote: string | null;
  activities: Activity[];
  reflections: Reflection[];
}

interface Activity {
  id: string;
  name: string;
  category: string;
  excitement: number | null;
  hoursPerWeek: number | null;
  isOngoing: boolean;
}

interface Reflection {
  id: string;
  promptText: string;
  responseText: string | null;
  promptType: string;
  isSharedWithCounselor: boolean;
}

interface Student {
  id: string;
  firstName: string;
}

const STEP_LABELS = [
  "Pulse Check",
  "Activities",
  "Reflection",
  "Map Moment",
  "Privacy",
];

export default function SessionWizard({
  session,
  student,
  allActivities,
}: {
  session: Session;
  student: Student;
  allActivities: Activity[];
}) {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [localSession, setLocalSession] = useState(session);

  const sessionTitle = session.template?.title
    ? `Reflection ${session.template.orderNum}: ${session.template.title}`
    : session.monthKey
    ? new Date(
        parseInt(session.monthKey.split("-")[0]!),
        parseInt(session.monthKey.split("-")[1]!) - 1
      ).toLocaleString("default", { month: "long", year: "numeric" }) + " Reflection"
    : `Reflection ${session.sessionNumber ?? ""}`;

  const handleSubmit = useCallback(async () => {
    setSubmitting(true);
    setSubmitError(null);
    try {
      const res = await fetch(`/api/sessions/${session.id}/submit`, {
        method: "POST",
      });
      if (res.ok) {
        router.push(`/reflect/${session.id}/complete`);
      } else {
        const data = await res.json().catch(() => null) as { error?: string } | null;
        setSubmitError(data?.error ?? "Something went wrong. Please try again.");
      }
    } catch {
      setSubmitError("Network error. Please check your connection and try again.");
    } finally {
      setSubmitting(false);
    }
  }, [session.id, router]);

  return (
    <div className="min-h-screen">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-lg font-bold text-[#1A1A2E]">
            {sessionTitle}
          </h1>
          <p className="text-xs text-[#6B7280]">Step {step} of 5</p>
        </div>
        <div className="flex items-center gap-1">
          {STEP_LABELS.map((_, i) => (
            <div
              key={i}
              className={`h-1.5 rounded-full transition-all duration-300 ${
                i + 1 < step
                  ? "bg-[#10B981] w-6"
                  : i + 1 === step
                  ? "bg-[#3B82F6] w-8"
                  : "bg-gray-200 w-4"
              }`}
            />
          ))}
        </div>
      </div>

      {/* Step Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={step}
          variants={fadeUpVariant}
          initial="hidden"
          animate="visible"
          exit={{ opacity: 0, y: -10 }}
        >
          {step === 1 && (
            <PulseCheckStep
              session={localSession}
              student={student}
              onNext={(data) => {
                setLocalSession((prev) => ({ ...prev, ...data }));
                setStep(2);
              }}
            />
          )}
          {step === 2 && (
            <ActivityLoggerStep
              session={localSession}
              allActivities={allActivities}
              onNext={(activities) => {
                setLocalSession((prev) => ({ ...prev, activities }));
                setStep(3);
              }}
              onBack={() => setStep(1)}
            />
          )}
          {step === 3 && (
            <ReflectionPromptsStep
              session={localSession}
              onNext={(reflections) => {
                setLocalSession((prev) => ({ ...prev, reflections }));
                setStep(4);
              }}
              onBack={() => setStep(2)}
            />
          )}
          {step === 4 && (
            <MapMomentStep
              session={localSession}
              onNext={() => setStep(5)}
              onBack={() => setStep(3)}
            />
          )}
          {step === 5 && (
            <PrivacyReviewStep
              session={localSession}
              onSubmit={handleSubmit}
              onBack={() => setStep(4)}
              submitting={submitting}
              error={submitError}
            />
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
