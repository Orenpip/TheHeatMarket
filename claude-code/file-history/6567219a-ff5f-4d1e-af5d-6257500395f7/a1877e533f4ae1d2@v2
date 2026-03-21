"use client";

import { cn } from "./utils";

type SignalStrength = "strong" | "moderate" | "emerging" | "new";

interface SignalBadgeProps {
  label: string;
  strength?: SignalStrength;
  className?: string;
  onClick?: () => void;
}

const strengthConfig: Record<
  SignalStrength,
  { dot: string; bg: string; text: string; border: string }
> = {
  strong: {
    dot: "bg-[#10B981]",
    bg: "bg-emerald-50",
    text: "text-emerald-800",
    border: "border-emerald-200",
  },
  moderate: {
    dot: "bg-[#F59E0B]",
    bg: "bg-amber-50",
    text: "text-amber-800",
    border: "border-amber-200",
  },
  emerging: {
    dot: "bg-[#8B5CF6]",
    bg: "bg-violet-50",
    text: "text-violet-800",
    border: "border-violet-200",
  },
  new: {
    dot: "bg-[#3B82F6]",
    bg: "bg-blue-50",
    text: "text-blue-800",
    border: "border-blue-200",
  },
};

export function SignalBadge({
  label,
  strength = "moderate",
  className,
  onClick,
}: SignalBadgeProps) {
  const config = strengthConfig[strength];

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border",
        config.bg,
        config.text,
        config.border,
        onClick && "cursor-pointer hover:opacity-80 transition-opacity",
        className
      )}
      onClick={onClick}
    >
      <span className={cn("w-1.5 h-1.5 rounded-full", config.dot)} />
      {label}
    </span>
  );
}
