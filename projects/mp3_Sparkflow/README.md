# SparkFlow

**AI-powered startup opportunity matching for first-time entrepreneurs.**

Live: [sparkflow.ventures](https://sparkflow.ventures)

---

## What is SparkFlow?

SparkFlow helps people who want to start a business but don't know what to build. It combines a scenario-based founder assessment with a database of 1,200+ real startup opportunities, then uses a three-layer AI matching algorithm to find the best fit for each user's skills, resources, and preferences.

Every opportunity in the database comes from real discussions on Reddit, Quora, Indie Hackers, and other entrepreneurial communities — not AI-generated ideas.

## How It Works

```
Questionnaire (10 questions, 3 pages)
        ↓
Rule-based tag mapping (milliseconds)
        ↓
AI Founder Persona (6 archetypes, 3 scores)
        ↓
Registration
        ↓
3-layer matching: Tags → Hard filter → AI scoring
        ↓
Personalized opportunity list with action plans
```

### Matching Pipeline

1. **Tag Mapping:** Questionnaire answers → structured user tags (skills, industries, resources, constraints, preferences)
2. **Hard Filtering:** Code-level elimination of opportunities that don't fit (budget, time, skill thresholds)
3. **AI Scoring:** DeepSeek scores remaining candidates across 5 dimensions:
   - Skill match (30%)
   - Industry match (25%)
   - Resource match (20%)
   - Risk tolerance (15%)
   - Interest alignment (10%)

### Opportunity Quality Scoring

Every opportunity has an independent quality score based on real market data:
- **Demand strength:** Search result volume and platform distribution (Tavily)
- **Market size:** Breadth of discussion across platforms (Tavily)
- **Competition level:** Number of existing solutions found (Tavily)
- **Monetization potential:** Pain intensity and willingness to pay signals (DeepSeek)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 16 (App Router) + React + TypeScript |
| Styling | Tailwind CSS + Framer Motion |
| AI | DeepSeek API |
| Search / Data | Tavily API |
| Database & Auth | Supabase (PostgreSQL + Auth) |
| Email | Resend |
| Deployment | Vercel |
| Domain | Namecheap (sparkflow.ventures) |

## Project Structure

```
app/
  page.tsx                    — Main SPA (all steps + dashboard)
  globals.css                 — Theme, animations (marquee, dot-pulse, scroll)
  layout.tsx                  — Root layout
  about/page.tsx              — About / How It Works (bilingual)
  privacy/page.tsx            — Privacy Policy (bilingual)
  handbook/
    page.tsx                  — 12-chapter startup handbook (copy-protected)
    data.ts                   — Handbook content
  api/
    generate/route.ts         — Persona generation (DeepSeek SSE)
    opportunities/route.ts    — Hard filter + AI scoring
    opportunity-detail/       — Personalized detail (China market adapted)
    competitor-analysis/      — Competitor search (domestic/international)
    generate-email/           — Cold outreach email generation
    validate-idea/            — Idea validation (5-dimension scoring)
    persona-compare/          — AI comparison of two assessments
    personas/                 — Persona CRUD
    favorites/                — Favorites CRUD
    match-history/            — Match history CRUD
    auth/register/            — Registration with referral code
    landing-stats/            — Real-time stats for landing page
    analyze-file/             — Resume parsing
lib/
  supabase.ts                 — Supabase client
scripts/
  batch-collect-600.mjs       — Batch opportunity collection
  upgrade-scoring.mjs         — Tavily+DeepSeek scoring upgrade
  audit-excellence.mjs        — Profitability audit (4-dimension)
  batch-tag-opportunities.mjs — Structured field tagging
  daily-collect.mjs           — Daily auto-collection
  search-queries-pool.json    — 880+ search queries across 18 industries
public/
  logo.png                    — Gold flame logo
  characters/                 — 6 archetype character PNGs
```

## Database

### opportunities (1,200+ rows)

Core fields: title/title_zh, pain_point/pain_point_zh, summary/summary_zh, domain, quotes (real user quotes with URLs), builder_min/seller_min/operator_min, capital_tier, time_tier.

9 structured tag fields: specific_industry, required_skills, ideal_background, resource_advantage, difficulty, solo_friendly, revenue_speed, revenue_model, target_customer.

Quality scoring: opportunity_score, pain_intensity, demand_breadth, competition_gap, monetization_clarity, search_result_count, platform_count, competitor_count, scoring_method (all entries are tavily_full).

### Other Tables

- **user_profiles:** email, referral_code (SF-XXXX), referral_count, handbook_unlocked
- **user_personas:** persona JSON (archetype, scores, text), timestamps for growth tracking
- **user_favorites:** user → opportunity bookmarks
- **user_match_history:** full match results per session

## Features

- Bilingual (Chinese / English) with localStorage-based language sync
- Dark theme UI (Apple-inspired, #0a0a0a + gold #C5A044)
- 6 founder archetypes: Builder, Seller, Operator, Integrator, Explorer, Specialist
- Triangle radar chart + character illustration + strength/weakness analysis
- Shareable persona card (html2canvas)
- Opportunity quality displayed with 4-dimension breakdown and real data counts
- Jargon auto-translation (UGC, FBA, DTC, SaaS → plain Chinese)
- Idea validation with 5-dimension scoring + market trend analysis
- 12-chapter startup handbook with copy protection (selection disabled, keyboard shortcuts blocked, email watermark)
- Referral system: share code → referrer unlocks handbook (one-way incentive)
- Growth timeline for multi-assessment tracking
- Profile comparison with AI-powered insights
- Dashboard for logged-in users (6 feature cards + stats overview)

## Data Quality Pipeline

The opportunity database went through 7 stages:

1. Initial Tavily collection from 5 platforms
2. Empty-quote removal (92 deleted)
3. Generic/duplicate analysis via DeepSeek (150 deleted)
4. Batch tagging of 9 structured fields
5. Profitability audit — A/B/C/D grading, C+D deleted (217 deleted)
6. Full Tavily+DeepSeek scoring upgrade for all remaining entries
7. Second collection round (600 new entries with full pipeline)

## Live Demo

Visit [sparkflow.ventures](https://sparkflow.ventures) to try it out.

## Author

**Tianze Xiong** — Babson College, Business Administration (Operations Management), Class of 2027.

Contact: [Contact Form](https://forms.gle/J6BWjSGSWtCC6e249)

## License

Private — All rights reserved.