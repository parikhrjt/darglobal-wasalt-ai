"""
Consolidation Pipeline
Merges DarGlobal projects and Wasalt real estate listings into a normalized,
search-optimized knowledge repository for the AI agent.
"""

import json
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def consolidate_datasets(
    darglobal_file: str = "data/darglobal_projects.json",
    wasalt_file: str = "data/wasalt_properties.json",
    output_file: str = "data/consolidated_properties.json"
):
    logger.info("Starting consolidation of DarGlobal and Wasalt datasets...")
    dg_items = []
    ws_items = []

    if os.path.exists(darglobal_file):
        with open(darglobal_file, "r", encoding="utf-8") as f:
            dg_items = json.load(f)
            logger.info(f"Loaded {len(dg_items)} DarGlobal developments.")

    if os.path.exists(wasalt_file):
        with open(wasalt_file, "r", encoding="utf-8") as f:
            ws_items = json.load(f)
            logger.info(f"Loaded {len(ws_items)} Wasalt listings.")

    consolidated = []

    # Normalize DarGlobal records
    for item in dg_items:
        norm = {
            "id": item.get("id"),
            "source": "DarGlobal",
            "name": item.get("name"),
            "brand_partner": item.get("brand_partner", "DarGlobal Signature"),
            "property_types": item.get("property_types", ["Luxury Residence"]),
            "city": item.get("location", {}).get("city", "International"),
            "country": item.get("location", {}).get("country", ""),
            "neighborhood": item.get("location", {}).get("neighborhood", ""),
            "bedrooms_display": f"{min(item.get('bedrooms', [1]))} - {max(item.get('bedrooms', [4]))} BR" if isinstance(item.get("bedrooms"), list) else f"{item.get('bedrooms')} BR",
            "bedrooms_list": item.get("bedrooms", []),
            "bathrooms_display": f"{min(item.get('bathrooms', [2]))} - {max(item.get('bathrooms', [5]))} Baths" if isinstance(item.get("bathrooms"), list) else f"{item.get('bathrooms')} Baths",
            "area_display": f"{item.get('area_sqft', {}).get('min', 0):,} - {item.get('area_sqft', {}).get('max', 0):,} sq ft",
            "area_sqft_min": item.get("area_sqft", {}).get("min", 0),
            "price_usd": item.get("price", {}).get("starting_price_usd", 0),
            "price_aed": item.get("price", {}).get("starting_price_aed", 0),
            "price_sar": item.get("price", {}).get("starting_price_sar", 0),
            "price_gbp": item.get("price", {}).get("starting_price_gbp", 0),
            "price_eur": item.get("price", {}).get("starting_price_eur", 0),
            "payment_plan": item.get("payment_plan", "Flexible Developer Installments"),
            "completion_status": item.get("completion_status", "Off-Plan"),
            "completion_date": item.get("completion_date", "TBA"),
            "amenities": item.get("amenities", []),
            "description": item.get("description", ""),
            "projected_roi_pct": item.get("investment_highlights", {}).get("projected_roi_pct", 8.0),
            "golden_visa_eligible": item.get("investment_highlights", {}).get("golden_visa_eligible", True),
            "hero_image_url": item.get("hero_image_url", ""),
            "url": item.get("official_url", "https://darglobal.co.uk"),
            "search_tokens": " ".join([
                item.get("name", ""),
                item.get("brand_partner", ""),
                item.get("location", {}).get("city", ""),
                item.get("location", {}).get("neighborhood", ""),
                item.get("location", {}).get("country", ""),
                " ".join(item.get("amenities", [])),
                " ".join(item.get("property_types", []))
            ]).lower()
        }
        consolidated.append(norm)

    # Normalize Wasalt records
    for item in ws_items:
        norm = {
            "id": item.get("id"),
            "source": "Wasalt",
            "name": item.get("name"),
            "brand_partner": "Wasalt Verified Marketplace",
            "property_types": [item.get("property_type", "Residential")],
            "city": item.get("location", {}).get("city", "Saudi Arabia"),
            "country": "Saudi Arabia",
            "neighborhood": item.get("location", {}).get("neighborhood", ""),
            "bedrooms_display": f"{item.get('bedrooms')} BR" if item.get("bedrooms") else "Commercial",
            "bedrooms_list": [item.get("bedrooms")] if item.get("bedrooms") else [],
            "bathrooms_display": f"{item.get('bathrooms')} Baths",
            "area_display": f"{item.get('area_sqm', 0)} sqm ({item.get('area_sqft', 0):,} sq ft)",
            "area_sqft_min": item.get("area_sqft", 0),
            "price_usd": item.get("price", {}).get("price_usd", 0),
            "price_aed": item.get("price", {}).get("price_aed", 0),
            "price_sar": item.get("price", {}).get("price_sar", 0),
            "price_gbp": item.get("price", {}).get("price_gbp", 0),
            "price_eur": item.get("price", {}).get("price_eur", 0),
            "payment_plan": "Cash / Saudi Mortgage Bank Financing Ready",
            "completion_status": "Ready to Move In",
            "completion_date": "Completed",
            "amenities": item.get("features", []),
            "description": item.get("description", ""),
            "projected_roi_pct": 8.5,
            "golden_visa_eligible": False,
            "rega_license_id": item.get("rega_license_id", "REGA-Verified"),
            "is_verified": item.get("is_verified", True),
            "hero_image_url": item.get("image_url", ""),
            "url": item.get("wasalt_url", "https://wasalt.com"),
            "search_tokens": " ".join([
                item.get("name", ""),
                item.get("property_type", ""),
                item.get("location", {}).get("city", ""),
                item.get("location", {}).get("neighborhood", ""),
                "Saudi Arabia",
                " ".join(item.get("features", []))
            ]).lower()
        }
        consolidated.append(norm)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(consolidated, f, indent=2, ensure_ascii=False)

    logger.info(f"Consolidation complete: {len(consolidated)} total properties indexed in {output_file}.")
    return consolidated

if __name__ == "__main__":
    consolidate_datasets()
