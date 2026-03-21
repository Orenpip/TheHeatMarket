import { requireStudent } from "@/lib/auth";
import { prisma } from "@compass/db";
import Link from "next/link";
import SignalSummary from "@/components/SignalSummary";
import BreadthBar from "@/components/BreadthBar";
import SessionCountdown from "@/components/SessionCountdown";
import NotificationPreview from "@/components/NotificationPreview";
import { COOLDOWN_DAYS } from "@/lib/constants";

export default async function HomePage() {
  const student = await requireStudent();
  const now = new Date();

  const [signalProfile, notifications, lastSession] = await Promise.all([
    prisma.signalProfile.findFirst({
      where: { studentId: student.id },
      orderBy: { createdAt: "desc" },
    }),
    prisma.notification.findMany({
      where: { studentId: student.id, readAt: null },
      orderBy: { createdAt: "desc" },
      take: 2,
    }),
    prisma.reflectionSession.findFirst({
      where: { studentId: student.id },
      orderBy: { createdAt: "desc" },
      include: { template: { select: { title: true, orderNum: true } } },
    }),
  ]);

  // Determine session CTA state
  const inProgress = !lastSession?.completedAt ? lastSession : null;

  let daysLeft = 0;
  if (lastSession?.completedAt) {
    const unlockDate = new Date(lastSession.completedAt);
    unlockDate.setDate(unlockDate.getDate() + COOLDOWN_DAYS);
    daysLeft = Math.max(0, Math.ceil((unlockDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)));
  }

  // Count completed sessions and total available templates
  const currentYear = String(now.getFullYear());
  const [completedCount, totalTemplates] = await Promise.all([
    prisma.reflectionSession.count({
      where: { studentId: student.id, completedAt: { not: null } },
    }),
    prisma.reflectionTemplate.count({
      where: { yearKey: currentYear, isActive: true },
    }),
  ]);

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="pt-2">
        <h1 className="text-2xl font-bold text-[#1A1A2E]">
          Hey, {student.firstName} 👋
        </h1>
        <p className="text-[#6B7280] text-sm mt-1">
          {signalProfile
            ? "Here's what COMPASS sees in you"
            : "Start your first reflection to see your signals"}
        </p>
      </div>

      {/* Session CTA */}
      <div className="glass-card p-5">
        {inProgress ? (
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-[#1A1A2E]">
                {inProgress.template
                  ? `Reflection ${inProgress.template.orderNum}: ${inProgress.template.title}`
                  : "Your reflection is in progress"}
              </p>
              <p className="text-xs text-[#6B7280] mt-0.5">Pick up where you left off</p>
            </div>
            <Link href={`/reflect/${inProgress.id}`} className="btn-primary py-2 px-4 text-sm">
              Continue
            </Link>
          </div>
        ) : daysLeft > 0 ? (
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-[#1A1A2E]">
                Reflection {completedCount} of {totalTemplates || "?"} complete ✓
              </p>
              <p className="text-xs text-[#6B7280] mt-0.5">
                Next opens in {daysLeft} day{daysLeft !== 1 ? "s" : ""}
              </p>
            </div>
            <Link href="/reflections" className="text-sm text-[#3B82F6] font-medium hover:underline">
              View history
            </Link>
          </div>
        ) : (
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-[#1A1A2E]">
                {completedCount === 0
                  ? "Ready for your first reflection?"
                  : `Reflection ${completedCount + 1} is ready`}
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
      {signalProfile && <BreadthBar score={signalProfile.breadthScore} />}

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
                Explore the Career &amp; Education Map
              </p>
              <p className="text-xs text-[#6B7280] mt-0.5">
                Discover paths aligned with your interests
              </p>
            </div>
            <svg className="w-5 h-5 text-[#3B82F6]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8.25 4.5l7.5 7.5-7.5 7.5" />
            </svg>
          </div>
        </div>
      </Link>
    </div>
  );
}
