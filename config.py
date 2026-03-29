import os
import json
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量
load_dotenv()

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = os.getenv('DATA_DIR', str(BASE_DIR / 'instance' / 'data'))
CONVERSATION_DATA_DIR = os.path.join(DATA_DIR, 'conversation_data')

class Config:
    # Flask 配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev临时密钥')

    # SQLAlchemy 配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{DATA_DIR}/sessions.db')  # 统一使用sessions.db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI 配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # 必填
    OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://yibuapi.com/v1')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')
    
    # 会话配置 - 确保这些配置正确
    SESSION_TYPE = 'sqlalchemy'
    SESSION_SQLALCHEMY = None  # 将在app.py中设置
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = 3600 * 2  # 2小时
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    EXAM_MAX_TURNS = 40
    EXAM_TIME_LIMIT = 50 * 60  # 50分钟，单位秒
    CONVERSATION_DATA_DIR = os.path.join(DATA_DIR, 'conversations')
    
    @staticmethod
    def init_dirs():
        """确保所有必要的目录存在"""
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        os.makedirs(Config.SESSION_FILE_DIR, exist_ok=True)
        os.makedirs(Config.CONVERSATION_DATA_DIR, exist_ok=True)

    # 数据目录配置
    DATA_DIR = DATA_DIR
    SESSION_FILE_DIR = os.path.join(DATA_DIR, 'sessions')
    CONVERSATIONS_DB_PATH = os.path.join(DATA_DIR, 'conversations.db')  # 明确指定对话数据库路径

    @classmethod
    def init_dirs(cls):
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(cls.SESSION_FILE_DIR, exist_ok=True)
        os.makedirs(cls.CONVERSATION_DATA_DIR, exist_ok=True)
        client_data_file = os.path.join(DATA_DIR, 'client_data.json')
        if not os.path.exists(client_data_file):
            with open(client_data_file, 'w') as f:
                json.dump({}, f)


Config.init_dirs()

class ProductionConfig(Config):
    # Render生产环境专用配置
    SESSION_TYPE = 'sqlalchemy'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # 数据库连接池配置
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'pool_recycle': 3600  # 30分钟回收连接
    }

class DevelopmentConfig(Config):
    # 开发环境配置
    SESSION_TYPE = 'sqlalchemy'
    SESSION_COOKIE_SECURE = False
    DEBUG = True

current_env = os.getenv('RENDER', 'development')  # Render平台会设置RENDER环境变量
if current_env.lower() == 'true':
    config = ProductionConfig()
else:
    config = DevelopmentConfig()

# 对话管理配置
class ConversationConfig:
    # 阶段转换阈值
    STAGE_TRANSITION = {
        'defensive_to_exploratory': 8,  # 8轮后进入试探期
        'exploratory_to_open': 15       # 15轮后进入开放期
    }
    
    # 记忆管理
    MEMORY_COMPRESSION = {
        'enable': True,
        'interval': 5,           # 每5轮压缩一次
        'max_memories': 3,       # 保留最近3个关键记忆
        'summary_length': 50     # 摘要最大长度
    }
    
    # 响应生成
    RESPONSE_SETTINGS = {
        'max_retries': 2,
    }

class BaseConfig:
    # 共享配置项
    MAX_CONVERSATION_TURNS = 100
    DATA_DIR = DATA_DIR  # 使用统一的DATA_DIR
    
    @classmethod
    def get_config(cls):
        """返回当前配置字典"""
        return {
            key: value 
            for key, value in cls.__dict__.items() 
            if not key.startswith('_') and not callable(value)
        }

class APIConfig(BaseConfig):
    # API专用配置
    API_VERSION = "0.1.0"
    API_TITLE = "AI来访者模拟器API"
    API_KEYS = os.getenv('API_KEYS', '').split(',')
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_WINDOW = 60
    MAX_REQUESTS_PER_WINDOW = 60

class AppConfig(BaseConfig):
    # 应用配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev临时密钥')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://yibuapi.com/v1')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')
    SESSION_TYPE = 'sqlalchemy'

