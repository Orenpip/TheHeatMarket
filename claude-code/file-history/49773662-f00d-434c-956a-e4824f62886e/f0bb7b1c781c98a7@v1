"use client";

interface Session {
  completedAt?: Date | null;
  monthKey: string;
}

function getDaysUntilNext(lastSession: Session | null): number {
  if (!lastSession?.completedAt) return 0;

  const completedAt = new Date(lastSession.completedAt);
  const nextMonth = new Date(completedAt);
  nextMonth.setMonth(nextMonth.getMonth() + 1);
  nextMonth.setDate(1);

  const now = new Date();
  const diff = nextMonth.getTime() - now.getTime();
  return Math.max(0, Math.ceil(diff / (1000 * 60 * 60 * 24)));
}

export default function SessionCountdown({
  lastSession,
}: {
  lastSession: Session | null;
}) {
  const daysUntil = getDaysUntilNext(lastSession);

  if (!lastSession) return null;
  if (daysUntil === 0) return null;

  return (
    <div className="glass-card p-4">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-[#3B82F6] text-lg font-bold">
          {daysUntil}
        </div>
        <div>
          <p className="text-sm font-medium text-[#1A1A2E]">
            Days until next reflection
          </p>
          <p className="text-xs text-[#6B7280]">
            Monthly reflections keep your signals fresh
          </p>
        </div>
      </div>
    </div>
  );
}
