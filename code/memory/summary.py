# code/memory/summary.py
"""
Conversation summarization memory.
Purpose:
- Keep a short, always-updated summary of the full conversation.
- When messages grow too long, collapse older history into summaries.
- Works together with long-term Memory to store stable knowledge.

Usage:
    sm = SummaryMemory(namespace="chat123")
    sm.add_message("user", "hello")
    sm.add_message("assistant", "hi, how can I help?")
    text = sm.build_prompt()  # returns summarized history for LM
"""

from __future__ import annotations
import time
import uuid
from typing import List, Dict, Any, Optional
from .memory import Memory

MAX_MESSAGES_BEFORE_SUMMARY = 12       # 触发总结的对话轮次
MAX_RUNNING_TEXT = 1800                # 触发总结的纯文本长度
MAX_SUMMARY_LENGTH = 500               # 摘要的最大长度（字符）


def _now_ms() -> int:
    return int(time.time() * 1000)


class SummaryMemory:
    """
    Maintains running messages + auto summary.
    Stores 3 parts:
        1. messages: recent messages, short-lived
        2. summary: summary of older messages
        3. long-term memory: via Memory(namespace)
    """

    def __init__(self, namespace: str = "default"):
        self.namespace = namespace
        self.summary_text: str = ""   # current accumulated summary
        self.messages: List[Dict[str, str]] = []  # [{role, content}]
        self.memory = Memory(namespace=namespace)

    # ------------------------------------------------------------
    # Add a message to running buffer
    # ------------------------------------------------------------
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

        if self._should_summarize():
            self._perform_summarization()

    # ------------------------------------------------------------
    # Decide whether to summarize
    # ------------------------------------------------------------
    def _should_summarize(self) -> bool:
        if len(self.messages) >= MAX_MESSAGES_BEFORE_SUMMARY:
            return True
        total_len = sum(len(m["content"]) for m in self.messages)
        if total_len >= MAX_RUNNING_TEXT:
            return True
        return False

    # ------------------------------------------------------------
    # Helper to make text safe for summary
    # ------------------------------------------------------------
    def _trim(self, text: str, limit: int) -> str:
        if len(text) <= limit:
            return text
        return text[:limit] + "..."

    # ------------------------------------------------------------
    # Summarize the recent messages + existing summary_text
    # ------------------------------------------------------------
    def _perform_summarization(self):
        """
        Summaries old messages into summary_text and clear them.
        Then store distilled stable facts into long-term memory.
        """

        full_text = self.summary_text + "\n" + "\n".join(
            f"{m['role']}: {m['content']}" for m in self.messages
        )

        # 生成简短总结（未来可以换成 LLM 调用，这里做简单压缩）
        summary = self._simple_summarize(full_text)
        summary = self._trim(summary, MAX_SUMMARY_LENGTH)

        # 保存更新后的摘要
        self.summary_text = summary

        # 将信息写入长期记忆（摘要不会重复写入，只写“内容事实”）
        self.memory.add(
            text="【对话摘要】" + summary,
            meta={"type": "summary", "timestamp": _now_ms()}
        )

        # 清空短期消息
        self.messages = []

    # ------------------------------------------------------------
    # Simple summary algorithm (placeholder for LLM)
    # ------------------------------------------------------------
    def _simple_summarize(self, text: str) -> str:
        """
        A very coarse summarizer: keep important lines only.
        You can replace this with an actual LLM summarizer later.
        """
        lines = [t.strip() for t in text.split("\n") if t.strip()]
        # Keep first 3 and last 3 lines as "summary window"
        if len(lines) <= 6:
            return "\n".join(lines)
        return "\n".join(lines[:3] + ["..."] + lines[-3:])

    # ------------------------------------------------------------
    # Build prompt for LLM
    # ------------------------------------------------------------
    def build_prompt(self) -> str:
        """
        Returns the combined summary + messages for the model.
        """
        s = ""
        if self.summary_text:
            s += "【过往总结】\n" + self.summary_text + "\n\n"

        if self.messages:
            s += "【近期对话】\n"
            for m in self.messages:
                s += f"{m['role']}: {m['content']}\n"

        return s.strip()

    # ------------------------------------------------------------
    # Export for debug
    # ------------------------------------------------------------
    def export(self) -> Dict[str, Any]:
        return {
            "namespace": self.namespace,
            "summary": self.summary_text,
            "messages": self.messages,
            "long_term_count": self.memory.count(),
        }
