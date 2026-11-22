# Project: AI-Powered Personal Digital Newspaper

## 1. Project Vision

Build a full-stack, AI-powered Personal Digital Newspaper that automatically researches, generates, publishes, and archives a comprehensive digital newspaper every day.

The primary objective is to help me stay informed about everything important happening in India and around the world, understand why those events matter, and continuously improve my general knowledge, financial awareness, economic understanding, and knowledge of international affairs.

This must feel like reading a professional digital newspaper, not a simple news summarisation application or a generic AI chatbot.

The newspaper should contain detailed, well-structured, informative articles written in professional newspaper style, with appropriate headlines, subheadings, background information, factual explanations, analysis, and references.

**An essential requirement:** Every daily edition must end with a comprehensive but concise **Daily Edition Summary** that brings together the most important developments covered throughout that particular newspaper. A reader should be able to read this final section and understand the major events of the day without having to revisit every article.

The system must operate automatically every day, maintain a permanent archive of all editions, and track which editions and individual articles I have read or missed.

The final objective is a fully working, deployable digital newspaper application.

---

## 2. Core Requirements

### A. Comprehensive Daily News Coverage

The newspaper must cover important developments from:

- India
- Asia
- Europe
- North America
- South America
- Middle East
- Africa
- Other significant international regions.

India should receive priority in coverage, but major global developments must never be ignored.

The system must cover:

1. All very important developments from the coverage period.
2. Moderately important developments worth knowing.
3. Major trending stories in India and globally.
4. International developments that directly or indirectly affect India.
5. Important developments across all sectors, not just politics and business.

Never impose an arbitrary fixed number of articles per category. Coverage should depend on the actual importance and volume of news during the period.

Do not omit an important story simply to keep the newspaper short.

The objective is comprehensive awareness, not generating a predetermined number of articles.

### B. Newspaper Sections and Categories

Use flexible categories depending on the developments of the day.

Suggested newspaper structure:

**PART 1: INDIA**

1. National News
2. Politics and Government
3. Economy and Finance
4. Business and Corporate News
5. Indian Stock Market
6. Banking, RBI and Financial Regulations
7. Infrastructure and Development
8. Education and Employment
9. Science and Technology
10. Environment and Climate
11. Health
12. Sports
13. Law, Courts and Judiciary
14. Regional and Other Important News

**PART 2: WORLD**

1. International Affairs
2. Geopolitics and Diplomacy
3. Wars, Conflicts and Security
4. Global Economy
5. Global Financial Markets
6. International Business and Trade
7. Global Technology and AI
8. Science and Space
9. Environment and Climate
10. International Sports
11. Other Major Global Developments

**PART 3: GLOBAL DEVELOPMENTS AFFECTING INDIA**

Create a dedicated section explaining international developments that could influence India.

Examples:

- US tariffs and their effect on Indian exports.
- Crude oil price movements and their impact on India's import bill.
- US Federal Reserve decisions and their influence on Indian markets.
- Geopolitical conflicts affecting Indian trade routes.
- International technology restrictions affecting Indian companies.
- Changes in global demand affecting Indian industries.
- Changes in global interest rates and their impact on Indian capital flows.
- International supply-chain disruptions affecting Indian businesses.

Explain both direct and indirect consequences.

**PART 4: IMPORTANT TRENDING STORIES**

Include significant trending events that deserve attention even if they do not fit into the existing sections.

Trending does not automatically mean important. Evaluate actual significance before including a story.

**PART 5: WHAT TO WATCH NEXT**

Include upcoming:

- Government announcements.
- RBI and Federal Reserve decisions.
- Important court hearings and judgments.
- Elections and diplomatic meetings.
- Corporate earnings and economic releases.
- Important sporting events.
- Ongoing geopolitical developments.
- Major policy decisions and international negotiations.

Include dates and expected timelines wherever verified.

**PART 6: DAILY KNOWLEDGE CORNER**

Include 3–5 useful concepts, terms, institutions, economic principles, or other subjects that can be learned from the day's news.

Explain concepts in simple but informative language.

Examples:

- What is a sovereign bond?
- How does quantitative tightening work?
- What is a trade deficit?
- What is OPEC?
- What is a current account deficit?
- How do tariffs affect international trade?

Prefer concepts connected to the day's news so the reader learns the underlying principles behind real-world developments.

Avoid repeating basic concepts unnecessarily.

**PART 7: DAILY EDITION SUMMARY**

This is a mandatory section and must appear at the very end of every daily newspaper.

Its purpose is to provide a consolidated overview of the important news covered throughout the entire edition.

It must be generated only after all the edition's articles have been researched, verified, written, and finalised.

Include the following subsections:

1. **Today's Biggest Headlines**
   - Highlight the most important developments from India and around the world.
   - Include the most significant political, economic, geopolitical, business, scientific, technological, and other developments.
   - Give priority to Critical and High importance stories.

2. **India in Focus**
   - Summarise the most important national developments.
   - Include major political, government, economic, business, financial, infrastructure, and social developments.

3. **World in Focus**
   - Summarise the most significant international events.
   - Include major geopolitical, diplomatic, military, economic, and international developments.

4. **Impact on India**
   - Highlight international developments that could directly or indirectly affect India.
   - Explain the most relevant implications for Indian trade, economy, markets, industries, energy, diplomacy, and national interests.

5. **Business and Markets**
   - Summarise the important corporate announcements, stock-market movements, economic indicators, banking developments, and financial news covered in the edition.
   - Distinguish actual market movements from possible future consequences.

6. **Other Important Developments**
   - Highlight important stories from technology, AI, science, space, health, education, environment, sports, and other sectors that deserve attention.

7. **Key Takeaways**
   - Provide approximately 5–10 of the most important things a reader should remember from the entire edition.
   - These should capture the main developments and their significance, not merely repeat headlines.
   - Include important facts, decisions, trends, consequences, or changes that help the reader understand what happened that day.

**Daily Edition Summary writing requirements:**

- Keep it concise but informative, ideally readable in approximately 3–5 minutes.
- Cover the entire newspaper, not just the first few headlines.
- Do not give equal importance to every article. Prioritise developments based on actual significance.
- Do not introduce new, unverified news or information that was not covered in the edition.
- Do not simply copy the introduction of every article.
- Consolidate related stories where appropriate.
- Explain why the day's developments matter.
- Provide links to the corresponding full articles so the reader can explore further.
- Use simple, clear English.
- Avoid unnecessary repetition.
- Preserve important figures, dates, and facts where they help the reader understand the developments.

The summary should function as a final review of the complete newspaper.

**Important generation rule:** The Daily Edition Summary must be generated after the full article collection is finalised. It must be based on the exact articles included in that edition. Store it as part of the same published edition so it always corresponds to the original newspaper.

---

## 3. News Importance Classification

Every article must receive an importance classification.

**CRITICAL**

Major events with substantial national or international consequences.

Examples:

- Major wars or military escalations.
- Financial crises.
- Landmark government decisions.
- Major geopolitical developments.
- Significant economic shocks.
- Major national security developments.
- Events with substantial global consequences.

**HIGH**

Very important developments such as:

- Major corporate announcements.
- Significant policy changes.
- Important scientific breakthroughs.
- Major market developments.
- Important diplomatic agreements.
- Significant regulatory changes.
- Major industry developments.

**MODERATE**

Relevant developments that are worth knowing, including:

- Industry updates.
- Regional news.
- Research developments.
- Relevant corporate announcements.
- Other meaningful developments.

Display importance clearly using visually distinct labels.

Critical and High news should receive more detailed coverage. Moderate news can be relatively concise while remaining informative.

Do not classify news solely by popularity, social-media engagement, or media coverage.

The importance classification should consider:

- Scale of impact.
- Number of people, businesses, or countries affected.
- Economic consequences.
- Political or strategic significance.
- Long-term implications.
- Relevance to India.
- Whether the development changes an existing situation.

The Daily Edition Summary should give appropriate priority to Critical and High importance developments while still acknowledging other meaningful stories.

---

## 4. Article Writing Requirements

This is one of the most important parts of the project.

The generated newspaper must read like a professional newspaper with detailed articles rather than collections of short bullet-point summaries.

Each article should contain the following wherever relevant:

1. **Headline:** Clear and informative headline.
2. **Introduction:** Briefly explain what happened.
3. **Detailed Reporting:** Explain the complete development with relevant facts, figures, dates, people, organisations, countries, and events.
4. **Background and Context:** Explain the historical or recent background necessary to understand the development.
5. **Key Developments:** Explain the most important details and announcements.
6. **Why It Matters:** Explain the significance of the event.
7. **Impact on India:** Explain Indian implications wherever relevant.
8. **Economic or Industry Impact:** Discuss consequences for markets, companies, consumers, trade, or industries where applicable.
9. **What Happens Next:** Explain upcoming developments and uncertainties.
10. **Sources and References:** Provide clickable links to original reporting and official sources.

Do not force irrelevant subsections into every article.

**Writing style:**

- Professional newspaper journalism.
- Detailed but easy-to-understand English.
- Objective, factual, and balanced.
- Explain complicated economic, financial, political, and technological terms.
- Avoid unnecessary jargon.
- Avoid repetitive paragraphs.
- Distinguish facts, allegations, estimates, opinions, and forecasts.
- Never present speculation as confirmed information.
- Provide adequate background for readers who have not followed the story previously.

The objective is that a reader who has not followed the development previously should understand the entire story after reading the article.

Articles should be detailed enough to explain developments properly, but should not contain unnecessary filler.

---

## 5. News Collection and Verification

The system must collect news using multiple independent sources.

Possible sources include:

- Indian and international newspapers.
- Established news organisations.
- Official government websites.
- RBI, SEBI, IMF, World Bank, UN, and other institutional websites.
- Stock exchanges and corporate announcements.
- Official sports organisations.
- Scientific and research institutions.
- RSS feeds.
- News APIs and search engines.

Requirements:

1. Collect multiple reports about major developments.
2. Identify duplicate reports about the same event.
3. Consolidate duplicate reports into one comprehensive article.
4. Verify important claims through independent sources whenever possible.
5. Prefer original announcements and primary sources for official developments.
6. Include publication dates and source links.
7. Never fabricate events, statistics, quotes, or references.
8. Clearly communicate when information is preliminary or developing.
9. Distinguish an article's original publication date from its update date.
10. Maintain source attribution for every generated article.
11. Identify disagreements between sources when they materially affect the story.
12. Use reliable sources and do not treat social-media trends as verified facts.

For significant events, prefer multiple credible independent sources alongside primary sources where available.

Maintain a record of:

- Source name.
- Source URL.
- Publication timestamp.
- Last updated timestamp, if available.
- Date and time the information was collected.
- Claims supported by the source.
- Source type, such as official, primary, or independent reporting.

Every article must have its own source references.

The Daily Edition Summary should link to the relevant published articles rather than introduce unsupported claims.

---

## 6. Daily Automatic Newspaper Generation

The newspaper must be generated every day at a configured time in Indian Standard Time (Asia/Kolkata).

The system must use a rolling coverage window.

Example:

- Edition 1: November 22, 8:00 AM.
- Edition 2: November 23, 8:00 AM.
- Edition 3: November 24, 8:00 AM.

Each edition must cover news published after the previous successful edition's cutoff until the current edition's cutoff.

Do not simply search the last 24 hours independently without considering the previous edition.

Maintain the following:

- Last successful generation timestamp.
- Current generation start timestamp.
- Current generation end timestamp.
- Edition publication timestamp.
- Generation status.

**Reliability requirements:**

1. Use the last successfully published edition's cutoff as the next starting point.
2. Allow a small overlapping collection period to discover late-indexed news.
3. Deduplicate previously collected stories.
4. Detect new developments in ongoing stories.
5. If generation fails, do not advance the successful cutoff.
6. Retry failed generations.
7. If a generation is missed, the next successful run must cover the entire missed period.
8. Save an edition only when the complete generation workflow succeeds.
9. Prevent duplicate editions for the same coverage window.
10. Never silently lose news because of scheduling failures.

**Complete generation workflow:**

The daily generation process should follow this order:

1. Determine the coverage window.
2. Collect news from relevant sources.
3. Research developments across all categories.
4. Verify important claims.
5. Deduplicate related reports.
6. Identify ongoing stories and new developments.
7. Classify news by importance.
8. Analyse relevance and impact on India.
9. Select and organise the final articles.
10. Generate detailed newspaper articles.
11. Validate facts, dates, references, and article quality.
12. Generate the Daily Knowledge Corner.
13. Generate the What to Watch Next section.
14. Generate the Daily Edition Summary from the finalised articles.
15. Validate that the summary accurately represents the entire edition and links to its articles.
16. Save and publish the complete immutable edition.
17. Update the successful generation checkpoint.

Do not publish an incomplete edition if a mandatory section or the final summary has failed to generate.

The system should never silently lose news because of scheduling failures.

---

## 7. Ongoing Story Tracking

Maintain continuity for major ongoing developments.

For example:

Day 1: A country announces new tariffs.

Day 2: Other countries announce retaliatory tariffs.

Day 3: Stock markets react and negotiations begin.

These are related developments.

The newspaper should:

- Identify that the events belong to an ongoing story.
- Explain what has changed since the previous edition.
- Provide the necessary earlier context.
- Avoid reproducing yesterday's complete article.
- Preserve all previous editions unchanged.
- Distinguish new developments from previously reported information.

The Daily Edition Summary should reflect the latest meaningful development rather than repeat the entire history of an ongoing story.

---

## 8. Reading Tracker and Newspaper Archive

Every generated edition must be permanently saved.

Create an archive with a calendar-based or date-based interface.

Each edition should have one of these statuses:

- Unread.
- In Progress.
- Completed.
- Skipped.

Each individual article should have:

- Unread.
- Read.
- Saved for Later.

Important behaviour:

1. Opening a newspaper must not automatically mark all articles as read.
2. Articles should be individually marked as read.
3. Reading progress must be saved persistently.
4. When returning to an older edition, the user must be able to continue where they stopped.
5. Unread articles must remain accessible indefinitely.
6. Reading one article must not mark another article as read.
7. Completed editions must remain available in the archive.
8. The user must be able to manually change reading status.

**Daily Edition Summary reading behaviour:**

- The Daily Edition Summary should be accessible independently within each edition.
- Reading the summary must not automatically mark every full article as read.
- Reading individual articles must not automatically mark the summary as read.
- Track the summary's reading status separately if practical.
- The summary should retain its original content even if newer editions contain further developments.

Dashboard sections:

- Today's Newspaper.
- Continue Reading.
- Unread Editions.
- Unread Articles.
- Saved Articles.
- Completed Editions.
- Historical Archive.

---

## 9. Catch-Up Mode

Create a dedicated catch-up feature.

If the user misses several days, display all missed editions.

Provide:

- Number of missed editions.
- Total unread articles.
- Critical and High importance unread articles.
- Ability to read the complete original editions.
- A prioritised catch-up view.
- Option to mark individual articles as read.
- Access to each missed edition's Daily Edition Summary.

The catch-up view should help the user quickly understand what happened during the missed period.

A useful approach is to show the Daily Edition Summary of each missed edition, followed by the most important unread full articles.

For multiple missed days, optionally provide a consolidated catch-up overview that identifies major developments across the entire missed period and avoids unnecessary repetition.

Never delete or overwrite missed editions.

---

## 10. Additional Features

### A. Weekly Review

Generate a weekly edition containing:

- Most important events of the week.
- Major Indian developments.
- Major global developments.
- Economic and market developments.
- Significant ongoing geopolitical events.
- Important developments affecting India.
- Stories that developed over multiple days.

Also include a **Weekly Summary** at the end of the weekly review.

The weekly summary should consolidate the most important developments of the week, key trends, major consequences, and important things to remember.

It should be based on the actual weekly review content and link to the relevant articles or daily editions.

### B. Breaking News

Provide a mechanism to publish a separate breaking-news update when an extremely important event occurs outside the normal newspaper generation window.

Breaking news should not replace the regular newspaper edition.

The system should:

- Verify breaking developments before publishing.
- Clearly identify preliminary information.
- Include timestamps and sources.
- Update the story as reliable information becomes available.
- Link breaking updates to the relevant ongoing story.
- Avoid sending unnecessary alerts for ordinary developments.

### C. Historical Search

Allow searching previously published news by:

- Keywords.
- Countries.
- Companies.
- People.
- Categories.
- Dates.
- Importance level.

Search results should allow opening the original article and its original edition.

### D. Market Impact

For major financial and geopolitical developments, explain possible impacts on:

- Nifty and Sensex.
- Indian rupee.
- Crude oil.
- Gold.
- Indian exports and imports.
- Relevant Indian industries and companies.

Clearly distinguish actual market reactions from potential future impacts.

Avoid making unsupported market predictions.

### E. Daily Edition Overview

The dashboard should provide a quick preview of the latest edition:

- Edition date.
- Coverage period.
- Number of articles.
- Number of Critical, High, and Moderate articles.
- Main headlines.
- Reading progress.
- Link to the Daily Edition Summary.

This overview should help the user decide what to read next without replacing the full newspaper.

---

## 11. Technology Stack

Use the following preferred architecture:

**Frontend**

- React or Next.js.
- Responsive design.
- Professional digital newspaper interface.
- Modern typography and readable article layouts.

**Backend**

- Python.
- FastAPI.
- REST APIs.

**AI and Agent Architecture**

- LangGraph for multi-agent orchestration.
- Groq or OpenAI LLMs.
- Specialist research agents.
- News verification and classification workflows.
- Newspaper writing agent.
- Daily summary generation agent or a dedicated final generation node.

**News Collection**

- News APIs.
- RSS feeds.
- Web search.
- Official websites and primary sources.

**Database**

- PostgreSQL or Supabase.
- Persistent storage for editions, articles, sources, and reading progress.
- pgvector if semantic search becomes necessary.

**Scheduling**

- Reliable daily scheduler.
- Asia/Kolkata timezone.
- Retry and failure handling.
- Persistent generation checkpoints.

**Deployment**

- Railway or Render.
- Docker.
- Environment-based configuration.

Use appropriate alternatives if a preferred service is unavailable or unsuitable.

---

## 12. Suggested Agent Architecture

Implement a supervisor-based LangGraph workflow.

Suggested agents:

1. India News Research Agent.
2. Global News Research Agent.
3. Economy and Finance Agent.
4. Business and Stock Market Agent.
5. Technology and Science Agent.
6. Sports and Other News Agent.
7. News Verification Agent.
8. Deduplication and Ongoing Story Agent.
9. Importance and India Impact Analysis Agent.
10. Newspaper Writing Agent.
11. Daily Edition Summary Generation Agent.

The supervisor should coordinate agents, combine their findings, and manage the workflow.

**Daily Edition Summary Generation Agent responsibilities:**

- Receive the complete finalised list of published articles.
- Read the final article content and importance classifications.
- Identify the most significant developments across the entire edition.
- Consolidate related stories.
- Generate all required summary subsections.
- Produce approximately 5–10 key takeaways.
- Link each summary item to its corresponding full article.
- Ensure no new or unverified information is introduced.
- Check that important sections and categories are represented.
- Validate that the final summary accurately reflects the published edition.

The summary agent must operate after article selection and finalisation, not during initial research.

Avoid unnecessary agent complexity. Agents should have clearly defined responsibilities and structured outputs.

Where appropriate, the Daily Edition Summary can be implemented as a dedicated LangGraph node rather than a completely independent agent. Choose the architecture that is reliable, maintainable, and cost-effective.

---

## 13. Suggested Database Entities

Create an appropriate relational database schema.

Suggested entities:

- users
- newsletters
- articles
- newsletter_articles
- news_sources
- ongoing_stories
- story_updates
- reading_progress
- saved_articles
- generation_logs
- scheduler_state
- breaking_news
- weekly_reviews

Additional fields or entities can be introduced where necessary.

**Daily edition storage requirements:**

Each newsletter edition should store:

- Edition ID.
- Edition date.
- Coverage window start.
- Coverage window end.
- Publication timestamp.
- Edition status.
- Total article count.
- Importance-level counts.
- Daily Knowledge Corner content.
- What to Watch Next content.
- Daily Edition Summary content.
- Summary generation status.
- Summary generation timestamp.
- Version or publication snapshot information.

The Daily Edition Summary should be associated with its exact edition. It should not be a general summary that changes whenever new news is collected.

You may implement it as:

1. A dedicated summary table associated with the newsletter edition, or
2. A structured summary field within the newsletter edition.

Choose the option that gives the cleanest and most maintainable architecture.

Ensure proper relationships, foreign keys, timestamps, indexes, and database constraints.

Maintain historical editions independently of future article updates.

**Important: Separate research data from published newspaper data.**

The research database can be updated, deduplicated, and enriched as new information arrives.

However, published editions must remain immutable snapshots. This includes:

- Original article content.
- Original source references.
- Importance classifications.
- Daily Edition Summary.
- Publication timestamp.
- Coverage window.

If a major correction is necessary, preserve the original publication and record the correction or revised version transparently.

---

## 14. User Interface Requirements

The interface should resemble a modern professional digital newspaper.

Suggested navigation:

- Home.
- Today's Newspaper.
- India.
- World.
- Business & Finance.
- Technology & Science.
- Sports.
- Global Impact on India.
- Knowledge Corner.
- Daily Edition Summary.
- Unread News.
- Saved Articles.
- Archive.
- Weekly Review.

**Home dashboard:**

Display:

- Today's edition.
- Main headlines.
- Important stories.
- Reading progress.
- Continue Reading.
- Unread editions.
- Saved articles.
- Latest breaking news, if any.
- A preview of the Daily Edition Summary.

**Newspaper reading page:**

- Professional editorial layout.
- Newspaper-style headline hierarchy.
- Clear article categories.
- Importance labels.
- Article publication timestamps.
- Source links.
- Read/unread status.
- Save for Later option.
- Navigation between articles.
- Reading progress indicator.

**Daily Edition Summary interface:**

The final summary should have a clearly identifiable section at the end of each edition.

Provide:

- A prominent heading.
- Separate subsections.
- Concise explanations.
- Links to full articles.
- Key takeaways.
- A clear visual distinction from the detailed articles.

It should be easy to access from the edition's table of contents or navigation without forcing the user to scroll through the entire newspaper.

**Archive interface:**

Allow users to:

- Select a date.
- Open previous editions.
- Continue reading.
- View completed editions.
- Find unread articles.
- Access historical Daily Edition Summaries.

**Design requirements:**

- Professional editorial layout.
- Strong typography and clear reading hierarchy.
- Prominent headlines.
- Readable article widths.
- Category labels.
- Importance labels.
- Source links.
- Publication timestamps.
- Reading progress indicators.
- Search and filtering.
- Responsive desktop and mobile experience.
- Dark and light themes.

Do not make the interface look like a generic AI chatbot dashboard.

The primary user experience should be reading a newspaper.

---

## 15. Important Quality and Reliability Rules

- Never invent news.
- Never fabricate source links.
- Never omit major stories simply to maintain a fixed article count.
- Never confuse publication time with event time.
- Never advance the coverage cutoff after failed generation.
- Never automatically mark an entire edition as read.
- Never lose historical editions.
- Never overwrite an old article without preserving its original published version.
- Avoid duplicate articles.
- Include both Indian and global perspectives.
- Clearly explain developments affecting India.
- Preserve source attribution.
- Handle missing APIs, rate limits, timeouts, and failed agents gracefully.
- Do not present allegations as proven facts.
- Do not present estimates as confirmed figures.
- Do not present forecasts as actual outcomes.
- Do not generate summaries from incomplete or unverified article drafts.
- Never publish the Daily Edition Summary before all articles have been finalised.
- Never introduce information in the Daily Edition Summary that is not supported by the published edition.
- Ensure the Daily Edition Summary represents the entire newspaper rather than only a handful of headlines.
- Preserve the Daily Edition Summary as part of the original immutable edition.
- If summary generation fails, retry it and do not silently publish an incomplete edition.
- Never mark all full articles as read simply because the user reads the Daily Edition Summary.

---

## 16. Development Instructions

Build this project in phases.

**Phase 1: Project Structure, Database and Backend Foundation**

- Set up frontend and backend.
- Configure database.
- Create database models.
- Establish API structure.
- Configure environment variables.
- Set up Docker.

**Phase 2: News Collection and Research Agents**

- Integrate news APIs and RSS feeds.
- Implement web research.
- Develop specialist research agents.
- Store collected information and source metadata.

**Phase 3: Verification, Deduplication and Classification**

- Implement verification.
- Detect duplicate stories.
- Track ongoing developments.
- Classify importance.
- Analyse relevance and impact on India.

**Phase 4: Newspaper Generation**

- Generate detailed articles.
- Organise newspaper sections.
- Generate Daily Knowledge Corner.
- Generate What to Watch Next.
- Validate the final edition content.
- Implement the Daily Edition Summary generation workflow.
- Validate summary completeness and article links.

**Phase 5: Daily Scheduling and Failure Recovery**

- Implement automatic daily scheduling.
- Configure Asia/Kolkata timezone.
- Implement rolling coverage windows.
- Add retries and persistent checkpoints.
- Prevent duplicate editions.
- Ensure incomplete editions are not published.

**Phase 6: Archive and Reading Tracker**

- Store immutable editions.
- Implement article-level reading progress.
- Implement edition-level reading progress.
- Implement saved articles.
- Implement historical archive.

**Phase 7: Frontend Digital Newspaper Interface**

- Build dashboard.
- Build newspaper reading experience.
- Build article pages.
- Build Daily Edition Summary interface.
- Build archive and search.
- Implement responsive design.

**Phase 8: Weekly Reviews, Breaking News and Catch-Up**

- Implement weekly review.
- Generate weekly summary.
- Implement breaking news.
- Implement missed-edition detection.
- Implement prioritised catch-up.
- Provide access to missed editions and their summaries.

**Phase 9: Testing, Deployment and Monitoring**

- Test complete daily generation workflow.
- Test source verification.
- Test duplicate detection.
- Test summary accuracy and completeness.
- Test scheduling and recovery.
- Test reading progress.
- Test archive immutability.
- Deploy the complete application.
- Add monitoring and error logging.

**Before implementation:**

1. Present the complete system architecture.
2. Explain the data flow.
3. Design the database schema.
4. Define the LangGraph workflow.
5. Establish the API structure.
6. Explain the generation and recovery mechanism.
7. Explain how the Daily Edition Summary will be generated and validated.
8. Explain how published editions and summaries will remain immutable.

Then implement each phase step by step.

Write clean, modular, maintainable code.

Provide:

- Complete project directory structure.
- Backend and frontend code.
- Database models and migrations.
- API documentation.
- Environment variable examples.
- Docker configuration.
- Deployment instructions.
- Testing instructions.

Do not use fake news data in production logic.

For initial UI development, mock data is acceptable, but clearly separate it from the real news collection pipeline.

Do not stop at generating a project plan or UI prototype. The final objective is a fully working, deployable digital newspaper application.

---

## 17. Final Product Objective

Deliver a reliable AI-powered digital newspaper that:

1. Automatically researches the important news of every day.
2. Covers India and all significant global developments.
3. Writes comprehensive professional newspaper articles.
4. Explains the background and significance of developments.
5. Connects global developments to India.
6. Provides useful economic, financial, political, technological, and general knowledge.
7. Tracks ongoing stories across multiple days.
8. Generates a comprehensive **Daily Edition Summary at the end of every newspaper**, consolidating the most important news and key takeaways from the entire edition.
9. Preserves every edition and its summary for future reading.
10. Tracks reading progress and helps the user catch up on missed editions.
11. Operates reliably through automatic daily generation and failure recovery.

The experience should make the user feel as though they are opening their own personalised professional newspaper every morning, staying informed about the world and continuously learning.

**The most important distinction:** The application should not merely tell the user what happened. It should help the user understand what happened, why it happened, why it matters, how it affects India and the world, and what they should remember from the day's developments.