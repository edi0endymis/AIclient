from functools import wraps
from flask import request, jsonify, current_app
import time
from datetime import datetime

def validate_api_key(f):
    """
    API密钥验证装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从配置中获取有效API密钥
        valid_keys = current_app.config.get('API_KEYS', [])
        
        # 如果没有配置API密钥，则跳过验证
        if not valid_keys:
            return f(*args, **kwargs)
            
        # 从请求头或JSON中获取API密钥
        api_key = request.headers.get('X-API-KEY') or (request.json.get('api_key') if request.json else None)
        
        if api_key not in valid_keys:
            return jsonify({
                "error": "无效的API密钥",
                "status": 401
            }), 401
            
        return f(*args, **kwargs)
    return decorated_function

def rate_limit(f):
    """
    简单的速率限制装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 获取客户端IP
        client_ip = request.remote_addr
        
        # 初始化速率限制字典
        if not hasattr(current_app, 'rate_limits'):
            current_app.rate_limits = {}
            
        # 检查速率限制
        now = time.time()
        window = current_app.config.get('RATE_LIMIT_WINDOW', 60)  # 默认60秒窗口
        max_requests = current_app.config.get('MAX_REQUESTS_PER_WINDOW', 60)  # 默认60次/窗口
        
        # 初始化或更新客户端记录
        if client_ip not in current_app.rate_limits:
            current_app.rate_limits[client_ip] = {
                'count': 1,
                'start_time': now
            }
        else:
            # 如果超出时间窗口，重置计数器
            if now - current_app.rate_limits[client_ip]['start_time'] > window:
                current_app.rate_limits[client_ip] = {
                    'count': 1,
                    'start_time': now
                }
            else:
                current_app.rate_limits[client_ip]['count'] += 1
                
                # 如果超出限制，返回错误
                if current_app.rate_limits[client_ip]['count'] > max_requests:
                    return jsonify({
                        "error": "请求过于频繁",
                        "retry_after": window - (now - current_app.rate_limits[client_ip]['start_time'])
                    }), 429
                    
        return f(*args, **kwargs)
    return decorated_function

