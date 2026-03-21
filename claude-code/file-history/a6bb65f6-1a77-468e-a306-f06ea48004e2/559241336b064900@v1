"use client";

import { useState } from "react";
import { Button } from "@compass/ui";
import { ActivityCategory } from "@compass/db";

interface Activity {
  id: string;
  name: string;
  category: string;
  excitement: number | null;
  hoursPerWeek: number | null;
  isOngoing: boolean;
}

interface Session {
  id: string;
  activities: Activity[];
}

const CATEGORIES = [
  { value: "ACADEMIC", label: "Academic" },
  { value: "EXTRACURRICULAR", label: "Extracurricular" },
  { value: "READING", label: "Reading" },
  { value: "PROJECT", label: "Project" },
  { value: "WORK", label: "Work" },
  { value: "VOLUNTEER", label: "Volunteer" },
  { value: "HOBBY", label: "Hobby" },
] as const;

export default function ActivityLoggerStep({
  session,
  allActivities,
  onNext,
  onBack,
}: {
  session: Session;
  allActivities: Activity[];
  onNext: (activities: Activity[]) => void;
  onBack: () => void;
}) {
  const [activities, setActivities] = useState<Activity[]>(
    session.activities.length > 0 ? session.activities : allActivities
  );
  const [showAddForm, setShowAddForm] = useState(false);
  const [newActivity, setNewActivity] = useState({
    name: "",
    category: "HOBBY" as string,
    excitement: 3,
    hoursPerWeek: "" as string | number,
    isOngoing: true,
  });
  const [saving, setSaving] = useState(false);

  async function addActivity() {
    if (!newActivity.name.trim()) return;

    setSaving(true);
    try {
      const res = await fetch("/api/activities", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sessionId: session.id,
          ...newActivity,
          hoursPerWeek: newActivity.hoursPerWeek
            ? parseFloat(newActivity.hoursPerWeek as string)
            : undefined,
        }),
      });

      if (res.ok) {
        const activity = await res.json() as Activity;
        setActivities((prev) => [...prev, activity]);
        setNewActivity({
          name: "",
          category: "HOBBY",
          excitement: 3,
          hoursPerWeek: "",
          isOngoing: true,
        });
        setShowAddForm(false);
      }
    } finally {
      setSaving(false);
    }
  }

  const excitementEmojis = ["", "😐", "🙂", "😊", "😄", "🤩"];

  return (
    <div className="space-y-4">
      <div className="glass-card p-5">
        <h2 className="text-xl font-bold text-[#1A1A2E] mb-1">
          What have you been doing?
        </h2>
        <p className="text-sm text-[#6B7280] mb-4">
          Add or update your activities. Focus on what&apos;s felt engaging this past month.
        </p>

        {/* Activity List */}
        {activities.length > 0 && (
          <div className="space-y-2 mb-4">
            {activities.map((activity) => (
              <div
                key={activity.id}
                className="flex items-center justify-between p-3 bg-white/50 rounded-xl border border-gray-200/40"
              >
                <div className="flex-1">
                  <span className="text-sm font-medium text-[#1A1A2E]">
                    {activity.name}
                  </span>
                  <span className="text-xs text-[#6B7280] ml-2">
                    {activity.category}
                  </span>
                </div>
                {activity.excitement && (
                  <span className="text-lg">
                    {excitementEmojis[activity.excitement]}
                  </span>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Add Activity Form */}
        {showAddForm ? (
          <div className="space-y-3 p-4 bg-blue-50/50 rounded-xl border border-blue-200/30">
            <input
              type="text"
              placeholder="Activity name"
              value={newActivity.name}
              onChange={(e) =>
                setNewActivity((prev) => ({ ...prev, name: e.target.value }))
              }
              className="w-full px-3 py-2.5 bg-white rounded-lg text-sm border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
            />

            <select
              value={newActivity.category}
              onChange={(e) =>
                setNewActivity((prev) => ({ ...prev, category: e.target.value }))
              }
              className="w-full px-3 py-2.5 bg-white rounded-lg text-sm border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
            >
              {CATEGORIES.map((cat) => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>

            <div className="flex items-center gap-3">
              <label className="text-sm text-[#6B7280] whitespace-nowrap">
                Excitement:
              </label>
              <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((n) => (
                  <button
                    key={n}
                    onClick={() =>
                      setNewActivity((prev) => ({ ...prev, excitement: n }))
                    }
                    className={`text-xl transition-transform ${
                      newActivity.excitement === n ? "scale-125" : "opacity-50"
                    }`}
                  >
                    {excitementEmojis[n]}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex gap-2">
              <Button
                onClick={addActivity}
                loading={saving}
                size="sm"
                variant="primary"
              >
                Add
              </Button>
              <Button
                onClick={() => setShowAddForm(false)}
                size="sm"
                variant="ghost"
              >
                Cancel
              </Button>
            </div>
          </div>
        ) : (
          <button
            onClick={() => setShowAddForm(true)}
            className="w-full py-3 border-2 border-dashed border-gray-300/60 rounded-xl text-sm text-[#6B7280] hover:border-blue-300 hover:text-[#3B82F6] transition-colors"
          >
            + Add Activity
          </button>
        )}
      </div>

      <div className="flex gap-3">
        <Button onClick={onBack} variant="ghost" size="lg">
          Back
        </Button>
        <Button
          onClick={() => onNext(activities)}
          variant="primary"
          size="lg"
          fullWidth
        >
          Continue to Reflection →
        </Button>
      </div>
    </div>
  );
}
