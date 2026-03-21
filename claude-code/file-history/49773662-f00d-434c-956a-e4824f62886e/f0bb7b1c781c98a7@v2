"use client";

const COOLDOWN_DAYS = 21;

interface Session {
  completedAt?: Date | string | null;
}

function getDaysUntilNext(lastSession: Session | null): number {
  if (!lastSession?.completedAt) return 0;

  const completedAt = new Date(lastSession.completedAt);
  const unlockDate = new Date(completedAt);
  unlockDate.setDate(unlockDate.getDate() + COOLDOWN_DAYS);

  const now = new Date();
  return Math.max(0, Math.ceil((unlockDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)));
}

export default function SessionCountdown({
  lastSession,
}: {
  lastSession: Session | null;
}) {
  const daysUntil = getDaysUntilNext(lastSession);

  if (!lastSession || daysUntil === 0) return null;

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
            Reflections open every 3 weeks
          </p>
        </div>
      </div>
    </div>
  );
}
