# Project Proposal: AI-Powered B2B Lead Generation Tool

## What I'm Building

An AI-powered lead generation tool that helps B2B companies automatically discover potential customers, evaluate their fit through multi-stage AI filtering, and find contact information — turning what normally takes hours of manual research into an automated pipeline.

## Why I Chose This

Manual B2B prospecting is one of the most time-consuming parts of running a small business. A salesperson might spend 5-6 hours researching companies, visiting websites, and hunting for contact details just to build a list of 20 prospects. Most of those won't even be a good fit. I wanted to build a tool that automates this entire workflow using AI, APIs, and smart filtering — reducing hours of work to minutes while improving the quality of results.

This project also sits at the intersection of several technical areas I wanted to explore: API integration, AI/LLM-based analysis, web scraping, concurrent programming, and database management.

## Core Features

- **Automated company discovery** using Google Maps Places API across multiple industries and geographic regions
- **Three-stage AI filtering pipeline** using LLM (DeepSeek API) with progressively deeper analysis at each stage — from quick batch screening to individual deep-dive evaluation
- **Automated contact finding** through multiple fallback sources: Hunter.io API → website email scraping → email format verification → LinkedIn search
- **Email risk classification** that categorizes discovered emails by type (personal, generic, risky) and prioritizes accordingly
- **Incremental daily search** with industry rotation, deduplication, and contacted-company blacklisting
- **Structured output** with AI-generated insights on what each company might need and suggested outreach angles
- **Supabase database** for persistent storage with domain-level deduplication

## What I Don't Know Yet

- How to optimize the balance between AI filtering strictness and lead volume (too strict = too few results, too loose = low quality)
- How to improve personal email discovery rates for small companies not covered by major data providers
- Whether the three-round filtering architecture is optimal or if a different number of passes would work better
- How to handle API rate limits gracefully across multiple concurrent services

## Technical Stack

- **Language:** Python 3.10+
- **APIs:** Google Maps Places API, DeepSeek API (OpenAI-compatible), Hunter.io, Supabase
- **Libraries:** requests, BeautifulSoup4, concurrent.futures, tldextract, supabase-py
- **Database:** Supabase (PostgreSQL)
- **Architecture:** Modular pipeline with separate modules for search, analysis, contact finding, filtering, and database operations