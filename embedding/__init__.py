from transformers import AutoModel # type: ignore
from threading import Lock
from typing import Any
from random import random


__all__ = ['Embedding', 'EmbeddingTest']


DEFAULT_MODEL_PATH = '/root/autodl-tmp/embedding/jina-embeddings-v3'


class EmbeddingTest:
    '''
    ## 文本嵌入向量, 具有内置的锁机制

    用于测试, 向量为随机生成
    '''
    def __init__(self):
        pass

    def embedding_api(self, text: str) -> list[float]:
        embedding: list[float] = []
        for _ in range(1024):
            embedding.append(random())
        return embedding


class Embedding:
    '''
    ## 文本嵌入向量, 具有内置的锁机制
    '''
    model: Any
    lock: Lock

    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True) # type: ignore
        self.lock = Lock()

    def embedding_api(self, text: str) -> list[float]:
        embedding: list[float] = []
        self.lock.acquire()
        try:
            embeddings = self.model.encode(
                [text],
                task='text-matching',
            )
            embedding = embeddings[0].tolist()
        finally:
            self.lock.release()

        return embedding
