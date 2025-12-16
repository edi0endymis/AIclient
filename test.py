import unittest
from memory.utils import similarity, call_memories, date_to_text, messages_to_text, remove_think, calculate_length_change
from memory.types import EventMemory
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam
from openai.types.chat.chat_completion_assistant_message_param import ChatCompletionAssistantMessageParam
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam


class TestUtils(unittest.TestCase):

    def test_similarity(self):
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [4.0, 5.0, 6.0]
        result = similarity(vec1, vec2)
        self.assertAlmostEqual(result, 0.974631846, places=6)

    def test_call_memories(self):
        memories = [
            EventMemory(id="1", content="Memory 1", vector=[0.1, 0.2, 0.3], chat_start_time=0, chat_end_time=0),
            EventMemory(id="2", content="Memory 2", vector=[0.4, 0.5, 0.6], chat_start_time=0, chat_end_time=0),
            EventMemory(id="3", content="Memory 3", vector=[0.7, 0.8, 0.9], chat_start_time=0, chat_end_time=0)
        ]
        query_vector = [0.1, 0.2, 0.3]
        result = call_memories(memories=memories, query_vector=query_vector)
        self.assertTrue(len(result) > 0)

    def test_date_to_text(self):
        timestamp = 1745376209345
        result = date_to_text(timestamp)
        self.assertEqual(result, '2025年4月23日 星期三 10点43分')

    def test_messages_to_text(self):
        messages: list[ChatCompletionMessageParam] = [
            ChatCompletionUserMessageParam(role="user", content="Hello"),
            ChatCompletionAssistantMessageParam(role="assistant", content="Hi there!")
        ]
        result = messages_to_text(messages)
        self.assertIn("1. 来访者: Hello", result)
        self.assertIn("2. 咨询师: Hi there!", result)

    def test_remove_think(self):
        text = "This is a test <think>hidden content</think> end."
        result = remove_think(text)
        self.assertEqual(result, "This is a test  end.")
        text = '<think>\nhidden content\n</think>\nend.'
        text_expected = '\nend.'
        result = remove_think(text)
        self.assertEqual(result, text_expected)

    def test_calculate_length_change(self):
        result = calculate_length_change(tokens_pressure=0.85, old_history_length_reduce=5)
        self.assertEqual(result, 7)

if __name__ == "__main__":
    unittest.main()
