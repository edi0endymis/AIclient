"""
API模块入口
"""
from flask import Blueprint

api_blueprint = Blueprint('api', __name__)

# 导入所有版本API
from .v1 import api_blueprint as v1_blueprint

# 注册版本路由
api_blueprint.register_blueprint(v1_blueprint, url_prefix='/v1')

__all__ = ['api_blueprint']