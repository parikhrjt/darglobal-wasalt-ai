# Email Submission Template

**To:** [careers@darglobal.co.uk](mailto:careers@darglobal.co.uk)  
**Subject:** Application & Technical Assignment Submission: Senior AI Engineer – Agentic Systems – [Your Full Name]

---

Dear DarGlobal Talent Acquisition Team & Hiring Committee,

Thank you for the opportunity to interview for the **Senior AI Engineer – Agentic Systems** role at **DarGlobal**.

Please find below my requested candidate details, followed by the complete submission for the technical assignment, including architecture documentation, containerised source repository, and a live working demo URL.

---

### Candidate Information

* **Current Location:** [City, Country, e.g., London, UK / Dubai, UAE / Riyadh, Saudi Arabia]
* **Current Package:** [e.g., $XXX,XXX / £XX,XXX / SAR XXX,XXX per annum]
* **Expected Package:** [e.g., $XXX,XXX / £XX,XXX / SAR XXX,XXX per annum (Open to discussion based on total compensation & equity/relocation structure)]
* **Notice Period:** [e.g., Immediate / 30 Days / 2 Months]

---

### Technical Assignment: DarGlobal × Wasalt Agentic Real Estate Copilot

In response to the technical brief, I have designed, engineered, containerised, and deployed a production-grade **Autonomous Real Estate Intelligence Copilot** tailored to DarGlobal’s ultra-luxury co-branded developments and Wasalt’s verified Saudi proptech marketplace.

#### 🌐 Live Working URL & Demo Access
* **Live Application URL:** [https://darglobal-wasalt-ai.onrender.com](https://darglobal-wasalt-ai.onrender.com) *(or your Hugging Face Space / Tunnel URL)*
* **System Health Endpoint:** [https://darglobal-wasalt-ai.onrender.com/health](https://darglobal-wasalt-ai.onrender.com/health)
* **GitHub Repository:** [https://github.com/your-username/darglobal-wasalt-ai](https://github.com/your-username/darglobal-wasalt-ai)

*(Note: The application features an autonomous Dual-Engine Architecture with instant fallback to a deterministic agentic brain, ensuring 100% continuous uptime during evaluation regardless of upstream OpenRouter free-tier rate limits or key availability).*

---

### Solution Overview & Key Engineering Highlights

1. **Automated Web Scraping & Ingestion Pipeline (`scraper/`):**
   * **DarGlobal Scraper:** Extracts luxury branded developments (The Trump Organization, Pagani, Missoni, Aston Martin, Automobili Lamborghini, Elie Saab, Mouawad) across Dubai, Saudi Arabia, Oman, Qatar, and Spain, capturing unit configurations, handover schedules, and foreign investment structures.
   * **Wasalt Scraper:** Indexes verified Saudi residential & commercial inventory (Riyadh, Jeddah, Al Khobar, Dammam), adhering strictly to REGA (Real Estate General Authority) licensing protocols.
   * **Consolidation Engine:** Merges both corpora into a unified, high-speed multi-attribute retrieval catalog with pre-calculated multi-currency conversions (USD, SAR, AED, GBP, EUR).

2. **Agentic ReAct Architecture & Function Calling (`app/agent/`):**
   * **Autonomous Tool Execution Hub:**
     * `search_properties()`: Multi-faceted query filtering across brands, locations, property types, and budgets.
     * `get_property_details()`: Deep architectural dossiers and payment milestone schedules.
     * `compare_properties()`: Dynamic side-by-side matrices comparing square meterage, price per sqft, completion timelines, and projected yields.
     * `calculate_mortgage_and_roi()`: Real-time debt amortisation and 5-year cashflow projections.
     * `check_golden_visa_and_residency()`: Qualification logic for UAE 10-Year Golden Visa (AED 2M+), Saudi Premium Residency, and Oman Investor Visas.
     * `book_consultation_or_viewing()`: Captures qualified buyer leads into a persistent booking service generating unique confirmation tokens (`DG-XXXXXX`).
   * **OpenRouter Free Model Integration:** Native support for `meta-llama/llama-3.3-70b-instruct:free`, `qwen/qwen-2.5-72b-instruct:free`, and `mistralai/mistral-7b-instruct:free` with custom temperature and prompt optimization.
   * **Zero-Downtime Deterministic Fallback:** Implements an intelligent local execution engine that automatically takes over if OpenRouter encounters HTTP 429 rate limits or network latency, guaranteeing 100% uptime for evaluators.

3. **Luxury Responsive Single Page Application (`app/static/`):**
   * Bespoke luxury dark/gold aesthetic aligning with DarGlobal's high-end brand identity.
   * Dynamic real-time currency conversion (USD, AED, SAR, GBP, EUR).
   * Full English & Arabic (RTL) localization toggle.
   * Interactive property inspection lightbox and VIP private consultation scheduling forms.

4. **Containerization & Deployment (`Dockerfile`, `docker-compose.yml`):**
   * Hardened, multi-stage Docker container built on `python:3.11-slim` running as a non-privileged `appuser`.
   * Standardized REST API with OpenAPI documentation at `/docs` and automated Docker healthcheck probes.

---

### Deliverables & Attachments in Repository

* `Dockerfile` & `docker-compose.yml`: Ready for instant local container execution (`docker compose up --build`).
* `submission/ARCHITECTURE.md`: Technical whitepaper detailing agent reasoning loops, data schemas, and security design.
* `test_server.py`: Automated end-to-end test suite verifying API routes, tool executions, and health status.

I am very excited about DarGlobal’s vision to blend world-renowned luxury brands with cutting-edge real estate innovation. I look forward to discussing how my experience in building autonomous agentic systems can accelerate DarGlobal's AI initiatives.

Sincerely,

**[Your Full Name]**  
Senior AI Engineer  
[Phone Number] | [LinkedIn Profile] | [GitHub Profile]
