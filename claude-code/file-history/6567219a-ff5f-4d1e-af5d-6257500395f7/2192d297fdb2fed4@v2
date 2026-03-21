"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Button } from "@compass/ui";
import { fadeUpVariant } from "@compass/ui";

const CATEGORIES = [
  { value: "ACADEMIC", label: "Academics", emoji: "📚" },
  { value: "EXTRACURRICULAR", label: "Extracurriculars", emoji: "🏃" },
  { value: "READING", label: "Reading", emoji: "📖" },
  { value: "PROJECT", label: "Personal Projects", emoji: "🛠️" },
  { value: "WORK", label: "Work / Internship", emoji: "💼" },
  { value: "VOLUNTEER", label: "Volunteering", emoji: "🤝" },
  { value: "HOBBY", label: "Hobbies", emoji: "🎨" },
];

export default function OnboardingPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [gradeLevel, setGradeLevel] = useState(10);
  const [activities, setActivities] = useState<
    Array<{ name: string; category: string; excitement: number }>
  >([]);
  const [newName, setNewName] = useState("");
  const [newCategory, setNewCategory] = useState("HOBBY");
  const [newExcitement, setNewExcitement] = useState(3);
  const [submitting, setSubmitting] = useState(false);

  function addActivity() {
    if (!newName.trim()) return;
    setActivities((prev) => [
      ...prev,
      { name: newName, category: newCategory, excitement: newExcitement },
    ]);
    setNewName("");
    setNewExcitement(3);
  }

  async function handleSubmit() {
    setSubmitting(true);
    try {
      const res = await fetch("/api/students/onboarding", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          gradeLevel,
          initialActivities: activities,
        }),
      });

      if (res.ok) {
        router.push("/");
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#F2F4F7] flex items-center justify-center p-4">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-20%] right-[-10%] w-[600px] h-[600px] rounded-full bg-blue-200/30 blur-[80px]" />
        <div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-violet-200/20 blur-[80px]" />
      </div>

      <div className="relative z-10 w-full max-w-md">
        {/* Progress */}
        <div className="flex items-center justify-center gap-2 mb-8">
          {[1, 2, 3].map((n) => (
            <div
              key={n}
              className={`h-1.5 rounded-full transition-all duration-300 ${
                n <= step ? "bg-[#3B82F6] w-12" : "bg-gray-200 w-8"
              }`}
            />
          ))}
        </div>

        {step === 1 && (
          <motion.div variants={fadeUpVariant} initial="hidden" animate="visible">
            <div className="glass-card p-8">
              <div className="text-5xl mb-4 text-center">🧭</div>
              <h1 className="text-2xl font-bold text-[#1A1A2E] text-center mb-2">
                Welcome to COMPASS
              </h1>
              <p className="text-[#6B7280] text-sm text-center mb-8">
                I&apos;m here to help you see patterns in your interests and
                explore what&apos;s possible — not tell you what to do.
              </p>

              <div className="mb-6">
                <label className="text-sm font-medium text-[#1A1A2E] block mb-3">
                  What grade are you in?
                </label>
                <div className="grid grid-cols-4 gap-2">
                  {[9, 10, 11, 12].map((grade) => (
                    <button
                      key={grade}
                      onClick={() => setGradeLevel(grade)}
                      className={`py-3 rounded-xl text-sm font-semibold transition-all ${
                        gradeLevel === grade
                          ? "bg-[#3B82F6] text-white shadow-md"
                          : "bg-white/60 text-[#6B7280] border border-gray-200 hover:border-blue-300"
                      }`}
                    >
                      {grade}th
                    </button>
                  ))}
                </div>
              </div>

              <Button onClick={() => setStep(2)} fullWidth size="lg">
                Next →
              </Button>
            </div>
          </motion.div>
        )}

        {step === 2 && (
          <motion.div variants={fadeUpVariant} initial="hidden" animate="visible">
            <div className="glass-card p-8">
              <h2 className="text-xl font-bold text-[#1A1A2E] mb-1">
                What are you into?
              </h2>
              <p className="text-[#6B7280] text-sm mb-5">
                Add 2-5 things you&apos;ve been doing lately — school, hobbies,
                projects, anything. Be honest, not impressive.
              </p>

              {/* Added activities */}
              {activities.length > 0 && (
                <div className="space-y-2 mb-4">
                  {activities.map((a, i) => (
                    <div
                      key={i}
                      className="flex items-center justify-between p-2.5 bg-white/50 rounded-lg border border-gray-200/40"
                    >
                      <span className="text-sm text-[#1A1A2E]">{a.name}</span>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-[#9CA3AF]">
                          {a.category}
                        </span>
                        <button
                          onClick={() =>
                            setActivities((prev) =>
                              prev.filter((_, idx) => idx !== i)
                            )
                          }
                          className="text-[#9CA3AF] hover:text-red-500 text-xs"
                        >
                          ✕
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Add form */}
              <div className="space-y-2 mb-4">
                <input
                  type="text"
                  placeholder="Activity name (e.g., Robotics club)"
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                  className="w-full px-3 py-2.5 bg-white/60 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40"
                />
                <select
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value)}
                  className="w-full px-3 py-2.5 bg-white/60 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40"
                >
                  {CATEGORIES.map((c) => (
                    <option key={c.value} value={c.value}>
                      {c.emoji} {c.label}
                    </option>
                  ))}
                </select>
                <button
                  onClick={addActivity}
                  disabled={!newName.trim()}
                  className="w-full py-2 border-2 border-dashed border-gray-300 rounded-xl text-sm text-[#6B7280] hover:border-blue-300 hover:text-[#3B82F6] transition-colors disabled:opacity-40"
                >
                  + Add
                </button>
              </div>

              <div className="flex gap-3">
                <Button onClick={() => setStep(1)} variant="ghost" size="md">
                  Back
                </Button>
                <Button
                  onClick={() => setStep(3)}
                  variant="primary"
                  size="md"
                  fullWidth
                  disabled={activities.length === 0}
                >
                  Next →
                </Button>
              </div>
            </div>
          </motion.div>
        )}

        {step === 3 && (
          <motion.div variants={fadeUpVariant} initial="hidden" animate="visible">
            <div className="glass-card p-8 text-center">
              <div className="text-5xl mb-4">🎯</div>
              <h2 className="text-xl font-bold text-[#1A1A2E] mb-2">
                You&apos;re all set!
              </h2>
              <p className="text-[#6B7280] text-sm mb-4">
                COMPASS will learn about your interests as you complete monthly
                reflections. No judgment, no pressure.
              </p>

              <div className="text-left bg-blue-50/60 rounded-xl p-4 mb-6 space-y-2">
                <p className="text-sm font-medium text-[#1A1A2E]">
                  Here&apos;s how it works:
                </p>
                <p className="text-xs text-[#6B7280]">
                  📓 Monthly 10-min reflections on your activities
                </p>
                <p className="text-xs text-[#6B7280]">
                  🧭 AI builds a signal profile from your patterns
                </p>
                <p className="text-xs text-[#6B7280]">
                  🗺️ Explore careers and paths that match your interests
                </p>
                <p className="text-xs text-[#6B7280]">
                  🔒 You control exactly what your counselor sees
                </p>
              </div>

              <div className="flex gap-3">
                <Button onClick={() => setStep(2)} variant="ghost" size="md">
                  Back
                </Button>
                <Button
                  onClick={handleSubmit}
                  loading={submitting}
                  variant="primary"
                  size="md"
                  fullWidth
                >
                  Start Exploring →
                </Button>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
