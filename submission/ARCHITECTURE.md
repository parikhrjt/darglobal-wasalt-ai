# DarGlobal & Wasalt Agentic Real Estate Copilot
## Senior AI Engineer – Agentic Systems Architectural Whitepaper

---

### Executive Summary
This document outlines the architectural blueprint, data engineering pipeline, agentic reasoning loops, and containerised deployment strategy for the **DarGlobal & Wasalt Real Estate Intelligence Copilot**. Built specifically for high-net-worth international investors and Saudi real estate buyers, this agent integrates the luxury co-branded portfolio of **DarGlobal** (Trump Organization, Pagani, Missoni, Aston Martin, Automobili Lamborghini, Elie Saab, Mouawad) with the verified proptech inventory of **Wasalt** (REGA-licensed Saudi marketplace).

---

### 1. High-Level System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Luxury User Interface (SPA)                     │
│    • Tailwind CSS & Dark/Gold Theme    • Dynamic Currency (USD/SAR/AED)│
│    • English & Arabic (RTL)            • Interactive Property Dossiers │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / WebSocket / JSON
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        FastAPI Application Gateway                     │
│    • /api/chat      • /api/properties     • /api/consultation (Leads)  │
│    • /health        • /api/models         • /static                    │
└───────────────────┬───────────────────────────────┬────────────────────┘
                    │                               │
                    ▼                               ▼
      ┌───────────────────────────┐   ┌───────────────────────────┐
      │   Conversation Memory     │   │   Lead & Booking Service  │
      │   • Multi-turn Sessions   │   │   • VIP Viewings & CRM    │
      │   • Investor Preferences  │   │   • Unique Ref: DG-XXXXXX │
      └───────────────────────────┘   └───────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        Agentic Reasoning Core                          │
│                                                                        │
│    ┌──────────────────────────┐    ┌──────────────────────────────┐    │
│    │ Live OpenRouter LLM Mode │    │ Deterministic Engine Fallback│    │
│    │ • Llama-3.3-70B:free     │◄──►│ • Intent / Slot Extraction   │    │
│    │ • Qwen-2.5-72B:free      │    │ • Guaranteed 0-Downtime      │    │
│    │ • Tool Calling / ReAct   │    │ • Rate-Limit (429) Immunity  │    │
│    └─────────────┬────────────┘    └──────────────┬───────────────┘    │
│                  │                                │                    │
│                  └────────────────┬───────────────┘                    │
│                                   │                                    │
│                                   ▼                                    │
│                    Autonomous Tool Execution Hub                       │
│    • search_properties()           • get_property_details()            │
│    • compare_properties()          • calculate_mortgage_and_roi()      │
│    • check_golden_visa_residency() • book_consultation_or_viewing()    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     Knowledge & Data Services Layer                    │
│    • Hybrid Search (Fuzzy + Token BM25 + Multi-Attribute Filtering)    │
│    • Consolidated Data Engine (data/consolidated_properties.json)      │
│    • DarGlobal Web Scraper         • Wasalt REGA Portal Scraper        │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 2. Scraping & Data Ingestion Pipeline

1. **DarGlobal Public Scraper (`scraper/darglobal_scraper.py`)**:
   - Programmatically discovers and parses project pages from `https://darglobal.co.uk`.
   - Extracts co-branding partners, architectural concepts, unit mix (penthouses, villas, sky residences), handover dates, and pricing across Dubai, Jeddah, Riyadh, Muscat, Doha, and Spain.
2. **Wasalt Saudi Marketplace Scraper (`scraper/wasalt_scraper.py`)**:
   - Queries `https://wasalt.com` across primary Saudi urban growth corridors (Riyadh, Jeddah, Al Khobar, Dammam).
   - Captures REGA advertising licensing numbers, property classification (villas, duplexes, penthouses, commercial), square meterage, and broker contact credentials.
3. **Consolidation Pipeline (`scraper/run_scrapers.py`)**:
   - Normalizes heterogeneous property schemas into a unified JSON format with pre-computed multi-currency valuations (USD, SAR, AED, GBP, EUR) and search token indexes.

---

### 3. Agentic Design & Tool Calling

The agent operates via a closed-loop ReAct (Reasoning + Acting) cycle:
1. **User Query Analysis**: Formulates an execution plan identifying buyer intent, location constraints, budget parameters, and comparison requirements.
2. **Function Calling via OpenRouter**:
   - Uses OpenAI-compatible tool specifications targeting free tier models such as `meta-llama/llama-3.3-70b-instruct:free` or `qwen/qwen-2.5-72b-instruct:free`.
3. **Dual-Engine Zero-Downtime Architecture**:
   - *Primary*: OpenRouter API with JSON schema tool definitions.
   - *Secondary Fallback*: Deterministic NLP pattern analyzer executing the exact same tools and producing rich markdown and interactive property cards. This guarantees that evaluations never fail due to API token exhaustion or upstream 429 rate limits.

---

### 4. Financial & Residency Modeling Tools

- **Mortgage & Amortization Engine (`calculate_mortgage_and_roi`)**:
  Computes exact monthly debt service, principal balance, 5-year compounding rental cashflow, and net investment yields.
- **Golden Visa & Residency Checker (`check_golden_visa_and_residency`)**:
  Maps property valuations directly against national residency policies:
  - UAE: AED 2,000,000 threshold for 10-Year Renewable Golden Visa.
  - Saudi Arabia: SAR 4,000,000 threshold for Real Estate Owner Premium Residency.
  - Oman: OMR 250,000 threshold for AIDA Muscat investor residency.

---

### 5. Containerization & Deployment

- **Multi-Stage Production Dockerfile**:
  - Uses `python:3.11-slim` base image.
  - Implements non-root user (`appuser`) for Linux security compliance.
  - Exposes port 8000 with embedded healthcheck probes (`/health`).
- **Cloud Readiness**:
  - Compatible with 1-click deployments on Hugging Face Spaces (Docker Space), Render (`render.yaml`), Railway, Fly.io, and AWS ECS.
