"use client";

interface Opportunity {
  id: string;
  title: string;
  description: string;
  category: string;
  url: string | null;
  location: string | null;
  organizerName: string | null;
  deadline: string | null;
  tags: string[];
  matchScore: number;
  matchReason: string;
  isSaved: boolean;
  isDismissed: boolean;
  isPersonalized: boolean;
}

const CATEGORY_COLORS: Record<string, string> = {
  COMPETITION: "bg-orange-100 text-orange-700",
  RESEARCH: "bg-purple-100 text-purple-700",
  EVENT: "bg-blue-100 text-blue-700",
  HACKATHON: "bg-green-100 text-green-700",
  PROGRAM: "bg-indigo-100 text-indigo-700",
  CLUB: "bg-yellow-100 text-yellow-700",
  VOLUNTEER: "bg-teal-100 text-teal-700",
  PUBLICATION: "bg-rose-100 text-rose-700",
};

function formatDeadline(deadline: string | null): { text: string; urgent: boolean } | null {
  if (!deadline) return null;
  const d = new Date(deadline);
  const daysUntil = Math.ceil((d.getTime() - Date.now()) / (1000 * 60 * 60 * 24));
  if (daysUntil < 0) return { text: "Deadline passed", urgent: false };
  if (daysUntil === 0) return { text: "Due today", urgent: true };
  if (daysUntil <= 7) return { text: `${daysUntil}d left`, urgent: true };
  if (daysUntil <= 30) return { text: `${daysUntil}d left`, urgent: false };
  return { text: d.toLocaleDateString("en-US", { month: "short", day: "numeric" }), urgent: false };
}

export default function OpportunityCard({
  opportunity,
  onSave,
  onDismiss,
}: {
  opportunity: Opportunity;
  onSave: (id: string, saved: boolean) => void;
  onDismiss: (id: string) => void;
}) {
  const deadline = formatDeadline(opportunity.deadline);
  const categoryColor = CATEGORY_COLORS[opportunity.category] ?? "bg-gray-100 text-gray-700";
  const matchPercent = Math.round(opportunity.matchScore * 100);

  return (
    <div className="glass-card p-5 space-y-3">
      {/* Header row */}
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full uppercase tracking-wide ${categoryColor}`}>
              {opportunity.category}
            </span>
            {deadline && (
              <span className={`text-[10px] font-medium ${deadline.urgent ? "text-red-500" : "text-[#6B7280]"}`}>
                {deadline.text}
              </span>
            )}
          </div>
          <h3 className="font-semibold text-[#1A1A2E] text-sm leading-snug line-clamp-2">
            {opportunity.title}
          </h3>
          {opportunity.organizerName && (
            <p className="text-xs text-[#6B7280] mt-0.5">{opportunity.organizerName}</p>
          )}
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-1 shrink-0">
          <button
            onClick={() => onSave(opportunity.id, !opportunity.isSaved)}
            className={`p-1.5 rounded-lg transition-colors ${
              opportunity.isSaved
                ? "text-[#3B82F6] bg-blue-50"
                : "text-[#6B7280] hover:text-[#3B82F6] hover:bg-blue-50"
            }`}
            aria-label={opportunity.isSaved ? "Unsave" : "Save"}
          >
            <svg className="w-4 h-4" fill={opportunity.isSaved ? "currentColor" : "none"} viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0 1 11.186 0Z" />
            </svg>
          </button>
          <button
            onClick={() => onDismiss(opportunity.id)}
            className="p-1.5 rounded-lg text-[#6B7280] hover:text-red-400 hover:bg-red-50 transition-colors"
            aria-label="Dismiss"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      {/* Description */}
      <p className="text-xs text-[#6B7280] line-clamp-2">{opportunity.description}</p>

      {/* Match info */}
      {opportunity.isPersonalized && matchPercent > 0 && (
        <div className="space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-[#6B7280] font-medium">Match</span>
            <span className="text-[10px] font-semibold text-[#3B82F6]">{matchPercent}%</span>
          </div>
          <div className="w-full bg-gray-100 rounded-full h-1">
            <div
              className="bg-[#3B82F6] h-1 rounded-full transition-all"
              style={{ width: `${matchPercent}%` }}
            />
          </div>
          {opportunity.matchReason && (
            <p className="text-[10px] text-[#6B7280] italic">{opportunity.matchReason}</p>
          )}
        </div>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between pt-1">
        <div className="flex items-center gap-2 text-[10px] text-[#6B7280]">
          {opportunity.location && <span>{opportunity.location}</span>}
          {opportunity.tags.slice(0, 2).map((tag) => (
            <span key={tag} className="bg-gray-100 px-2 py-0.5 rounded-full">{tag}</span>
          ))}
        </div>
        {opportunity.url && (
          <a
            href={opportunity.url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={() => onDismiss(opportunity.id)}
            className="text-[10px] font-medium text-[#3B82F6] hover:underline flex items-center gap-0.5"
          >
            Learn more
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 6H5.25A2.25 2.25 0 0 0 3 8.25v10.5A2.25 2.25 0 0 0 5.25 21h10.5A2.25 2.25 0 0 0 18 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
            </svg>
          </a>
        )}
      </div>
    </div>
  );
}
