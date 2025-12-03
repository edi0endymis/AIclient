import unittest
from unittest.mock import Mock
from ai_role_simulator import AIRoleSimulator

class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.simulator = AIRoleSimulator(self.mock_client)

    def test_response_generation(self):
        test_msg = [{"role": "user", "content": "你好"}]
        result = self.simulator.generate_response(test_msg)
        self.assertIsInstance(result, str)