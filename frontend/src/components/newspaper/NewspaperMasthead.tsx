import { formatDate } from "@/lib/utils";
import { Newsletter } from "@/lib/types";

export default function NewspaperMasthead({ edition }: { edition: Newsletter }) {
  return (
    <div className="border-b-2 border-stone-800 dark:border-stone-200 pb-4 mb-8 text-center">
      <div className="flex justify-between items-center text-xs border-b border-stone-300 dark:border-stone-700 py-1 mb-3 text-stone-600 dark:text-stone-400 font-sans uppercase tracking-widest">
        <span>Edition Date: {formatDate(edition.edition_date)}</span>
        <span>Verified Multi-Source Intelligence</span>
        <span>Status: {edition.status}</span>
      </div>

      <h2 className="newspaper-title text-3xl md:text-5xl font-black text-ink dark:text-ink-dark uppercase tracking-tight">
        DAILY COMPLETE EDITION
      </h2>
      <p className="text-sm italic text-stone-600 dark:text-stone-400 mt-1 font-serif">
        Published at {new Date(edition.published_at || edition.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} • Covering India & Global Strategic Affairs
      </p>

      {/* Metrics Bar */}
      <div className="mt-4 flex flex-wrap justify-center items-center gap-4 text-xs font-sans font-semibold">
        <span className="bg-stone-200 dark:bg-stone-800 px-2.5 py-1 rounded">
          {edition.total_articles} Articles
        </span>
        <span className="bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300 px-2.5 py-1 rounded border border-red-300">
          ⚡ {edition.critical_count} Critical
        </span>
        <span className="bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 px-2.5 py-1 rounded border border-amber-300">
          ★ {edition.high_count} High Importance
        </span>
        <span className="bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 px-2.5 py-1 rounded border border-blue-300">
          ℹ {edition.moderate_count} Moderate
        </span>
      </div>
    </div>
  );
}
