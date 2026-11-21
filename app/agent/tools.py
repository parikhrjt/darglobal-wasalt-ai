"""
Agentic Tool Definitions & Execution Engine
Defines JSON schemas for OpenRouter function calling and local execution logic.
"""

import json
import logging
from typing import Any, Dict, List, Optional
from app.services.property_service import property_service
from app.services.lead_service import lead_service

logger = logging.getLogger(__name__)

# Tool Definitions in OpenAI / OpenRouter function calling format
AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_properties",
            "description": "Search and filter luxury residences from DarGlobal and verified Saudi listings from Wasalt based on city, country, brand, budget, or property type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keywords, e.g. 'Pagani', 'Red Sea waterfront', 'KAFD penthouse', 'golf villa'"
                    },
                    "city": {
                        "type": "string",
                        "description": "City name, e.g. Dubai, Riyadh, Jeddah, Muscat, Doha, Marbella"
                    },
                    "country": {
                        "type": "string",
                        "description": "Country name, e.g. United Arab Emirates, Saudi Arabia, Oman, Qatar, Spain"
                    },
                    "source": {
                        "type": "string",
                        "enum": ["DarGlobal", "Wasalt", "All"],
                        "description": "Filter by source developer or marketplace portal"
                    },
                    "min_price_usd": {
                        "type": "number",
                        "description": "Minimum budget in USD"
                    },
                    "max_price_usd": {
                        "type": "number",
                        "description": "Maximum budget in USD"
                    },
                    "bedrooms": {
                        "type": "integer",
                        "description": "Minimum number of bedrooms required"
                    },
                    "brand_partner": {
                        "type": "string",
                        "description": "Luxury co-brand partner, e.g. Pagani, Trump, Missoni, Aston Martin, Elie Saab, Lamborghini, Mouawad"
                    },
                    "property_type": {
                        "type": "string",
                        "description": "Type of property, e.g. Villa, Apartment, Penthouse, Duplex, Mansion"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_property_details",
            "description": "Retrieve comprehensive architectural specifications, payment plan breakdown, amenities, and developer details for a specific property ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "property_id": {
                        "type": "string",
                        "description": "The unique property identifier, e.g. 'dg-davinci-pagani' or 'ws-riyadh-almalqa-villa-01'"
                    }
                },
                "required": ["property_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_properties",
            "description": "Generate a comparative matrix between 2 or 3 properties across pricing, location, ROI, brand, and specifications.",
            "parameters": {
                "type": "object",
                "properties": {
                    "property_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of 2 to 3 property IDs to compare"
                    }
                },
                "required": ["property_ids"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_mortgage_and_roi",
            "description": "Calculate monthly mortgage payments, interest amortisation, expected rental cashflow, and net investment yield (ROI).",
            "parameters": {
                "type": "object",
                "properties": {
                    "property_price": {
                        "type": "number",
                        "description": "Total purchase price"
                    },
                    "currency": {
                        "type": "string",
                        "enum": ["USD", "AED", "SAR", "GBP", "EUR"],
                        "description": "Currency of calculation (default: USD)"
                    },
                    "down_payment_pct": {
                        "type": "number",
                        "description": "Percentage down payment (e.g. 20 for 20%)"
                    },
                    "interest_rate_pct": {
                        "type": "number",
                        "description": "Annual mortgage interest rate (e.g. 4.5 for 4.5%)"
                    },
                    "loan_term_years": {
                        "type": "integer",
                        "description": "Mortgage duration in years (e.g. 25)"
                    },
                    "expected_rental_yield_pct": {
                        "type": "number",
                        "description": "Expected annual gross or net rental yield % (e.g. 8.0)"
                    }
                },
                "required": ["property_price"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_consultation_or_viewing",
            "description": "Schedule a VIP private viewing, showroom consultation, or investor advisory call with a senior DarGlobal/Wasalt property advisor.",
            "parameters": {
                "type": "object",
                "properties": {
                    "client_name": {
                        "type": "string",
                        "description": "Full name of the client"
                    },
                    "email": {
                        "type": "string",
                        "description": "Client email address"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Contact phone number with international country code"
                    },
                    "property_id": {
                        "type": "string",
                        "description": "Optional property ID of interest"
                    },
                    "property_name": {
                        "type": "string",
                        "description": "Name of the development or residence"
                    },
                    "preferred_datetime": {
                        "type": "string",
                        "description": "Preferred appointment date and time"
                    },
                    "notes": {
                        "type": "string",
                        "description": "Specific investment inquiries, language preference, or questions"
                    }
                },
                "required": ["client_name", "email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_golden_visa_and_residency",
            "description": "Check eligibility for UAE Golden Visa (10-Year Residency), Oman Investor Residency, or Saudi Arabia Premium Residency based on property purchase.",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "enum": ["United Arab Emirates", "Saudi Arabia", "Oman", "Qatar", "Spain"],
                        "description": "Country of investment"
                    },
                    "investment_amount_usd": {
                        "type": "number",
                        "description": "Total proposed property investment in USD"
                    }
                },
                "required": ["country", "investment_amount_usd"]
            }
        }
    }
]

def execute_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Executes an agent tool by name with provided arguments and returns structured output."""
    logger.info(f"Executing tool: {name} with args: {arguments}")
    try:
        if name == "search_properties":
            src = arguments.get("source")
            if src == "All":
                src = None
            props = property_service.filter(
                query=arguments.get("query"),
                city=arguments.get("city"),
                country=arguments.get("country"),
                source=src,
                min_price_usd=arguments.get("min_price_usd"),
                max_price_usd=arguments.get("max_price_usd"),
                bedrooms=arguments.get("bedrooms"),
                brand_partner=arguments.get("brand_partner"),
                property_type=arguments.get("property_type"),
                limit=arguments.get("limit", 6)
            )
            return {
                "success": True,
                "count": len(props),
                "properties": props
            }

        elif name == "get_property_details":
            prop_id = arguments.get("property_id", "")
            prop = property_service.get_by_id(prop_id)
            if prop:
                return {"success": True, "property": prop}
            return {"success": False, "error": f"Property with ID '{prop_id}' was not found in catalog."}

        elif name == "compare_properties":
            prop_ids = arguments.get("property_ids", [])
            items = []
            for pid in prop_ids:
                p = property_service.get_by_id(pid)
                if p:
                    items.append({
                        "id": p.get("id"),
                        "name": p.get("name"),
                        "brand_partner": p.get("brand_partner"),
                        "source": p.get("source"),
                        "city": p.get("city"),
                        "country": p.get("country"),
                        "price_usd": p.get("price_usd"),
                        "price_sar": p.get("price_sar"),
                        "bedrooms": p.get("bedrooms_display"),
                        "area": p.get("area_display"),
                        "projected_roi_pct": p.get("projected_roi_pct"),
                        "golden_visa_eligible": p.get("golden_visa_eligible"),
                        "completion_status": p.get("completion_status"),
                        "completion_date": p.get("completion_date"),
                        "amenities": p.get("amenities", [])[:4]
                    })
            return {"success": True, "comparison": items}

        elif name == "calculate_mortgage_and_roi":
            price = float(arguments.get("property_price", 0))
            curr = arguments.get("currency", "USD").upper()
            down_pct = float(arguments.get("down_payment_pct", 20.0))
            rate_pct = float(arguments.get("interest_rate_pct", 5.0))
            years = int(arguments.get("loan_term_years", 25))
            rental_yield_pct = float(arguments.get("expected_rental_yield_pct", 8.0))

            down_payment = price * (down_pct / 100.0)
            loan_amount = price - down_payment
            monthly_rate = (rate_pct / 100.0) / 12.0
            num_payments = years * 12

            if monthly_rate > 0:
                monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
            else:
                monthly_payment = loan_amount / num_payments

            total_payment = monthly_payment * num_payments
            total_interest = total_payment - loan_amount

            annual_rental_income = price * (rental_yield_pct / 100.0)
            monthly_rental_income = annual_rental_income / 12.0
            net_monthly_cashflow = monthly_rental_income - monthly_payment

            return {
                "success": True,
                "currency": curr,
                "purchase_price": round(price, 2),
                "down_payment": round(down_payment, 2),
                "loan_principal": round(loan_amount, 2),
                "monthly_mortgage_payment": round(monthly_payment, 2),
                "total_interest_cost": round(total_interest, 2),
                "loan_term_years": years,
                "interest_rate_pct": rate_pct,
                "projected_annual_rent": round(annual_rental_income, 2),
                "projected_net_monthly_cashflow": round(net_monthly_cashflow, 2),
                "rental_yield_pct": rental_yield_pct,
                "five_year_total_rental_return": round(annual_rental_income * 5, 2)
            }

        elif name == "book_consultation_or_viewing":
            booking = lead_service.create_booking(
                client_name=arguments.get("client_name", ""),
                email=arguments.get("email", ""),
                phone=arguments.get("phone"),
                property_id=arguments.get("property_id"),
                property_name=arguments.get("property_name"),
                preferred_datetime=arguments.get("preferred_datetime"),
                notes=arguments.get("notes")
            )
            return {
                "success": True,
                "message": f"Consultation scheduled successfully! Booking Reference: {booking['booking_reference']}.",
                "booking": booking
            }

        elif name == "check_golden_visa_and_residency":
            country = arguments.get("country", "")
            amount_usd = float(arguments.get("investment_amount_usd", 0))

            if "United Arab Emirates" in country or "UAE" in country or "Dubai" in country:
                aed_equiv = amount_usd * 3.6725
                is_eligible = aed_equiv >= 2000000
                return {
                    "success": True,
                    "country": "United Arab Emirates",
                    "investment_usd": amount_usd,
                    "investment_aed": round(aed_equiv, 2),
                    "threshold_aed": 2000000,
                    "is_eligible": is_eligible,
                    "visa_type": "10-Year Renewable UAE Golden Visa",
                    "benefits": [
                        "100% foreign business ownership",
                        "Residency for investor, spouse, children & domestic staff",
                        "No minimum stay requirement in UAE to maintain visa",
                        "0% personal income & capital gains tax"
                    ]
                }
            elif "Saudi Arabia" in country:
                sar_equiv = amount_usd * 3.75
                is_eligible = sar_equiv >= 4000000
                return {
                    "success": True,
                    "country": "Saudi Arabia",
                    "investment_usd": amount_usd,
                    "investment_sar": round(sar_equiv, 2),
                    "threshold_sar": 4000000,
                    "is_eligible": is_eligible,
                    "visa_type": "Saudi Real Estate Owner Premium Residency",
                    "benefits": [
                        "Permanent / Extended residency without a Saudi sponsor",
                        "Exemption from expat levy fees",
                        "Right to own property throughout the Kingdom (including Makkah/Madinah leaseholds)",
                        "Seamless visa-free entry and exit"
                    ]
                }
            elif "Oman" in country:
                omr_equiv = amount_usd * 0.385
                is_eligible = omr_equiv >= 250000
                return {
                    "success": True,
                    "country": "Oman",
                    "investment_usd": amount_usd,
                    "is_eligible": is_eligible,
                    "visa_type": "5-10 Year Oman Investor Residency",
                    "benefits": [
                        "Freehold property ownership at AIDA Muscat",
                        "Family residency sponsorship",
                        "0% personal income tax"
                    ]
                }
            else:
                return {
                    "success": True,
                    "country": country,
                    "message": f"Residency schemes for {country} vary by EU/national guidelines."
                }

        return {"success": False, "error": f"Unknown tool: {name}"}

    except Exception as e:
        logger.error(f"Error in tool {name}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
