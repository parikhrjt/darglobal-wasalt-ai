# Email Submission to DarGlobal

**To:** [careers@darglobal.co.uk](mailto:careers@darglobal.co.uk)  
**Subject:** Application & Technical Assignment Submission: Senior AI Engineer – Agentic Systems – Rajat Parikh

---

Dear DarGlobal Talent Acquisition Team & Hiring Committee,

Thank you for the opportunity to interview for the **Senior AI Engineer – Agentic Systems** role at **DarGlobal**.

Please find below my requested candidate information and the complete submission for the technical assignment, including architecture documentation, containerised source repository, and a live working URL.

---

### Candidate Information

* **Full Name:** Rajat Parikh
* **LinkedIn:** [https://www.linkedin.com/in/rajat-parikh-0848b488/](https://www.linkedin.com/in/rajat-parikh-0848b488/)
* **Contact Phone:** [+91-8839121877](tel:+918839121877)
* **Current Location:** Bengaluru, India
* **Current Package:** 46 LPA (~$55,000 USD / ~SAR 207,000 per annum)
* **Expected Package:** 46 LPA (Open to alignment with DarGlobal's regional UAE/UK/KSA compensation structure)
* **Notice Period:** 0 days (Immediately available to join)

---

### Technical Assignment: DarGlobal × Wasalt Agentic Real Estate Copilot

In response to the technical brief, I have designed, engineered, containerised, and deployed an autonomous real estate copilot connecting DarGlobal's ultra-luxury co-branded developments (The Trump Organization, Pagani, Missoni, Aston Martin, Automobili Lamborghini, Elie Saab, Mouawad) with Wasalt's verified Saudi proptech marketplace.

#### 🌐 Live Working URL & Demo Access
* **Live Application URL:** [https://darglobal-wasalt-ai.onrender.com](https://darglobal-wasalt-ai.onrender.com)
* **System Health Endpoint:** [https://darglobal-wasalt-ai.onrender.com/health](https://darglobal-wasalt-ai.onrender.com/health)
* **GitHub Repository:** [https://github.com/parikhrjt/darglobal-wasalt-ai](https://github.com/parikhrjt/darglobal-wasalt-ai)

*(The platform includes a resilient Dual-Engine Architecture with instant fallback to a deterministic property reasoning engine, ensuring 100% continuous uptime and zero rate-limit disruptions during candidate evaluation).*

---

### Solution Overview & Key Engineering Highlights

1. **Automated Web Scraping & Ingestion Pipeline (`scraper/`):**
   * **DarGlobal Scraper:** Extracts luxury branded developments across Dubai, Saudi Arabia (Riyadh & Jeddah), Oman (AIDA Muscat), Qatar (Doha), and Spain (Costa del Sol), indexing co-branding partners, unit mixes, handover dates, and foreign freehold investment eligibility.
   * **Wasalt Scraper:** Ingests verified Saudi residential and commercial inventory (Riyadh, Jeddah, Al Khobar, Dammam), adhering strictly to REGA (Real Estate General Authority) licensing protocols.
   * **Consolidation Pipeline:** Normalizes heterogeneous schemas into a unified, high-speed multi-attribute retrieval catalog with pre-computed multi-currency valuations (**USD, SAR, AED, GBP, EUR**).

2. **Agentic ReAct Architecture & Function Calling (`app/agent/`):**
   * **Autonomous Tool Hub:**
     * `search_properties`: Multi-faceted parametric filtering across cities, brands, budgets, and property types.
     * `get_property_details`: Architectural dossiers, floor specs, and payment milestone schedules.
     * `compare_properties`: Dynamic side-by-side matrices comparing square meterage, price per sqft, completion timelines, and projected yields.
     * `calculate_mortgage_and_roi`: Real-time debt amortisation, annual cashflow, and 5-year compounding ROI forecasts.
     * `check_golden_visa_and_residency`: Automated qualification checks for UAE 10-Year Golden Visa (AED 2M+), Saudi Premium Residency, and Oman Investor Visas.
     * `book_consultation_or_viewing`: Captures qualified buyer leads into a persistent booking service generating unique confirmation tokens (`DG-XXXXXX`).
   * **OpenRouter Free Model Integration:** Native support for `meta-llama/llama-3.3-70b-instruct:free`, `qwen/qwen-2.5-72b-instruct:free`, and `mistralai/mistral-7b-instruct:free`.
   * **Zero-Downtime Deterministic Fallback:** Implements an intelligent local execution engine that automatically takes over if OpenRouter encounters HTTP 429 rate limits or network latency, guaranteeing 100% uptime for evaluators.

3. **Luxury Responsive Single Page Application (`app/static/`):**
   * Bespoke luxury dark/gold aesthetic reflecting DarGlobal's elite corporate identity.
   * Dynamic real-time currency conversion (USD, AED, SAR, GBP, EUR).
   * Full English & Arabic (RTL) localization toggle.
   * Interactive property inspection lightbox and VIP private consultation scheduling forms.

4. **Containerization & Production Readiness (`Dockerfile`, `docker-compose.yml`):**
   * Hardened, multi-stage Docker container built on `python:3.11-slim` running as a non-privileged `appuser`.
   * Standardized REST API with OpenAPI documentation at `/docs` and automated Docker healthcheck probes.
   * Verified by an end-to-end automated test suite (`test_server.py`).

---

### Deliverables & Attachments in Repository

* `Dockerfile` & `docker-compose.yml`: Ready for instant local container execution (`docker compose up --build`).
* `submission/ARCHITECTURE.md`: Technical whitepaper detailing agent reasoning loops, data schemas, and security design.
* `test_server.py`: Automated test suite verifying all routes, agent tools, and health status.

I am very excited about DarGlobal’s vision to blend world-renowned luxury brands with cutting-edge real estate innovation. I look forward to discussing how my experience in building autonomous agentic systems can accelerate DarGlobal's AI initiatives.

Sincerely,

**Rajat Parikh**  
Senior AI Engineer  
Phone: [+91-8839121877](tel:+918839121877)  
LinkedIn: [linkedin.com/in/rajat-parikh-0848b488](https://www.linkedin.com/in/rajat-parikh-0848b488/)  
GitHub: [github.com/parikhrjt](https://github.com/parikhrjt)
