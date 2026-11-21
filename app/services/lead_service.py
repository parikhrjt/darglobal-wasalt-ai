"""
Lead & Consultation Booking Service
Captures prospective buyer details, scheduled VIP private viewings, and investor consultations.
"""

import datetime
import json
import logging
import os
import uuid
from typing import Dict, List, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class LeadService:
    def __init__(self, leads_file: str = settings.LEADS_DATA_PATH):
        self.leads_file = leads_file
        os.makedirs(os.path.dirname(leads_file) if os.path.dirname(leads_file) else ".", exist_ok=True)
        self.leads: List[Dict] = []
        self._load()

    def _load(self):
        if os.path.exists(self.leads_file):
            try:
                with open(self.leads_file, "r", encoding="utf-8") as f:
                    self.leads = json.load(f)
            except Exception as e:
                logger.error(f"Error loading leads file: {e}")
                self.leads = []
        else:
            self.leads = []

    def _save(self):
        try:
            with open(self.leads_file, "w", encoding="utf-8") as f:
                json.dump(self.leads, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save leads: {e}")

    def create_booking(
        self,
        client_name: str,
        email: str,
        phone: Optional[str] = None,
        property_id: Optional[str] = None,
        property_name: Optional[str] = None,
        preferred_datetime: Optional[str] = None,
        budget_range: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict:
        booking_ref = f"DG-{uuid.uuid4().hex[:6].upper()}"
        now_iso = datetime.datetime.now().isoformat()
        
        record = {
            "booking_reference": booking_ref,
            "client_name": client_name,
            "email": email,
            "phone": phone or "N/A",
            "property_id": property_id,
            "property_name": property_name or "General Portfolio Advisory",
            "preferred_datetime": preferred_datetime or "Earliest Executive Slot",
            "budget_range": budget_range or "Not specified",
            "notes": notes or "Requested via DarGlobal AI Agentic Assistant",
            "status": "Confirmed / Priority Route to Senior Consultant",
            "created_at": now_iso
        }

        self.leads.append(record)
        self._save()
        logger.info(f"New lead recorded: {booking_ref} for {client_name}")
        return record

    def list_leads(self, limit: int = 50) -> List[Dict]:
        return list(reversed(self.leads))[:limit]

lead_service = LeadService()
