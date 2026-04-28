# Lead-Gen-Bot

An AI-powered B2B lead generation tool that automatically discovers potential business customers, evaluates their fit through a multi-stage AI filtering pipeline, and finds contact information.

## Overview

Traditional B2B prospecting requires hours of manual research — browsing company websites, evaluating fit, hunting for contact details. This tool automates the entire pipeline:

```
Google Maps API  →  Website Scraping  →  AI Round 1 (Quick Filter)
                                              ↓
                                     AI Round 2 (Medium Filter)
                                              ↓
                                     AI Round 3 (Deep Analysis)
                                              ↓
                                     Contact Discovery
                                              ↓
                                     Database (Supabase)
```

**Input:** A list of target industry keywords (e.g., "parking meter manufacturer", "LED lighting manufacturer")

**Output:** A database of qualified leads with company info, contact emails, and AI-generated insights on what they might need

## Features

### Multi-Source Company Discovery
- **Google Maps Places API** as the primary data source — searches across multiple US regions for each industry
- Automatic deduplication by domain
- Blacklist system for already-contacted companies
- Incremental daily search with industry rotation

### Three-Stage AI Filtering Pipeline
Each stage uses progressively more information and stricter criteria:

| Stage | Info Available | Batch Size | Purpose |
|-------|---------------|------------|---------|
| **Round 1** | Company name + 300 chars from homepage | 10 per API call | Quick disqualification of obvious non-fits (service companies, distributors, non-US) |
| **Round 2** | Homepage + /about + /products (1200 chars) | 20 per API call | Medium evaluation — is this a product company? Do they design their own products? |
| **Round 3** | 7 pages, up to 2500 chars | 1 per API call | Deep analysis — specific product needs, sourcing potential, suggested outreach angle |

### Intelligent Contact Discovery
Multi-fallback contact finding with email risk classification:

1. **Hunter.io Domain Search** — find known contacts at the company
2. **Website Email Scraping** — crawl contact/about/team pages for email addresses
3. **Hunter Email Verifier** — verify common email formats (info@, sales@, etc.)
4. **LinkedIn Fallback** — search for relevant personnel with company name matching

### Email Risk Classification
```
safe_personal  →  firstname@company.com     (highest priority)
safe_generic   →  sales@, info@, contact@   (usable)
risky          →  warranty@, techsupport@   (auto-skipped)
```

### AI-Generated Insights
For each qualified lead, the tool generates:
- `what_they_need` — specific components the company likely sources (e.g., "1. Cast iron burner components 2. Stainless steel panels 3. Digital thermostats")
- `suggested_angle` — recommended outreach approach

## Architecture

```
lead-gen-bot/
├── main.py                      # Entry point — two modes: --search-only, --find-contacts
├── config.py                    # All configuration: industries, API settings, blacklists
├── modules/
│   ├── search.py                # Google Maps API integration, website scraping
│   ├── analyzer.py              # Round 1 AI filter (DeepSeek batch analysis)
│   ├── round2_filter.py         # Round 2 AI filter (medium-depth analysis)
│   ├── round3_filter.py         # Round 3 AI filter (deep analysis with insights)
│   ├── contact_finder.py        # Multi-source contact discovery + email classification
│   ├── database.py              # Supabase CRUD operations
│   └── sources/
│       └── google_maps.py       # Google Maps Places API wrapper
├── candidates.json              # Intermediate output between search and contact phases
├── searched_industries.json     # Tracks which industries have been searched this cycle
└── .env                         # API keys (not committed)
```

## Setup

### Prerequisites
- Python 3.10+
- API keys for: Google Maps Places API, DeepSeek, Hunter.io
- Supabase project with a `leads` table

### Installation

```bash
git clone https://github.com/yourusername/lead-gen-bot.git
cd lead-gen-bot
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_google_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
HUNTER_API_KEY=your_hunter_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Database Setup

Create a `leads` table in Supabase with the following schema:

```sql
CREATE TABLE leads (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    industry TEXT,
    company_name TEXT,
    website TEXT,
    contact_name TEXT,
    role TEXT,
    email TEXT,
    confidence INTEGER,
    linkedin_url TEXT,
    status TEXT DEFAULT 'new',
    pain_signal_type TEXT,
    pain_signal_strength INTEGER,
    company_type TEXT,
    ai_reasoning TEXT,
    source_query TEXT,
    domain TEXT,
    phone TEXT,
    what_they_need TEXT,
    suggested_angle TEXT
);

CREATE INDEX idx_leads_domain ON leads(domain);
```

## Usage

### Step 1: Search for companies

```bash
export $(grep -v '^#' .env | xargs)
python main.py --search-only
```

This will:
- Select industries for today's run (rotates through the full list)
- Search Google Maps across multiple US regions
- Run three rounds of AI filtering
- Output qualified candidates to `candidates.json`

### Step 2: Find contacts

```bash
python main.py --find-contacts
```

This will:
- Process candidates from `candidates.json`
- Search for contact information using multiple sources
- Classify emails by risk level
- Save results to Supabase (only records with valid emails)

### Typical Output

```
📊 Round 1: 1308 → 168 (pass rate 13%)
📊 Round 2: 168 → 58 (pass rate 35%)
📊 Round 3: 58 → 42 (pass rate 72%)

📊 FINAL RESULTS
  👤 Named contacts   : 5
  📬 Generic contacts : 33
```

## Configuration

Key settings in `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `DAILY_SEARCH_LIMIT` | 30 | Number of industries to search per run |
| `SEARCH_REGIONS` | 10 US states | Geographic regions to rotate through |
| `MIN_PAIN_SIGNAL_STRENGTH` | 3 | Minimum AI score to pass Round 1 |
| `CONTACTED_DOMAINS` | [] | Domains to skip (already contacted) |
| `APPLICATION_INDUSTRIES` | 75+ entries | Target industry search terms |

## Design Decisions

### Why Google Maps instead of Google Custom Search?
Google Maps returns structured company data (name, address, phone, website) rather than web pages. The data quality is significantly higher — searching "kiosk manufacturer" on Maps returns actual kiosk companies, while Custom Search returns eBay listings, news articles, and directory pages.

### Why three AI rounds instead of one?
A single AI pass with full information would be too expensive (1300+ API calls with 2500 chars each). The three-round funnel progressively increases information depth while decreasing candidate volume — Round 1 processes 1300 companies with minimal info, Round 3 only processes ~50 companies with deep analysis.

### Why DeepSeek instead of GPT-4 or Claude?
Cost efficiency. DeepSeek's API is significantly cheaper while providing sufficient quality for the structured classification tasks in this pipeline. The three-round architecture compensates for any quality gap by giving the model multiple chances to evaluate each company.

### Why not use Apollo.io or ZoomInfo?
This tool is designed as a free/low-cost alternative. Apollo's People Search API requires a paid plan ($49+/month), while this tool uses only free-tier APIs (Google Maps $200/month free credit, Hunter.io 25 free searches/month, DeepSeek near-zero cost).

## Limitations

- **Contact discovery rate:** ~60-70% of qualified companies have discoverable email addresses. Small companies often have no public email presence.
- **Personal email rate:** Only ~10% of discovered emails are personal (firstname@domain). Most are generic (info@, sales@).
- **Search volume:** Limited by Google Maps API quotas and DeepSeek rate limits. A full run of 30 industries takes 40-60 minutes.
- **AI accuracy:** The three-round filter achieves ~53% final accuracy (validated by manual review). Some false positives still pass through.

## Future Improvements

- [ ] Reverse search — start from people with relevant job titles, then evaluate their companies
- [ ] Apollo.io integration for higher personal email discovery rates
- [ ] Web UI dashboard for reviewing and managing leads
- [ ] Automated email composition based on AI-generated insights
- [ ] Scheduled daily runs with email notifications for new leads