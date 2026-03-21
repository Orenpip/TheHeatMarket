"use client";

const LEGEND_ITEMS = [
  { type: "CAREER", label: "Career", color: "#3B82F6" },
  { type: "MAJOR", label: "Major", color: "#8B5CF6" },
  { type: "INDUSTRY", label: "Industry", color: "#10B981" },
  { type: "PROGRAM", label: "Program", color: "#F59E0B" },
  { type: "SKILL", label: "Skill", color: "#EF4444" },
];

export default function MapLegend() {
  return (
    <div className="glass-card p-3">
      <div className="flex flex-col gap-1.5">
        {LEGEND_ITEMS.map((item) => (
          <div key={item.type} className="flex items-center gap-2">
            <div
              className="w-3 h-3 rounded-full flex-shrink-0"
              style={{ backgroundColor: item.color }}
            />
            <span className="text-[10px] text-[#6B7280]">{item.label}</span>
          </div>
        ))}
        <div className="flex items-center gap-2 mt-1 pt-1 border-t border-gray-200/40">
          <div className="w-3 h-3 rounded-full bg-blue-400 ring-2 ring-white flex-shrink-0" />
          <span className="text-[10px] text-[#3B82F6]">Matches you</span>
        </div>
      </div>
    </div>
  );
}
