"use client";

import { motion, HTMLMotionProps } from "framer-motion";
import { cn } from "./utils";

interface GlassCardProps extends Omit<HTMLMotionProps<"div">, "children"> {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  onClick?: () => void;
  padding?: "none" | "sm" | "md" | "lg";
}

const paddingMap = {
  none: "",
  sm: "p-3",
  md: "p-5",
  lg: "p-8",
};

export function GlassCard({
  children,
  className,
  hover = false,
  onClick,
  padding = "md",
  ...props
}: GlassCardProps) {
  return (
    <motion.div
      className={cn(
        "rounded-[16px] border border-white/[0.18]",
        "bg-white/[0.72] backdrop-blur-[20px] backdrop-saturate-[180%]",
        "shadow-[0_8px_32px_0_rgba(31,38,135,0.15)]",
        paddingMap[padding],
        hover &&
          "cursor-pointer transition-all duration-200 hover:shadow-[0_12px_40px_0_rgba(31,38,135,0.25)] hover:-translate-y-0.5",
        className
      )}
      onClick={onClick}
      whileHover={hover ? { scale: 1.01 } : undefined}
      whileTap={onClick ? { scale: 0.99 } : undefined}
      {...props}
    >
      {children}
    </motion.div>
  );
}
