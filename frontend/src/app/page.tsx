"use client";

import Link from "next/link";
import { useDashboard, triggerManualGeneration, getGenerationStatus } from "@/lib/api";
import BreakingNewsBanner from "@/components/dashboard/BreakingNewsBanner";
import ArticleCard from "@/components/newspaper/ArticleCard";
import SectionHeader from "@/components/newspaper/SectionHeader";
import { ArticleCardSkeleton } from "@/components/ui/skeleton";
import { formatDate } from "@/lib/utils";
import { Newspaper, Flame, RefreshCw, Calendar, ArrowRight, ShieldCheck, CheckCircle2, AlertCircle } from "lucide-react";
import { useState, useEffect, useRef } from "react";

export default function FrontPage() {
  const { data, error, isLoading, mutate } = useDashboard();
  const [generating, setGenerating] = useState(false);
  const [generateMsg, setGenerateMsg] = useState<string | null>(null);
  const [isError, setIsError] = useState(false);
  const pollRef = useRef<NodeJS.Timeout | null>(null);

  // Sync state if server reports active generation on initial load
  useEffect(() => {
    if (data?.is_generating && !generating) {
      setGenerating(true);
      setGenerateMsg("AI agents are currently researching and publishing today's edition...");
      startPolling();
    }
  }, [data?.is_generating]);

  // Clean up timer on unmount
  useEffect(() => {
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, []);

  const startPolling = () => {
    if (pollRef.current) clearInterval(pollRef.current);

    pollRef.current = setInterval(async () => {
      try {
        const status = await getGenerationStatus();

        if (status.is_generating) {
          // Live status message reported directly by the agent pipeline in real time
          if (status.last_status && status.last_status !== "IDLE") {
            setGenerateMsg(status.last_status);
          } else {
            setGenerateMsg("AI agents actively researching and compiling today's edition...");
          }
        } else {
          // Generation has finished or stopped
          if (pollRef.current) clearInterval(pollRef.current);
          pollRef.current = null;
          setGenerating(false);

          if (status.last_status === "SUCCESS") {
            setIsError(false);
            setGenerateMsg("Today's newspaper published successfully!");
            mutate();
          } else if (status.last_status && status.last_status.startsWith("FAILED")) {
            setIsError(true);
            setGenerateMsg(`Publication stopped: ${status.last_status}`);
          } else {
            setIsError(false);
            setGenerateMsg(null);
            mutate();
          }
        }
      } catch (err) {
        console.warn("Polling status error:", err);
      }
    }, 2000);
  };

  const handleGenerate = async () => {
    setGenerating(true);
    setIsError(false);
    setGenerateMsg("Initiating multi-agent news pipeline...");

    try {
      const res = await triggerManualGeneration();
      if (!res.ok) {
        setGenerating(false);
        setIsError(true);
        setGenerateMsg(`Server error ${res.status}: Failed to initiate generation.`);
        return;
      }
      setGenerateMsg("Pipeline running. AI agents are collecting and writing articles...");
      startPolling();
    } catch (err: any) {
      console.error("Failed to trigger generation:", err);
      setGenerating(false);
      setIsError(true);
      setGenerateMsg("Connection failed. Please check backend status.");
    }
  };

  return (
    <div className="space-y-8">
      {/* Breaking News Ribbon if active */}
      <BreakingNewsBanner news={data?.breaking_news} />

      {/* Front Page Headline Banner */}
      <div className="border-b-2 border-stone-800 dark:border-stone-200 pb-6 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <span className="text-xs uppercase font-sans font-bold tracking-widest text-accent">
            Volume I • Morning Edition
          </span>
          <h1 className="newspaper-title text-4xl md:text-6xl font-black text-ink dark:text-ink-dark uppercase tracking-tight mt-1">
            FRONT PAGE INTELLIGENCE
          </h1>
          <p className="text-stone-600 dark:text-stone-400 text-sm font-serif italic mt-1">
            Researched and synthesized by multi-agent factual pipelines • Verified against official & wire dispatches
          </p>
        </div>

        <div className="flex flex-col items-end gap-2">
          <button
            onClick={handleGenerate}
            disabled={generating}
            className={`px-4 py-2.5 rounded text-xs font-sans font-bold uppercase tracking-wider flex items-center gap-2 transition-all shadow-sm ${
              generating
                ? "bg-amber-600 text-white cursor-wait opacity-90 animate-pulse"
                : "bg-stone-900 dark:bg-stone-100 text-white dark:text-stone-900 hover:bg-stone-800"
            }`}
          >
            <RefreshCw className={`w-4 h-4 ${generating ? "animate-spin" : ""}`} />
            {generating ? "Publishing News in Progress..." : "Trigger Live Publish"}
          </button>
          {generateMsg && (
            <div className={`flex items-center gap-1.5 text-xs font-sans px-2.5 py-1 rounded border max-w-md text-right ${
              isError
                ? "bg-red-50 text-red-700 border-red-200 dark:bg-red-950/40 dark:text-red-300 dark:border-red-800"
                : generating
                ? "bg-amber-50 text-amber-800 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800"
                : "bg-emerald-50 text-emerald-800 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800"
            }`}>
              {isError ? (
                <AlertCircle className="w-3.5 h-3.5 text-red-600 dark:text-red-400 shrink-0" />
              ) : generating ? (
                <RefreshCw className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400 animate-spin shrink-0" />
              ) : (
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400 shrink-0" />
              )}
              <span>{generateMsg}</span>
            </div>
          )}
        </div>
      </div>

      {/* Today's Edition Card Hero */}
      {data?.today_edition && (
        <div className="bg-paper dark:bg-stone-900/60 p-6 rounded border border-stone-300 dark:border-stone-700 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 shadow-sm">
          <div>
            <span className="text-xs font-sans font-bold uppercase tracking-wider text-emerald-700 dark:text-emerald-400 flex items-center gap-1.5 mb-1">
              <ShieldCheck className="w-4 h-4" />
              Published Daily Edition • {formatDate(data.today_edition.edition_date)}
            </span>
            <h2 className="newspaper-title text-2xl md:text-3xl font-extrabold">
              Today&apos;s Complete Newspaper is Ready
            </h2>
            <div className="mt-2 flex flex-wrap gap-3 text-xs font-sans">
              <span className="bg-stone-200 dark:bg-stone-800 px-2 py-0.5 rounded font-semibold">
                {data.today_edition.total_articles} Verified Articles
              </span>
              <span className="text-red-700 dark:text-red-400 font-bold">
                ⚡ {data.today_edition.critical_count} Critical
              </span>
              <span className="text-amber-700 dark:text-amber-400 font-bold">
                ★ {data.today_edition.high_count} High Importance
              </span>
            </div>
          </div>

          <div className="flex gap-3">
            <Link
              href="/today"
              className="px-5 py-2.5 bg-accent text-white font-sans font-bold text-xs uppercase tracking-wider rounded hover:bg-accent-hover transition-colors shadow flex items-center gap-2"
            >
              <Newspaper className="w-4 h-4" />
              Open Complete Edition
            </Link>
          </div>
        </div>
      )}

      {/* Top Stories Section */}
      <div>
        <SectionHeader title="Top Lead Stories" subtitle="Highest Importance & National Strategic Developments" />
        
        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <ArticleCardSkeleton />
            <ArticleCardSkeleton />
            <ArticleCardSkeleton />
          </div>
        ) : data?.top_stories && data.top_stories.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {data.top_stories.map((story) => (
              <ArticleCard
                key={story.id}
                article={{
                  ...story,
                  newsletter_id: data.today_edition?.id || "",
                  content: story.introduction || "",
                  tags: [],
                  countries: [],
                  sources: []
                }}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-16 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded p-6">
            <Newspaper className="w-12 h-12 text-stone-400 mx-auto mb-3" />
            <h3 className="newspaper-title text-xl font-bold">No Edition Published Yet</h3>
            <p className="text-sm text-stone-500 max-w-md mx-auto mt-1 font-sans">
              Click &apos;Trigger Live Publish&apos; above or allow the autonomous daily scheduler to run at 8:00 AM IST.
            </p>
          </div>
        )}
      </div>

      {/* Fast Links Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-6">
        <Link
          href="/catchup"
          className="p-6 bg-amber-500/10 border border-amber-500/30 rounded hover:border-amber-500 transition-all group"
        >
          <div className="flex items-center gap-3 mb-2 text-amber-700 dark:text-amber-400">
            <Flame className="w-5 h-5" />
            <h3 className="newspaper-title text-lg font-bold">Catch-Up Mode</h3>
          </div>
          <p className="text-xs text-stone-600 dark:text-stone-300 font-sans">
            Missed several days? Review rapid synthesized summaries and prioritized unread critical stories.
          </p>
          <span className="text-xs text-accent font-sans font-bold flex items-center gap-1 mt-4 group-hover:underline">
            Catch Up Now <ArrowRight className="w-3.5 h-3.5" />
          </span>
        </Link>

        <Link
          href="/today"
          className="p-6 bg-accent/10 border border-accent/30 rounded hover:border-accent transition-all group"
        >
          <div className="flex items-center gap-3 mb-2 text-accent">
            <Newspaper className="w-5 h-5" />
            <h3 className="newspaper-title text-lg font-bold">Daily Edition Summary</h3>
          </div>
          <p className="text-xs text-stone-600 dark:text-stone-300 font-sans">
            Access the mandatory 7-part Daily Summary with key takeaways at the end of today&apos;s paper.
          </p>
          <span className="text-xs text-accent font-sans font-bold flex items-center gap-1 mt-4 group-hover:underline">
            Read Summary <ArrowRight className="w-3.5 h-3.5" />
          </span>
        </Link>

        <Link
          href="/archive"
          className="p-6 bg-stone-500/10 border border-stone-500/30 rounded hover:border-stone-500 transition-all group"
        >
          <div className="flex items-center gap-3 mb-2 text-stone-700 dark:text-stone-300">
            <Calendar className="w-5 h-5" />
            <h3 className="newspaper-title text-lg font-bold">Permanent Archive</h3>
          </div>
          <p className="text-xs text-stone-600 dark:text-stone-300 font-sans">
            Browse through all historical editions with permanent immutability and date-based calendar tracking.
          </p>
          <span className="text-xs text-accent font-sans font-bold flex items-center gap-1 mt-4 group-hover:underline">
            View Calendar <ArrowRight className="w-3.5 h-3.5" />
          </span>
        </Link>
      </div>
    </div>
  );
}
