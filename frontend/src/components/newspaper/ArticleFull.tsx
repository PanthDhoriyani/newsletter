"use client";

import { useState } from "react";
import Link from "next/link";
import { Article } from "@/lib/types";
import { ImportanceBadge, SectionBadge } from "@/components/ui/badge";
import { formatDate } from "@/lib/utils";
import { markArticleStatus } from "@/lib/api";
import { Check, Bookmark, Share2, ExternalLink, ArrowLeft } from "lucide-react";

export default function ArticleFull({ article }: { article: Article }) {
  const [isRead, setIsRead] = useState(article.read_status === "READ");
  const [isSaved, setIsSaved] = useState(article.read_status === "SAVED_FOR_LATER");

  const handleToggleRead = async () => {
    const nextStatus = isRead ? "UNREAD" : "READ";
    setIsRead(!isRead);
    await markArticleStatus(article.id, nextStatus);
  };

  const handleToggleSave = async () => {
    const nextStatus = isSaved ? "UNREAD" : "SAVED_FOR_LATER";
    setIsSaved(!isSaved);
    await markArticleStatus(article.id, nextStatus);
  };

  return (
    <article className="max-w-4xl mx-auto py-8 px-4">
      {/* Breadcrumb Navigation */}
      <div className="mb-6 flex items-center gap-2 text-xs font-sans text-stone-500 uppercase tracking-wider">
        <Link href="/" className="hover:text-accent flex items-center gap-1">
          <ArrowLeft className="w-3.5 h-3.5" />
          Front Page
        </Link>
        <span>/</span>
        <Link href={`/edition/${article.newsletter_id}`} className="hover:text-accent">
          Edition
        </Link>
        <span>/</span>
        <span className="text-stone-800 dark:text-stone-200">{article.section}</span>
      </div>

      {/* Meta header */}
      <div className="flex flex-wrap justify-between items-center gap-3 border-b border-stone-200 dark:border-stone-800 pb-3 mb-6">
        <div className="flex items-center gap-3">
          <SectionBadge>{article.category || article.section}</SectionBadge>
          <ImportanceBadge importance={article.importance} />
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleToggleRead}
            className={`px-3 py-1 text-xs font-sans font-semibold rounded border flex items-center gap-1.5 transition-colors ${
              isRead
                ? "bg-emerald-100 text-emerald-800 border-emerald-300"
                : "bg-white dark:bg-stone-800 hover:border-stone-400"
            }`}
          >
            <Check className="w-3.5 h-3.5" />
            {isRead ? "Marked as Read" : "Mark as Read"}
          </button>
          <button
            onClick={handleToggleSave}
            className={`px-3 py-1 text-xs font-sans font-semibold rounded border flex items-center gap-1.5 transition-colors ${
              isSaved
                ? "bg-blue-100 text-blue-800 border-blue-300"
                : "bg-white dark:bg-stone-800 hover:border-stone-400"
            }`}
          >
            <Bookmark className="w-3.5 h-3.5" />
            {isSaved ? "Saved" : "Save for Later"}
          </button>
        </div>
      </div>

      {/* Headline */}
      <h1 className="newspaper-title text-3xl md:text-5xl font-black text-ink dark:text-ink-dark leading-tight mb-4">
        {article.headline}
      </h1>

      {/* Subhead / Publication Details */}
      <div className="text-xs text-stone-500 font-sans border-b border-stone-200 dark:border-stone-800 pb-4 mb-8">
        Published on {formatDate(article.published_at)} • Comprehensive Multi-Source Editorial
      </div>

      {/* Lead Paragraph */}
      {article.introduction && (
        <div className="text-lg md:text-xl font-serif text-stone-800 dark:text-stone-200 font-medium leading-relaxed mb-6 border-l-4 border-accent pl-4 italic">
          {article.introduction}
        </div>
      )}

      {/* Main Reporting Content */}
      <div className="prose prose-stone dark:prose-invert max-w-none text-base md:text-lg leading-relaxed font-body space-y-6">
        <p className="whitespace-pre-line">{article.content}</p>

        {/* Structured Sections */}
        {article.background_context && (
          <div className="my-6 p-4 bg-paper dark:bg-stone-900 rounded border border-stone-200 dark:border-stone-800">
            <h3 className="newspaper-title text-lg font-bold uppercase tracking-wider mb-2 text-stone-800 dark:text-stone-200">
              Background & Recent Context
            </h3>
            <p className="text-sm font-body leading-relaxed">{article.background_context}</p>
          </div>
        )}

        {article.key_developments && (
          <div className="my-6 p-4 bg-stone-50 dark:bg-stone-900 rounded border border-stone-200 dark:border-stone-800">
            <h3 className="newspaper-title text-lg font-bold uppercase tracking-wider mb-2 text-stone-800 dark:text-stone-200">
              Key Developments & Official Details
            </h3>
            <p className="text-sm font-body leading-relaxed whitespace-pre-line">{article.key_developments}</p>
          </div>
        )}

        {article.why_it_matters && (
          <div className="my-6 p-4 bg-amber-50/60 dark:bg-amber-950/20 rounded border-l-4 border-l-amber-600">
            <h3 className="newspaper-title text-lg font-bold uppercase tracking-wider mb-2 text-amber-900 dark:text-amber-200">
              Why It Matters
            </h3>
            <p className="text-sm font-body leading-relaxed">{article.why_it_matters}</p>
          </div>
        )}

        {article.india_impact && (
          <div className="my-6 p-4 bg-blue-50/60 dark:bg-blue-950/20 rounded border-l-4 border-l-blue-600">
            <h3 className="newspaper-title text-lg font-bold uppercase tracking-wider mb-2 text-blue-900 dark:text-blue-200">
              Impact on India
            </h3>
            <p className="text-sm font-body leading-relaxed">{article.india_impact}</p>
          </div>
        )}

        {article.economic_industry_impact && (
          <div className="my-6 p-4 bg-emerald-50/60 dark:bg-emerald-950/20 rounded border-l-4 border-l-emerald-600">
            <h3 className="newspaper-title text-lg font-bold uppercase tracking-wider mb-2 text-emerald-900 dark:text-emerald-200">
              Economic & Market Implications
            </h3>
            <p className="text-sm font-body leading-relaxed">{article.economic_industry_impact}</p>
          </div>
        )}

        {article.what_happens_next && (
          <div className="my-6 p-4 bg-purple-50/60 dark:bg-purple-950/20 rounded border-l-4 border-l-purple-600">
            <h3 className="newspaper-title text-lg font-bold uppercase tracking-wider mb-2 text-purple-900 dark:text-purple-200">
              What Happens Next
            </h3>
            <p className="text-sm font-body leading-relaxed">{article.what_happens_next}</p>
          </div>
        )}
      </div>

      {/* Verified Primary Sources List */}
      <div className="mt-12 pt-6 border-t-2 border-stone-300 dark:border-stone-700 font-sans">
        <h4 className="text-xs font-bold uppercase tracking-widest text-stone-500 mb-3">
          Verified Primary & Reporting Sources ({article.sources?.length || 0})
        </h4>
        <div className="space-y-2">
          {article.sources?.map((s) => (
            <div
              key={s.id}
              className="p-3 bg-stone-50 dark:bg-stone-900/60 rounded border border-stone-200 dark:border-stone-800 flex justify-between items-center text-xs"
            >
              <div>
                <span className="font-semibold text-ink dark:text-ink-dark">{s.source_name}</span>
                <span className="ml-2 text-[10px] text-stone-400 uppercase">({s.source_type})</span>
                {s.snippet && (
                  <p className="text-[11px] text-stone-500 mt-1 line-clamp-1 italic">&ldquo;{s.snippet}&rdquo;</p>
                )}
              </div>
              <a
                href={s.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-accent hover:underline flex items-center gap-1 font-medium ml-4 shrink-0"
              >
                Original Source <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          ))}
        </div>
      </div>
    </article>
  );
}
