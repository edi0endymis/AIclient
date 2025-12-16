from dataclasses import dataclass
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam


@dataclass
class EventMemory:
    '''
    ## 事件记忆

    - `id`: 该条事件记忆的唯一标识符 (UUID)
    - `content`: 事件记忆的内容
    - `vector`: 事件记忆的向量表示
    - `chat_start_time`: 事件记忆所属对话的开始时间 (**毫秒级**时间戳)
    - `chat_end_time`: 事件记忆所属对话的结束时间 (**毫秒级**时间戳)

    ### 使用示例

    ```python
    from .memory import EventMemory
    from .embedding import Embedding
    import uuid
    import time

    # 创建一个嵌入对象
    emb = Embedding()
    # 假设的事件记忆内容
    text = '来访者最近感到焦虑和失眠'
    # 假设本次咨询发生在 4 小时前
    start_time = int(time.time() * 1000 - 1000 * 60 * 60 * 4) 
    # 假设本次咨询结束在 2 小时前
    end_time = int(time.time() * 1000 - 1000 * 60 * 60 * 2)
    # 创建一个事件记忆
    memory = EventMemory(
        id=str(uuid.uuid4()),
        content=text,
        vector=emb.embedding_api(text),
        chat_start_time=start_time,
        chat_end_time=end_time,
    )
    ```
    '''
    id: str
    content: str
    vector: list[float]
    chat_start_time: int
    chat_end_time: int


@dataclass
class ChatResult:
    output_messages: list[ChatCompletionMessageParam]
    new_history_messages_length_reduce: int
    new_memo_calls: list[str]
