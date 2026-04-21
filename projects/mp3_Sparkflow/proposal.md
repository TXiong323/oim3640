# SparkFlow — AI-Powered Startup Opportunity Matching Platform

## Project Proposal

**Author:** Tianze Xiong  
**Program:** Business Administration (Operations Management), Babson College  
**Expected Graduation:** 2027  
**Live URL:** [https://sparkflow.ventures](https://sparkflow.ventures)  
**Repository:** Private

---

## Executive Summary

SparkFlow is an AI-powered platform that helps first-time entrepreneurs discover startup opportunities tailored to their skills, resources, and preferences. Unlike generic "business idea" lists, SparkFlow combines a scenario-based personality assessment with a curated database of 1,200+ real startup opportunities sourced from online entrepreneurial communities — then uses a three-layer matching algorithm to deliver personalized recommendations with actionable next steps.

The core insight behind SparkFlow is that most aspiring entrepreneurs fail not because of lack of motivation, but because they pick the wrong idea for their specific situation. SparkFlow solves this by treating opportunity selection as a matching problem rather than an inspiration problem.

---

## Problem Statement

Millions of people want to start a business but face a paralyzing first question: **"What should I build?"**

Existing resources fall short:

- **Generic idea lists** (blog posts, YouTube videos) offer no personalization — the same "top 10 side hustle ideas" regardless of who's reading
- **Business courses** teach frameworks but don't help with the initial spark — they assume you already know what you want to do
- **AI chatbots** can brainstorm ideas on demand, but generate untethered suggestions with no market validation or feasibility assessment

The result: aspiring entrepreneurs either pick ideas randomly, copy what's trending, or stay stuck indefinitely.

---

## Solution

SparkFlow addresses this gap through four integrated capabilities:

### 1. Scenario-Based Founder Assessment
A 10-question questionnaire using realistic business scenarios (not abstract sliders) to map users across three dimensions — Builder, Seller, and Operator — and identify their archetype from six founder profiles. The assessment also captures industry knowledge, available resources, budget constraints, time commitment, and business preferences.

### 2. AI-Powered Opportunity Matching
A three-layer matching pipeline:
- **Layer 1 — Rule-Based Tag Mapping:** Questionnaire answers are converted to structured user tags via deterministic rules (millisecond-level, no AI needed)
- **Layer 2 — Hard Filtering:** Code-level filters eliminate opportunities that violate user constraints (e.g., budget too high, requires full-time commitment)
- **Layer 3 — AI Scoring:** DeepSeek LLM scores remaining candidates across five weighted dimensions: skill match (30%), industry match (25%), resource match (20%), risk tolerance (15%), and interest alignment (10%)

### 3. Real-World Opportunity Database
1,200+ startup opportunities sourced from Reddit, Quora, Indie Hackers, Hacker News, and Product Hunt — each backed by real user discussions, pain points, and original post links. Every opportunity is scored on a quality index covering demand strength, market size, competition level, and monetization potential, using both Tavily search data and DeepSeek analysis.

### 4. Personalized Action Plans
For each matched opportunity, the platform generates:
- A step-by-step action plan customized to the user's profile
- Revenue strategy with pricing tiers adapted to the China market (¥9.9 / ¥49 / ¥299)
- Competitor analysis (domestic competitors for Chinese users, international for English users)
- Cold outreach email templates
- Idea validation tool with market trend analysis

---

## Technical Architecture

### Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 16 (App Router) + React + TypeScript |
| Styling | Tailwind CSS + Framer Motion |
| AI / LLM | DeepSeek API (persona generation, matching, analysis, validation) |
| Data Collection | Tavily API (Reddit, Quora, Indie Hackers scraping + competitor search) |
| Database & Auth | Supabase (PostgreSQL + Auth, US West) |
| Email | Resend (custom domain SMTP, bilingual templates) |
| Deployment | Vercel (Hobby plan, custom domain) |
| Domain | Namecheap (sparkflow.ventures) |

### Database Schema

- **opportunities** (1,200+ rows): Title, pain point, summary (bilingual), domain, minimum skill thresholds, capital/time tiers, real user quotes, 9 structured tag fields, quality scores from Tavily+DeepSeek dual analysis
- **user_profiles**: Auth linkage, referral code, handbook unlock status
- **user_personas**: Full persona data (archetype, scores, text) with timestamps for growth tracking
- **user_favorites**: Bookmarked opportunities
- **user_match_history**: Complete match results per session

### Data Quality Pipeline

The opportunity database went through a rigorous multi-stage quality process:

1. **Initial Collection:** Tavily API scraping from 5 platforms across 12+ industries
2. **Empty Quote Removal:** Eliminated entries without real user quotes (92 removed)
3. **Generic/Duplicate Analysis:** DeepSeek-powered review flagged overly generic and duplicate entries (150 removed)
4. **Batch Tagging:** 9 structured fields populated via DeepSeek for all entries
5. **Profitability Audit:** Four-dimension scoring (demand reality, market size, profit margin, payback speed) with A/B/C/D grading — C and D grades deleted (217 removed)
6. **Full Scoring Upgrade:** All entries upgraded to Tavily+DeepSeek dual analysis (tavily_full)
7. **Second Collection Round:** 600 additional high-quality entries collected with the full scoring pipeline

---

## Key Features

### For Users
- Bilingual interface (Chinese / English) with automatic language detection
- Apple-inspired dark theme UI with gold accents
- Founder persona with radar chart, archetype illustration, strengths/weaknesses analysis
- Shareable persona card (html2canvas screenshot)
- Opportunity quality scoring with transparent methodology (4 dimensions displayed)
- Idea validation tool: input any business idea, get a 5-dimension feasibility score + market trend analysis
- 12-chapter startup handbook (unlocked through referral system)
- Growth timeline: track how your founder profile evolves over multiple assessments
- Profile comparison: AI-powered analysis of changes between assessments

### For Growth
- Referral code system (SF-XXXX): share your code → when a friend registers with it, YOU unlock the handbook (one-way incentive to keep the sharing chain going)
- Copy-to-clipboard share message for frictionless word-of-mouth
- Dashboard for logged-in users showing all features at a glance

---

## Market Positioning

**Target Audience:** Chinese-speaking first-time entrepreneurs with zero business experience.

**Language Principle:** All AI-generated content uses plain, jargon-free language. A banned-terms list enforces this at the prompt level (no MBA terminology like MVP, SaaS, B2B, ROI, etc. — or these are auto-translated to plain Chinese on the frontend).

**China Market Adaptation:**
- Pricing tiers in RMB (¥9.9 → ¥49 → ¥299)
- Domestic acquisition channels (Xiaohongshu, Douyin, WeChat)
- Domestic tools (Feishu, Youzan, WeChat Mini Programs)
- Competitor analysis searches for domestic competitors when language is Chinese

---

## Differentiation

| Feature | SparkFlow | Generic AI Chat | Business Idea Lists |
|---------|-----------|----------------|-------------------|
| Personalized to user profile | Yes (3-layer matching) | No | No |
| Real market data backing | Yes (1,200+ sourced entries) | No (hallucination risk) | Rarely |
| Actionable next steps | Yes (personalized) | Generic | Generic |
| Quality scoring | Yes (4-dimension) | No | No |
| Idea validation | Yes (5-dimension) | Partial | No |
| Growth tracking | Yes | No | No |

---

## Development Timeline

| Phase | Period | Deliverables |
|-------|--------|-------------|
| Phase 1 | March 2026 | Core architecture, questionnaire V1, basic matching |
| Phase 2 | Early April 2026 | Scenario questionnaire V2, 3-layer matching, persona system, Supabase integration |
| Phase 3 | Mid April 2026 | Data quality pipeline (4 cleanup rounds), scoring system, 600-entry expansion |
| Phase 4 | Late April 2026 | Dashboard, UI polish, About/Privacy pages, referral system, handbook |
| Phase 5 (Planned) | May 2026 | Google Analytics, mobile responsiveness pass, persona page redesign, daily auto-collection |

---

## Metrics & Current State

- **Live at:** sparkflow.ventures
- **Opportunity database:** 1,200+ entries, all with Tavily+DeepSeek dual quality scoring
- **Industries covered:** 18+ (tech/SaaS, e-commerce, food & beverage, real estate, education, health/fitness, beauty, pets, home services, local services, finance/legal, auto services, agriculture, content creation, wedding/events, and more)
- **Data quality:** Every entry has real user quotes with source URLs, 9 structured tag fields, and a composite quality score

---

## Future Roadmap

- **Persona Evolution Tracking:** Longitudinal analysis of how users grow over time
- **Opportunity Kanban:** Drag-and-drop board to manage opportunities from "exploring" to "launched"
- **Pitch Deck Generator:** Auto-generate a basic pitch deck based on selected opportunity + user profile
- **Startup Cost Estimator:** Break down expected costs for any opportunity
- **Daily Auto-Collection:** Vercel Cron job to add 3-15 new opportunities per day automatically
- **Behavioral Feedback Loop:** Use favorites/skips data to improve matching recommendations

---

## Contact

For questions or demo access, please fill out the [contact form](https://forms.gle/J6BWjSGSWtCC6e249).