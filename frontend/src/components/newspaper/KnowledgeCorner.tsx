import { KnowledgeConcept } from "@/lib/types";
import { BookOpen, HelpCircle } from "lucide-react";

export default function KnowledgeCorner({ concepts }: { concepts?: KnowledgeConcept[] }) {
  if (!concepts || concepts.length === 0) return null;

  return (
    <section className="my-12 p-6 md:p-8 bg-paper dark:bg-stone-900 border border-stone-300 dark:border-stone-700 rounded-sm shadow-sm">
      <div className="flex items-center gap-3 mb-6 border-b border-stone-200 dark:border-stone-800 pb-3">
        <BookOpen className="w-6 h-6 text-accent" />
        <div>
          <h2 className="newspaper-title text-2xl font-black uppercase text-ink dark:text-ink-dark">
            DAILY KNOWLEDGE CORNER
          </h2>
          <p className="text-xs text-stone-500 font-sans uppercase tracking-widest">
            3 to 5 Concepts, Economic Principles & Institutional Terms Explained From Today&apos;s News
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {concepts.map((c, i) => (
          <div key={i} className="bg-white dark:bg-stone-800/80 p-5 rounded border border-stone-200 dark:border-stone-700 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 mb-2 text-accent">
                <HelpCircle className="w-4 h-4 shrink-0" />
                <h3 className="font-bold text-base font-sans tracking-tight">{c.term}</h3>
              </div>
              <p className="text-xs text-stone-700 dark:text-stone-300 font-body leading-relaxed mt-2">
                {c.simple_explanation}
              </p>
            </div>
            {c.why_relevant_today && (
              <div className="mt-4 pt-3 border-t border-stone-100 dark:border-stone-700 text-[11px] text-stone-500 font-sans italic">
                <span className="font-semibold text-accent not-italic">Connection: </span>
                {c.why_relevant_today}
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
