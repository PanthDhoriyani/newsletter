"use client";

import useSWR from "swr";
import Link from "next/link";
import { formatDate } from "@/lib/utils";
import SectionHeader from "@/components/newspaper/SectionHeader";
import { Calendar as CalendarIcon, ArrowRight, ShieldCheck } from "lucide-react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ArchivePage() {
  const { data: editions, isLoading } = useSWR("/api/editions/", (url) =>
    fetch(`${API_BASE}${url}`).then((r) => r.json())
  );

  return (
    <div className="max-w-6xl mx-auto">
      <SectionHeader
        title="Historical Newspaper Archive"
        subtitle="Permanent Immutability • Date-Based Edition Browsing"
      />

      <div className="bg-paper dark:bg-stone-900/60 p-6 rounded border border-stone-200 dark:border-stone-800 mb-8">
        <p className="text-sm font-body text-stone-700 dark:text-stone-300">
          Every published edition of <em>The Digital Gazette</em> is preserved indefinitely as an immutable record. Older editions retain their original reporting and summary snapshots without being modified or overwritten.
        </p>
      </div>

      {isLoading ? (
        <div className="space-y-4">
          <div className="h-16 bg-stone-200 dark:bg-stone-800 animate-pulse rounded"></div>
          <div className="h-16 bg-stone-200 dark:bg-stone-800 animate-pulse rounded"></div>
        </div>
      ) : editions && editions.length > 0 ? (
        <div className="space-y-4">
          {editions.map((ed: any) => (
            <div
              key={ed.id}
              className="p-5 bg-white dark:bg-stone-900 rounded border border-stone-200 dark:border-stone-800 hover:border-stone-400 transition-all flex flex-col md:flex-row justify-between items-start md:items-center gap-4"
            >
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <CalendarIcon className="w-4 h-4 text-accent" />
                  <span className="font-bold text-base newspaper-title text-ink dark:text-ink-dark">
                    {formatDate(ed.edition_date)}
                  </span>
                  <span className="text-xs bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-sans font-semibold">
                    Published
                  </span>
                </div>
                <div className="flex gap-3 text-xs text-stone-500 font-sans mt-1">
                  <span>{ed.total_articles} Articles</span>
                  <span>•</span>
                  <span className="text-red-600 font-semibold">{ed.critical_count} Critical</span>
                  <span>•</span>
                  <span className="text-amber-600 font-semibold">{ed.high_count} High</span>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <Link
                  href={`/edition/${ed.id}`}
                  className="px-4 py-2 bg-accent text-white text-xs font-sans uppercase font-bold tracking-wider rounded hover:bg-accent-hover flex items-center gap-1.5"
                >
                  Read Edition <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-16 bg-white dark:bg-stone-900 rounded border">
          <p className="text-stone-500 text-sm">No historical editions archived yet.</p>
        </div>
      )}
    </div>
  );
}
