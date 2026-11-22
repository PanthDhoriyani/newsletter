import { BreakingNews } from "@/lib/types";
import { AlertCircle } from "lucide-react";

export default function BreakingNewsBanner({ news }: { news?: BreakingNews[] }) {
  if (!news || news.length === 0) return null;

  const latest = news[0];

  return (
    <div className="bg-red-600 text-white py-2 px-4 shadow-sm animate-fadeIn">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-2 text-xs md:text-sm">
        <div className="flex items-center gap-2 font-sans">
          <span className="bg-white text-red-700 text-xs uppercase px-2 py-0.5 rounded font-black tracking-wider flex items-center gap-1 animate-pulse">
            <AlertCircle className="w-3.5 h-3.5" />
            Breaking News
          </span>
          <span className="font-semibold line-clamp-1">{latest.headline}</span>
        </div>
        <p className="text-red-100 text-xs hidden lg:block line-clamp-1 max-w-xl">
          {latest.summary}
        </p>
      </div>
    </div>
  );
}
