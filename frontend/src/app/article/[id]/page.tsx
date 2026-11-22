"use client";

import { useArticle } from "@/lib/api";
import ArticleFull from "@/components/newspaper/ArticleFull";
import { Skeleton } from "@/components/ui/skeleton";

export default function ArticlePage({ params }: { params: { id: string } }) {
  const { data: article, error, isLoading } = useArticle(params.id);

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto py-12 px-4 space-y-6">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-12 w-full" />
        <Skeleton className="h-20 w-full" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (error || !article) {
    return (
      <div className="text-center py-20">
        <h2 className="newspaper-title text-2xl font-bold mb-2">Article Not Found</h2>
        <p className="text-stone-500 text-sm">The requested newspaper article could not be loaded.</p>
      </div>
    );
  }

  return <ArticleFull article={article} />;
}
