"""
session_history.py
------------------
Manages persistent session history for multi-session support.

History is keyed by (client_id, counselor_id), stored as:
  data/session_history/{client_id}__{counselor_id}.json

This lets the same AI client build separate relationship histories
with different counselors-in-training.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from mongo_store import mongo_store


DATA_DIR = os.getenv(
    'DATA_DIR',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'data')
)
HISTORY_DIR = os.path.join(DATA_DIR, 'session_history')

DEFAULT_COUNSELOR = 'default'


def _ensure_dirs():
    os.makedirs(HISTORY_DIR, exist_ok=True)


def _safe(s: str) -> str:
    return "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in (s or DEFAULT_COUNSELOR))


def _history_file(client_id: str, counselor_id: str = DEFAULT_COUNSELOR) -> str:
    _ensure_dirs()
    return os.path.join(HISTORY_DIR, f"{_safe(client_id)}__{_safe(counselor_id)}.json")


def _load(client_id: str, counselor_id: str = DEFAULT_COUNSELOR) -> Dict[str, Any]:
    mongo_data = mongo_store.load_session_history(client_id, counselor_id)
    if mongo_data:
        return mongo_data

    path = _history_file(client_id, counselor_id)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "client_id": client_id,
        "counselor_id": counselor_id,
        "sessions": [],
        "cross_session_summary": ""
    }


def _dump(client_id: str, counselor_id: str, data: Dict[str, Any]):
    mongo_store.save_session_history(data)
    path = _history_file(client_id, counselor_id)
    tmp = path + '.tmp'
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def save_session(client_id: str, session_id: str, conversation: List[Dict],
                 report: Optional[Dict] = None, summary: str = "",
                 counselor_id: str = DEFAULT_COUNSELOR) -> Dict[str, Any]:
    """Save a completed session. Returns the saved record."""
    history = _load(client_id, counselor_id)

    user_turns = [m for m in conversation if m.get('role') == 'user']
    ai_turns   = [m for m in conversation if m.get('role') in ('ai', 'assistant')]

    session_num = len(history["sessions"]) + 1
    record = {
        "session_id":       session_id,
        "session_number":   session_num,
        "counselor_id":     counselor_id,
        "timestamp":        datetime.now().isoformat(),
        "date_display":     datetime.now().strftime('%Y-%m-%d %H:%M'),
        "total_user_turns": len(user_turns),
        "total_ai_turns":   len(ai_turns),
        "conversation":     conversation,
        "report":           report,
        "session_summary":  summary
    }

    history["sessions"].append(record)

    # Recursive cross-session summary
    if summary:
        prev = history.get("cross_session_summary", "")
        block = f"【第{session_num}次咨询摘要】{summary}"
        history["cross_session_summary"] = (prev + "\n\n" + block).strip()

    _dump(client_id, counselor_id, history)
    return record


def get_session_list(client_id: str,
                     counselor_id: str = DEFAULT_COUNSELOR) -> List[Dict[str, Any]]:
    """Return past sessions (without full conversation) for display."""
    history = _load(client_id, counselor_id)
    return [
        {
            "session_id":       s.get("session_id", ""),
            "session_number":   s.get("session_number", i + 1),
            "timestamp":        s.get("timestamp", ""),
            "date_display":     s.get("date_display", ""),
            "total_user_turns": s.get("total_user_turns", 0),
            "session_summary":  s.get("session_summary", ""),
            "has_report":       bool(s.get("report"))
        }
        for i, s in enumerate(history.get("sessions", []))
    ]


def get_session_count(client_id: str,
                      counselor_id: str = DEFAULT_COUNSELOR) -> int:
    return len(_load(client_id, counselor_id).get("sessions", []))


def get_cross_session_summary(client_id: str,
                               counselor_id: str = DEFAULT_COUNSELOR) -> str:
    """Accumulated recursive summary of all past sessions for this counselor."""
    return _load(client_id, counselor_id).get("cross_session_summary", "")


def get_session_detail(client_id: str, session_id: str,
                       counselor_id: str = DEFAULT_COUNSELOR) -> Optional[Dict[str, Any]]:
    """Full session record including conversation."""
    for s in _load(client_id, counselor_id).get("sessions", []):
        if s.get("session_id") == session_id:
            return s
    return None


def get_last_session(client_id: str,
                     counselor_id: str = DEFAULT_COUNSELOR) -> Optional[Dict[str, Any]]:
    """Most recent session for this client-counselor pair."""
    sessions = _load(client_id, counselor_id).get("sessions", [])
    return sessions[-1] if sessions else None
