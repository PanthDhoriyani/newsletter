"use client";

import useSWR from "swr";
import Link from "next/link";
import SectionHeader from "@/components/newspaper/SectionHeader";
import { Bookmark, ArrowRight } from "lucide-react";
import { formatDate } from "@/lib/utils";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function SavedArticlesPage() {
  const { data: savedArticles, isLoading } = useSWR("/api/articles/saved", (url) =>
    fetch(`${API_BASE}${url}`).then((r) => r.json())
  );

  return (
    <div className="max-w-5xl mx-auto">
      <SectionHeader
        title="Saved For Later"
        subtitle="Your Curated Personal Library of Important Articles"
      />

      {isLoading ? (
        <div className="space-y-4">
          <div className="h-16 bg-stone-200 dark:bg-stone-800 animate-pulse rounded"></div>
        </div>
      ) : savedArticles && savedArticles.length > 0 ? (
        <div className="space-y-4">
          {savedArticles.map((article: any) => (
            <div
              key={article.id}
              className="p-5 bg-white dark:bg-stone-900 rounded border border-stone-200 dark:border-stone-800 flex justify-between items-center gap-4 hover:border-stone-400 transition-all"
            >
              <div>
                <span className="text-[10px] font-sans font-bold uppercase tracking-wider text-accent">
                  {article.category || article.section} • {formatDate(article.published_at)}
                </span>
                <Link href={`/article/${article.id}`}>
                  <h3 className="newspaper-title text-xl font-bold mt-1 text-ink dark:text-ink-dark hover:text-accent">
                    {article.headline}
                  </h3>
                </Link>
              </div>

              <Link
                href={`/article/${article.id}`}
                className="px-4 py-2 bg-accent text-white text-xs font-sans font-bold uppercase tracking-wider rounded hover:bg-accent-hover shrink-0 flex items-center gap-1.5"
              >
                Read <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-20 bg-white dark:bg-stone-900 border rounded p-8">
          <Bookmark className="w-10 h-10 text-stone-300 dark:text-stone-700 mx-auto mb-3" />
          <h3 className="newspaper-title text-xl font-bold">No Saved Articles Yet</h3>
          <p className="text-stone-500 text-sm mt-1 font-sans">
            Click &apos;Save for Later&apos; on any article to build your permanent reference reading list.
          </p>
        </div>
      )}
    </div>
  );
}
