"use client";

import useSWR from "swr";
import Link from "next/link";
import SectionHeader from "@/components/newspaper/SectionHeader";
import { Flame, ArrowRight, ShieldAlert, Award } from "lucide-react";
import { formatDate } from "@/lib/utils";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function CatchupPage() {
  const { data, isLoading } = useSWR("/api/reading/catchup", (url) =>
    fetch(`${API_BASE}${url}`, { method: "POST" }).then((r) => r.json())
  );

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <SectionHeader
        title="Prioritized Catch-Up Mode"
        subtitle="Consolidated Intelligence For Readers Returning After Missed Days"
      />

      <div className="bg-amber-500/10 border border-amber-500/30 p-6 rounded flex items-center justify-between flex-wrap gap-4">
        <div>
          <span className="text-xs uppercase font-sans font-bold tracking-wider text-amber-800 dark:text-amber-300 flex items-center gap-1.5">
            <Flame className="w-4 h-4 text-amber-600" />
            Catch-Up Status
          </span>
          <h2 className="newspaper-title text-2xl font-black text-ink dark:text-ink-dark mt-1">
            {data?.missed_editions_count || 0} Recent Editions Analyzed
          </h2>
          <p className="text-xs text-stone-600 dark:text-stone-300 font-sans mt-0.5">
            Prioritizing Critical & High-impact reporting to rapidly bring you up to speed without reading hundreds of articles.
          </p>
        </div>
        <div className="flex gap-4 text-center text-xs font-sans">
          <div className="bg-white dark:bg-stone-900 px-3 py-2 rounded border">
            <span className="block text-lg font-black text-red-600">{data?.critical_unread_count || 0}</span>
            <span className="text-stone-500">Critical Stories</span>
          </div>
          <div className="bg-white dark:bg-stone-900 px-3 py-2 rounded border">
            <span className="block text-lg font-black text-amber-600">{data?.total_unread_articles || 0}</span>
            <span className="text-stone-500">Total Unread</span>
          </div>
        </div>
      </div>

      {/* Critical Stories First */}
      {data?.prioritized_articles && data.prioritized_articles.length > 0 && (
        <div>
          <h3 className="newspaper-title text-xl font-bold mb-4 flex items-center gap-2 text-red-600">
            <ShieldAlert className="w-5 h-5" />
            Must-Read Critical Developments
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.prioritized_articles.map((item: any) => (
              <div key={item.id} className="p-4 bg-white dark:bg-stone-900 rounded border border-red-200 dark:border-red-900/50 shadow-sm flex flex-col justify-between">
                <div>
                  <span className="text-[10px] font-sans font-bold uppercase text-red-600">{item.category}</span>
                  <h4 className="font-bold text-base newspaper-title mt-1 text-ink dark:text-ink-dark">{item.headline}</h4>
                </div>
                <div className="mt-3 pt-2 border-t flex justify-end">
                  <Link href={`/article/${item.id}`} className="text-accent text-xs font-bold font-sans flex items-center gap-1 hover:underline">
                    Read Story <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Missed Editions Summaries */}
      <div>
        <h3 className="newspaper-title text-xl font-bold mb-4 flex items-center gap-2 text-accent">
          <Award className="w-5 h-5" />
          Missed Edition Summaries
        </h3>
        <div className="space-y-4">
          {data?.missed_editions?.map((ed: any) => (
            <div key={ed.id} className="p-5 bg-white dark:bg-stone-900 rounded border flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <span className="font-bold text-base newspaper-title">{formatDate(ed.date)}</span>
                <span className="text-xs text-stone-500 block mt-0.5">{ed.total_articles} Articles in this edition</span>
                {ed.summary_preview && ed.summary_preview.length > 0 && (
                  <ul className="mt-2 text-xs text-stone-600 dark:text-stone-400 space-y-1">
                    {ed.summary_preview.map((p: string, idx: number) => (
                      <li key={idx} className="line-clamp-1">• {p}</li>
                    ))}
                  </ul>
                )}
              </div>
              <Link
                href={`/edition/${ed.id}`}
                className="px-4 py-2 bg-stone-900 dark:bg-stone-100 text-white dark:text-stone-900 rounded text-xs font-sans font-bold uppercase tracking-wider whitespace-nowrap hover:bg-stone-800"
              >
                Review Edition →
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
