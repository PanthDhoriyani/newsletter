import type { Metadata } from "next";
import Navbar from "@/components/navbar";
import "@/app/globals.css";

export const metadata: Metadata = {
  title: "The Digital Gazette • Personal AI Morning Newspaper",
  description: "An AI-powered factual digital newspaper covering India and international affairs daily without hallucinations.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-paper-light dark:bg-paper-dark text-ink dark:text-ink-dark">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-6 md:py-8">
          {children}
        </main>
        <footer className="border-t border-stone-300 dark:border-stone-800 py-6 text-center text-xs text-stone-500 font-sans">
          <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-2">
            <span>The Digital Gazette • Automated Daily Factual Publishing</span>
            <span>Rolling 24-Hour Coverage Window • Indian Standard Time (Asia/Kolkata)</span>
          </div>
        </footer>
      </body>
    </html>
  );
}
