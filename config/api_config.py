# API专用配置文件
import os
from dotenv import load_dotenv

load_dotenv()

class APIConfig:
    # API版本控制
    API_VERSION = "1.0.0"
    API_TITLE = "AI来访者模拟器API"
    API_DESCRIPTION = "提供AI来访者模拟的RESTful API服务"
    
    # 认证配置
    API_KEYS = os.getenv('API_KEYS', '').split(',')  # 从环境变量读取多个API密钥
    REQUIRED_API_KEY = len(API_KEYS) > 0  # 是否强制要求API密钥
    
    # 限流配置
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_WINDOW = 60  # 时间窗口(秒)
    MAX_REQUESTS_PER_WINDOW = 60  # 每个窗口最大请求数
    MAX_CONVERSATION_TURNS = 100  # 最大对话轮次设置为100
    
    # 跨域配置
    CORS_ENABLED = True
    ALLOWED_ORIGINS = ["*"]
    
    # 日志配置
    API_LOG_FILE = "logs/api.log"
    MAX_LOG_SIZE = 1024 * 1024 * 10  # 10MB
    LONG_CONVERSATION_SETTINGS = {
        'memory_compression_interval': 10,  # 每10轮压缩一次记忆
        'max_history_length': 50,          # 保留的最大历史记录长度
        'summary_enabled': True           # 启用自动摘要
    }
    
    @classmethod
    def get_config(cls):
        """返回当前配置字典"""
        config = {
            key: value 
            for key, value in cls.__dict__.items() 
            if not key.startswith('_') and not callable(value)
        }
        
        # 合并长对话配置到主配置
        config.update(cls.LONG_CONVERSATION_SETTINGS)
        return config