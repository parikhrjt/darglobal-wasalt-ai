"""
OpenRouter API Client
Provides integration with OpenRouter's free models, supporting tool calling,
streaming, error handling, and multi-turn conversations.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional
import httpx
from app.config import settings
from app.agent.tools import AGENT_TOOLS

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are the Senior AI Agentic Real Estate Consultant for DarGlobal and Wasalt.
DarGlobal is an elite London Stock Exchange-listed developer specializing in ultra-luxury co-branded residences (Trump Organization, Pagani, Missoni, Aston Martin, Elie Saab, Lamborghini, Fendi Casa, Mouawad) across Dubai, Saudi Arabia, Oman, Qatar, and Spain.
Wasalt (وصلت) is Saudi Arabia's premier REGA-licensed digital proptech platform for verified residential and commercial listings.

Your core objectives:
1. Act as an articulate, highly sophisticated private wealth property advisor.
2. Maintain bilingual fluency: seamlessly converse in English or Arabic depending on user preference.
3. Proactively utilize your available tools:
   - Use `search_properties` to locate matching developments and listings.
   - Use `get_property_details` when deep technical/payment plan specs are required.
   - Use `compare_properties` when a user mentions two or more projects.
   - Use `calculate_mortgage_and_roi` to provide financial models and cashflow analyses.
   - Use `check_golden_visa_and_residency` when international buyers ask about residency or citizenship by investment.
   - Use `book_consultation_or_viewing` to capture qualified investor leads.
4. Always present currency figures clearly (USD, AED, SAR, GBP, EUR).
5. Tone: Executive, polite, deeply knowledgeable, authoritative, and welcoming.
"""

class OpenRouterClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = api_key or settings.OPENROUTER_API_KEY
        self.model = model or settings.OPENROUTER_MODEL
        self.base_url = settings.OPENROUTER_BASE_URL

    def get_headers(self, override_key: Optional[str] = None) -> Dict[str, str]:
        key = override_key or self.api_key
        headers = {
            "Content-Type": "application/json",
            "HTTP-Referer": settings.SITE_URL,
            "X-Title": settings.SITE_NAME,
        }
        if key:
            headers["Authorization"] = f"Bearer {key}"
        return headers

    async def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict]] = None,
        model: Optional[str] = None,
        override_key: Optional[str] = None,
        temperature: float = 0.4
    ) -> Optional[Dict[str, Any]]:
        """Sends chat completion request to OpenRouter API."""
        key = override_key or self.api_key
        if not key:
            logger.info("No OpenRouter API key provided; will route to Deterministic Agentic Engine.")
            return None

        chosen_model = model or self.model
        headers = self.get_headers(key)

        payload = {
            "model": chosen_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1500
        }

        # Include tools if specified
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                logger.info(f"Dispatching query to OpenRouter (Model: {chosen_model})...")
                res = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )

                if res.status_code == 200:
                    data = res.json()
                    logger.info("OpenRouter response received successfully.")
                    return data
                elif res.status_code == 429:
                    logger.warning(f"OpenRouter rate limit hit (429) on model {chosen_model}. Falling back to Local Agentic Engine.")
                    return None
                elif res.status_code in (401, 403):
                    logger.warning(f"OpenRouter authentication error ({res.status_code}). Check API key.")
                    return None
                else:
                    logger.warning(f"OpenRouter returned status {res.status_code}: {res.text}")
                    return None
        except httpx.RequestError as exc:
            logger.warning(f"Network error communicating with OpenRouter: {exc}")
            return None
        except Exception as exc:
            logger.error(f"Unexpected error in OpenRouterClient: {exc}", exc_info=True)
            return None

openrouter_client = OpenRouterClient()
