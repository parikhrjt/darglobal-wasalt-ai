# DarGlobal × Wasalt — Agentic AI Real Estate Copilot

[![Live Demo](https://img.shields.io/badge/Demo-darglobal--wasalt--ai.vercel.app-gold.svg)](https://darglobal-wasalt-ai.vercel.app/)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Free%20Models-orange.svg)](https://openrouter.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-gold.svg)](LICENSE)

An enterprise-grade, autonomous real estate intelligence copilot built for **DarGlobal** (London Stock Exchange listed luxury developer) and **Wasalt** (Saudi Arabia's premier REGA-licensed digital proptech portal).

Designed for high-net-worth international investors and GCC buyers, the agent automates property discovery, side-by-side branded development comparisons, mortgage/cashflow simulations, Golden Visa residency evaluation, and VIP private viewing bookings.

---

## 🌟 Key Capabilities & Highlights

1. **Scraped Multi-Source Intelligence (`scraper/`)**:
   - **DarGlobal Luxury Portfolio**: Extracted branded residences across Dubai, Saudi Arabia (Riyadh & Jeddah), Oman (AIDA Muscat), Qatar (Doha), and Spain (Costa del Sol) in collaboration with **The Trump Organization, Pagani, Missoni, Aston Martin, Automobili Lamborghini, Elie Saab, and Mouawad**.
   - **Wasalt Verified Marketplace**: Real-time indexed residential villas, executive penthouses, and Grade-A commercial spaces in Riyadh, Jeddah, and Al Khobar with verified **REGA advertising licenses**.
2. **Autonomous Tool Calling Engine (`app/agent/tools.py`)**:
   - `search_properties()`: Multi-attribute parametric filtering.
   - `get_property_details()`: Complete architectural specifications and payment plans.
   - `compare_properties()`: Dynamic multi-property comparison matrix.
   - `calculate_mortgage_and_roi()`: Exact debt service, annual rental cashflows, and 5-year ROI forecasts.
   - `check_golden_visa_and_residency()`: Automated qualification for UAE 10-Year Golden Visa (AED 2M+), Saudi Premium Residency, and Oman Investor Visas.
   - `book_consultation_or_viewing()`: Qualified investor lead capture with auto-generated booking tokens (`DG-XXXXXX`).
3. **OpenRouter Free Model Integration & Dual-Engine Fallback**:
   - Native integration with OpenRouter free models (`meta-llama/llama-3.3-70b-instruct:free`, `qwen/qwen-2.5-72b-instruct:free`, `mistralai/mistral-7b-instruct:free`, `deepseek/deepseek-r1:free`).
   - **Zero-Downtime Deterministic Fallback**: Automatic failover to an internal deterministic agent engine if upstream OpenRouter APIs return 429 rate limits or are unauthenticated, guaranteeing 100% continuous uptime during candidate evaluation!
4. **Bespoke Luxury Single Page App (`app/static/`)**:
   - Sleek dark/gold visual aesthetic reflecting DarGlobal's elite pedigree.
   - Real-time multi-currency switcher (**USD, SAR, AED, GBP, EUR**).
   - Full bilingual support with English & Arabic (العربية) RTL toggle.
5. **Production Docker Containerization**:
   - Multi-stage Docker build, non-root user security hardening, and built-in healthcheck probes.

---

## 🏗️ Architecture Overview

```
darglobal-wasalt-ai/
├── Dockerfile                     # Multi-stage production container
├── docker-compose.yml             # Docker compose setup
├── render.yaml                    # 1-click deployment on Render
├── Procfile                       # Process manager for cloud PaaS
├── requirements.txt               # Backend Python dependencies
├── .env.example                   # Environment configuration template
│
├── app/                           # FastAPI Agentic Backend
│   ├── main.py                   # REST endpoints, CORS, static mounting
│   ├── config.py                 # Application configuration & env settings
│   ├── agent/
│   │   ├── agent.py              # Master agent orchestrator
│   │   ├── tools.py              # Tool schemas & execution functions
│   │   ├── openrouter.py         # OpenRouter API client
│   │   ├── memory.py             # Multi-turn conversation store
│   │   └── fallback_engine.py    # Deterministic zero-downtime agent engine
│   ├── services/
│   │   ├── property_service.py   # Property querying & currency conversion
│   │   └── lead_service.py       # VIP viewing & consultation booking store
│   └── static/                   # Luxury Web Client
│       ├── index.html            # Luxury Single Page Application
│       ├── css/style.css         # Custom styling, dark/gold accents, RTL
│       └── js/
│           ├── api.js            # Frontend REST client
│           └── app.js            # Chat UI controller & interactive cards
│
├── scraper/                       # Web Scraping Pipeline
│   ├── darglobal_scraper.py      # DarGlobal official website scraper
│   ├── wasalt_scraper.py         # Wasalt Saudi portal scraper
│   └── run_scrapers.py           # Normalization & consolidation pipeline
│
├── data/                          # Data Repository
│   ├── darglobal_projects.json   # 13 DarGlobal luxury developments
│   ├── wasalt_properties.json    # 10 Wasalt Saudi verified listings
│   ├── consolidated_properties.json # Search-indexed consolidated corpus
│   └── leads.json                # VIP viewing requests
│
├── submission/                    # Candidate Submission Package
│   ├── SUBMISSION_EMAIL.md       # Formatted email for careers@darglobal.co.uk
│   └── ARCHITECTURE.md           # Engineering architectural whitepaper
│
└── test_server.py                 # Automated verification test suite
```

---

## 🚀 Quickstart Guide

### Option 1: Run Locally with Python

1. **Clone the repository:**
   ```bash
   git clone https://github.com/parikhrjt/darglobal-wasalt-ai.git
   cd darglobal-wasalt-ai
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables (Optional):**
   ```bash
   cp .env.example .env
   # Add your OPENROUTER_API_KEY in .env if desired, or test with built-in zero-downtime fallback
   ```

4. **Launch the application:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   Open **`http://localhost:8000`** in your browser.

---

### Option 2: Run with Docker & Docker Compose

1. **Build and start the container:**
   ```bash
   docker compose up --build
   ```

2. **Access the application:**
   - Web Application: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Healthcheck: `http://localhost:8000/health`

---

## ☁️ Deployment Guide (Live Working URL)

To fulfill the requirement: *"Deploy the solution rather than providing source code only. Provide a working URL so the chatbot can be tested directly"*, here are ready-to-use options:

### 1. Instant Free Cloud Deployment on Render (Recommended)
1. Push this repository to GitHub.
2. Sign in to [Render](https://render.com) (Free tier).
3. Click **New +** -> **Web Service** -> Connect your GitHub repo.
4. Select **Docker** environment. Render will automatically detect the `Dockerfile` and `render.yaml`.
5. Click **Create Web Service**. You will receive an instant public URL: `https://darglobal-wasalt-ai.onrender.com`.

### 2. Instant Free Deployment on Hugging Face Spaces (Docker)
1. Create a free account on [Hugging Face](https://huggingface.co).
2. Click **New Space** -> Choose **Docker** SDK (Blank).
3. Push or upload this repository files into the Space.
4. Hugging Face automatically builds the Docker container and provides an instant 24/7 public URL (`https://<username>-darglobal-wasalt-ai.hf.space`).

### 3. Instant Public URL via Ngrok Tunnel (from local machine)
If running the server locally on port 8000:
```bash
ngrok http 8000
```
Ngrok generates a public HTTPS URL (e.g. `https://xxxx.ngrok-free.app`) that can be tested directly from anywhere in the world!

---

## 🧪 Verification & Test Suite

Run the automated test suite to verify all endpoints, agent tools, calculations, and catalog indexing:

```bash
python test_server.py
```

Expected output:
```
Testing GET /health...
Health Data: {'status': 'healthy', 'properties_indexed': 23, 'darglobal_developments': 13, 'wasalt_listings': 10}
Testing GET / (Frontend Single Page App)...
Frontend successfully served!
Testing GET /api/properties...
Retrieved 5 properties.
Testing POST /api/chat (Property Discovery)...
Property cards attached: 1
Tools executed: ['search_properties']
Testing POST /api/chat (Financial Mortgage & ROI Model)...
Mortgage Analysis Tools: ['calculate_mortgage_and_roi']
Testing POST /api/consultation (Lead Capture)...
Booking confirmed: DG-XXXXXX
ALL VERIFICATION TESTS PASSED SUCCESSFULLY! 🚀
```

---

## 📚 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the Luxury Single Page Web Client |
| `GET` | `/health` | Application healthcheck & dataset statistics |
| `POST` | `/api/chat` | Agentic chat completions with tool execution |
| `GET` | `/api/properties` | Parametric filtering across DarGlobal & Wasalt catalog |
| `GET` | `/api/properties/{id}`| Detailed property specs, payment plan, amenities |
| `POST` | `/api/consultation` | VIP private viewing & investor lead capture |
| `GET` | `/api/models` | List of supported OpenRouter free models |
| `GET` | `/docs` | Interactive Swagger API Explorer |

---

## 📄 License
Released under the MIT License. Developed for the DarGlobal Senior AI Engineer – Agentic Systems Technical Assessment.
