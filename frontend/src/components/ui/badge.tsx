import React from "react";
import { cn } from "@/lib/utils";
import { ImportanceLevel } from "@/lib/types";

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  importance?: ImportanceLevel;
  variant?: "default" | "outline" | "section";
}

export function ImportanceBadge({ importance = "MODERATE", className, ...props }: BadgeProps) {
  const colors = {
    CRITICAL: "bg-red-100 text-red-800 border-red-300 dark:bg-red-950 dark:text-red-300 dark:border-red-800",
    HIGH: "bg-amber-100 text-amber-800 border-amber-300 dark:bg-amber-950 dark:text-amber-300 dark:border-amber-800",
    MODERATE: "bg-blue-100 text-blue-800 border-blue-300 dark:bg-blue-950 dark:text-blue-300 dark:border-blue-800"
  };

  return (
    <span
      className={cn(
        "inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold tracking-wider uppercase border",
        colors[importance],
        className
      )}
      {...props}
    >
      {importance === "CRITICAL" && <span className="mr-1">●</span>}
      {importance}
    </span>
  );
}

export function SectionBadge({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <span className={cn("text-xs font-semibold uppercase tracking-wider text-accent border-b border-accent pb-0.5", className)}>
      {children}
    </span>
  );
}
