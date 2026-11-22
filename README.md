# AI-Powered Personal Digital Newspaper

An autonomous, full-stack, AI-driven personal digital newspaper that researches, synthesizes, verifies, writes, and publishes a professional daily newspaper edition every morning at **08:00 AM IST (Asia/Kolkata)**.

---

## 🌟 Key Architecture & Highlights

1. **Zero Hallucination / Fact-Anchored Architecture:**
   - Articles are generated **strictly from verified primary & wire sources** (NewsData.io, Currents API, GNews API, The Hindu, Economic Times, LiveMint, PIB India, BBC, Reuters).
   - The LLM acts as a senior journalist synthesizing verified excerpts, never inventing quotes, figures, or unverified claims.
   - Cross-source verification requires $\ge 2$ independent outlets before confirming breaking events.

2. **Mandatory Daily Edition Summary:**
   - Every daily paper ends with an exhaustive **7-part Daily Edition Summary** linking back to each published article.
   - Includes *Today's Biggest Headlines*, *India in Focus*, *World in Focus*, *Impact on India*, *Business and Markets*, *Other Important Developments*, and *5-10 Key Takeaways*.

3. **Complete Editorial Structure:**
   - **Part 1:** India (National, Politics, Economy, Corporate, Stock Market, Banking/RBI, Infrastructure, S&T, Health, Sports, Law).
   - **Part 2:** World (International Affairs, Geopolitics, Wars/Security, Global Economy, World Tech).
   - **Part 3:** Global Developments Affecting India (Tariffs, crude prices, Fed interest rates, supply chains).
   - **Part 4:** Trending Stories.
   - **Part 5:** What to Watch Next (Upcoming court dates, RBI meetings, elections, earnings).
   - **Part 6:** Daily Knowledge Corner (3-5 financial, economic, and legal concepts explained simply).
   - **Part 7:** Daily Edition Summary.

4. **Permanent Archive & Reading Tracker:**
   - Editions are published as immutable historical records.
   - Granular reading progress: read individual articles, save for later, and read the summary independently without falsely marking articles as read.
   - Catch-Up mode for readers returning after several missed days.

---

## 🛠️ Tech Stack (Free Tiers Utilized)

- **Backend:** FastAPI, Python 3.11, SQLAlchemy 2.0 (Async), Pydantic v2, APScheduler.
- **AI & Models:**
  - **Google Gemini 1.5 Flash** (Primary Writer & Summarizer — free tier with Search Grounding).
  - **Groq Llama 3.1 70B** (Ultra-fast Classifier & Claim Verifier — free tier).
- **News APIs & Feeds:**
  - NewsData.io (200 credits/day free)
  - Currents API (250 req/day free)
  - GNews API (100 req/day free)
  - 14+ Live High-Integrity RSS Feeds (PIB, RBI, The Hindu, NDTV, ET, LiveMint, BBC, Reuters, Google News)
- **Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide Icons.
- **Database:** SQLite (default zero-config local async) or PostgreSQL via asyncpg.

---

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate # Linux/Mac

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger documentation.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) for the newspaper interface.

### 3. Docker Deployment
```bash
docker-compose up --build
```
