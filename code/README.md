# 第三版模型对应记忆模块

本代码库实现了一个记忆模块 `memory` 和向量化模块 `embedding`, 用于来访者与模型之间的对话和记忆生成

- `Python` 版本要求: `3.12` 及以上
- 项目依赖
  - `openai` (仅用于 `memory` 模块)
  - `pdoc` (仅用于文档生成)
  - `transformers` (仅用于 `embedding` 模块)
- 项目管理: `uv`
- 虚拟环境: `venv`
- 运行单元测试: `uv run test.py`
- 运行文档生成: `uv run docs.py`
- 运行模拟对话: `uv run chat.py`

## 目录

- [第三版模型对应记忆模块](#第三版模型对应记忆模块)
  - [目录](#目录)
  - [`embedding` 模块](#embedding-模块)
  - [`memory` 模块](#memory-模块)
  - [测试](#测试)

## `embedding` 模块

- `Embedding`: 具有内置锁机制的嵌入类
- `EmbeddingTest`: 嵌入测试类, 向量为 `1024` 位随机浮点数

```python
from .embedding import Embedding, EmbeddingTest

# 默认模型地址为 '/root/autodl-tmp/embedding/jina-embeddings-v3'
embedding = Embedding()
# 也可以指定模型地址
embedding = Embedding(model_path='/path/to/model')
# 用于测试的嵌入类
embedding_test = EmbeddingTest()

# 向量化
text = '待向量化的文本'
vector = embedding.embedding_api(text)
```

## `memory` 模块

- `EventMemory`: 事件记忆 `dataclass` **(详见 `memory/types.py` 中的文档注释)**
- `chat`: 对话函数 **(详见 `memory/chat.py` 中的文档注释)**
- `update_user_info`: 更新用户画像函数 **(详见 `memory/memory.py` 中的文档注释)**
- `update_summary`: 更新对话内总结函数 **(详见 `memory/summary.py` 中的文档注释)**

> 注: 在 `VSCode`、`PyCharm` 等 IDE 中, 鼠标悬停在函数名上, 即可查看函数的文档注释

## 测试

🚧
