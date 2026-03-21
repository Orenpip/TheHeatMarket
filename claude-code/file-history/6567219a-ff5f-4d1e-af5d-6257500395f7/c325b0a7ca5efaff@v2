"use client";

import { useState } from "react";

export default function MapSearchBar({
  onSearch,
}: {
  onSearch: (query: string) => void;
}) {
  const [query, setQuery] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onSearch(query);
  }

  function handleClear() {
    setQuery("");
    onSearch("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex-1 glass-card !p-0 flex items-center overflow-hidden"
    >
      <svg
        className="w-4 h-4 text-[#6B7280] ml-3 flex-shrink-0"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={1.5}
          d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
        />
      </svg>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search careers, majors, programs..."
        className="flex-1 px-3 py-2.5 bg-transparent text-sm text-[#1A1A2E] placeholder-[#9CA3AF] focus:outline-none"
      />
      {query && (
        <button
          type="button"
          onClick={handleClear}
          className="px-3 text-[#9CA3AF] hover:text-[#1A1A2E]"
        >
          ✕
        </button>
      )}
    </form>
  );
}
