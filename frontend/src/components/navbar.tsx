"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Newspaper, Calendar, Search, BookmarkCheck, Clock, Flame } from "lucide-react";
import { format } from "date-fns";

export default function Navbar() {
  const pathname = usePathname();
  const todayFormatted = format(new Date(), "EEEE, MMMM d, yyyy");

  const navLinks = [
    { href: "/", label: "Front Page", icon: Newspaper },
    { href: "/today", label: "Today's Edition", icon: Clock },
    { href: "/india", label: "India", icon: null },
    { href: "/world", label: "World", icon: null },
    { href: "/business", label: "Economy & Markets", icon: null },
    { href: "/catchup", label: "Catch-Up Mode", icon: Flame },
    { href: "/archive", label: "Archive", icon: Calendar },
    { href: "/saved", label: "Saved", icon: BookmarkCheck },
    { href: "/search", label: "Search", icon: Search },
  ];

  return (
    <header className="border-b border-stone-300 dark:border-stone-800 bg-paper-light dark:bg-paper-dark sticky top-0 z-50">
      {/* Top Banner Bar */}
      <div className="border-b border-stone-200 dark:border-stone-800/60 py-1.5 px-4 text-xs flex justify-between items-center text-stone-600 dark:text-stone-400 max-w-7xl mx-auto">
        <span>{todayFormatted} • Indian Standard Time (Asia/Kolkata)</span>
        <div className="flex items-center gap-4">
          <span className="font-medium text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
            Daily AI News Engine Active
          </span>
          <span>Rolling 24h Window</span>
        </div>
      </div>

      {/* Masthead */}
      <div className="max-w-7xl mx-auto px-4 py-5 text-center">
        <Link href="/" className="inline-block">
          <h1 className="newspaper-title text-4xl md:text-6xl font-black tracking-tight text-ink dark:text-ink-dark">
            THE DIGITAL GAZETTE
          </h1>
          <p className="text-xs uppercase tracking-widest mt-1 text-stone-500 dark:text-stone-400 font-sans">
            AI-Powered Personal Morning Newspaper • Zero Hallucination Factual Intelligence
          </p>
        </Link>
      </div>

      {/* Navigation Bar */}
      <nav className="border-t border-b border-stone-300 dark:border-stone-700/80 bg-paper dark:bg-stone-900/40">
        <div className="max-w-7xl mx-auto px-4 flex items-center justify-center gap-1 md:gap-6 overflow-x-auto py-2 text-xs md:text-sm font-sans font-semibold uppercase tracking-wider">
          {navLinks.map((link) => {
            const isActive = pathname === link.href;
            const Icon = link.icon;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`px-3 py-1 rounded transition-colors whitespace-nowrap flex items-center gap-1.5 ${
                  isActive
                    ? "bg-accent text-white dark:bg-accent-hover"
                    : "text-stone-700 dark:text-stone-300 hover:text-accent dark:hover:text-white"
                }`}
              >
                {Icon && <Icon className="w-3.5 h-3.5" />}
                {link.label}
              </Link>
            );
          })}
        </div>
      </nav>
    </header>
  );
}
