import Link from "next/link";
import { Article } from "@/lib/types";
import { ImportanceBadge, SectionBadge } from "@/components/ui/badge";
import { ExternalLink, Bookmark } from "lucide-react";

export default function ArticleCard({ article }: { article: Article }) {
  const isCritical = article.importance === "CRITICAL";

  return (
    <article
      className={`border rounded-sm p-5 transition-all bg-white dark:bg-stone-900/60 shadow-sm hover:shadow-md flex flex-col justify-between ${
        isCritical
          ? "border-red-300 dark:border-red-900/70 border-l-4 border-l-red-600"
          : "border-stone-200 dark:border-stone-800 hover:border-stone-400"
      }`}
    >
      <div>
        <div className="flex justify-between items-center mb-2.5 gap-2">
          <SectionBadge>{article.category || article.section}</SectionBadge>
          <ImportanceBadge importance={article.importance} />
        </div>

        <Link href={`/article/${article.id}`}>
          <h3 className="newspaper-title text-xl md:text-2xl font-bold leading-snug text-ink dark:text-ink-dark hover:text-accent dark:hover:text-accent-hover transition-colors">
            {article.headline}
          </h3>
        </Link>

        {article.simplified_summary ? (
          <div className="mt-2.5">
            <span className="text-[10px] font-sans font-bold uppercase tracking-wider text-amber-700 dark:text-amber-400 block mb-1">
              Plain Words:
            </span>
            <p className="text-stone-700 dark:text-stone-300 text-sm line-clamp-3 font-body leading-relaxed">
              {article.simplified_summary}
            </p>
          </div>
        ) : article.introduction ? (
          <p className="text-stone-700 dark:text-stone-300 text-sm mt-2.5 line-clamp-3 font-body leading-relaxed">
            {article.introduction}
          </p>
        ) : null}

        {article.explained_terms && article.explained_terms.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">
            {article.explained_terms.slice(0, 3).map((t, idx) => (
              <span key={idx} className="px-1.5 py-0.5 bg-stone-100 dark:bg-stone-800 text-stone-600 dark:text-stone-400 rounded text-[10px] font-mono">
                {t.term}
              </span>
            ))}
            {article.explained_terms.length > 3 && (
              <span className="text-[10px] text-stone-400 self-center">
                +{article.explained_terms.length - 3} terms
              </span>
            )}
          </div>
        )}

        {article.why_it_matters && (
          <div className="mt-3 bg-paper dark:bg-stone-800/50 p-2.5 rounded text-xs text-stone-800 dark:text-stone-200 border-l-2 border-accent">
            <span className="font-semibold uppercase tracking-wider block text-[10px] text-accent">Why It Matters:</span>
            <p className="line-clamp-2">{article.why_it_matters}</p>
          </div>
        )}
      </div>

      <div className="mt-4 pt-3 border-t border-stone-100 dark:border-stone-800 flex justify-between items-center text-xs text-stone-500 font-sans">
        <span className="flex items-center gap-1.5">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
          {article.sources?.length || 1} verified source{article.sources?.length === 1 ? "" : "s"}
        </span>
        <Link
          href={`/article/${article.id}`}
          className="text-accent font-semibold hover:underline flex items-center gap-1"
        >
          Read Full Article →
        </Link>
      </div>
    </article>
  );
}
