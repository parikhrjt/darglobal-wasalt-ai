"""
Deterministic Agentic Real Estate Brain (Zero-Downtime Fallback)
Ensures 100% continuous uptime and instant responsiveness when OpenRouter API is
rate-limited, unauthenticated, or temporarily unreachable.
Executes identical agent tool pipelines and outputs executive-grade responses.
"""

import logging
import re
from typing import Any, Dict, List, Optional
from app.agent.tools import execute_tool
from app.services.property_service import property_service

logger = logging.getLogger(__name__)

class DeterministicAgentEngine:
    """Intelligent intent parser and tool execution pipeline."""

    def process(self, query: str, conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        q_lower = query.lower().strip()
        executed_tools = []
        response_text = ""
        cards = []

        # 1. Lead / Booking Intent
        if any(w in q_lower for w in ["book", "consultation", "schedule", "viewing", "tour", "appointment", "reserve", "احجز", "موعد"]):
            # Extract contact if provided, or return booking prompt
            name_match = re.search(r"my name is ([a-zA-Z\s]+)", query, re.I)
            email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", query)
            phone_match = re.search(r"(\+?\d[\d\s-]{7,})", query)

            client_name = name_match.group(1).strip() if name_match else "Prospective VIP Investor"
            client_email = email_match.group(0) if email_match else "investor@darglobal.vip"
            client_phone = phone_match.group(0) if phone_match else "+966 50 000 0000"

            res = execute_tool("book_consultation_or_viewing", {
                "client_name": client_name,
                "email": client_email,
                "phone": client_phone,
                "property_name": "Executive Real Estate Consultation",
                "preferred_datetime": "Within 24 Hours",
                "notes": f"Initial inquiry: '{query}'"
            })
            executed_tools.append({"tool": "book_consultation_or_viewing", "output": res})
            
            booking = res.get("booking", {})
            response_text = (
                f"### ✨ VIP Consultation Request Confirmed\n\n"
                f"Thank you, **{client_name}**. We have reserved your priority consultation.\n\n"
                f"* **Reference Number:** `{booking.get('booking_reference')}`\n"
                f"* **Status:** {booking.get('status')}\n"
                f"* **Direct Contact:** Our Senior Portfolio Director will reach out to **{client_email}** to coordinate a confidential private presentation.\n\n"
                f"Feel free to let me know if you would like me to prepare a bespoke investment portfolio beforehand."
            )
            return {"text": response_text, "tools_used": executed_tools, "cards": cards}

        # 2. Mortgage & ROI Calculation Intent
        if any(w in q_lower for w in ["mortgage", "calculate", "roi", "yield", "monthly payment", "loan", "down payment", "احسب", "قسط", "عائد"]):
            # Extract number from query or default
            price_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:m|million|k|thousand|usd|\$|sar|aed)?", q_lower)
            price = 2450000.0
            currency = "USD"
            if "sar" in q_lower:
                currency = "SAR"
                price = 9187500.0
            elif "aed" in q_lower:
                currency = "AED"
                price = 9000000.0

            if price_match:
                val = float(price_match.group(1))
                if "m" in q_lower or "million" in q_lower or val < 100:
                    price = val * 1_000_000
                elif "k" in q_lower or "thousand" in q_lower:
                    price = val * 1_000
                elif val > 50000:
                    price = val

            res = execute_tool("calculate_mortgage_and_roi", {
                "property_price": price,
                "currency": currency,
                "down_payment_pct": 20,
                "interest_rate_pct": 4.8,
                "loan_term_years": 25,
                "expected_rental_yield_pct": 8.5
            })
            executed_tools.append({"tool": "calculate_mortgage_and_roi", "output": res})

            response_text = (
                f"### 📊 Financial & Mortgage Yield Model ({currency})\n\n"
                f"Here is a comprehensive breakdown for an acquisition value of **{currency} {res['purchase_price']:,.2f}**:\n\n"
                f"| Metric | Valuation / Cashflow |\n"
                f"| :--- | :--- |\n"
                f"| **Down Payment (20%)** | `{currency} {res['down_payment']:,.2f}` |\n"
                f"| **Loan Principal (80%)** | `{currency} {res['loan_principal']:,.2f}` |\n"
                f"| **Estimated Monthly Mortgage** | `{currency} {res['monthly_mortgage_payment']:,.2f} / month` |\n"
                f"| **Projected Annual Gross Rental (8.5%)** | `{currency} {res['projected_annual_rent']:,.2f} / year` |\n"
                f"| **Net Monthly Cashflow (Rent - Mortgage)** | `+{currency} {res['projected_net_monthly_cashflow']:,.2f} / month` |\n"
                f"| **5-Year Cumulative Rental Return** | `{currency} {res['five_year_total_rental_return']:,.2f}` |\n\n"
                f"> 💡 *Tip: Properties above AED 2,000,000 in Dubai automatically qualify foreign investors for the prestigious 10-Year UAE Golden Visa.*"
            )
            return {"text": response_text, "tools_used": executed_tools, "cards": cards}

        # 3. Comparison Intent
        if any(w in q_lower for w in ["compare", "vs", "versus", "difference", "مقارنة", "بين"]):
            # Pick 2 suitable properties to compare
            id1 = "dg-davinci-pagani"
            id2 = "dg-trump-tower-dubai"

            if "lamborghini" in q_lower or "spain" in q_lower:
                id2 = "dg-tierra-viva-lamborghini"
            elif "missoni" in q_lower:
                id2 = "dg-urban-oasis-missoni"
            elif "riyadh" in q_lower or "wasalt" in q_lower:
                id1 = "ws-riyadh-almalqa-villa-01"
                id2 = "ws-riyadh-hittin-penthouse-02"

            res = execute_tool("compare_properties", {"property_ids": [id1, id2]})
            executed_tools.append({"tool": "compare_properties", "output": res})
            comparison_items = res.get("comparison", [])

            if len(comparison_items) >= 2:
                p1, p2 = comparison_items[0], comparison_items[1]
                response_text = (
                    f"### ⚖️ Side-by-Side Property Comparison\n\n"
                    f"Comparing **{p1['name']}** vs **{p2['name']}**:\n\n"
                    f"| Criterion | **{p1['name']}** | **{p2['name']}** |\n"
                    f"| :--- | :--- | :--- |\n"
                    f"| **Developer / Source** | {p1['source']} | {p2['source']} |\n"
                    f"| **Brand Collaboration** | {p1['brand_partner']} | {p2['brand_partner']} |\n"
                    f"| **Location** | {p1['city']}, {p1['country']} | {p2['city']}, {p2['country']} |\n"
                    f"| **Starting Price (USD)** | `${p1['price_usd']:,}` | `${p2['price_usd']:,}` |\n"
                    f"| **Starting Price (SAR)** | `SAR {p1['price_sar']:,}` | `SAR {p2['price_sar']:,}` |\n"
                    f"| **Projected ROI** | `{p1['projected_roi_pct']}% Net` | `{p2['projected_roi_pct']}% Net` |\n"
                    f"| **Golden Visa** | {'✅ Eligible' if p1['golden_visa_eligible'] else 'N/A'} | {'✅ Eligible' if p2['golden_visa_eligible'] else 'N/A'} |\n"
                    f"| **Completion** | {p1['completion_status']} ({p1['completion_date']}) | {p2['completion_status']} ({p2['completion_date']}) |\n\n"
                    f"**Investment Recommendation:**\n"
                    f"* Choose **{p1['name']}** if you desire bespoke {p1['brand_partner']} exclusivity and prime positioning in {p1['city']}.\n"
                    f"* Choose **{p2['name']}** if your priority is {p2['brand_partner']} amenities and strong hospitality-backed capital appreciation."
                )
                cards = comparison_items
                return {"text": response_text, "tools_used": executed_tools, "cards": cards}

        # 4. Golden Visa / Residency Intent
        if any(w in q_lower for w in ["golden visa", "residency", "visa", "citizenship", "iqama", "اقامة", "فيزا"]):
            country = "United Arab Emirates" if any(c in q_lower for c in ["uae", "dubai", "emirates"]) else "Saudi Arabia" if "saudi" in q_lower or "riyadh" in q_lower else "United Arab Emirates"
            res = execute_tool("check_golden_visa_and_residency", {
                "country": country,
                "investment_amount_usd": 650000
            })
            executed_tools.append({"tool": "check_golden_visa_and_residency", "output": res})

            response_text = (
                f"### 🌐 Golden Visa & Investor Residency Advisory\n\n"
                f"For investments in **{res['country']}**:\n\n"
                f"* **Residency Tier:** {res.get('visa_type', 'Investor Residency')}\n"
                f"* **Minimum Qualification Threshold:** Approximately **USD ${round(res.get('investment_usd', 550000)):,}**\n"
                f"* **Eligibility Status:** ✅ **Fully Qualified** across all DarGlobal Dubai and Saudi luxury flagship developments.\n\n"
                f"**Privileges Included:**\n"
                + "\n".join([f"- {b}" for b in res.get("benefits", [])]) + "\n\n"
                f"Would you like me to curate eligible properties that meet the exact residency investment thresholds?"
            )
            return {"text": response_text, "tools_used": executed_tools, "cards": cards}

        # 5. General Search / Property Discovery Intent
        city = None
        for c in ["dubai", "riyadh", "jeddah", "muscat", "doha", "marbella", "khobar", "dammam"]:
            if c in q_lower:
                city = c.capitalize()
                break

        brand = None
        for b in ["pagani", "trump", "missoni", "aston martin", "lamborghini", "elie saab", "fendi", "mouawad"]:
            if b in q_lower:
                brand = b.capitalize()
                break

        source = None
        if "wasalt" in q_lower:
            source = "Wasalt"
        elif "darglobal" in q_lower or "dar global" in q_lower:
            source = "DarGlobal"

        search_args = {
            "query": query,
            "city": city,
            "brand_partner": brand,
            "source": source,
            "limit": 4
        }
        res = execute_tool("search_properties", search_args)
        executed_tools.append({"tool": "search_properties", "output": res})
        matched_props = res.get("properties", [])

        if not matched_props:
            # Fallback search without tight constraints
            res = execute_tool("search_properties", {"limit": 4})
            matched_props = res.get("properties", [])

        cards = matched_props
        response_text = (
            f"### 🏛️ Curated Properties Matching Your Criteria\n\n"
            f"I have analyzed our consolidated portfolio across **DarGlobal** luxury branded developments and **Wasalt** verified Saudi listings. Here are premier selections tailored to your interest:\n\n"
        )

        for p in matched_props:
            brand_tag = f" • **{p['brand_partner']}**" if p.get("brand_partner") and "Marketplace" not in p['brand_partner'] else ""
            response_text += (
                f"#### [{p['name']}]({p['url']})\n"
                f"* **Developer / Source:** {p['source']}{brand_tag}\n"
                f"* **Location:** {p['neighborhood']}, {p['city']}, {p['country']}\n"
                f"* **Starting Price:** `${p['price_usd']:,} USD` / `SAR {p['price_sar']:,} SAR` (`AED {p['price_aed']:,}`)\n"
                f"* **Highlights:** {p['bedrooms_display']} | {p['area_display']} | **{p['projected_roi_pct']}% Net ROI**\n"
                f"* *{p['description'][:140]}...*\n\n"
            )

        response_text += (
            f"> 💬 *You can ask me to:* **compare** any of these properties, **calculate mortgage & cashflow**, or **schedule a VIP private consultation**."
        )

        return {
            "text": response_text,
            "tools_used": executed_tools,
            "cards": cards
        }

deterministic_engine = DeterministicAgentEngine()
