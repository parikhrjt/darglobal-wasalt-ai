"""
Master Agentic Controller
Orchestrates OpenRouter LLM interactions, tool routing, conversation context,
and resilient zero-downtime execution.
"""

import json
import logging
from typing import Any, Dict, List, Optional
from app.agent.tools import AGENT_TOOLS, execute_tool
from app.agent.openrouter import openrouter_client, SYSTEM_PROMPT
from app.agent.memory import memory_manager
from app.agent.fallback_engine import deterministic_engine
from app.config import settings

logger = logging.getLogger(__name__)

class RealEstateAgent:
    """Senior AI Agentic Real Estate Consultant for DarGlobal and Wasalt."""

    async def chat(
        self,
        session_id: str,
        message: str,
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        logger.info(f"Session {session_id} received message: '{message[:80]}...'")
        
        # Save user message to session memory
        memory_manager.add_message(session_id, "user", message)
        history = memory_manager.get_history(session_id)

        chosen_model = model or settings.OPENROUTER_MODEL
        key = api_key or settings.OPENROUTER_API_KEY

        tools_executed = []
        cards = []
        final_text = ""
        engine_label = ""

        # 1. Attempt OpenRouter Live Model Execution if API key is present
        if key:
            try:
                messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}] + history

                completion = await openrouter_client.chat_completion(
                    messages=messages_payload,
                    tools=AGENT_TOOLS,
                    model=chosen_model,
                    override_key=key
                )

                if completion and "choices" in completion and len(completion["choices"]) > 0:
                    choice = completion["choices"][0]
                    msg_obj = choice.get("message", {})
                    tool_calls = msg_obj.get("tool_calls")

                    if tool_calls:
                        logger.info(f"OpenRouter requested {len(tool_calls)} tool call(s).")
                        # Add assistant tool intent message
                        messages_payload.append(msg_obj)

                        for tc in tool_calls:
                            func = tc.get("function", {})
                            fn_name = func.get("name")
                            fn_args_raw = func.get("arguments", "{}")
                            try:
                                fn_args = json.loads(fn_args_raw) if isinstance(fn_args_raw, str) else fn_args_raw
                            except Exception:
                                fn_args = {}

                            tool_res = execute_tool(fn_name, fn_args)
                            tools_executed.append({"tool": fn_name, "args": fn_args, "output": tool_res})

                            # Extract cards for UI
                            if fn_name == "search_properties" and tool_res.get("properties"):
                                cards.extend(tool_res.get("properties", []))
                            elif fn_name == "compare_properties" and tool_res.get("comparison"):
                                cards.extend(tool_res.get("comparison", []))
                            elif fn_name == "get_property_details" and tool_res.get("property"):
                                cards.append(tool_res.get("property"))

                            # Append tool response message for LLM synthesis
                            messages_payload.append({
                                "role": "tool",
                                "tool_call_id": tc.get("id", "call_1"),
                                "name": fn_name,
                                "content": json.dumps(tool_res)
                            })

                        # Second pass: synthesize final response with tool outputs
                        synthesis = await openrouter_client.chat_completion(
                            messages=messages_payload,
                            tools=None,
                            model=chosen_model,
                            override_key=key
                        )

                        if synthesis and "choices" in synthesis and len(synthesis["choices"]) > 0:
                            final_text = synthesis["choices"][0]["message"].get("content", "")
                            engine_label = f"{chosen_model} (OpenRouter Live)"
                    else:
                        final_text = msg_obj.get("content", "")
                        engine_label = f"{chosen_model} (OpenRouter Live)"

            except Exception as e:
                logger.warning(f"Error during OpenRouter execution: {e}. Cascading to fallback.", exc_info=True)

        # 2. Resilient Deterministic Engine Fallback (Zero-Downtime)
        if not final_text:
            logger.info("Executing via Deterministic Agentic Property Brain.")
            fallback_res = deterministic_engine.process(message, history)
            final_text = fallback_res["text"]
            tools_executed = fallback_res.get("tools_used", [])
            cards = fallback_res.get("cards", [])
            engine_label = "DarGlobal Real Estate Agentic Brain (Deterministic Mode)"

        # Save assistant message to session memory
        memory_manager.add_message(session_id, "assistant", final_text)

        # Deduplicate cards
        seen_ids = set()
        deduped_cards = []
        for c in cards:
            cid = c.get("id")
            if cid and cid not in seen_ids:
                seen_ids.add(cid)
                deduped_cards.append(c)

        return {
            "session_id": session_id,
            "response": final_text,
            "engine": engine_label,
            "tools_executed": tools_executed,
            "cards": deduped_cards[:4]
        }

agent = RealEstateAgent()
