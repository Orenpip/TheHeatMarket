import Link from "next/link";

export default function CompletePage() {
  return (
    <div className="min-h-[80vh] flex items-center justify-center">
      <div className="glass-card p-10 text-center max-w-sm">
        <div className="text-6xl mb-4">✓</div>
        <h2 className="text-2xl font-bold text-[#1A1A2E] mb-2">
          All caught up for {new Date().toLocaleString("default", { month: "long" })}
        </h2>
        <p className="text-[#6B7280] text-sm mb-8">
          Your monthly reflection is complete. Your signal profile has been
          updated — head home to see your new insights.
        </p>

        <div className="space-y-3">
          <Link href="/" className="block btn-primary text-center">
            See Your Signals
          </Link>
          <Link
            href="/map"
            className="block text-sm text-[#3B82F6] font-medium hover:underline"
          >
            Explore the Map →
          </Link>
        </div>
      </div>
    </div>
  );
}
