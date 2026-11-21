"""
Conversation Session & Context Memory Manager
Maintains multi-turn context and investor preferences across sessions.
"""

import logging
import time
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, max_history_per_session: int = 12):
        self.max_history = max_history_per_session
        self.sessions: Dict[str, List[Dict]] = {}
        self.session_timestamps: Dict[str, float] = {}

    def get_history(self, session_id: str) -> List[Dict]:
        return self.sessions.get(session_id, [])

    def add_message(self, session_id: str, role: str, content: str, **kwargs):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        
        msg = {"role": role, "content": content}
        for k, v in kwargs.items():
            if v is not None:
                msg[k] = v

        self.sessions[session_id].append(msg)
        self.session_timestamps[session_id] = time.time()

        # Prune if too long
        if len(self.sessions[session_id]) > self.max_history * 2:
            self.sessions[session_id] = self.sessions[session_id][-self.max_history * 2:]

    def clear(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.session_timestamps:
            del self.session_timestamps[session_id]

memory_manager = MemoryManager()
