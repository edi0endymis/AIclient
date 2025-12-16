# code/chat.py
"""
Main chat logic integrating:
- SummaryMemory
- Long-term Memory
- Prompt building pipeline

This file is called by the backend API.
"""

from __future__ import annotations
from typing import List, Dict, Any
import uuid

from memory.summary import SummaryMemory
from memory.memory import Memory
from memory.utils import clean_text, now_timestamp

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def _extract_namespace(messages: List[Dict[str, Any]]) -> str:
    """
    Try to read client_id or session id from messages.
    Fallback: auto generate.
    """
    for m in messages:
        if "client_id" in m:
            return str(m["client_id"])
        if "namespace" in m:
            return str(m["namespace"])
    return "session_" + uuid.uuid4().hex[:8]


def build_full_prompt(
    summary_memory: SummaryMemory,
    long_memory: Memory,
    user_message: str
) -> str:
    """
    Combine:
    - summary
    - retrieved long-term memories
    - recent messages
    - new user message
    """
    # 1) summary + short-term history
    base_text = summary_memory.build_prompt()

    # 2) search long-term memory
    recalled = long_memory.search(user_message, top_k=5)
    mem_block = ""
    if recalled:
        mem_block += "【相关长期记忆】\n"
        for r in recalled:
            mem_block += f"- {r['text']}\n"

    # 3) new incoming user query
    new_msg = f"\n【当前用户消息】\n用户: {user_message}\n"

    final_prompt = ""
    if base_text:
        final_prompt += base_text + "\n\n"
    if mem_block:
        final_prompt += mem_block + "\n"
    final_prompt += new_msg

    return final_prompt.strip()


# ------------------------------------------------------------
# Main chat interface
# ------------------------------------------------------------

def chat(model: str, messages: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
    """
    The main function called by backend routes.

    messages format example:
    [
        {"role": "user", "content": "...", "client_id": "abc"},
        {"role": "assistant", "content": "..."},
        ...
    ]

    Returns:
        {
            "role": "assistant",
            "content": "...",
            "debug": {...}
        }
    """

    # ------------------------------------------------------------
    # 1. Determine namespace
    # ------------------------------------------------------------
    namespace = _extract_namespace(messages)
    summary_mem = SummaryMemory(namespace=namespace)
    long_mem = Memory(namespace=namespace)

    # ------------------------------------------------------------
    # 2. Reconstruct conversation into summary module
    # ------------------------------------------------------------
    for m in messages[:-1]:  # except the newest one
        summary_mem.add_message(m["role"], clean_text(m["content"]))

    # newest user message:
    user_msg = clean_text(messages[-1]["content"])
    summary_mem.add_message("user", user_msg)

    # ------------------------------------------------------------
    # 3. Build prompt from summary + memory
    # ------------------------------------------------------------
    prompt = build_full_prompt(
        summary_memory=summary_mem,
        long_memory=long_mem,
        user_message=user_msg
    )

    # ------------------------------------------------------------
    # 4. Call model（此处保留你的项目原有的模型调用）
    # ------------------------------------------------------------
    # 如果你的项目是通过 OpenAI API 调用大模型，这里应该替换成相应代码
    #
    # 我保留一个稳定的 placeholder：
    assistant_reply = fake_local_model_answer(prompt)

    # ------------------------------------------------------------
    # 5. 写入长期记忆（写入：AI 回复）
    # ------------------------------------------------------------
    long_mem.add(
        text=f"AI回复: {assistant_reply}",
        meta={"type": "assistant", "timestamp": now_timestamp()}
    )

    # ------------------------------------------------------------
    # 6. 返回并让前端继续渲染
    # ------------------------------------------------------------
    return {
        "role": "assistant",
        "content": assistant_reply,
        "debug": {
            "namespace": namespace,
            "prompt_used": prompt,
            "long_term_memory_count": long_mem.count()
        }
    }


# ------------------------------------------------------------
# Placeholder model
# 你未来可以换成真实大模型调用
# ------------------------------------------------------------
def fake_local_model_answer(prompt: str) -> str:
    """
    Simple placeholder response. Replace with real model call.
    """
    return f"(AI已接收信息)\n{prompt[:200]} ..."


if __name__ == "__main__":
    # quick manual test
    msgs = [
        {"role": "user", "content": "你好，我喜欢猫", "client_id": "demo1"},
        {"role": "assistant", "content": "你好，我是AI"},
        {"role": "user", "content": "我今天去了上海动物园"}
    ]
    print(chat("dummy", msgs))
