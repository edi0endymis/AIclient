"""
API版本1模块
"""
from flask import Blueprint
from .client import api_blueprint

# 版本信息
API_VERSION = "1.0.0"
API_STATUS = "beta"

# 创建版本蓝图
v1_blueprint = Blueprint('v1', __name__)
v1_blueprint.register_blueprint(api_blueprint)

__all__ = ['v1_blueprint', 'API_VERSION', 'API_STATUS']