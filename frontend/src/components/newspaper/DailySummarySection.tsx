"use client";

import { useState } from "react";
import Link from "next/link";
import { DailySummary } from "@/lib/types";
import { markSummaryRead } from "@/lib/api";
import { CheckCircle2, Bookmark, ArrowUpRight, Award, ShieldAlert } from "lucide-react";

export default function DailySummarySection({
  summary,
  editionId
}: {
  summary?: DailySummary;
  editionId: string;
}) {
  const [isMarked, setIsMarked] = useState(false);

  if (!summary) return null;

  const handleMarkRead = async () => {
    setIsMarked(true);
    await markSummaryRead(editionId);
  };

  return (
    <section className="mt-16 pt-8 border-t-4 border-double border-stone-800 dark:border-stone-300 bg-amber-50/50 dark:bg-stone-900/80 p-6 md:p-10 rounded-sm shadow-md">
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto mb-10 pb-6 border-b border-stone-300 dark:border-stone-700">
        <span className="text-xs font-sans font-bold uppercase tracking-widest text-accent bg-accent/10 px-3 py-1 rounded">
          Mandatory Final Section
        </span>
        <h2 className="newspaper-title text-3xl md:text-5xl font-black mt-2 text-ink dark:text-ink-dark">
          DAILY EDITION SUMMARY
        </h2>
        <p className="text-stone-600 dark:text-stone-400 text-sm mt-2 font-serif italic">
          An editorial synthesis of today&apos;s essential developments across India and the globe. Designed to be read in 3 to 5 minutes.
        </p>
        <div className="mt-4 flex justify-center">
          <button
            onClick={handleMarkRead}
            disabled={isMarked}
            className={`px-4 py-1.5 text-xs font-sans font-bold uppercase tracking-wider rounded flex items-center gap-1.5 transition-all ${
              isMarked
                ? "bg-emerald-600 text-white cursor-default"
                : "bg-accent hover:bg-accent-hover text-white shadow-sm"
            }`}
          >
            <CheckCircle2 className="w-4 h-4" />
            {isMarked ? "Daily Summary Marked As Read" : "Mark Daily Summary As Read"}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">
        {/* Subsection 1: Today's Biggest Headlines */}
        <div className="col-span-full bg-white dark:bg-stone-900 p-6 rounded border border-stone-200 dark:border-stone-800 shadow-sm">
          <h3 className="newspaper-title text-xl font-bold border-b border-stone-200 dark:border-stone-800 pb-2 mb-4 flex items-center gap-2 text-red-600 dark:text-red-400">
            <ShieldAlert className="w-5 h-5" />
            1. Today&apos;s Biggest Headlines
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {summary.biggest_headlines?.map((h, i) => (
              <div key={i} className="p-3 bg-stone-50 dark:bg-stone-800/60 rounded border-l-4 border-l-red-500">
                <Link
                  href={`/article/${h.article_id}`}
                  className="font-bold text-sm text-ink dark:text-ink-dark hover:text-accent flex items-start justify-between gap-1 group"
                >
                  <span>{h.title}</span>
                  <ArrowUpRight className="w-4 h-4 opacity-50 group-hover:opacity-100 shrink-0" />
                </Link>
                <p className="text-xs text-stone-600 dark:text-stone-400 mt-1">{h.brief_why_it_matters}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Subsection 2: India in Focus */}
        <div className="bg-white dark:bg-stone-900 p-6 rounded border border-stone-200 dark:border-stone-800">
          <h3 className="newspaper-title text-xl font-bold border-b border-stone-200 dark:border-stone-800 pb-2 mb-3 text-accent">
            2. India in Focus
          </h3>
          <p className="text-sm text-stone-700 dark:text-stone-300 leading-relaxed font-body">
            {summary.india_in_focus?.summary_text}
          </p>
          <ul className="mt-4 space-y-2">
            {summary.india_in_focus?.key_developments?.map((k, i) => (
              <li key={i} className="text-xs flex items-start gap-1.5">
                <span className="text-accent font-bold">•</span>
                <Link href={`/article/${k.article_id}`} className="hover:underline text-stone-800 dark:text-stone-200">
                  {k.point}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        {/* Subsection 3: World in Focus */}
        <div className="bg-white dark:bg-stone-900 p-6 rounded border border-stone-200 dark:border-stone-800">
          <h3 className="newspaper-title text-xl font-bold border-b border-stone-200 dark:border-stone-800 pb-2 mb-3 text-accent">
            3. World in Focus
          </h3>
          <p className="text-sm text-stone-700 dark:text-stone-300 leading-relaxed font-body">
            {summary.world_in_focus?.summary_text}
          </p>
          <ul className="mt-4 space-y-2">
            {summary.world_in_focus?.key_developments?.map((k, i) => (
              <li key={i} className="text-xs flex items-start gap-1.5">
                <span className="text-accent font-bold">•</span>
                <Link href={`/article/${k.article_id}`} className="hover:underline text-stone-800 dark:text-stone-200">
                  {k.point}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        {/* Subsection 4: Impact on India */}
        <div className="bg-white dark:bg-stone-900 p-6 rounded border border-stone-200 dark:border-stone-800">
          <h3 className="newspaper-title text-xl font-bold border-b border-stone-200 dark:border-stone-800 pb-2 mb-3 text-amber-700 dark:text-amber-400">
            4. Impact on India
          </h3>
          <p className="text-sm text-stone-700 dark:text-stone-300 leading-relaxed font-body">
            {summary.impact_on_india?.summary_text}
          </p>
          <div className="mt-4 space-y-2">
            {summary.impact_on_india?.developments?.map((d, i) => (
              <div key={i} className="p-2 bg-amber-50/70 dark:bg-stone-800 rounded text-xs">
                <span className="font-semibold block text-stone-900 dark:text-stone-100">{d.international_event}</span>
                <span className="text-stone-600 dark:text-stone-400 block mt-0.5">{d.india_implication}</span>
                <Link href={`/article/${d.article_id}`} className="text-accent text-[11px] underline block mt-1 font-sans">
                  Read related coverage →
                </Link>
              </div>
            ))}
          </div>
        </div>

        {/* Subsection 5: Business and Markets */}
        <div className="bg-white dark:bg-stone-900 p-6 rounded border border-stone-200 dark:border-stone-800">
          <h3 className="newspaper-title text-xl font-bold border-b border-stone-200 dark:border-stone-800 pb-2 mb-3 text-emerald-700 dark:text-emerald-400">
            5. Business and Markets
          </h3>
          <p className="text-sm text-stone-700 dark:text-stone-300 leading-relaxed font-body">
            {summary.business_and_markets?.summary_text}
          </p>
          <ul className="mt-4 space-y-2">
            {summary.business_and_markets?.highlights?.map((h, i) => (
              <li key={i} className="text-xs flex items-start gap-1.5">
                <span className="text-emerald-600 font-bold">•</span>
                <Link href={`/article/${h.article_id}`} className="hover:underline text-stone-800 dark:text-stone-200">
                  {h.point}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        {/* Subsection 6: Other Important Developments */}
        <div className="col-span-full bg-white dark:bg-stone-900 p-6 rounded border border-stone-200 dark:border-stone-800">
          <h3 className="newspaper-title text-xl font-bold border-b border-stone-200 dark:border-stone-800 pb-2 mb-3 text-stone-800 dark:text-stone-200">
            6. Technology, Science, Health & Other Important Updates
          </h3>
          <p className="text-sm text-stone-700 dark:text-stone-300 leading-relaxed font-body mb-4">
            {summary.other_important?.summary_text}
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {summary.other_important?.items?.map((item, i) => (
              <div key={i} className="p-3 bg-stone-50 dark:bg-stone-800 rounded text-xs border border-stone-200 dark:border-stone-700">
                <span className="text-[10px] font-sans font-bold uppercase tracking-wider text-accent block mb-1">
                  {item.category}
                </span>
                <Link href={`/article/${item.article_id}`} className="hover:underline font-medium text-stone-900 dark:text-stone-100 block">
                  {item.point}
                </Link>
              </div>
            ))}
          </div>
        </div>

        {/* Subsection 7: Key Takeaways (5 to 10 points) */}
        <div className="col-span-full bg-paper dark:bg-stone-950 p-6 md:p-8 rounded-sm border-2 border-accent">
          <h3 className="newspaper-title text-2xl font-black mb-2 flex items-center gap-2 text-accent">
            <Award className="w-6 h-6" />
            7. Key Takeaways — What You Must Remember Today
          </h3>
          <p className="text-xs text-stone-600 dark:text-stone-400 font-sans uppercase tracking-widest mb-6">
            Essential Strategic Lessons & Takeaways From This Edition
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {summary.key_takeaways?.map((t, i) => (
              <div key={i} className="flex items-start gap-3 p-3 bg-white dark:bg-stone-900 rounded border border-stone-200 dark:border-stone-800">
                <span className="h-6 w-6 rounded-full bg-accent text-white flex items-center justify-center text-xs font-bold shrink-0">
                  {i + 1}
                </span>
                <div>
                  <p className="text-sm font-body text-ink dark:text-ink-dark font-medium">{t.takeaway}</p>
                  <Link
                    href={`/article/${t.article_id}`}
                    className="text-[11px] text-accent font-sans font-semibold underline mt-1 inline-block"
                  >
                    View Original Article →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
