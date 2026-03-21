import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import Link from "next/link";
import SignalSummary from "@/components/SignalSummary";
import BreadthBar from "@/components/BreadthBar";
import SessionCountdown from "@/components/SessionCountdown";
import NotificationPreview from "@/components/NotificationPreview";

export default async function HomePage() {
  const student = await requireStudent();

  const [signalProfile, notifications, sessions] = await Promise.all([
    prisma.signalProfile.findFirst({
      where: { studentId: student.id },
      orderBy: { createdAt: "desc" },
    }),
    prisma.notification.findMany({
      where: { studentId: student.id, readAt: null },
      orderBy: { createdAt: "desc" },
      take: 2,
    }),
    prisma.reflectionSession.findMany({
      where: { studentId: student.id },
      orderBy: { createdAt: "desc" },
      take: 1,
    }),
  ]);

  const lastSession = sessions[0];
  const now = new Date();
  const currentMonthKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;
  const hasCurrentSession = lastSession?.monthKey === currentMonthKey;

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="pt-2">
        <h1 className="text-2xl font-bold text-[#1A1A2E]">
          Hey, {student.firstName} 👋
        </h1>
        <p className="text-[#6B7280] text-sm mt-1">
          {signalProfile
            ? "Here&apos;s what COMPASS sees in you"
            : "Start your first reflection to see your signals"}
        </p>
      </div>

      {/* Session CTA */}
      <div className="glass-card p-5">
        {hasCurrentSession && lastSession?.completedAt ? (
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-[#1A1A2E]">
                This month&apos;s reflection is done ✓
              </p>
              <p className="text-xs text-[#6B7280] mt-0.5">
                Next opens in about 30 days
              </p>
            </div>
            <Link
              href="/reflections"
              className="text-sm text-[#3B82F6] font-medium hover:underline"
            >
              View history
            </Link>
          </div>
        ) : hasCurrentSession ? (
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-[#1A1A2E]">
                Your reflection is in progress
              </p>
              <p className="text-xs text-[#6B7280] mt-0.5">
                Pick up where you left off
              </p>
            </div>
            <Link
              href={`/reflect/${lastSession?.id}`}
              className="btn-primary py-2 px-4 text-sm"
            >
              Continue
            </Link>
          </div>
        ) : (
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-[#1A1A2E]">
                Ready for your monthly reflection?
              </p>
              <p className="text-xs text-[#6B7280] mt-0.5">Takes 10–15 minutes</p>
            </div>
            <Link href="/reflect" className="btn-primary py-2 px-4 text-sm">
              Start
            </Link>
          </div>
        )}
      </div>

      {/* Signal Summary */}
      {signalProfile ? (
        <SignalSummary profile={signalProfile} />
      ) : (
        <div className="glass-card p-8 text-center">
          <div className="text-4xl mb-3">🧭</div>
          <h3 className="font-semibold text-[#1A1A2E] mb-1">
            Your signals will appear here
          </h3>
          <p className="text-sm text-[#6B7280]">
            Complete your first reflection to see patterns in your interests
          </p>
        </div>
      )}

      {/* Breadth Score */}
      {signalProfile && (
        <BreadthBar score={signalProfile.breadthScore} />
      )}

      {/* Countdown */}
      <SessionCountdown lastSession={lastSession ?? null} />

      {/* Notifications */}
      {notifications.length > 0 && (
        <NotificationPreview notifications={notifications} />
      )}

      {/* Map CTA */}
      <Link href="/map" className="block">
        <div className="glass-card p-5 border-blue-200/40 bg-blue-50/60 hover:bg-blue-50/80 transition-colors cursor-pointer">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold text-[#1A1A2E]">
                Explore the Career & Education Map
              </p>
              <p className="text-xs text-[#6B7280] mt-0.5">
                Discover paths aligned with your interests
              </p>
            </div>
            <svg
              className="w-5 h-5 text-[#3B82F6]"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M8.25 4.5l7.5 7.5-7.5 7.5"
              />
            </svg>
          </div>
        </div>
      </Link>
    </div>
  );
}
