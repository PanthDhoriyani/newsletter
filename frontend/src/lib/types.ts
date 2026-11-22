export type ImportanceLevel = "CRITICAL" | "HIGH" | "MODERATE";

export interface NewsSource {
  id: string;
  source_name: string;
  source_url: string;
  source_type: string;
  published_at?: string;
  snippet?: string;
}

export interface Article {
  id: string;
  newsletter_id: string;
  headline: string;
  section: string;
  category: string;
  importance: ImportanceLevel;
  introduction?: string;
  content: string;
  background_context?: string;
  key_developments?: string;
  why_it_matters?: string;
  india_impact?: string;
  economic_industry_impact?: string;
  what_happens_next?: string;
  tags: string[];
  countries: string[];
  market_impact?: {
    has_market_impact?: boolean;
    affected_markets?: string[];
  };
  published_at: string;
  is_ongoing_story?: boolean;
  sources: NewsSource[];
  read_status?: "UNREAD" | "READ" | "SAVED_FOR_LATER";
}

export interface KnowledgeConcept {
  term: string;
  simple_explanation: string;
  why_relevant_today: string;
  related_headline?: string;
}

export interface WatchNextItem {
  event: string;
  expected_date: string;
  category: string;
  why_important: string;
}

export interface DailySummary {
  biggest_headlines?: Array<{
    title: string;
    article_id: string;
    importance: string;
    brief_why_it_matters: string;
  }>;
  india_in_focus?: {
    summary_text: string;
    key_developments: Array<{ point: string; article_id: string }>;
  };
  world_in_focus?: {
    summary_text: string;
    key_developments: Array<{ point: string; article_id: string }>;
  };
  impact_on_india?: {
    summary_text: string;
    developments: Array<{
      international_event: string;
      india_implication: string;
      article_id: string;
    }>;
  };
  business_and_markets?: {
    summary_text: string;
    highlights: Array<{ point: string; article_id: string }>;
  };
  other_important?: {
    summary_text: string;
    items: Array<{ category: string; point: string; article_id: string }>;
  };
  key_takeaways?: Array<{
    takeaway: string;
    article_id: string;
    importance: string;
  }>;
}

export interface Newsletter {
  id: string;
  edition_date: string;
  coverage_start: string;
  coverage_end: string;
  published_at?: string;
  status: "PENDING" | "GENERATING" | "PUBLISHED" | "FAILED";
  total_articles: number;
  critical_count: number;
  high_count: number;
  moderate_count: number;
  daily_summary?: DailySummary;
  summary_status: string;
  knowledge_corner?: KnowledgeConcept[];
  what_to_watch_next?: WatchNextItem[];
  is_immutable: boolean;
  created_at: string;
  articles: Article[];
}

export interface BreakingNews {
  id: string;
  headline: string;
  summary: string;
  importance: string;
  published_at: string;
  sources?: any[];
  is_verified?: boolean;
}

export interface DashboardData {
  today_edition?: {
    id: string;
    edition_date: string;
    total_articles: number;
    critical_count: number;
    high_count: number;
    moderate_count: number;
    summary_preview?: any[];
  };
  breaking_news: BreakingNews[];
  top_stories: Array<{
    id: string;
    headline: string;
    section: string;
    category: string;
    importance: ImportanceLevel;
    introduction?: string;
    published_at: string;
  }>;
  reading_progress: {
    total_editions: number;
    read_articles: number;
    saved_count: number;
  };
}
