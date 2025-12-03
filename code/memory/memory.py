# code/memory/memory.py
"""
Long-term memory storage (file-backed, per-namespace).
- Stores memory items as JSON array in data_memory/{namespace}.json
- Each item: { "id": str, "text": str, "timestamp": int(ms), "meta": dict }
- Safe atomic writes (write tmp -> os.replace)
- Simple search based on token overlap + recency bonus.
- API:
    mem = Memory(namespace="default")
    mem.add("User likes cats", meta={"source":"chat"})
    mem.search("cats", top_k=5)
    mem.all()
    mem.delete(item_id)
    mem.clear()
"""
from __future__ import annotations
import os
import json
import time
import uuid
from typing import List, Dict, Optional, Any

# Storage directory (relative to project root). Make sure this exists.
STORAGE_DIR = os.path.join(os.getcwd(), "data_memory")
os.makedirs(STORAGE_DIR, exist_ok=True)

def _now_ms() -> int:
    return int(time.time() * 1000)

def _safe_filename(name: str) -> str:
    # keep alnum, -, _
    return "".join(ch for ch in name if ch.isalnum() or ch in ("_", "-")) or "default"

class MemoryItem:
    def __init__(self, id: str, text: str, timestamp: int, meta: Optional[Dict[str, Any]] = None):
        self.id = id
        self.text = text
        self.timestamp = int(timestamp)
        self.meta = meta or {}

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "text": self.text, "timestamp": self.timestamp, "meta": self.meta}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "MemoryItem":
        return MemoryItem(id=d.get("id"), text=d.get("text", ""), timestamp=int(d.get("timestamp", _now_ms())), meta=d.get("meta", {}) or {})

class Memory:
    def __init__(self, namespace: str = "default"):
        """
        namespace -> file: data_memory/{safe_namespace}.json
        """
        self.namespace = namespace or "default"
        self.filename = os.path.join(STORAGE_DIR, f"{_safe_filename(self.namespace)}.json")
        self._items: List[MemoryItem] = []
        self._load()

    # ------------------------
    # persistence
    # ------------------------
    def _load(self):
        self._items = []
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r", encoding="utf-8") as f:
                    arr = json.load(f)
                    if isinstance(arr, list):
                        for d in arr:
                            try:
                                self._items.append(MemoryItem.from_dict(d))
                            except Exception:
                                # skip corrupt entry but continue load others
                                continue
        except Exception:
            # on any error, keep memory empty but don't crash
            self._items = []

    def _save(self):
        # atomic write: write to tmp and replace
        tmp = f"{self.filename}.tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump([it.to_dict() for it in self._items], f, ensure_ascii=False, indent=2)
            os.replace(tmp, self.filename)
        except Exception:
            # if saving fails, best-effort: remove tmp if exists
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except Exception:
                pass

    # ------------------------
    # public API
    # ------------------------
    def add(self, text: str, meta: Optional[Dict[str, Any]] = None, id: Optional[str] = None) -> MemoryItem:
        """
        Add a memory item. If id not given, auto-generate uuid4 hex.
        Returns the MemoryItem stored.
        """
        if text is None:
            text = ""
        id_val = id or uuid.uuid4().hex
        ts = _now_ms()
        item = MemoryItem(id=id_val, text=str(text), timestamp=ts, meta=meta or {})
        # append to end (newest at end)
        self._items.append(item)
        # persist
        self._save()
        return item

    def all(self) -> List[Dict[str, Any]]:
        """
        Return all memory items as list of dicts (sorted by timestamp ascending).
        """
        return [it.to_dict() for it in sorted(self._items, key=lambda x: x.timestamp)]

    def count(self) -> int:
        return len(self._items)

    def clear(self):
        """
        Remove all items for this namespace (persisted).
        """
        self._items = []
        self._save()

    def delete(self, id: str) -> bool:
        """
        Delete item by id. Returns True if removed.
        """
        orig = len(self._items)
        self._items = [it for it in self._items if it.id != id]
        if len(self._items) != orig:
            self._save()
            return True
        return False

    # ------------------------
    # searching / recall
    # ------------------------
    def _tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        # simple whitespace + punctuation split, lowercase
        toks = []
        cur = []
        for ch in text.lower():
            if ch.isalnum():
                cur.append(ch)
            else:
                if cur:
                    toks.append("".join(cur))
                    cur = []
        if cur:
            toks.append("".join(cur))
        return toks

    def _score_by_overlap(self, query: str, item: MemoryItem) -> float:
        # overlap score between query and item text
        q_toks = set(self._tokenize(query))
        i_toks = set(self._tokenize(item.text))
        if not q_toks:
            return 0.0
        inter = q_toks.intersection(i_toks)
        base = len(inter) / max(len(q_toks), 1)
        return float(base)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search memories by a simple heuristic: token overlap + recency bonus.
        Returns up to top_k items as dicts sorted by score desc.
        If no meaningful hits, returns most recent items (best-effort).
        """
        if not query and top_k > 0:
            # return most recent items
            res = sorted(self._items, key=lambda x: x.timestamp, reverse=True)[:top_k]
            return [r.to_dict() for r in res]

        now_ms = _now_ms()
        scored = []
        q_toks = set(self._tokenize(query))
        for it in self._items:
            base = self._score_by_overlap(query, it)
            # recency bonus: linear decay over 30 days (in ms)
            age_ms = max(0, now_ms - it.timestamp)
            thirty_days_ms = 1000 * 60 * 60 * 24 * 30
            recency = max(0.0, 1.0 - (age_ms / float(thirty_days_ms)))
            score = base + 0.2 * recency  # small weight to recency
            if score > 0:
                scored.append((score, it))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = [it.to_dict() for score, it in scored[:top_k]]
        if not results:
            # fallback: return up to top_k most recent
            results = [it.to_dict() for it in sorted(self._items, key=lambda x: x.timestamp, reverse=True)[:top_k]]
        return results

    # ------------------------
    # helper: export / import (useful for admin / testing)
    # ------------------------
    def export_json(self) -> str:
        """
        Return JSON string of all items (pretty-printed).
        """
        return json.dumps(self.all(), ensure_ascii=False, indent=2)

    def import_json(self, json_str: str, overwrite: bool = False) -> int:
        """
        Load items from a JSON string. If overwrite True, replace existing items.
        Returns number of imported items.
        """
        try:
            arr = json.loads(json_str)
            if not isinstance(arr, list):
                return 0
            new_items = []
            for d in arr:
                try:
                    new_items.append(MemoryItem.from_dict(d))
                except Exception:
                    continue
            if overwrite:
                self._items = new_items
            else:
                # append
                self._items.extend(new_items)
            self._save()
            return len(new_items)
        except Exception:
            return 0

# convenience factory
def get_memory(namespace: str = "default") -> Memory:
    return Memory(namespace=namespace)

if __name__ == "__main__":
    # simple CLI for ad-hoc testing
    m = Memory(namespace="cli_test")
    print("Count before:", m.count())
    m.add("这是一个测试记忆: 我喜欢猫", meta={"source": "cli"})
    print("Count after add:", m.count())
    print("Search '猫' ->", m.search("猫", top_k=4))
    print("All ->", m.all()[:5])
