"use client";

import { useState, useEffect } from "react";
import { Button } from "@compass/ui";
import Link from "next/link";

interface MapNode {
  id: string;
  type: string;
  label: string;
  description: string | null;
  metadata: Record<string, unknown>;
}

interface Session {
  id: string;
  activities: unknown[];
}

export default function MapMomentStep({
  session: _session,
  onNext,
  onBack,
}: {
  session: Session;
  onNext: () => void;
  onBack: () => void;
}) {
  const [suggestedNodes, setSuggestedNodes] = useState<MapNode[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSuggestions() {
      try {
        const res = await fetch("/api/map/personalized");
        if (res.ok) {
          const data = await res.json() as { nodes: MapNode[] };
          // Show top 2 nodes
          setSuggestedNodes(data.nodes.slice(0, 2));
        }
      } catch {
        // No suggestions, that's fine
      } finally {
        setLoading(false);
      }
    }

    fetchSuggestions();
  }, []);

  const typeColors: Record<string, string> = {
    CAREER: "bg-blue-100 text-blue-800",
    MAJOR: "bg-violet-100 text-violet-800",
    INDUSTRY: "bg-emerald-100 text-emerald-800",
    PROGRAM: "bg-amber-100 text-amber-800",
    SKILL: "bg-red-100 text-red-800",
    VALUE: "bg-pink-100 text-pink-800",
  };

  return (
    <div className="space-y-4">
      <div className="glass-card p-5">
        <h2 className="text-xl font-bold text-[#1A1A2E] mb-1">Map Moment</h2>
        <p className="text-sm text-[#6B7280] mb-5">
          Based on your interests, here are some areas you might find interesting
          to explore. No pressure — just discovery.
        </p>

        {loading ? (
          <div className="space-y-3">
            {[0, 1].map((i) => (
              <div
                key={i}
                className="h-24 bg-gray-100/60 rounded-xl animate-pulse"
              />
            ))}
          </div>
        ) : suggestedNodes.length > 0 ? (
          <div className="space-y-3">
            {suggestedNodes.map((node) => (
              <div
                key={node.id}
                className="p-4 bg-white/50 rounded-xl border border-gray-200/40 hover:border-blue-200/60 transition-colors"
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span
                        className={`text-[10px] font-semibold px-2 py-0.5 rounded-full uppercase tracking-wide ${
                          typeColors[node.type] ?? "bg-gray-100 text-gray-800"
                        }`}
                      >
                        {node.type}
                      </span>
                    </div>
                    <h3 className="text-sm font-semibold text-[#1A1A2E]">
                      {node.label}
                    </h3>
                    {node.description && (
                      <p className="text-xs text-[#6B7280] mt-0.5 line-clamp-2">
                        {node.description}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}

            <Link
              href="/map"
              className="block text-center text-sm text-[#3B82F6] font-medium hover:underline pt-1"
            >
              Explore the full map →
            </Link>
          </div>
        ) : (
          <div className="text-center py-6">
            <div className="text-4xl mb-3">🗺️</div>
            <p className="text-sm text-[#6B7280] mb-3">
              Complete more reflections to get personalized map suggestions
            </p>
            <Link
              href="/map"
              className="text-sm text-[#3B82F6] font-medium hover:underline"
            >
              Explore the map anyway →
            </Link>
          </div>
        )}
      </div>

      <div className="flex gap-3">
        <Button onClick={onBack} variant="ghost" size="lg">
          Back
        </Button>
        <Button onClick={onNext} variant="primary" size="lg" fullWidth>
          Privacy Review →
        </Button>
      </div>
    </div>
  );
}
