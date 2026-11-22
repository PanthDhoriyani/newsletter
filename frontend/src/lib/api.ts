import useSWR from "swr";
import { DashboardData, Newsletter, Article, BreakingNews } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "https://newsletter-hpz3.onrender.com";

async function fetcher<T>(url: string): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`);
  if (!res.ok) {
    throw new Error(`API error: ${res.statusText}`);
  }
  return res.json();
}

export function useDashboard() {
  return useSWR<DashboardData>("/api/dashboard/", fetcher, { refreshInterval: 60000 });
}

export function useTodayEdition() {
  return useSWR<Newsletter>("/api/editions/today", fetcher, {
    revalidateOnFocus: false,
    shouldRetryOnError: false
  });
}

export function useEdition(id: string) {
  return useSWR<Newsletter>(id ? `/api/editions/${id}` : null, fetcher);
}

export function useArticle(id: string) {
  return useSWR<Article>(id ? `/api/articles/${id}` : null, fetcher);
}

export function useBreakingNews() {
  return useSWR<BreakingNews[]>("/api/breaking/", fetcher, { refreshInterval: 30000 });
}

export async function markArticleStatus(articleId: string, status: "READ" | "SAVED_FOR_LATER" | "UNREAD") {
  return fetch(`${API_BASE}/api/reading/article/${articleId}/status`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status })
  });
}

export async function markSummaryRead(editionId: string) {
  return fetch(`${API_BASE}/api/reading/edition/${editionId}/summary-read`, {
    method: "POST"
  });
}

export async function triggerManualGeneration() {
  return fetch(`${API_BASE}/api/editions/generate`, {
    method: "POST"
  });
}
