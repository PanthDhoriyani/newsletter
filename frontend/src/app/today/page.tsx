"use client";

import { useTodayEdition } from "@/lib/api";
import NewspaperMasthead from "@/components/newspaper/NewspaperMasthead";
import SectionHeader from "@/components/newspaper/SectionHeader";
import ArticleCard from "@/components/newspaper/ArticleCard";
import DailySummarySection from "@/components/newspaper/DailySummarySection";
import KnowledgeCorner from "@/components/newspaper/KnowledgeCorner";
import WatchNext from "@/components/newspaper/WatchNext";
import { ArticleCardSkeleton } from "@/components/ui/skeleton";
import { Article } from "@/lib/types";

export default function TodayNewspaper() {
  const { data: edition, error, isLoading } = useTodayEdition();

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
        <h2 className="newspaper-title text-2xl font-bold mb-2">Today&apos;s Edition is Not Published Yet</h2>
        <p className="text-sm text-stone-500 font-serif mb-6">
          The autonomous daily newspaper is generated every morning at 08:00 AM IST. You can trigger generation immediately from the Front Page.
        </p>
        <a
          href="/"
          className="px-4 py-2 bg-accent text-white text-xs font-sans uppercase tracking-wider font-bold rounded"
        >
          Return to Front Page
        </a>
      </div>
    );
  }

  // Partition articles by Section
  const indiaArticles = edition.articles?.filter((a) => a.section === "INDIA") || [];
  const worldArticles = edition.articles?.filter((a) => a.section === "WORLD") || [];
  const impactArticles = edition.articles?.filter((a) => a.section === "GLOBAL_IMPACT") || [];
  const otherArticles = edition.articles?.filter((a) => !["INDIA", "WORLD", "GLOBAL_IMPACT"].includes(a.section)) || [];

  return (
    <div className="max-w-6xl mx-auto">
      {/* Newspaper Masthead */}
      <NewspaperMasthead edition={edition} />

      {/* Part 1: India */}
      {indiaArticles.length > 0 && (
        <section className="mb-12">
          <SectionHeader
            title="PART 1: INDIA"
            subtitle="National News • Politics • Economy • Financial Markets • Law & Development"
          />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {indiaArticles.map((article: Article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        </section>
      )}

      {/* Part 2: World */}
      {worldArticles.length > 0 && (
        <section className="mb-12">
          <SectionHeader
            title="PART 2: WORLD"
            subtitle="International Affairs • Geopolitics • Global Trade • Conflicts & Security"
          />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {worldArticles.map((article: Article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        </section>
      )}

      {/* Part 3: Global Developments Affecting India */}
      {impactArticles.length > 0 && (
        <section className="mb-12">
          <SectionHeader
            title="PART 3: GLOBAL DEVELOPMENTS AFFECTING INDIA"
            subtitle="Analysis of Tariffs, Crude Oil Prices, Fed Decisions & Supply Chain Repercussions"
          />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {impactArticles.map((article: Article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        </section>
      )}

      {/* Other Important Trending Stories */}
      {otherArticles.length > 0 && (
        <section className="mb-12">
          <SectionHeader
            title="PART 4: TRENDING & SPECIAL REPORTS"
            subtitle="Sectoral Highlights • Science • Environment • Sports"
          />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {otherArticles.map((article: Article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        </section>
      )}

      {/* Part 5: What to Watch Next */}
      <WatchNext items={edition.what_to_watch_next} />

      {/* Part 6: Daily Knowledge Corner */}
      <KnowledgeCorner concepts={edition.knowledge_corner} />

      {/* Part 7: Mandatory Daily Edition Summary */}
      <DailySummarySection summary={edition.daily_summary} editionId={edition.id} />
    </div>
  );
}
