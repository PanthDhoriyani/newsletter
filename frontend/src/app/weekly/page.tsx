"use client";

import useSWR from "swr";
import SectionHeader from "@/components/newspaper/SectionHeader";
import { Award, Calendar } from "lucide-react";
import { formatDate } from "@/lib/utils";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function WeeklyReviewPage() {
  const { data: review, error, isLoading } = useSWR("/api/weekly/latest", (url) =>
    fetch(`${API_BASE}${url}`).then((r) => {
      if (!r.ok) return null;
      return r.json();
    })
  );

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <SectionHeader
        title="Weekly Sunday Review"
        subtitle="Consolidated 7-Day Macro Intelligence & Strategic Narrative Analysis"
      />

      {isLoading ? (
        <div className="space-y-4">
          <div className="h-20 bg-stone-200 dark:bg-stone-800 animate-pulse rounded"></div>
        </div>
      ) : review ? (
        <div className="bg-white dark:bg-stone-900 p-8 rounded border border-stone-200 dark:border-stone-800 space-y-6">
          <div className="flex items-center gap-2 text-xs font-sans text-accent font-bold uppercase tracking-wider border-b pb-3">
            <Calendar className="w-4 h-4" />
            <span>Week Coverage: {formatDate(review.week_start)} to {formatDate(review.week_end)}</span>
          </div>

          <h2 className="newspaper-title text-3xl font-bold">Comprehensive Weekly Digest</h2>

          <div className="prose prose-stone dark:prose-invert max-w-none text-base leading-relaxed font-body">
            <p>{JSON.stringify(review.content, null, 2)}</p>
          </div>
        </div>
      ) : (
        <div className="text-center py-20 bg-white dark:bg-stone-900 rounded border">
          <Award className="w-10 h-10 text-stone-400 mx-auto mb-2" />
          <h3 className="newspaper-title text-xl font-bold">No Weekly Review Published Yet</h3>
          <p className="text-sm text-stone-500 mt-1 font-sans">
            Weekly reviews are automatically compiled every Sunday at 09:00 AM IST.
          </p>
        </div>
      )}
    </div>
  );
}
