"use client";

import { useTodayEdition } from "@/lib/api";
import SectionHeader from "@/components/newspaper/SectionHeader";
import ArticleCard from "@/components/newspaper/ArticleCard";
import { ArticleCardSkeleton } from "@/components/ui/skeleton";
import { Article } from "@/lib/types";

export default function IndiaNewsPage() {
  const { data: edition, isLoading } = useTodayEdition();
  const articles = edition?.articles?.filter((a) => a.section === "INDIA") || [];

  return (
    <div className="max-w-6xl mx-auto">
      <SectionHeader
        title="India Domestic & National News"
        subtitle="Comprehensive Coverage Across Government, Politics, Economy, Infrastructure & Society"
      />

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <ArticleCardSkeleton />
          <ArticleCardSkeleton />
          <ArticleCardSkeleton />
        </div>
      ) : articles.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {articles.map((article: Article) => (
            <ArticleCard key={article.id} article={article} />
          ))}
        </div>
      ) : (
        <div className="text-center py-20 bg-white dark:bg-stone-900 rounded border">
          <p className="text-sm text-stone-500">No India section articles found in today&apos;s published edition.</p>
        </div>
      )}
    </div>
  );
}
