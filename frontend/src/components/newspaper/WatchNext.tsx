import { WatchNextItem } from "@/lib/types";
import { Eye, Calendar, ArrowRight } from "lucide-react";

export default function WatchNext({ items }: { items?: WatchNextItem[] }) {
  if (!items || items.length === 0) return null;

  return (
    <section className="my-12 p-6 md:p-8 bg-stone-900 text-stone-100 rounded-sm shadow-md">
      <div className="flex items-center gap-3 mb-6 border-b border-stone-700 pb-3">
        <Eye className="w-6 h-6 text-amber-400" />
        <div>
          <h2 className="newspaper-title text-2xl font-black uppercase text-white">
            WHAT TO WATCH NEXT
          </h2>
          <p className="text-xs text-stone-400 font-sans uppercase tracking-widest">
            Upcoming Hearings, Central Bank Meetings, Diplomatic Summits & Policy Milestones
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {items.map((item, i) => (
          <div key={i} className="bg-stone-800/80 p-5 rounded border border-stone-700 flex flex-col justify-between">
            <div>
              <span className="inline-block px-2 py-0.5 text-[10px] uppercase font-sans font-bold tracking-wider bg-amber-400/20 text-amber-300 rounded mb-2">
                {item.category || "Upcoming"}
              </span>
              <h3 className="font-bold text-sm text-stone-100 font-sans leading-snug">{item.event}</h3>
              <p className="text-xs text-stone-300 mt-2 font-body leading-relaxed">{item.why_important}</p>
            </div>
            {item.expected_date && (
              <div className="mt-4 pt-3 border-t border-stone-700 text-xs text-amber-400 font-sans flex items-center gap-1.5 font-semibold">
                <Calendar className="w-3.5 h-3.5" />
                <span>Expected: {item.expected_date}</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
