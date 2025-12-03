import unittest
import json
from unittest.mock import patch
from flask import Flask
from flask_testing import TestCase
from ..app import app, client_manager
from ..ai_role_simulator.data import base_profile

class APITestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        # 创建测试客户端
        self.client = app.test_client()
        
        # 添加测试来访者
        self.test_client_id = "test_client_123"
        client_manager.clients[self.test_client_id] = {
            "id": self.test_client_id,
            "name": "测试来访者",
            "issue": "测试问题",
            "role_data": {
                "base_profile": base_profile,
                "dynamic_state": {
                    "咨询记录": {"当前阶段": "防御期", "总次数": 0},
                    "心理特征": {"核心情绪": ["测试情绪"]}
                },
                "interaction_rules": {}
            },
            "created_at": "2023-01-01T00:00:00"
        }

    def tearDown(self):
        # 清理测试来访者
        if self.test_client_id in client_manager.clients:
            del client_manager.clients[self.test_client_id]

    def test_get_client_list(self):
        """测试获取来访者列表API"""
        response = self.client.get('/api/v1/client/list')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['count'], 1)

    def test_get_client_response(self):
        """测试获取来访者响应API"""
        test_data = {
            "client_id": self.test_client_id,
            "conversation": [
                {"role": "user", "content": "你好"}
            ]
        }
        
        # 使用mock替代真实的OpenAI调用
        with patch('openai.ChatCompletion.create') as mock_create:
            mock_create.return_value.choices[0].message.content = "测试响应"
            
            response = self.client.post(
                '/api/v1/client/response',
                data=json.dumps(test_data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['response'], "测试响应")
            self.assertEqual(data['client_id'], self.test_client_id)

    def test_invalid_client_id(self):
        """测试无效来访者ID的情况"""
        test_data = {
            "client_id": "invalid_id",
            "conversation": [{"role": "user", "content": "你好"}]
        }
        
        response = self.client.post(
            '/api/v1/client/response',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_missing_required_field(self):
        """测试缺少必要字段的情况"""
        test_data = {"conversation": []}  # 缺少client_id
        
        response = self.client.post(
            '/api/v1/client/response',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

if __name__ == '__main__':
    unittest.main()