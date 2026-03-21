"use client";

import { cn } from "./utils";

interface GlassPanelProps {
  children: React.ReactNode;
  className?: string;
  variant?: "light" | "dark" | "colored";
  color?: string;
}

export function GlassPanel({
  children,
  className,
  variant = "light",
}: GlassPanelProps) {
  return (
    <div
      className={cn(
        "rounded-[24px] border",
        variant === "light" &&
          "border-white/20 bg-white/50 backdrop-blur-[16px] backdrop-saturate-[160%]",
        variant === "dark" &&
          "border-white/10 bg-black/30 backdrop-blur-[20px] backdrop-saturate-[180%]",
        variant === "colored" &&
          "border-blue-200/30 bg-blue-50/60 backdrop-blur-[16px]",
        className
      )}
    >
      {children}
    </div>
  );
}
