"""
Property Catalog & Filtering Service
Manages property data structures, currency conversions, and catalog queries.
"""

import json
import logging
import os
from typing import Dict, List, Optional
from app.config import settings

logger = logging.getLogger(__name__)

CURRENCY_RATES = {
    "USD": 1.0,
    "AED": 3.6725,
    "SAR": 3.75,
    "GBP": 0.80,
    "EUR": 0.93
}

class PropertyService:
    def __init__(self):
        self.properties: List[Dict] = []
        self._load_data()

    def _load_data(self):
        path = settings.CONSOLIDATED_DATA_PATH
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.properties = json.load(f)
                logger.info(f"PropertyService initialized with {len(self.properties)} properties.")
            except Exception as e:
                logger.error(f"Error loading consolidated properties: {e}")
                self.properties = []
        else:
            logger.warning(f"Consolidated file not found at {path}, attempting rebuild...")
            from scraper.run_scrapers import consolidate_datasets
            self.properties = consolidate_datasets()

    def get_all(self, source: Optional[str] = None, limit: int = 50) -> List[Dict]:
        if source:
            filtered = [p for p in self.properties if p.get("source", "").lower() == source.lower()]
            return filtered[:limit]
        return self.properties[:limit]

    def get_by_id(self, prop_id: str) -> Optional[Dict]:
        for p in self.properties:
            if p.get("id") == prop_id:
                return p
        return None

    def filter(
        self,
        query: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        source: Optional[str] = None,
        min_price_usd: Optional[float] = None,
        max_price_usd: Optional[float] = None,
        bedrooms: Optional[int] = None,
        brand_partner: Optional[str] = None,
        property_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        results = []
        q_tokens = query.lower().split() if query else []

        for p in self.properties:
            # Source check (DarGlobal vs Wasalt)
            if source and p.get("source", "").lower() != source.lower():
                continue

            # Country check
            if country and country.lower() not in p.get("country", "").lower():
                continue

            # City check
            if city and city.lower() not in p.get("city", "").lower() and city.lower() not in p.get("neighborhood", "").lower():
                continue

            # Brand partner check
            if brand_partner and brand_partner.lower() not in p.get("brand_partner", "").lower():
                continue

            # Property type check
            if property_type:
                match_type = any(property_type.lower() in pt.lower() for pt in p.get("property_types", []))
                if not match_type:
                    continue

            # Bedroom check
            if bedrooms is not None:
                br_list = p.get("bedrooms_list", [])
                if br_list and not any(b >= bedrooms for b in br_list):
                    continue

            # Price bounds
            price = p.get("price_usd", 0)
            if min_price_usd and price < min_price_usd:
                continue
            if max_price_usd and price > max_price_usd:
                continue

            # Free-text token score
            score = 0
            if q_tokens:
                tokens_text = p.get("search_tokens", "")
                name_text = p.get("name", "").lower()
                desc_text = p.get("description", "").lower()

                for token in q_tokens:
                    if token in name_text:
                        score += 5
                    elif token in tokens_text:
                        score += 3
                    elif token in desc_text:
                        score += 1
                if score == 0:
                    continue
            else:
                score = 1

            p_copy = dict(p)
            p_copy["_relevance"] = score
            results.append(p_copy)

        results.sort(key=lambda x: x.get("_relevance", 0), reverse=True)
        return results[:limit]

    def convert_currency(self, amount: float, from_curr: str, to_curr: str) -> float:
        from_curr = from_curr.upper()
        to_curr = to_curr.upper()
        if from_curr not in CURRENCY_RATES or to_curr not in CURRENCY_RATES:
            return amount
        usd = amount / CURRENCY_RATES[from_curr]
        return round(usd * CURRENCY_RATES[to_curr], 2)

    def get_summary_stats(self) -> Dict:
        dg_count = sum(1 for p in self.properties if p.get("source") == "DarGlobal")
        ws_count = sum(1 for p in self.properties if p.get("source") == "Wasalt")
        cities = list(set(p.get("city") for p in self.properties if p.get("city")))
        brands = list(set(p.get("brand_partner") for p in self.properties if p.get("brand_partner") and p.get("brand_partner") != "Wasalt Verified Marketplace"))
        return {
            "total_properties": len(self.properties),
            "darglobal_developments": dg_count,
            "wasalt_listings": ws_count,
            "cities": sorted(cities),
            "luxury_brand_partners": sorted(brands)
        }

property_service = PropertyService()
