"use client";

import { useEdition } from "@/lib/api";
import NewspaperMasthead from "@/components/newspaper/NewspaperMasthead";
import SectionHeader from "@/components/newspaper/SectionHeader";
import ArticleCard from "@/components/newspaper/ArticleCard";
import DailySummarySection from "@/components/newspaper/DailySummarySection";
import KnowledgeCorner from "@/components/newspaper/KnowledgeCorner";
import WatchNext from "@/components/newspaper/WatchNext";
import { ArticleCardSkeleton } from "@/components/ui/skeleton";
import { Article } from "@/lib/types";

export default function EditionPage({ params }: { params: { id: string } }) {
  const { data: edition, error, isLoading } = useEdition(params.id);

  if (isLoading) {
    return (
      <div className="space-y-8 max-w-6xl mx-auto">
        <div className="h-28 bg-stone-200 dark:bg-stone-800 animate-pulse rounded"></div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <ArticleCardSkeleton />
          <ArticleCardSkeleton />
          <ArticleCardSkeleton />
        </div>
      </div>
    );
  }

  if (error || !edition) {
    return (
      <div className="text-center py-20 bg-white dark:bg-stone-900 border rounded p-8 max-w-2xl mx-auto">
        <h2 className="newspaper-title text-2xl font-bold mb-2">Edition Not Found</h2>
        <p className="text-sm text-stone-500 font-serif mb-6">
          The requested historical newspaper edition could not be located in the archive.
        </p>
      </div>
    );
  }

  const indiaArticles = edition.articles?.filter((a) => a.section === "INDIA") || [];
  const worldArticles = edition.articles?.filter((a) => a.section === "WORLD") || [];
  const impactArticles = edition.articles?.filter((a) => a.section === "GLOBAL_IMPACT") || [];
  const otherArticles = edition.articles?.filter((a) => !["INDIA", "WORLD", "GLOBAL_IMPACT"].includes(a.section)) || [];

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-amber-100/60 dark:bg-stone-800 border-l-4 border-l-amber-600 p-3 mb-6 text-xs text-amber-900 dark:text-amber-200 font-sans uppercase tracking-wider font-semibold">
        Historical Archive Snapshot • Immutable Record
      </div>

      <NewspaperMasthead edition={edition} />

      {indiaArticles.length > 0 && (
        <section className="mb-12">
          <SectionHeader title="PART 1: INDIA" subtitle="National News & Developments" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {indiaArticles.map((article: Article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        </section>
      )}

      {worldArticles.length > 0 && (
        <section className="mb-12">
          <SectionHeader title="PART 2: WORLD" subtitle="International Affairs & Geopolitics" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {worldArticles.map((article: Article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        </section>
      )}

      {impactArticles.length > 0 && (
        <section className="mb-12">
          <SectionHeader title="PART 3: GLOBAL DEVELOPMENTS AFFECTING INDIA" subtitle="Impact & Direct Consequences" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {impactArticles.map((article: Article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        </section>
      )}

      {otherArticles.length > 0 && (
        <section className="mb-12">
          <SectionHeader title="PART 4: TRENDING & SPECIAL REPORTS" subtitle="Sectoral & Technology Updates" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {otherArticles.map((article: Article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        </section>
      )}

      <WatchNext items={edition.what_to_watch_next} />
      <KnowledgeCorner concepts={edition.knowledge_corner} />
      <DailySummarySection summary={edition.daily_summary} editionId={edition.id} />
    </div>
  );
}
