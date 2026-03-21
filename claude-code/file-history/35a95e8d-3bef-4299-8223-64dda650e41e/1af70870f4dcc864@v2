"use client";

import { useState, useEffect, useCallback } from "react";
import OpportunityCard from "./OpportunityCard";

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

interface ExploreResponse {
  opportunities: Opportunity[];
  pagination: { page: number; limit: number; total: number; hasMore: boolean };
}

const CATEGORIES = [
  { value: "", label: "All" },
  { value: "COMPETITION", label: "Competitions" },
  { value: "RESEARCH", label: "Research" },
  { value: "EVENT", label: "Events" },
  { value: "HACKATHON", label: "Hackathons" },
  { value: "PROGRAM", label: "Programs" },
  { value: "CLUB", label: "Clubs" },
  { value: "VOLUNTEER", label: "Volunteer" },
  { value: "PUBLICATION", label: "Publications" },
];

export default function ExplorePageContent() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [category, setCategory] = useState("");
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(false);
  const [isPersonalized, setIsPersonalized] = useState(false);

  const fetchOpportunities = useCallback(async (cat: string, pg: number, append = false) => {
    if (pg === 1) setLoading(true);
    else setLoadingMore(true);

    try {
      const params = new URLSearchParams({ page: String(pg), limit: "20" });
      if (cat) params.set("category", cat);

      const res = await fetch(`/api/explore?${params}`);
      if (!res.ok) throw new Error("Failed to load opportunities");

      const data: ExploreResponse = await res.json();
      setOpportunities((prev) =>
        append ? [...prev, ...data.opportunities] : data.opportunities
      );
      setHasMore(data.pagination.hasMore);
      const first = data.opportunities[0];
      if (first) {
        setIsPersonalized(first.isPersonalized);
      }
    } catch {
      setError("Could not load opportunities. Please try again.");
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  }, []);

  useEffect(() => {
    setPage(1);
    fetchOpportunities(category, 1, false);
  }, [category, fetchOpportunities]);

  const handleLoadMore = () => {
    const next = page + 1;
    setPage(next);
    fetchOpportunities(category, next, true);
  };

  const handleSave = async (id: string, saved: boolean) => {
    // Optimistic update
    setOpportunities((prev) =>
      prev.map((opp) => (opp.id === id ? { ...opp, isSaved: saved } : opp))
    );
    try {
      await fetch(`/api/explore/${id}/interact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type: saved ? "SAVE" : "UNSAVE" }),
      });
    } catch {
      // Revert on failure
      setOpportunities((prev) =>
        prev.map((opp) => (opp.id === id ? { ...opp, isSaved: !saved } : opp))
      );
    }
  };

  const handleDismiss = async (id: string) => {
    // Optimistic remove from feed
    setOpportunities((prev) => prev.filter((opp) => opp.id !== id));
    try {
      await fetch(`/api/explore/${id}/interact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type: "DISMISS" }),
      });
    } catch {
      // Non-fatal — just leave dismissed in UI
    }
  };

  const visible = opportunities.filter((opp) => !opp.isDismissed);

  return (
    <div className="space-y-4">
      {/* Personalization badge */}
      {isPersonalized && (
        <p className="text-xs text-[#6B7280]">
          Ranked by match to your interests
        </p>
      )}

      {/* Category filters */}
      <div className="flex gap-2 overflow-x-auto pb-1 -mx-4 px-4 no-scrollbar">
        {CATEGORIES.map((cat) => (
          <button
            key={cat.value}
            onClick={() => setCategory(cat.value)}
            className={`shrink-0 text-xs font-medium px-3 py-1.5 rounded-full border transition-colors ${
              category === cat.value
                ? "bg-[#3B82F6] text-white border-[#3B82F6]"
                : "text-[#6B7280] border-gray-200 hover:border-[#3B82F6] hover:text-[#3B82F6]"
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="glass-card p-5 animate-pulse space-y-3">
              <div className="flex gap-2">
                <div className="h-4 w-20 bg-gray-200 rounded-full" />
                <div className="h-4 w-16 bg-gray-200 rounded-full" />
              </div>
              <div className="h-4 w-3/4 bg-gray-200 rounded" />
              <div className="h-3 w-full bg-gray-200 rounded" />
              <div className="h-3 w-5/6 bg-gray-200 rounded" />
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="glass-card p-8 text-center">
          <p className="text-sm text-red-500">{error}</p>
          <button
            onClick={() => fetchOpportunities(category, 1, false)}
            className="mt-3 text-sm text-[#3B82F6] hover:underline"
          >
            Try again
          </button>
        </div>
      ) : visible.length === 0 ? (
        <div className="glass-card p-8 text-center">
          <div className="text-4xl mb-3">🎯</div>
          <h3 className="font-semibold text-[#1A1A2E] mb-1">
            {category ? "No opportunities in this category yet" : "No opportunities yet"}
          </h3>
          <p className="text-sm text-[#6B7280]">
            {category
              ? "Try a different filter or check back soon."
              : "Complete your first reflection to get personalized recommendations, or check back soon."}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {visible.map((opp) => (
            <OpportunityCard
              key={opp.id}
              opportunity={opp}
              onSave={handleSave}
              onDismiss={handleDismiss}
            />
          ))}

          {hasMore && (
            <button
              onClick={handleLoadMore}
              disabled={loadingMore}
              className="w-full glass-card py-3 text-sm font-medium text-[#3B82F6] hover:bg-blue-50/40 transition-colors disabled:opacity-50"
            >
              {loadingMore ? "Loading..." : "Load more"}
            </button>
          )}
        </div>
      )}
    </div>
  );
}
