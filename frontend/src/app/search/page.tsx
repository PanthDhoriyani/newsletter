"use client";

import { useState } from "react";
import useSWR from "swr";
import Link from "next/link";
import SectionHeader from "@/components/newspaper/SectionHeader";
import { Search as SearchIcon, ArrowRight } from "lucide-react";
import { formatDate } from "@/lib/utils";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [section, setSection] = useState("");

  const searchUrl = `/api/articles/search?${query ? `q=${encodeURIComponent(query)}&` : ""}${
    section ? `section=${encodeURIComponent(section)}` : ""
  }`;

  const { data: results, isLoading } = useSWR(query.length >= 2 ? searchUrl : null, (url) =>
    fetch(`${API_BASE}${url}`).then((r) => r.json())
  );

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <SectionHeader
        title="Historical Newspaper Search"
        subtitle="Search Full-Text Reporting, Official Announcements & Archival Records"
      />

      {/* Search Input Bar */}
      <div className="bg-white dark:bg-stone-900 p-4 rounded border border-stone-300 dark:border-stone-700 shadow-sm flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <SearchIcon className="w-4 h-4 text-stone-400 absolute left-3 top-3.5" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search keywords, companies, institutions, RBI, treaties..."
            className="w-full pl-9 pr-4 py-2.5 bg-paper dark:bg-stone-800 rounded border border-stone-200 dark:border-stone-700 text-sm focus:outline-none focus:border-accent"
          />
        </div>

        <select
          value={section}
          onChange={(e) => setSection(e.target.value)}
          className="px-3 py-2 bg-paper dark:bg-stone-800 rounded border border-stone-200 dark:border-stone-700 text-xs font-sans uppercase font-semibold"
        >
          <option value="">All Sections</option>
          <option value="INDIA">India</option>
          <option value="WORLD">World</option>
          <option value="GLOBAL_IMPACT">Global Impact on India</option>
          <option value="TRENDING">Trending</option>
        </select>
      </div>

      {/* Search Results */}
      {query.length >= 2 ? (
        isLoading ? (
          <div className="space-y-4">
            <div className="h-20 bg-stone-200 dark:bg-stone-800 animate-pulse rounded"></div>
          </div>
        ) : results && results.length > 0 ? (
          <div className="space-y-4">
            <p className="text-xs text-stone-500 font-sans">Found {results.length} matched articles</p>
            {results.map((article: any) => (
              <div
                key={article.id}
                className="p-5 bg-white dark:bg-stone-900 rounded border border-stone-200 dark:border-stone-800 hover:border-stone-400 transition-all"
              >
                <div className="flex justify-between items-start gap-4">
                  <div>
                    <span className="text-[10px] font-sans font-bold uppercase text-accent">
                      {article.category || article.section} • {formatDate(article.published_at)}
                    </span>
                    <Link href={`/article/${article.id}`}>
                      <h3 className="newspaper-title text-xl font-bold mt-1 text-ink dark:text-ink-dark hover:text-accent">
                        {article.headline}
                      </h3>
                    </Link>
                    {article.introduction && (
                      <p className="text-xs text-stone-600 dark:text-stone-400 mt-1 line-clamp-2 font-body">
                        {article.introduction}
                      </p>
                    )}
                  </div>
                  <Link
                    href={`/article/${article.id}`}
                    className="text-xs font-sans font-bold text-accent hover:underline flex items-center gap-1 shrink-0"
                  >
                    Read <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16 bg-white dark:bg-stone-900 rounded border">
            <p className="text-stone-500 text-sm">No articles matched your search query.</p>
          </div>
        )
      ) : (
        <div className="text-center py-12 text-stone-400 text-xs font-sans uppercase tracking-wider">
          Type at least 2 characters to search published editions
        </div>
      )}
    </div>
  );
}
