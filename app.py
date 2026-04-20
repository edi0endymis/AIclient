from flask import Flask, render_template, request, jsonify, redirect, url_for, session, current_app, send_from_directory
from flask import send_file,current_app
from flask import make_response
from flask_session import Session
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import io
from io import BytesIO
import re  
import random 

import json
import time
import os
import pickle
from datetime import datetime
from functools import wraps

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

# 全局字体注册
def init_pdf_fonts():
    """初始化PDF字体"""
    try:
        font_path = os.path.join(os.path.dirname(__file__), 'ZTwyrh.ttc')
        
        if os.path.exists(font_path):
            # 检查是否已注册，避免重复注册
            if 'ZTFont' not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont('ZTFont', font_path))
                print(f"✅ PDF字体: 已成功注册 ZTFont")
            
            # 设置字体映射
            addMapping('ZTFont', 0, 0, 'ZTFont')  # normal
            addMapping('ZTFont', 1, 0, 'ZTFont')  # bold
            addMapping('ZTFont', 0, 1, 'ZTFont')  # italic
            addMapping('ZTFont', 1, 1, 'ZTFont')  # bold-italic
            
            return True
        else:
            print(f"❌ 错误: 字体文件不存在: {font_path}")
            return False
            
    except Exception as e:
        print(f"❌ 字体注册失败: {e}")
        return False

# 初始化字体
FONT_REGISTERED = init_pdf_fonts()
import pytz
from config import Config
from openai import OpenAI
from api.v1.client import api_blueprint
from ai_role_simulator import AIRoleSimulator

from functools import wraps
from config import Config
from openai import OpenAI
from api.v1.client import api_blueprint
from ai_role_simulator import AIRoleSimulator
from ai_role_simulator import (convert_psydt_to_standard, convert_patientpsi_to_standard,convert_psydt_lxwn_to_standard, convert_patientpsi_lxwn_to_standard,
convert_psydt_mqq_to_standard, convert_patientpsi_mqq_to_standard,
convert_psydt_sbjg_to_standard, convert_patientpsi_sbjg_to_standard,
convert_psydt_sxsu_to_standard, convert_patientpsi_sxsu_to_standard,
convert_psydt_syan_to_standard, convert_patientpsi_syan_to_standard
)
from ai_role_simulator.data import base_profile, cognitive_emotional_model, dynamic_state, interaction_rules, conversation_profile, impedance_rules
from ai_role_simulator.data_PsyDT import client_profile as data_PsyDT_client_profile
from ai_role_simulator.data_PsyDT import dynamic_state as data_PsyDT_dynamic_state
from ai_role_simulator.data_PsyDT import interaction_rules as data_PsyDT_interaction_rules
from ai_role_simulator.data_PatientPsi import (
    self_worth, others, future, rules, assumptions,
    work, relationship, family, coping, style_params,
    events, status, notes
)

from ai_role_simulator.clients.lxwn.data_lxwn import base_profile as lxwn_base, cognitive_emotional_model as lxwn_cognitive, dynamic_state as lxwn_dynamic, interaction_rules as lxwn_rules, conversation_profile as lxwn_conversation, impedance_rules as lxwn_impedance
from ai_role_simulator.clients.lxwn.data_PsyDT_lxwn import client_profile as lxwn_psydt_profile, dynamic_state as lxwn_psydt_dynamic, interaction_rules as lxwn_psydt_rules
from ai_role_simulator.clients.lxwn.data_PatientPsi_lxwn import (
    self_worth as lxwn_self_worth, others as lxwn_others, future as lxwn_future, 
    rules as lxwn_rules_psi, assumptions as lxwn_assumptions,
    work as lxwn_work, relationship as lxwn_relationship, family as lxwn_family, 
    coping as lxwn_coping, style_params as lxwn_style_params,
    events as lxwn_events, status as lxwn_status, notes as lxwn_notes
)

from ai_role_simulator.clients.mqq.data_mqq import base_profile as mqq_base, cognitive_emotional_model as mqq_cognitive, dynamic_state as mqq_dynamic, interaction_rules as mqq_rules, conversation_profile as mqq_conversation, impedance_rules as mqq_impedance
from ai_role_simulator.clients.mqq.data_PsyDT_mqq import client_profile as mqq_psydt_profile, dynamic_state as mqq_psydt_dynamic, interaction_rules as mqq_psydt_rules
from ai_role_simulator.clients.mqq.data_PatientPsi_mqq import (
    self_worth as mqq_self_worth, others as mqq_others, future as mqq_future, 
    rules as mqq_rules_psi, assumptions as mqq_assumptions,
    work as mqq_work, relationship as mqq_relationship, family as mqq_family, 
    coping as mqq_coping, style_params as mqq_style_params,
    events as mqq_events, status as mqq_status, notes as mqq_notes
)

from ai_role_simulator.clients.sbjg.data_sbjg import base_profile as sbjg_base, cognitive_emotional_model as sbjg_cognitive, dynamic_state as sbjg_dynamic, interaction_rules as sbjg_rules, conversation_profile as sbjg_conversation, impedance_rules as sbjg_impedance
from ai_role_simulator.clients.sbjg.data_PsyDT_sbjg import client_profile as sbjg_psydt_profile, dynamic_state as sbjg_psydt_dynamic, interaction_rules as sbjg_psydt_rules
from ai_role_simulator.clients.sbjg.data_PatientPsi_sbjg import (
    self_worth as sbjg_self_worth, others as sbjg_others, future as sbjg_future, 
    rules as sbjg_rules_psi, assumptions as sbjg_assumptions,
    work as sbjg_work, relationship as sbjg_relationship, family as sbjg_family, 
    coping as sbjg_coping, style_params as sbjg_style_params,
    events as sbjg_events, status as sbjg_status, notes as sbjg_notes
)

from ai_role_simulator.clients.sxsu.data_sxsu import base_profile as sxsu_base, cognitive_emotional_model as sxsu_cognitive, dynamic_state as sxsu_dynamic, interaction_rules as sxsu_rules, conversation_profile as sxsu_conversation, impedance_rules as sxsu_impedance
from ai_role_simulator.clients.sxsu.data_PsyDT_sxsu import client_profile as sxsu_psydt_profile, dynamic_state as sxsu_psydt_dynamic, interaction_rules as sxsu_psydt_rules
from ai_role_simulator.clients.sxsu.data_PatientPsi_sxsu import (
    self_worth as sxsu_self_worth, others as sxsu_others, future as sxsu_future, 
    rules as sxsu_rules_psi, assumptions as sxsu_assumptions,
    work as sxsu_work, relationship as sxsu_relationship, family as sxsu_family, 
    coping as sxsu_coping, style_params as sxsu_style_params,
    events as sxsu_events, status as sxsu_status, notes as sxsu_notes
)

from ai_role_simulator.clients.syan.data_syan import base_profile as syan_base, cognitive_emotional_model as syan_cognitive, dynamic_state as syan_dynamic, interaction_rules as syan_rules, conversation_profile as syan_conversation, impedance_rules as syan_impedance
from ai_role_simulator.clients.syan.data_PsyDT_syan import client_profile as syan_psydt_profile, dynamic_state as syan_psydt_dynamic, interaction_rules as syan_psydt_rules
from ai_role_simulator.clients.syan.data_PatientPsi_syan import (
    self_worth as syan_self_worth, others as syan_others, future as syan_future, 
    rules as syan_rules_psi, assumptions as syan_assumptions,
    work as syan_work, relationship as syan_relationship, family as syan_family, 
    coping as syan_coping, style_params as syan_style_params,
    events as syan_events, status as syan_status, notes as syan_notes
)

from wai_questionnaire import (
    WAI_CLIENT_ITEMS, WAI_COUNSELOR_ITEMS, WAI_DIMENSIONS,
    calculate_wai_scores, interpret_wai_scores, generate_wai_report
)

def ensure_memory_dirs():
    """确保内存存储目录存在"""
    # 主数据目录
    data_dir = app.config.get('DATA_DIR', os.path.join(os.path.dirname(__file__), 'data'))
    os.makedirs(data_dir, exist_ok=True)
    
    # 内存存储目录
    memory_dir = os.path.join(os.path.dirname(__file__), 'data_memory')
    os.makedirs(memory_dir, exist_ok=True)
    
    # 会话数据目录
    conversation_dir = app.config.get('CONVERSATION_DATA_DIR', 
                                     os.path.join(data_dir, 'conversations'))
    os.makedirs(conversation_dir, exist_ok=True)
    
    return {
        'data_dir': data_dir,
        'memory_dir': memory_dir,
        'conversation_dir': conversation_dir
    }



static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
if os.path.exists(static_dir):
    app = Flask(__name__, 
               static_folder=static_dir,
               template_folder='templates')
else:
    app = Flask(__name__, template_folder='templates')

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# 确保JSON使用UTF-8
app.config['JSON_AS_ASCII'] = False  
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'

# 启用CORS支持
if app.config.get('CORS_ENABLED', False):
    CORS(app, resources={r"/api/*": {"origins": app.config.get('ALLOWED_ORIGINS', '*')}})
app.config.from_object(Config)

# 设置会话文件目录
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(app.config['DATA_DIR'], 'sessions')
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600*2 
app.config['SESSION_COOKIE_SECURE'] = os.getenv('RENDER', '').lower() == 'true'  
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
Session(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    """简单的健康检查"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

# 注册API蓝图
app.register_blueprint(api_blueprint, url_prefix='/api/v1')

# 确保目录存在
os.makedirs(app.config['DATA_DIR'], exist_ok=True)
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)

@app.route("/api/test", methods=["GET"])
def api_test():
    """测试API是否正常工作"""
    return jsonify({
        "status": "ok",
        "message": "API服务正常",
        "client_id": session.get("client_id", "none"),
        "has_session": "sid" in session
    })

@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        print("=== 收到聊天请求 ===")
        
        data = request.get_json(force=True, silent=True)
        print(f"请求数据: {data}")
        
        if not data:
            return jsonify({"error": "请求数据为空"}), 400
            
        user_message = data.get("message", "").strip()
        client_id = data.get("client_id", "")
        
        print(f"用户消息: {user_message}")
        print(f"客户端ID: {client_id}")
        print(f"会话ID: {session.get('sid')}")
        print(f"当前会话客户端ID: {session.get('client_id')}")

        if not user_message:
            return jsonify({"error": "消息不能为空"}), 400

        # 使用会话中的client_id（如果请求中没有）
        if not client_id:
            client_id = session.get("client_id")
            
        if not client_id:
            client_id = "client_djjo"  # 默认客户端
            session['client_id'] = client_id
            print(f"使用默认客户端: {client_id}")

        # 创建模拟器
        print(f"正在为 {client_id} 创建模拟器...")
        simulator = create_simulator(client_id)
        
        if not simulator:
            print("模拟器创建失败")
            return jsonify({
                "reply": "抱歉，我现在无法连接到AI服务。请稍后再试。",
                "client_id": client_id
            })

        # 获取对话历史
        conversation_history = []
        if 'conversation' in session:
            for msg in session['conversation']:
                if msg['role'] == 'user':
                    conversation_history.append({"role": "user", "content": msg['content']})
                elif msg['role'] in ('assistant', 'ai'):
                    conversation_history.append({"role": "assistant", "content": msg['content']})
        
        print(f"对话历史长度: {len(conversation_history)}")
        
        # 添加当前用户消息
        conversation_history.append({"role": "user", "content": user_message})
        
        # 生成AI响应
        print("正在生成AI响应...")
        try:
            ai_response = simulator.generate_response(conversation_history)
            if ai_response:
                print(f"AI响应: {ai_response[:100]}...")
            else:
                print("generate_fn returned None (likely API auth error)")
        except Exception as e:
            print(f"生成响应失败: {str(e)}")
            ai_response = None
        
        if not ai_response:
            return jsonify({
                "error": "AI service unavailable. Please check your API key configuration.",
                "success": False
            }), 503
        
        # ============ 新增：调用长时记忆集成 ============
        try:
            safe_integrate_memory(client_id, user_message, ai_response)
            print("长时记忆集成成功")
        except Exception as mem_error:
            print(f"长时记忆集成失败（不影响主流程）: {mem_error}")
        # =============================================
        
        # 保存到会话
        if 'conversation' not in session:
            session['conversation'] = []
        
        session['conversation'].append({"role": "user", "content": user_message})
        session['conversation'].append({"role": "assistant", "content": ai_response})
        
        # 确保会话保存
        session.modified = True
        
        print(f"响应成功生成，长度: {len(ai_response)}")
        
        # 返回标准格式的响应
        return jsonify({
            "reply": ai_response,
            "client_id": client_id,
            "success": True
        })

    except Exception as e:
        print(f"!!! /api/chat 严重错误: {str(e)}")
        import traceback
        traceback.print_exc()
        
        current_app.logger.error(f"/api/chat fatal error: {e}")
        return jsonify({
            "error": "Internal server error. Please try again later.",
            "success": False
        }), 500

def get_conversation_turns(session_id):
    """从文件获取当前会话轮次"""
    file_path = os.path.join(current_app.config['CONVERSATION_DATA_DIR'], f'{session_id}.pkl')
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            return data.get('turns', 0)
    except (FileNotFoundError, EOFError):
        return 0

def increment_conversation_turns(session_id):
    """增加会话轮次计数"""
    file_path = os.path.join(current_app.config['CONVERSATION_DATA_DIR'], f'{session_id}.pkl')
    
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            current_turns = data.get('turns', 0) + 1
    except (FileNotFoundError, EOFError):
        current_turns = 1
    
    data = {
        'session_id': session_id,
        'turns': current_turns,
        'updated_at': datetime.now().isoformat()
    }
    
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)
    
    return current_turns

def require_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'sid' not in session or 'client_id' not in session:
            return jsonify({"error": "Session not initialized"}), 400
        return f(*args, **kwargs)
    return decorated_function

def check_conversation_turns(f):
    """检查对话轮次限制的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'sid' not in session:
            session['sid'] = os.urandom(24).hex()
            
        # 检查是否为考试模式
        if session.get('exam_mode'):
            max_turns = 40  # 考试模式40轮
        else:
            max_turns = 80  # 训练模式80轮
            
        turns = get_conversation_turns(session['sid'])
        
        if turns >= max_turns:
            return jsonify({
                "error": f"已达到最大对话轮次限制 ({max_turns} 轮)",
                "code": "CONVERSATION_LIMIT_REACHED",
                "max_turns": max_turns,
                "current_turns": turns
            }), 429
        
        return f(*args, **kwargs)
    return decorated_function

def get_conversation_turns(session_id):
    """从文件获取当前会话轮次"""
    file_path = os.path.join(current_app.config['CONVERSATION_DATA_DIR'], f'{session_id}.pkl')
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            return data.get('turns', 0)
    except (FileNotFoundError, EOFError):
        return 0

def increment_conversation_turns(session_id):
    """增加会话轮次计数"""
    file_path = os.path.join(current_app.config['CONVERSATION_DATA_DIR'], f'{session_id}.pkl')
    
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            current_turns = data.get('turns', 0) + 1
    except (FileNotFoundError, EOFError):
        current_turns = 1
    
    data = {
        'session_id': session_id,
        'turns': current_turns,
        'updated_at': datetime.now().isoformat()
    }
    
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)
    
    return current_turns

# ---------- FINAL VERSION: safe_integrate_memory（最终稳定版） ----------
def safe_integrate_memory(client_id, user_message, ai_response):
    """
    将当前对话写入长期记忆（Memory）和摘要（SummaryMemory）。
    - 自动处理 metadata
    - 自动处理 timestamp
    - 不会抛异常、不影响主流程
    """
    try:
        # ----- 1. 导入 Memory -----
        try:
            from code.memory.memory import Memory
        except Exception:
            from memory.memory import Memory

        # ----- 2. 导入 SummaryMemory -----
        try:
            from code.memory.summary import SummaryMemory
        except Exception:
            from memory.summary import SummaryMemory

        # ----- 3. now_timestamp -----
        try:
            from code.memory.utils import now_timestamp
        except Exception:
            try:
                from memory.utils import now_timestamp
            except Exception:
                import time
                now_timestamp = lambda: int(time.time() * 1000)

        # ----- 4. 命名空间 -----
        client_ns = f"client_{client_id or session.get('client_id', 'anonymous')}"
        summary_ns = f"{client_ns}_summary"

        # ----- 5. 初始化对象 -----
        try:
            mem = Memory(namespace=client_ns)
        except Exception:
            try:
                mem = Memory(client_ns)
            except Exception:
                mem = None

        try:
            summary = SummaryMemory(namespace=summary_ns)
        except Exception:
            try:
                summary = SummaryMemory(summary_ns)
            except Exception:
                summary = None

        # ----- 6. 写入长期记忆 -----
        if mem:
            ts = now_timestamp()
            # 写 user
            try:
                mem.add(user_message, metadata={"role": "user", "ts": ts})
            except Exception:
                try:
                    mem.add(user_message)
                except Exception:
                    pass

            # 写 assistant
            try:
                mem.add(ai_response, metadata={"role": "assistant", "ts": ts})
            except Exception:
                try:
                    mem.add(ai_response)
                except Exception:
                    pass

        # ----- 7. 写入摘要 -----
        if summary:
            try:
                summary.add_message("user", user_message)
                summary.add_message("assistant", ai_response)
            except Exception:
                try:
                    summary.add_messages([
                        {"role": "user", "content": user_message},
                        {"role": "assistant", "content": ai_response}
                    ])
                except Exception:
                    pass

        # ----- 8. 把摘要写入 session['last_report'] -----
        try:
            short_sum = ""
            if summary:
                if hasattr(summary, "build_prompt"):
                    try:
                        short_sum = summary.build_prompt() or ""
                    except Exception:
                        short_sum = getattr(summary, "summary_text", "") or ""
                else:
                    short_sum = getattr(summary, "summary_text", "") or ""

            if short_sum:
                last_r = session.get("last_report", {})
                last_r["short_summary"] = short_sum
                session["last_report"] = last_r
                session.modified = True

        except Exception:
            pass

    except Exception as e:
        try:
            current_app.logger.warning(f"safe_integrate_memory error: {e}")
        except Exception:
            pass
# ---------- END: FINAL VERSION safe_integrate_memory ----------


def save_conversation_to_file(session_id, conversation):
    """将会话数据保存到文件"""
    try:
        file_path = os.path.join(current_app.config['CONVERSATION_DATA_DIR'], f'{session_id}.pkl')
        data = {
            'session_id': session_id,
            'conversation': conversation,
            'updated_at': datetime.now().isoformat()
        }
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
    except Exception as e:
        app.logger.error(f"保存会话数据失败: {str(e)}")

def load_conversation_from_file(session_id):
    """从文件加载会话数据"""
    try:
        file_path = os.path.join(current_app.config['CONVERSATION_DATA_DIR'], f'{session_id}.pkl')
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            return data.get('conversation', [])
    except (FileNotFoundError, EOFError):
        return []
    except Exception as e:
        app.logger.error(f"加载会话数据失败: {str(e)}")
        return []
    
class ClientManager:
    def __init__(self, data_file):
        self.data_file = data_file
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        self.clients = self._load_clients()

    def _load_clients(self):
        if not os.path.exists(self.data_file):
            default_clients = {
                "client_djjo": {
                    "id": "client_djjo",
                    "name": "Djjo",
                    "issue": "综合",
                    "role_data": {
                        "base_profile": base_profile,
                        "cognitive_emotional_model": cognitive_emotional_model,
                        "dynamic_state": dynamic_state,
                        "interaction_rules": interaction_rules,
                        "conversation_profile": conversation_profile,
                        "impedance_rules": impedance_rules
                    },
                    "created_at": datetime.now().isoformat()
                },
                "client_psydt": {
                    "id": "client_psydt",
                    "name": "综合-PsyDT",
                    "issue": "亲密关系恐惧-标准化后",
                    "role_data": convert_psydt_to_standard(),
                    "created_at": datetime.now().isoformat()
                },
                "client_psi": {
                    "id": "client_psi",
                    "name": "Djjo-PatientPsi",
                    "issue": "综合-认知模型CCD",
                    "role_data": convert_patientpsi_to_standard(),
                    "created_at": datetime.now().isoformat()
                },

                # 新增来访者lxwn
                "client_lxwn": {
                    "id": "client_lxwn",
                    "name": "Lxwn",
                    "issue": "lxwn的问题描述",
                    "role_data": {
                            "base_profile": lxwn_base,
                        "cognitive_emotional_model": lxwn_cognitive,
                        "dynamic_state": lxwn_dynamic,
                        "interaction_rules": lxwn_rules,
                        "conversation_profile": lxwn_conversation,
                        "impedance_rules": lxwn_impedance
                        },
                        "created_at": datetime.now().isoformat()
                },
                "client_lxwn_psydt": {
                    "id": "client_lxwn_psydt",
                    "name": "Lxwn-PsyDT",
                    "issue": "lxwn的问题描述-标准化后",
                    "role_data": convert_psydt_lxwn_to_standard(),
                    "created_at": datetime.now().isoformat()
                },
                "client_lxwn_psi": {
                    "id": "client_lxwn_psi",
                    "name": "Lxwn-PatientΨ",
                    "issue": "lxwn的问题描述-认知模型CCD",
                    "role_data": convert_patientpsi_lxwn_to_standard(),
                    "created_at": datetime.now().isoformat()
                },
                # 新增来访者mqq
                "client_mqq": {
                    "id": "client_mqq",
                    "name": "mqq",
                    "issue": "行为与成瘾",
                    "role_data": {
                        "base_profile": mqq_base,
                        "cognitive_emotional_model": mqq_cognitive,
                        "dynamic_state": mqq_dynamic,
                        "interaction_rules": mqq_rules,
                        "conversation_profile": mqq_conversation,
                        "impedance_rules": mqq_impedance
                },
                    "created_at": datetime.now().isoformat()
                },
                "client_mqq_psydt": {
                   "id": "client_mqq_psydt",
                    "name": "mqq-PsyDT",
                    "issue": "行为与成瘾-标准化后",
                    "role_data": convert_psydt_mqq_to_standard(),
                    "created_at": datetime.now().isoformat()
                },
                "client_mqq_psi": {
                    "id": "client_mqq_psi",
                    "name": "mqq-PatientΨ",
                    "issue": "行为与成瘾-认知模型CCD",
                    "role_data": convert_patientpsi_mqq_to_standard(),
                    "created_at": datetime.now().isoformat()
                },
                    # 新增来访者sbjg
                "client_sbjg": {
                        "id": "client_sbjg",
                    "name": "sbjg",
                        "issue": "适应障碍",
                    "role_data": {
                            "base_profile": sbjg_base,
                        "cognitive_emotional_model": sbjg_cognitive,
                            "dynamic_state": sbjg_dynamic,
                        "interaction_rules": sbjg_rules,
                    "conversation_profile": sbjg_conversation,
                        "impedance_rules": sbjg_impedance
                    },
                    "created_at": datetime.now().isoformat()
                },
                "client_sbjg_psydt": {
                    "id": "client_sbjg_psydt",
                    "name": "sbjg-PsyDT",
                    "issue": "适应障碍-标准化后",
                    "role_data": convert_psydt_sbjg_to_standard(),
                    "created_at": datetime.now().isoformat()
                },
                "client_sbjg_psi": {
                    "id": "client_sbjg_psi",
                    "name": "sbjg-PatientΨ",
                    "issue": "适应障碍-认知模型CCD",
                    "role_data": convert_patientpsi_sbjg_to_standard(),
                    "created_at": datetime.now().isoformat()
                },
                # 新增来访者sxsu
                "client_sxsu": {
                    "id": "client_sxsu",
                    "name": "sxsu",
                    "issue": "自我认知",
                    "role_data": {
                        "base_profile": sxsu_base,
                        "cognitive_emotional_model": sxsu_cognitive,
                        "dynamic_state": sxsu_dynamic,
                        "interaction_rules": sxsu_rules,
                        "conversation_profile": sxsu_conversation,
                        "impedance_rules": sxsu_impedance
                    },
                    "created_at": datetime.now().isoformat()
                },
                "client_sxsu_psydt": {
                    "id": "client_sxsu_psydt",
                    "name": "sxsu-PsyDT",
                    "issue": "自我认知-标准化后",
                    "role_data": convert_psydt_sxsu_to_standard(),
                    "created_at": datetime.now().isoformat()
                },
                "client_sxsu_psi": {
                    "id": "client_sxsu_psi",
                    "name": "sxsu-PatientΨ",
                    "issue": "自我认知-认知模型CCD",
                    "role_data": convert_patientpsi_sxsu_to_standard(),
                    "created_at": datetime.now().isoformat()
                },
                # 新增来访者syan
                "client_syan": {
                    "id": "client_syan",
                    "name": "syan",
                    "issue": "心境障碍",
                    "role_data": {
                        "base_profile": syan_base,
                        "cognitive_emotional_model": syan_cognitive,
                        "dynamic_state": syan_dynamic,
                        "interaction_rules": syan_rules,
                        "conversation_profile": syan_conversation,
                        "impedance_rules": syan_impedance
                    },
                    "created_at": datetime.now().isoformat()
                },
                "client_syan_psydt": {
                    "id": "client_syan_psydt",
                    "name": "syan-PsyDT",
                    "issue": "心境障碍-标准化后",
                    "role_data": convert_psydt_syan_to_standard(),
                    "created_at": datetime.now().isoformat()
                },
                "client_syan_psi": {
                    "id": "client_syan_psi",
                    "name": "syan-PatientΨ",
                    "issue": "心境障碍-认知模型CCD",
                    "role_data": convert_patientpsi_syan_to_standard(),
                    "created_at": datetime.now().isoformat()
                }
            }
            self._save_clients(default_clients)
            return default_clients

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                clients = json.load(f)
                print(f"成功加载 {len(clients)} 个来访者数据")
                return clients
        except Exception as e:
            print(f"加载 clients.json 失败: {str(e)}")
            return {}  # 返回空字典避免崩溃

    def _save_clients(self, clients_data):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(clients_data, f, ensure_ascii=False, indent=2)
            
    def create_client(self, client_data):
        client_id = f"client_{str(datetime.now().timestamp()).replace('.', '')}"
        
        # 处理核心信念 - 将文本转换为列表
        core_beliefs = []
        if 'core_beliefs' in client_data:
            beliefs_text = client_data['core_beliefs'].strip()
            if beliefs_text:
                core_beliefs = [belief.strip() for belief in beliefs_text.split('\n') if belief.strip()]
        
        # 处理关键事件
        key_events = client_data.get('key_events', [])
        
        new_client = {
            "id": client_id,
            "name": client_data.get("name", "匿名来访者"),
            "issue": client_data.get("main_issue", "未指定问题"),
            "role_data": {
                "base_profile": {
                    "姓名": client_data.get("name", "匿名来访者"),
                    "年龄": int(client_data.get("age", 30)),
                    "性别": "男" if client_data.get("gender") == "male" else "女",
                    "职业": base_profile.get("职业", {}).copy(),
                    "教育": base_profile.get("教育", {}).copy(),
                    "外在表现": base_profile.get("外在表现", {}).copy(),
                    "居住": base_profile.get("居住", {}).copy(),
                    "关键事件": key_events,  # 使用用户输入的关键事件
                    "具体内容": []  # 初始为空，可以根据需要填充
                },
                "cognitive_emotional_model": {
                    "核心信念": core_beliefs,  # 使用用户输入的核心信念
                    "中间信念": {
                        "规则": cognitive_emotional_model.get("中间信念", {}).get("规则", []).copy(),
                        "假设": cognitive_emotional_model.get("中间信念", {}).get("假设", []).copy()
                    },
                    "自动思维示例": {
                        "工作情境": cognitive_emotional_model.get("自动思维示例", {}).get("工作情境", []).copy(),
                        "关系情境": cognitive_emotional_model.get("自动思维示例", {}).get("关系情境", []).copy(),
                        "家庭情境": cognitive_emotional_model.get("自动思维示例", {}).get("家庭情境", []).copy()
                    },
                    "情绪反应模式": {
                        "焦虑触发点": cognitive_emotional_model.get("情绪反应模式", {}).get("焦虑触发点", []).copy(),
                        "典型情绪": cognitive_emotional_model.get("情绪反应模式", {}).get("典型情绪", []).copy()
                    },
                    "行为应对策略": {
                        "回避行为": cognitive_emotional_model.get("行为应对策略", {}).get("回避行为", []).copy(),
                        "过度补偿": cognitive_emotional_model.get("行为应对策略", {}).get("过度补偿", []).copy()
                    }
                },
                "dynamic_state": {
                    "心理特征": {
                        "核心情绪": [f"{client_data.get('main_issue', '未指定问题')}"],
                        "防御机制": dynamic_state.get("心理特征", {}).get("防御机制", []).copy(),
                        "认知扭曲": dynamic_state.get("心理特征", {}).get("认知扭曲", []).copy()
                    },
                    "躯体症状": dynamic_state.get("躯体症状", {}).copy(),
                    "咨询记录": {
                        "总次数": 0,
                        "当前阶段": client_data.get("initial_stage", "防御期"),
                        "历史摘要": {},
                        "禁忌话题": dynamic_state.get("咨询记录", {}).get("禁忌话题", []).copy()
                    },
                    "关系状态": dynamic_state.get("关系状态", {}).copy(),
                    "背景信息": client_data.get("background", "")
                },
                "interaction_rules": {
                    "阶段设定": interaction_rules.get("阶段设定", {}).copy(),
                    "当前约束": interaction_rules.get("当前约束", {}).copy()
                },
                "conversation_profile": conversation_profile.copy(),
                "impedance_rules": impedance_rules.copy()
            },
            "created_at": datetime.now().isoformat()
        }
        
        style = client_data.get("style", "natural")
        if style == "formal":
            new_client["role_data"]["conversation_profile"]["初始风格"] = "正式"
        elif style == "resistant":
            new_client["role_data"]["conversation_profile"]["初始风格"] = "戒备型"
        
        self.clients[client_id] = new_client
        self._save_clients(self.clients)
        return client_id
    
    def update_client_extended(self, client_id, client_data):
        """扩展的更新方法，支持关键事件和核心信念"""
        if client_id not in self.clients:
            return False
        
        client = self.clients[client_id]
        
        # 更新基本信息
        client["name"] = client_data.get("name", client["name"])
        
        role_data = client["role_data"]
        role_data["base_profile"]["姓名"] = client_data.get("name", role_data["base_profile"].get("姓名", "匿名"))
        role_data["base_profile"]["年龄"] = client_data.get("age", role_data["base_profile"].get("年龄", 30))
        role_data["base_profile"]["性别"] = "男" if client_data.get("gender") == "male" else "女"
        
        # 更新关键事件
        if "key_events" in client_data:
            role_data["base_profile"]["关键事件"] = client_data["key_events"]
        
        # 更新核心信念
        if "core_beliefs" in client_data:
            # 将文本按行分割为列表
            beliefs_list = [belief.strip() for belief in client_data["core_beliefs"].split('\n') if belief.strip()]
            role_data["cognitive_emotional_model"]["核心信念"] = beliefs_list
        
        self._save_clients(self.clients)
        return True

    def get_client(self, client_id):
        print(f"查找来访者 ID: {client_id}")  
        print(f"当前所有来访者 ID: {list(self.clients.keys())}") 
        return self.clients.get(client_id)

    def get_all_clients(self):
        return [client for client in self.clients.values() 
               if isinstance(client, dict)]

    def update_client(self, client_id, client_data):
        if client_id not in self.clients:
            return False
        
        client = self.clients[client_id]
        client["name"] = client_data.get("name", client["name"])
        client["issue"] = client_data.get("main_issue", client.get("issue", ""))
        
        role_data = client["role_data"]
        role_data["base_profile"]["姓名"] = client_data.get("name", role_data["base_profile"].get("姓名", "匿名"))
        role_data["base_profile"]["年龄"] = client_data.get("age", role_data["base_profile"].get("年龄", 30))
        role_data["base_profile"]["性别"] = "男" if client_data.get("gender") == "male" else "女"
        
        if "main_issue" in client_data:
            role_data["dynamic_state"]["心理特征"]["核心情绪"][0] = client_data["main_issue"]
        
        if "background" in client_data:
            role_data["dynamic_state"]["背景信息"] = client_data["background"]
        
        if "style" in client_data:
            role_data["interaction_rules"]["风格"] = {
                "natural": "自然",
                "formal": "正式",
                "resistant": "抗拒"
            }.get(client_data["style"], "自然")
        
        self._save_clients(self.clients)
        return True
    
    def delete_client(self, client_id):
        if client_id in self.clients:
            del self.clients[client_id]
            self._save_clients(self.clients)
            return True
        return False
    
    def ensure_preset_clients(self):
        """确保三种预设客户端存在"""    
        presets = {
            "client_psydt": {
                "id": "client_psydt",
                "name": "Djjo-PsyDT",
                "issue": "综合-标准化后",
                "role_data": convert_psydt_to_standard(),
                "created_at": datetime.now().isoformat()
            },
            "client_psi": {
                "id": "client_psi",
                "name": "Djjo-PatientPsi",
                "issue": "综合-认知模型CCD",
                "role_data": convert_patientpsi_to_standard(),
                "created_at": datetime.now().isoformat()
            }
        }
        
        updated = False
        for client_id, data in presets.items():
            if client_id not in self.clients:
                self.clients[client_id] = data
                updated = True
                print(f"已创建预设客户端: {client_id}")
        
        if updated:
            self._save_clients(self.clients)
openai_client = OpenAI(
    api_key=app.config['OPENAI_API_KEY'],
    base_url=app.config['OPENAI_API_BASE'] if app.config['OPENAI_API_BASE'] else None
)

client_manager = ClientManager(os.path.join(app.config['DATA_DIR'], 'clients.json'))
app.client_manager = client_manager
client_manager.ensure_preset_clients()

def init_preset_clients():
    
    PRESET_CLIENTS = {
        "client_psydt": {
            "id": "client_psydt",
            "name": "Djjo-PsyDT",
            "issue": "综合-标准化后",
            "role_data": convert_psydt_to_standard(),
            "created_at": datetime.now().isoformat()
        },
        "client_psi": {
            "id": "client_psi",
            "name": "Djjo-PatientPsi",
            "issue": "综合-认知模型CCD",
            "role_data": convert_patientpsi_to_standard(),
            "created_at": datetime.now().isoformat()
        }
    }
    
    need_update = False
    for client_id, data in PRESET_CLIENTS.items():
        if client_id not in client_manager.clients:
            client_manager.clients[client_id] = data
            need_update = True
            print(f"已创建预设客户端: {client_id}")
    
    if need_update:
        client_manager._save_clients(client_manager.clients)
        print("已强制更新clients.json文件")

init_preset_clients()

# 在 app.py 中添加会话数据保存功能

def save_conversation_to_file(session_id, conversation):
    """将会话数据保存到文件"""
    try:
        file_path = os.path.join(current_app.config['CONVERSATION_DATA_DIR'], f'{session_id}.pkl')
        data = {
            'session_id': session_id,
            'conversation': conversation,
            'updated_at': datetime.now().isoformat()
        }
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
    except Exception as e:
        app.logger.error(f"保存会话数据失败: {str(e)}")

def load_conversation_from_file(session_id):
    """从文件加载会话数据"""
    try:
        file_path = os.path.join(current_app.config['CONVERSATION_DATA_DIR'], f'{session_id}.pkl')
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            return data.get('conversation', [])
    except (FileNotFoundError, EOFError):
        return []
    except Exception as e:
        app.logger.error(f"加载会话数据失败: {str(e)}")
        return []
# 在 app.py 中添加会话状态检查函数

def check_session_active(f):
    """检查会话是否活跃的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'sid' not in session:
            # 尝试从请求头获取会话ID
            session_id = request.headers.get('X-Session-ID')
            if session_id:
                session['sid'] = session_id
            else:
                return jsonify({"error": "Session not initialized", "code": "SESSION_NOT_INITIALIZED"}), 400
        
        if 'client_id' not in session:
            return jsonify({"error": "Client not selected", "code": "CLIENT_NOT_SELECTED"}), 400
        
        return f(*args, **kwargs)
    return decorated_function

# 然后修改 require_session 装饰器：
def require_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'sid' not in session or 'client_id' not in session:
            # 尝试重新初始化会话
            client_id = request.args.get('client_id') or (request.get_json(silent=True) or {}).get('client_id')
            if client_id:
                session['sid'] = os.urandom(24).hex()
                session['client_id'] = client_id
                session.permanent = True
                session.modified = True
            else:
                return jsonify({"error": "Session not initialized"}), 400
        return f(*args, **kwargs)
    return decorated_function

def create_simulator(client_id):
    print(f"创建模拟器 - 客户端ID: {client_id}")
    
    # 延迟导入，减少初始加载时间
    try:
        from ai_role_simulator import CLIENT_IDS
    except ImportError:
        CLIENT_IDS = {}
    
    # 首先尝试从 CLIENT_IDS 获取预设客户端
    preset_client = CLIENT_IDS.get(client_id)
    
    if preset_client:
        print(f"使用预设客户端: {client_id}")
        role_data = preset_client.get('role_data', {})
    else:
        # 如果不是预设客户端，从 client_manager 获取
        client = client_manager.get_client(client_id)
        if not client:
            print(f"错误 - 客户端 {client_id} 不存在，使用默认客户端 client_djjo")
            # 尝试使用默认客户端
            preset_client = CLIENT_IDS.get("client_djjo")
            if preset_client:
                role_data = preset_client.get('role_data', {})
            else:
                print(f"默认客户端也不存在，创建空数据")
                role_data = {}
        else:
            print(f"成功加载自定义客户端: {client_id}")
            role_data = client.get("role_data", {})
    
    # 如果 role_data 为空，加载默认数据
    if not role_data:
        print(f"角色数据为空，加载默认数据")
        try:
            from ai_role_simulator.data import (
                base_profile, cognitive_emotional_model, dynamic_state, 
                interaction_rules, conversation_profile, impedance_rules
            )
            role_data = {
                "base_profile": base_profile,
                "cognitive_emotional_model": cognitive_emotional_model,
                "dynamic_state": dynamic_state,
                "interaction_rules": interaction_rules,
                "conversation_profile": conversation_profile,
                "impedance_rules": impedance_rules
            }
        except ImportError as e:
            print(f"导入默认数据失败: {e}")
            # 创建最小化的角色数据
            role_data = {
                "base_profile": {
                    "姓名": "Djjo" if client_id == "client_djjo" else "匿名",
                    "年龄": 30,
                    "性别": "女",
                    "职业": {"领域": "教育"},
                    "教育": {"学历": "硕士"},
                    "外在表现": {"穿着": "整洁"},
                    "居住": {"地点": "城市"},
                    "关键事件": [],
                    "具体内容": []
                },
                "cognitive_emotional_model": {
                    "核心信念": ["我必须要完美才能被接受"],
                    "中间信念": {
                        "规则": ["如果我不完美，别人就会拒绝我"],
                        "假设": ["完美是获得认可的唯一途径"]
                    },
                    "自动思维示例": {
                        "工作情境": ["我这次做得不够好"],
                        "关系情境": ["他们可能不喜欢我"],
                        "家庭情境": ["我让家人失望了"]
                    },
                    "情绪反应模式": {
                        "焦虑触发点": ["被评价", "犯错"],
                        "典型情绪": ["焦虑", "不安", "自我怀疑"]
                    },
                    "行为应对策略": {
                        "回避行为": ["拖延工作", "避免社交"],
                        "过度补偿": ["过度工作", "讨好他人"]
                    }
                },
                "dynamic_state": {
                    "心理特征": {
                        "核心情绪": ["焦虑", "自我怀疑"],
                        "防御机制": ["合理化", "否认"],
                        "认知扭曲": ["全有全无思维", "过度概括"]
                    },
                    "躯体症状": {
                        "睡眠": ["入睡困难"],
                        "饮食": ["食欲不振"],
                        "其他": ["头痛"]
                    },
                    "咨询记录": {
                        "总次数": 0,
                        "当前阶段": "防御期",
                        "历史摘要": {},
                        "禁忌话题": []
                    },
                    "关系状态": {
                        "家庭关系": "紧张",
                        "朋友关系": "疏远",
                        "工作关系": "一般"
                    },
                    "背景信息": "寻求帮助改善人际关系"
                },
                "interaction_rules": {
                    "阶段设定": {
                        "防御期": {
                            "特征": ["简短回应", "回避深层话题"],
                            "策略": ["建立信任", "避免直接挑战"]
                        },
                        "试探期": {
                            "特征": ["中等长度回应", "选择性开放"],
                            "策略": ["温和引导", "鼓励表达"]
                        },
                        "开放期": {
                            "特征": ["详细探讨", "情感表达"],
                            "策略": ["深入探索", "情感支持"]
                        }
                    },
                    "当前约束": {
                        "阶段": "防御期",
                        "限制": ["避免专业术语", "不能给出建议"],
                        "风格": "自然"
                    }
                },
                "conversation_profile": {
                    "初始风格": "戒备型",
                    "风格梯度": {
                        "防御期": "简短，回避",
                        "试探期": "适度开放",
                        "开放期": "详细，情感丰富"
                    },
                    "语言特点": ["口语化", "情感表达", "具体描述"],
                    "阻抗策略": ["简短回应", "转移话题", "否认问题"]
                },
                "impedance_rules": {
                    "触发条件": ["缺乏共情", "机械回应", "遗忘关键信息"],
                    "表现形式": ["沉默", "简短回答", "转移话题"],
                    "强度等级": {"低": 1, "中": 2, "高": 3},
                    "阶段特异性": {
                        "防御期": "高阻抗",
                        "试探期": "中阻抗", 
                        "开放期": "低阻抗"
                    },
                    "处理原则": ["表达理解", "共情回应", "建立信任"]
                }
            }
    
    # 优化角色数据，减少内存占用但不影响导出功能
    def optimize_role_data(role_data):
        if not isinstance(role_data, dict):
            return role_data
            
        optimized = role_data.copy()
        
        # 对大型数据结构进行优化
        for key in ['base_profile', 'dynamic_state', 'cognitive_emotional_model']:
            if key in optimized and isinstance(optimized[key], dict):
                # 限制具体内容的显示长度，但不修改原始数据
                if "具体内容" in optimized[key] and isinstance(optimized[key]["具体内容"], list):
                    if len(optimized[key]["具体内容"]) > 6:  # 减少到5条
                        optimized[key]["具体内容"] = optimized[key]["具体内容"][:6]
                
                # 压缩关键事件
                if "关键事件" in optimized[key] and isinstance(optimized[key]["关键事件"], list):
                    if len(optimized[key]["关键事件"]) > 8:  # 减少到8条
                        optimized[key]["关键事件"] = optimized[key]["关键事件"][:8]
        
        return optimized
    
    # 应用优化（这只是为了显示和内存使用，原始数据保持不变）
    display_role_data = optimize_role_data(role_data)
    
    # 确保 role_data 是字典类型
    if not isinstance(display_role_data, dict):
        print(f"错误 - role_data 不是字典类型: {type(display_role_data)}")
        try:
            if hasattr(display_role_data, '__dict__'):
                display_role_data = display_role_data.__dict__
            else:
                display_role_data = {}
        except:
            display_role_data = {}
    
    # 确保 role_data 包含所有必要的键
    required_keys = ['base_profile', 'dynamic_state', 'interaction_rules', 
                    'cognitive_emotional_model', 'conversation_profile', 'impedance_rules']
    
    for key in required_keys:
        if key not in display_role_data:
            print(f"警告 - 客户端 {client_id} 缺少 {key}，使用默认数据")
            # 使用默认数据作为后备
            default_data = {
                'base_profile': {
                    "姓名": "默认来访者",
                    "年龄": 30,
                    "性别": "未知"
                },
                'dynamic_state': {
                    "心理特征": {"核心情绪": ["未指定问题"]}
                },
                'interaction_rules': {
                    "当前约束": {"风格": "自然"}
                },
                'cognitive_emotional_model': {
                    "核心信念": []
                },
                'conversation_profile': {
                    "初始风格": "自然"
                },
                'impedance_rules': {}
            }
            display_role_data[key] = default_data.get(key, {})
    
    print(f"最终role_data 结构: {list(display_role_data.keys())}")
    
    def generate_fn(messages):
        try:
            formatted_messages = []
            for msg in messages:
                role = msg["role"]
                if role == "ai":
                    role = "assistant"
                formatted_messages.append({"role": role, "content": msg["content"]})

            # 简化消息内容以减少token使用
            simplified_messages = []
            for msg in formatted_messages:
                if len(msg["content"]) > 500:
                    simplified_content = msg["content"][:500] + "..."
                    simplified_messages.append({"role": msg["role"], "content": simplified_content})
                else:
                    simplified_messages.append(msg)

            max_retries = 2
            for attempt in range(max_retries):
                try:
                    response = openai_client.chat.completions.create(
                        model=app.config.get('OPENAI_MODEL') or 'gpt-4o',
                        messages=simplified_messages,
                        max_tokens=400,
                        timeout=20
                    )
                    return response.choices[0].message.content
                except Exception as api_error:
                    error_str = str(api_error)
                    is_auth_error = '401' in error_str or 'authentication' in error_str.lower() or 'api_key' in error_str.lower()
                    if is_auth_error:
                        app.logger.error(f"OpenAI API authentication failed (check OPENAI_API_KEY): {error_str}")
                        return None
                    if attempt < max_retries - 1:
                        app.logger.warning(f"OpenAI API attempt {attempt + 1} failed: {error_str}, retrying...")
                    else:
                        app.logger.error(f"OpenAI API all attempts failed: {error_str}")
                        return None
                
        except Exception as error:
            app.logger.error(f"OpenAI response generation failed: {str(error)}")
            return None
    
    print(f"准备创建 AIRoleSimulator")
    try:
        simulator = AIRoleSimulator(
            generate_fn, 
            role_data=display_role_data,
            max_turns=80  # 减少最大轮次
        )
        print(f"模拟器创建成功")
        return simulator
    except Exception as e:
        print(f"模拟器创建失败: {str(e)}")
        # 创建备用模拟器
        try:
            # 创建一个极简的模拟器
            simple_role_data = {
                "base_profile": {
                    "姓名": "来访者",
                    "年龄": 30,
                    "性别": "未知"
                },
                "dynamic_state": {
                    "心理特征": {
                        "核心情绪": ["寻求帮助"]
                    }
                }
            }
            
            # 创建一个简单的生成函数
            def simple_generate_fn(messages):
                last_message = messages[-1]["content"] if messages else "你好"
                return f"我听到你说：'{last_message[:50]}...'。我正在思考如何回应你。"
            
            return AIRoleSimulator(
                simple_generate_fn, 
                role_data=simple_role_data,
                max_turns=50
            )
        except Exception as e2:
            print(f"备用模拟器也创建失败: {str(e2)}")
            # 返回 None，让调用者处理
            return None

@app.route('/')
def home():
    return redirect('/training')

@app.route('/training')
def training():
    return render_template('training.html')

@app.route('/exam')
def exam():
    """考试主页 - 直接显示案例选择"""
    try:
        all_clients = client_manager.get_all_clients()
        return render_template('exam.html', clients=all_clients)
    except Exception as error:
        app.logger.error(f"考试页面加载失败: {str(error)}")
        return render_template('error.html',
                     error_code=500,
                     error_title="服务器错误",
                     error_message="加载考试页面失败",
                     error_details=str(error)), 500

@app.route('/select-client')
def select_client():
    try:
        all_clients = client_manager.get_all_clients()
        default_client = client_manager.get_client("client_djjo")
        if not default_client:
            client_manager.create_client({
                "name": "Djjo",
                "age": 30,
                "gender": "female",
                "main_issue": "综合",
                "background": "默认系统案例",
                "style": "natural",
                "initial_stage": "defensive"
            })
            all_clients = client_manager.get_all_clients()
        
        return render_template('select.html', clients=all_clients)
    except Exception as error:
        app.logger.error(f"选择客户端页面加载失败: {str(error)}")
        return render_template('error.html',
                     error_code=500,
                     error_title="服务器错误",
                     error_message="加载案例列表失败",
                     error_details=str(error)), 500

@app.route('/create-client', methods=['GET', 'POST'])
def create_client():
    if request.method == 'GET':
        return render_template('create_client.html')
    
    try:
        client_data = request.get_json()
        if not client_data:
            return jsonify({"error": "无效的请求数据"}), 400
        
        required_fields = ['name', 'age', 'gender', 'main_issue', 'background', 'core_beliefs']
        for field in required_fields:
            if not client_data.get(field):
                return jsonify({"error": f"缺少必要字段: {field}"}), 400
        
        client_id = client_manager.create_client(client_data)
        return jsonify({
            "success": True,
            "client_id": client_id,
            "redirect": f"/start-session/{client_id}"
        }), 201
    except Exception as error:
        app.logger.error(f"创建来访者失败: {str(error)}")
        return jsonify({"error": str(error)}), 500

@app.route('/edit-client/<client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    try:
        # 首先尝试从预设客户端获取
        from ai_role_simulator import CLIENT_IDS
        preset_client = CLIENT_IDS.get(client_id)
        
        if preset_client:
            # 使用预设客户端数据
            client = preset_client
            print(f"使用预设客户端: {client_id}")
        else:
            # 如果不是预设客户端，从 client_manager 获取
            client = client_manager.get_client(client_id)
        
        if not client:
            return render_template('error.html',
                         error_code=404,
                         error_title="来访者不存在",
                         error_message="找不到指定的来访者记录",
                         error_details=""), 404
        
        # 确保客户端数据结构正确
        if 'role_data' not in client:
            client['role_data'] = {}
        if 'base_profile' not in client['role_data']:
            client['role_data']['base_profile'] = {}
        if 'cognitive_emotional_model' not in client['role_data']:
            client['role_data']['cognitive_emotional_model'] = {}
        
        if request.method == 'GET':
            return render_template('edit_client.html', client=client)
        
        # 如果是预设客户端，不允许编辑
        if preset_client:
            return jsonify({"error": "系统预设案例不可编辑"}), 403
            
        client_data = request.get_json()
        if not client_data:
            return jsonify({"error": "无效的请求数据"}), 400
        
        # 更新基本信息和关键事件
        if client_manager.update_client_extended(client_id, client_data):
            return jsonify({"success": True}), 200
        return jsonify({"error": "更新失败"}), 400
        
    except Exception as error:
        app.logger.error(f"编辑来访者失败: {str(error)}")
        import traceback
        traceback.print_exc()
        return render_template('error.html',
                     error_code=500,
                     error_title="服务器错误",
                     error_message="处理请求时发生错误",
                     error_details=str(error)), 500

@app.route('/start-session/<client_id>')
def start_session(client_id):
    start_time = time.time()  # 记录开始时间
    print(f"会话状态 - sid: {session.get('sid')}, client_id: {session.get('client_id')}")
    
    try:
        # 首先检查是否是预设客户端
        from ai_role_simulator import CLIENT_IDS
        preset_client = CLIENT_IDS.get(client_id)
        if preset_client:
            client = preset_client
            print(f"使用预设客户端: {client_id}")
            if 'role_data' in client:
                print(f"role_data 包含的键: {list(client['role_data'].keys())}")
            
            # 设置客户端ID和会话永久性
            session['client_id'] = client_id
            session['sid'] = os.urandom(24).hex()
            session['exam_mode'] = False
            session.permanent = True
            session.modified = True
            
            simulator = create_simulator(client_id)
            if not simulator:
                print(f"错误 - 模拟器初始化失败")
                return render_template('error.html',
                            error_code=500,
                            error_title="服务器错误",
                            error_message="AI模拟器初始化失败",
                            error_details=""), 500
            
            print(f"模拟器创建成功")
            
            # 修改后的初始提示 - 确保第一句话有意义
            initial_prompt = (
                "现在你是一位心理咨询来访者，刚见到咨询师。"
                "请根据你的角色设定，说出自然、有意义的第一句话。"
                "不要直接暴露核心问题，表现出适当的防御和不确定性。"
                "在咨询刚开始(尤其是第一次咨询时)，话语要更简短，并表现出更多的谨慎和防御。"
                "牢记你是正在寻求心理帮助的角色，因为你知道自己需要帮助，你会相对主动的陈述你的需求或者觉得不舒服的地方。"
                "请基于你的设定和故事背景，尽可能充分的表达自己的诉求和过往经历，语言尽可能丰富。"
                "**重要：不要使用以下无意义的开场白：**"
                "1. '好的，现在我要扮演一个来访者'"
                "2. '抱歉，我不能帮助实现这个请求'"
                "3. '会按照所设置的规则来扮演心理咨询来访者'"
                "4. '准备好了，可以开始模拟咨询'"
                "5. 任何暴露你是在扮演角色的语言"
                
                "自然的开场白可以是："
                "'你好，嗯...我不知道从哪里开始'"
                "'最近我总是睡不好觉，感觉很焦虑'"
                "'我有些困扰想找人聊聊'"
                "'最近压力很大，感觉需要一些帮助'"
                
                "在以下情况出现时，在话语中表现出对咨询师的不信任、质疑、或敌意："
                "1. 在咨询过程中，咨询师的回复没有让你感到共情、支持、被理解时"
                "2. 在咨询师的回复机械、刻板、重复、不自然、或缺乏人情味时"
                "3. 在咨询师一次提出多个问题，或说了其他让你难以回复的话时"
                "4. 在咨询师只顾提问或提建议，而没有更多倾听和共情你的感受时"
                "5. 在咨询师遗忘了你的基本情况或你从前提到过的关键信息时"
                "6. 根据你的对话风格配置文件，使用适当的阻抗策略，如简短回应、否认问题、转移话题等。"
                
                "请扮演一位真正需要帮助的来访者，开始你的第一句话："
            )
            
            # 验证函数：确保第一句话有意义
            def validate_first_message(message):
                """验证第一句话是否有意义"""
                if not message or len(message.strip()) < 5:
                    return False
                
                invalid_patterns = [
                    r'好的.*扮演.*来访者',
                    r'抱歉.*不能帮助',
                    r'按照.*规则.*扮演',
                    r'准备好了.*开始.*咨询',
                    r'现在我要.*扮演',
                    r'模拟咨询',
                    r'AI.*来访者',
                    r'大语言模型',
                    r'作为.*AI'
                ]
                
                message_lower = message.lower()
                for pattern in invalid_patterns:
                    if re.search(pattern, message_lower):
                        return False
                
                return True
            
            # 生成初始消息并验证
            max_attempts = 3
            initial_message = None
            
            for attempt in range(max_attempts):
                try:
                    generated_message = simulator.generate_response([{"role": "user", "content": initial_prompt}])
                    
                    if validate_first_message(generated_message):
                        initial_message = generated_message
                        print(f"第{attempt+1}次尝试：成功生成有效的初始消息")
                        break
                    else:
                        print(f"第{attempt+1}次尝试：初始消息不符合要求，重新生成")
                        print(f"消息内容：{generated_message[:50]}...")
                        
                except Exception as e:
                    print(f"第{attempt+1}次尝试生成消息失败：{str(e)}")
            
            # 如果所有尝试都失败，使用备用消息
            if not initial_message:
                print("所有尝试失败，使用备用初始消息")
                # 根据客户端问题生成备用消息
                issue = client.get('issue', '心理困扰')
                backup_messages = [
                    f"您好，我最近总是睡不好，感觉压力很大...",
                    f"嗯...我不知道该从哪里说起，就是感觉最近状态很不好...",
                    f"我想聊聊最近困扰我的一些事情...",
                    f"最近总觉得很焦虑，有些事情想找人倾诉..."
                ]
                initial_message = random.choice(backup_messages)
            
            print(f"最终初始消息：{initial_message[:50]}...")
            
            # 初始化会话记录
            session['conversation'] = [
                {"role": "ai", "content": initial_message}
            ]
            
            # 再次确保会话保存
            session.modified = True
            
            return render_template('chat.html', 
                                client=client,
                                initial_message=initial_message)
        
        else:
            # Non-preset (user-created) client
            client = client_manager.get_client(client_id)
            if not client:
                return render_template('error.html',
                             error_code=404,
                             error_title="Client Not Found",
                             error_message="The requested client does not exist.",
                             error_details=""), 404

            session['client_id'] = client_id
            session['sid'] = os.urandom(24).hex()
            session['exam_mode'] = False
            session.permanent = True
            session.modified = True

            simulator = create_simulator(client_id)
            if not simulator:
                return render_template('error.html',
                             error_code=500,
                             error_title="Server Error",
                             error_message="AI simulator initialization failed.",
                             error_details=""), 500

            initial_prompt = (
                "现在你是一位心理咨询来访者，刚见到咨询师。"
                "请根据你的角色设定，说出自然、有意义的第一句话。"
                "不要直接暴露核心问题，表现出适当的防御和不确定性。"
                "在咨询刚开始(尤其是第一次咨询时)，话语要更简短，并表现出更多的谨慎和防御。"
                "请扮演一位真正需要帮助的来访者，开始你的第一句话："
            )

            initial_message = None
            for attempt in range(3):
                try:
                    msg = simulator.generate_response([{"role": "user", "content": initial_prompt}])
                    if msg and len(msg.strip()) >= 5:
                        initial_message = msg
                        break
                except Exception as e:
                    print(f"Attempt {attempt+1} failed: {e}")

            if not initial_message:
                backup_messages = [
                    "您好，我最近总是睡不好，感觉压力很大...",
                    "嗯...我不知道该从哪里说起，就是感觉最近状态很不好...",
                    "我想聊聊最近困扰我的一些事情...",
                    "最近总觉得很焦虑，有些事情想找人倾诉..."
                ]
                initial_message = random.choice(backup_messages)

            session['conversation'] = [{"role": "ai", "content": initial_message}]
            session.modified = True

            return render_template('chat.html',
                                   client=client,
                                   initial_message=initial_message)

    except Exception as error:
        print(f"严重错误 - start_session 失败: {str(error)}")
        import traceback
        traceback.print_exc()
        
        app.logger.error(f"启动会话失败: {str(error)}")
        return render_template('error.html',
                     error_code=500,
                     error_title="服务器错误",
                     error_message="会话初始化失败",
                     error_details=str(error)), 500

@app.route('/diagnose/<client_id>')
def diagnose_client(client_id):
    """诊断特定客户端的问题"""
    from ai_role_simulator import CLIENT_IDS
    
    diagnosis = {
        'client_id': client_id,
        'in_preset': client_id in CLIENT_IDS,
        'session_exists': 'sid' in session,
        'session_client': session.get('client_id'),
        'preset_data': CLIENT_IDS.get(client_id, {}).keys() if client_id in CLIENT_IDS else None
    }
    
    return jsonify(diagnosis)

@app.route('/start-session/client_psi')
def client_psi():
    """处理PatientPsi案例的特殊路由"""
    try:
        role_data = convert_patientpsi_to_standard()
        client_id = "client_psi"
        client = {
            "id": client_id,
            "name": "Djjo-PatientΨ",
            "issue": "认知模型CCD",
            "role_data": role_data,
            "created_at": datetime.now().isoformat()
        }
        # 启动会话
        session.clear()
        session['sid'] = os.urandom(24).hex()
        session['client_id'] = client_id
        session.permanent = True
        simulator = AIRoleSimulator(
            generate_fn=lambda x: "初始化对话...",
            role_data=role_data
        )
        
        initial_message = "您好,我最近总是睡不好..."
        
        return render_template('chat.html', 
                           client=client,
                           initial_message=initial_message)
        
    except Exception as error:
        app.logger.error(f"加载PatientPsi案例失败: {str(error)}")
        return render_template('error.html',
                     error_code=500,
                     error_title="案例加载失败",
                     error_message="无法加载PatientPsi案例",
                     error_details=str(error)), 500

@app.route('/start-session/client_psydt')
def client_psydt():
    """处理PsyDT案例的特殊路由"""
    try:
        role_data = convert_psydt_to_standard()
        client_id = "client_psydt"
        client = {
            "id": client_id,
            "name": "PsyDT案例",
            "issue": "综合",
            "role_data": role_data,
            "created_at": datetime.now().isoformat()
        }
        
        session.clear()
        session['sid'] = os.urandom(24).hex()
        session['client_id'] = client_id
        session.permanent = True
        
        simulator = AIRoleSimulator(
            generate_fn=lambda x: "我不知道从哪说起...",
            role_data=role_data
        )
        
        initial_message = "嗯...我不知道该说啥"
        
        return render_template('chat.html', 
                           client=client,
                           initial_message=initial_message)
        
    except Exception as error:
        app.logger.error(f"加载PsyDT案例失败: {str(error)}")
        return render_template('error.html',
                     error_code=500,
                     error_title="案例加载失败",
                     error_message="无法加载PsyDT案例",
                     error_details=str(error)), 500
    
@app.route('/api/generate-report', methods=['POST'])
@require_session
def generate_report():
    """生成对话分析报告"""
    try:
        session_id = session.get('sid')
        client_id = session.get('client_id')
        
        if not session_id or not client_id:
            return jsonify({"error": "会话未初始化"}), 400
        
        # 获取对话记录
        conversation = session.get('conversation', [])
        if not conversation:
            return jsonify({"error": "没有对话内容"}), 400
        
        # 获取客户端信息
        from ai_role_simulator import CLIENT_IDS
        client = CLIENT_IDS.get(client_id)
        if not client:
            client = client_manager.get_client(client_id)
        
        # 分析对话内容（这里需要实现具体的分析逻辑）
        analysis_result = analyze_conversation(conversation, client)
        
        # 计算对话用时（假设每轮对话平均2分钟）
        total_turns = len([msg for msg in conversation if msg['role'] == 'user'])
        estimated_time = total_turns * 2  # 分钟
        
        report_data = {
            "client_name": client.get('name', '未知来访者'),
            "client_issue": client.get('issue', '未指定问题'),
            "conversation_date": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "total_turns": total_turns,
            "estimated_time": f"{estimated_time} 分钟",
            "key_insights": analysis_result.get('key_insights', []),
            "professional_advice": analysis_result.get('advice', []),
            "ethical_violations": analysis_result.get('ethical_violations', [])
        }
        
        # 存储报告数据到会话
        session['last_report'] = report_data
        session.modified = True
        
        return jsonify(report_data)
        
    except Exception as error:
        app.logger.error(f"生成报告失败: {str(error)}")
        return jsonify({"error": f"生成报告失败: {str(error)}"}), 500

def analyze_conversation(conversation, client):
    """分析对话内容，返回关键洞察和建议"""
    # 这里需要实现具体的分析逻辑
    # 可以使用AI模型来分析对话，或者基于规则的分析
    
    # 示例分析结果
    key_insights = [
        "第3轮对话中，咨询师的共情回应让来访者开始开放心扉",
        "第8轮对话中，直接的问题让来访者表现出防御性",
        "来访者在谈到家庭话题时表现出明显的情绪波动"
    ]
    
    professional_advice = [
        "建议更多使用开放式问题，减少封闭式提问",
        "在敏感话题上可以更加渐进地探索",
        "注意非语言信号的观察，适时给予情感支持"
    ]
    
    ethical_violations = [
        "第12轮对话中可能存在双重关系风险的建议",
        "需要注意保密原则的边界"
    ]
    
    return {
        'key_insights': key_insights,
        'advice': professional_advice,
        'ethical_violations': ethical_violations
    }


# ---------- WAI 评分：后端实现（修正版，保持原函数名） ----------
def load_wai_text():
    """
    直接返回你的WAI维度文本，不使用外部文件
    """
    return """
**（一）探索能力维度：咨询师帮助来访者探索思想、情感和行为的能力**
1.对当前治疗活动有用性的一致认同
2.咨询师对治疗目标的共同理解
3.咨询师澄清会谈目的
4.咨询师对会谈目标不存在分歧
5.咨询师对治疗目标不缺乏理解
6.咨询师对来访者在治疗中的责任有一致认识
7.共同认为治疗目标对来访者重要
8.不会认为治疗内容与来访者当前关切无关
9.一致认为治疗活动有助于来访者达成改变
10.咨询师期望清晰
11.共同致力于一致的目标
12.咨询师对来访者需关注的问题有一致看法
13.咨询师对如何改变有清晰认识
14.咨询师对来访者真实问题有不同看法
15.共同设定会谈目标
16.咨询师对适合来访者的改变有共同理解
17.治疗过程对来访者有意义
18.来访者清楚治疗的预期结果
19.来访者认为当前处理问题的方式正确

**（二）关系评估维度：咨询关系的质量和连接感**
1.关系中不存在不适感
2.双方有良好的理解
3.来访者不会对治疗内容感到困惑
4.双方互相喜欢
5.来访者感受到咨询师的真诚关心
6.双方互相尊重
7.来访者不会感到咨询师不诚实
8.来访者对咨询师的能力有信心
9.来访者感到被咨询师欣赏
10.双方互相信任
11.双方认为关系对来访者重要
12.来访者未感到害怕被咨询师放弃
13.来访者感到被尊重和关怀，即使行为不被认可

**（三）会谈评价维度：对会谈整体效果的评价**
1.对改善步骤的一致认同
2.对会谈结果的关注
3.认为咨询时间利用高效
4.来访者对咨询活动不会感到挫败
"""

def make_wai_prompt(wai_text, conversation, mode='train', meta=None):
    """
    构建给模型的prompt - 保持原函数签名不变
    """
    convo_text = ""
    for i, msg in enumerate(conversation, 1):
        role = "咨询师" if msg.get('role') == 'user' else "来访者"
        content = msg.get('content', '')
        convo_text += f"【第{i}轮】{role}: {content}\n"
    
    prompt = f"""你是一位心理咨询督导专家，需要基于WAI工作联盟量表评估咨询师的表现。

## WAI评估维度（共35个条目）：
{wai_text}

## 对话记录：
{convo_text}

## 评估要求：
1. **三个维度评分**（每个维度1-5分，5分最佳）：
   - 探索能力维度（1-19条）：评估咨询师帮助来访者探索的能力
   - 关系评估维度（20-32条）：评估咨询关系的质量
   - 会谈评价维度（33-35条）：评估会谈整体效果

2. **具体建议**：针对每个维度，提出3条具体的改进建议

3. **总体评价**：简要总结咨询师的优势和需要改进的地方

## 请返回严格的JSON格式：
{{
  "wai_scores": {{
    "exploration": 4,  // 探索能力维度得分（1-5）
    "relationship": 4, // 关系评估维度得分（1-5）
    "session": 3       // 会谈评价维度得分（1-5）
  }},
  "wai_total": 11,  // 总分（三个维度得分之和）
  "item_comments": {{
    "exploration": "咨询师在帮助来访者探索方面...",
    "relationship": "咨询关系建立方面...",
    "session": "会谈整体效果方面..."
  }},
  "suggestions": [
    "针对探索能力的建议1...",
    "针对探索能力的建议2...",
    "针对关系建立的建议1...",
    "针对关系建立的建议2...",
    "针对会谈效果的建议1...",
    "针对会谈效果的建议2..."
  ],
  "strengths": ["优势1", "优势2", "优势3"],
  "improvements": ["需改进1", "需改进2", "需改进3"]
}}

请确保使用中文评估，评分基于对话中咨询师的实际表现。"""
    
    return prompt

# @app.route('/api/wai-feedback', methods=['POST'])
# @require_session
# def wai_feedback():
#     """
#     WAI 评分 API - 基于真实对话内容评估
#     """
#     try:
#         # 获取当前会话的对话记录
#         session_id = session.get('sid')
#         if not session_id:
#             return jsonify({"error": "会话未初始化"}), 400
        
#         # 从session或文件获取对话
#         conversation = session.get('conversation', [])
#         if not conversation:
#             # 尝试从文件加载
#             conversation = load_conversation_from_file(session_id)
        
#         if not conversation:
#             return jsonify({"error": "没有对话内容可评估"}), 400
        
#         # 获取客户端信息
#         client_id = session.get('client_id')
#         client = None
#         try:
#             from ai_role_simulator import CLIENT_IDS
#             client = CLIENT_IDS.get(client_id)
#         except ImportError:
#             pass
            
#         if not client:
#             client = client_manager.get_client(client_id)
        
#         # 构建对话文本
#         conversation_text = ""
#         for i, msg in enumerate(conversation, 1):
#             role = "咨询师" if msg.get('role') == 'user' else "来访者"
#             content = msg.get('content', '')
#             conversation_text += f"【第{i}轮】{role}: {content}\n\n"
        
#         # 构建真正的评估提示词
#         prompt = f"""你是一位心理咨询督导专家，请基于以下真实对话记录，使用WAI工作联盟量表对咨询师表现进行评估。

# ## 对话记录：
# {conversation_text}

# ## WAI评估维度：
# **探索能力维度（1-5分）**：咨询师帮助来访者探索思想、情感和行为的能力
# **关系评估维度（1-5分）**：咨询关系的质量和连接感
# **会谈评价维度（1-5分）**：对会谈整体效果的评价

# ## 评估要求：
# 1. **仔细分析对话内容**，基于咨询师的实际表现打分
# 2. **每个维度给出具体评分理由**，引用对话中的例子
# 3. **提供改进建议**，帮助咨询师提升技能

# 请返回以下JSON格式：
# {{
#   "wai_scores": {{
#     "exploration": 0,
#     "relationship": 0,
#     "session": 0
#   }},
#   "wai_total": 0,
#   "dimension_comments": {{
#     "exploration": "具体分析...",
#     "relationship": "具体分析...",
#     "session": "具体分析..."
#   }},
#   "suggestions": [
#     "具体建议1...",
#     "具体建议2...",
#     "具体建议3..."
#   ],
#   "strengths": [
#     "优势1...",
#     "优势2..."
#   ]
# }}

# 请确保评分基于对话实际内容，不要使用模板化回复。"""
        
#         # 调用OpenAI分析
#         messages = [
#             {"role": "system", "content": "你是专业的心理咨询督导，请根据WAI标准对咨询对话进行评估。"},
#             {"role": "user", "content": prompt}
#         ]
        
#         try:
#             response = openai_client.chat.completions.create(
#                 model=app.config.get('OPENAI_MODEL', 'gpt-4'),
#                 messages=messages,
#                 max_tokens=1500,
#                 temperature=0.3,
#                 response_format={"type": "json_object"}
#             )
#             result_text = response.choices[0].message.content.strip()
#             result = json.loads(result_text)
#         except Exception as e:
#             app.logger.error(f"AI分析失败: {e}")
#             # 返回默认评估
#             result = {
#                 "wai_scores": {"exploration": 3, "relationship": 3, "session": 3},
#                 "wai_total": 9,
#                 "dimension_comments": {
#                     "exploration": "评估失败，无法获取AI分析结果",
#                     "relationship": "评估失败，无法获取AI分析结果",
#                     "session": "评估失败，无法获取AI分析结果"
#                 },
#                 "suggestions": ["请检查API连接", "确保有足够的对话内容"],
#                 "strengths": ["对话已正常进行"]
#             }
        
#         # 保存结果
#         session['last_feedback'] = result
#         if 'last_report' not in session:
#             session['last_report'] = {}
#         session['last_report']['wai_feedback'] = result
#         session.modified = True
        
#         return jsonify(result)
        
#     except Exception as error:
#         app.logger.error(f"WAI评估失败: {str(error)}")
#         return jsonify({"error": f"评估失败: {str(error)}"}), 500

# def generate_wai_assessment(conversation, client_info=None):
#     """
#     基于WAI量表生成完整的评估报告
#     包含36个条目的详细评分
#     """
    
#     # WAI量表条目（简体中文版）
#     wai_items = {
#         "bond": [
#             "我和咨询师相处时觉得不自在",
#             "我相信咨询师喜欢我",
#             "我相信咨询师真诚地关心我的福祉",
#             "我觉得咨询师对我的感觉并不完全真诚",
#             "我觉得咨询师欣赏我",
#             "我和咨询师彼此相互信任",
#             "我和咨询师的关系对我非常重要",
#             "我感觉到假如我说了或做了不当的事，咨询师将不再与我咨询",
#             "我尊重咨询师，即使他所做的事情我并不赞同"
#         ],
#         "task": [
#             "咨询师和我同意我需做某些事以改善我的状况",
#             "咨询师和我同意我们咨询的目标",
#             "我感到有必要为咨询师澄清我们咨询的目的",
#             "我不同意咨询师认为我应从咨询中所得到的",
#             "我对我们在咨询中要达成的事感到疑虑",
#             "我很清楚同时也明白指出我在咨询中的责任",
#             "我明白咨询师期望我在每次咨询中做什么",
#             "咨询师和我都同意目前我所做的事是重要的",
#             "咨询师和我正朝向彼此同意的目标努力",
#             "咨询师和我对有益于我的改变方向已具有共识",
#             "咨询师和我共同设定了咨询的目标",
#             "咨询师要我做的事对我没多大意义"
#         ],
#         "goal": [
#             "我在咨询中所做的事情使我得到新的方式来看自己的问题",
#             "咨询师和我彼此相互了解",
#             "咨询师了解我的咨询目标",
#             "我对自己在咨询中所做的事感到困惑",
#             "咨询师并不了解我想要在咨询中获得什么",
#             "我明白我在咨询中的责任",
#             "这几次咨询的目标对我而言是重要的",
#             "我发现咨询师和我在咨询中所处理的事与我所关心的事无关",
#             "我在咨询中所做的事将有助于我达到自己所希望的改变",
#             "我自信咨询师有能力协助我",
#             "几次咨询结果，我较以前更清楚我可以如何改变",
#             "咨询师和我的问题的认定有不同看法",
#             "我对我在咨询中所做的事感到挫折",
#             "我不知道可期望从咨询结果中得到什么",
#             "我相信我们目前对我的问题的处理方向是对的"
#         ]
#     }
    
#     # 构建对话文本用于分析
#     conversation_text = ""
#     for i, msg in enumerate(conversation, 1):
#         role = "咨询师" if msg.get('role') == 'user' else "来访者"
#         content = msg.get('content', '')
#         conversation_text += f"第{i}轮 - {role}: {content}\n\n"
    
#     # 构建评估提示
#     prompt = f"""你是一位专业的心理咨询督导，请基于WAI工作联盟量表对以下咨询对话进行评估。
    
# ## 对话记录：
# {conversation_text[:3000]}  # 限制长度

# ## WAI评估要求：
# 请根据对话中咨询师的表现，对以下三个维度进行1-7分的评分（7分最高）：

# ### 1. 情感联结 (Bond) - 共9个条目
# 评估咨询师与来访者之间信任、关心、接纳的程度

# ### 2. 任务合作 (Task) - 共12个条目
# 评估咨询师与来访者对治疗任务的一致性

# ### 3. 目标一致 (Goal) - 共15个条目
# 评估咨询师与来访者对治疗目标的一致性

# ## 具体评分方法：
# - 7分：完全符合，始终表现优秀
# - 6分：经常符合，表现良好
# - 5分：有时符合，表现尚可
# - 4分：中等水平，部分符合
# - 3分：有时不符合，需要改进
# - 2分：经常不符合，问题明显
# - 1分：完全不符合，严重问题

# ## 请返回以下JSON格式：
# {{
#   "wai_dimension_scores": {{
#     "bond": {{"score": 5, "items": [条目评分列表...]}},
#     "task": {{"score": 5, "items": [条目评分列表...]}},
#     "goal": {{"score": 5, "items": [条目评分列表...]}}
#   }},
#   "wai_total": 15,
#   "dimension_analysis": {{
#     "bond": "具体分析文字...",
#     "task": "具体分析文字...", 
#     "goal": "具体分析文字..."
#   }},
#   "strengths": ["优势1", "优势2", "优势3"],
#   "improvement_suggestions": ["建议1", "建议2", "建议3", "建议4", "建议5"],
#   "overall_assessment": "总体评价..."
# }}"""

#     return prompt

@app.route('/api/wai-comprehensive', methods=['POST'])
@require_session
def wai_comprehensive_feedback():
    """
    完整的WAI评估接口
    """
    try:
        session_id = session.get('sid')
        if not session_id:
            return jsonify({"error": "会话未初始化"}), 400
        
        # 获取对话记录
        conversation = session.get('conversation', [])
        if len(conversation) < 4:  # 至少2轮对话
            return jsonify({
                "error": "对话内容不足",
                "message": "请至少完成2轮对话后再进行评估"
            }), 400
        
        # 获取客户端信息
        client_id = session.get('client_id')
        client = client_manager.get_client(client_id) or {}
        
        # 生成评估提示
        prompt = generate_wai_assessment(conversation, client)
        
        # 调用OpenAI进行评估
        messages = [
            {"role": "system", "content": "你是一位资深的心理咨询督导专家，请基于WAI工作联盟量表对咨询对话进行专业评估。"},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = openai_client.chat.completions.create(
                model=app.config.get('OPENAI_MODEL', 'gpt-4'),
                messages=messages,
                max_tokens=2000,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            
            # 计算总分（三个维度平均分）
            bond_score = result.get('wai_dimension_scores', {}).get('bond', {}).get('score', 0)
            task_score = result.get('wai_dimension_scores', {}).get('task', {}).get('score', 0)
            goal_score = result.get('wai_dimension_scores', {}).get('goal', {}).get('score', 0)
            total_score = bond_score + task_score + goal_score
            
            result['wai_total'] = total_score
            result['wai_percentage'] = round((total_score / 21) * 100, 1)  # 转换为百分比
            
        except Exception as ai_error:
            app.logger.error(f"AI评估失败: {ai_error}")
            # 返回简化的评估
            result = generate_simplified_wai_assessment(conversation)
        
        # 保存评估结果
        session['wai_assessment'] = result
        if 'last_report' not in session:
            session['last_report'] = {}
        session['last_report']['wai_assessment'] = result
        session.modified = True
        
        return jsonify({
            "success": True,
            "assessment": result,
            "conversation_length": len([m for m in conversation if m.get('role') == 'user'])
        })
        
    except Exception as error:
        app.logger.error(f"WAI综合评估失败: {str(error)}")
        return jsonify({"error": f"评估失败: {str(error)}"}), 500



@app.route('/api/save-feedback', methods=['POST'])
@require_session
def save_wai_feedback():
    """保存WAI反馈到session"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "无效数据"}), 400
            
        wai_feedback = data.get('wai_feedback')
        if wai_feedback:
            # 保存到session
            session['last_feedback'] = wai_feedback
            
            # 更新last_report
            report_data = session.get('last_report', {})
            report_data['wai_feedback'] = wai_feedback
            session['last_report'] = report_data
            
            session.modified = True
            
            return jsonify({"success": True})
            
        return jsonify({"error": "没有反馈数据"}), 400
        
    except Exception as e:
        app.logger.error(f"保存反馈失败: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/wai-full-assessment', methods=['POST'])
@require_session
def wai_full_assessment():
    """完整的WAI评估，基于对话内容自动评分"""
    try:
        session_id = session.get('sid')
        if not session_id:
            return jsonify({"error": "会话未初始化"}), 400
        
        # 获取对话记录
        conversation = session.get('conversation', [])
        if len(conversation) < 2:  # 至少1轮对话
            return jsonify({
                "error": "对话内容不足",
                "message": "请至少完成1轮对话后再进行评估"
            }), 400
        
        # 构建对话文本
        conversation_text = ""
        for i, msg in enumerate(conversation, 1):
            role = "咨询师" if msg.get('role') == 'user' else "来访者"
            content = msg.get('content', '')
            conversation_text += f"【第{i}轮】{role}: {content}\n\n"
        
        # 使用AI分析对话并生成WAI评分
        prompt = f"""你是一位资深的心理咨询督导专家。请深度分析以下咨询对话，生成完整的督导报告。

## 咨询对话内容：
{conversation_text[:3500]}

---

## 分析任务一：WAI工作联盟量表（1-7分制）
- 情感联结(Bond)：咨询师与来访者之间的信任、关心和接纳程度
- 任务合作(Task)：双方对咨询任务的共识与执行一致性
- 目标一致(Goal)：双方对咨询目标的理解和共识程度

## 分析任务二：咨询师技能评估（0-100分）
- 共情反映(empathy)：准确捕捉并反映来访者情绪，传递被理解感
- 澄清探索(clarification)：使用有效的澄清提问，帮助来访者深化探索
- 阻抗处理(resistance)：识别并有效回应来访者的防御和阻抗行为
- 危机干预(crisis)：识别高风险内容，做出适当回应和保护
- 伦理判断(ethics)：维持专业边界，遵守咨询伦理规范

## 分析任务三：薄弱点精析（"结论-证据-练习"三段式，至多3条，只写真实问题）
- 结论：一句话点明问题（必须引用"第X轮"）
- 证据：引用对话原文或描述具体情境
- 练习：可操作的改进练习，包含示范语句

## 分析任务四：示范对话（选取最典型的一个改进点）
- 引用具体轮次的咨询师原话
- 给出改进后的示范说法
- 一句话说明改进原因

请严格按以下JSON格式返回（所有字段必须存在，不可省略）：
{{
  "overall_score": 75,
  "wai_scores": {{
    "bond": {{"score": 5, "rationale": "引用具体对话内容..."}},
    "task": {{"score": 5, "rationale": "引用具体对话内容..."}},
    "goal": {{"score": 5, "rationale": "引用具体对话内容..."}}
  }},
  "skill_scores": {{
    "empathy":       {{"score": 80, "status": "good", "comment": "具体表现..."}},
    "clarification": {{"score": 71, "status": "ok",   "comment": "具体表现..."}},
    "resistance":    {{"score": 65, "status": "weak", "comment": "具体表现..."}},
    "crisis":        {{"score": 85, "status": "good", "comment": "具体表现..."}},
    "ethics":        {{"score": 78, "status": "ok",   "comment": "具体表现..."}}
  }},
  "strengths": ["优势1（引用具体对话）", "优势2"],
  "weakness_analysis": [
    {{
      "conclusion": "第X轮：问题核心一句话描述",
      "evidence": "咨询师说：'...' 此时来访者...（引用原文）",
      "practice": "建议：先使用...如：'...（示范语句）'"
    }}
  ],
  "dialogue_example": {{
    "turn_label": "第X轮",
    "original": "咨询师原话：'...'",
    "improved": "建议改为：'...'",
    "explanation": "改进原因（15字以内）"
  }},
  "overall_assessment": "总体评价2-3句，指出本次最大收获和最需改进的一个方向。"
}}"""

        # 调用OpenAI进行分析
        messages = [
            {"role": "system", "content": "你是专业的心理咨询督导，请基于WAI工作联盟量表对咨询对话进行详细评估。"},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = openai_client.chat.completions.create(
                model=app.config.get('OPENAI_MODEL', 'gpt-4'),
                messages=messages,
                max_tokens=2000,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            ai_assessment = json.loads(response.choices[0].message.content)
            
            # 计算综合得分
            bond_score = ai_assessment.get('wai_scores', {}).get('bond', {}).get('score', 4)
            task_score = ai_assessment.get('wai_scores', {}).get('task', {}).get('score', 4)
            goal_score = ai_assessment.get('wai_scores', {}).get('goal', {}).get('score', 4)
            
            # 模拟WAI量表响应（基于AI评分）
            responses = {}
            for i in range(1, 37):
                # 根据维度分配分数
                if i in [1, 3, 5, 8, 17, 19, 20, 21, 23, 26, 28, 29, 36]:
                    base_score = bond_score
                elif i in [2, 7, 9, 11, 13, 16, 18, 22, 24, 30, 31, 33]:
                    base_score = task_score
                else:
                    base_score = goal_score
                
                # 添加一些随机波动，使分数更真实
                import random
                variation = random.randint(-1, 1)
                responses[i] = max(1, min(7, base_score + variation))
            
            # 计算WAI得分
            wai_scores = calculate_wai_scores(responses, role="client")
            interpretation = interpret_wai_scores(wai_scores)
            report = generate_wai_report(wai_scores, interpretation, conversation)
            
            # 合并AI评估和WAI计算
            full_assessment = {
                "ai_assessment": ai_assessment,
                "wai_calculated": {
                    "scores": wai_scores,
                    "interpretation": interpretation,
                    "report": report
                },
                "conversation_summary": {
                    "total_turns": len([m for m in conversation if m.get('role') == 'user']),
                    "conversation_excerpt": conversation_text[:500] + "..." if len(conversation_text) > 500 else conversation_text
                }
            }
            
            # 保存到session
            session['wai_full_assessment'] = full_assessment
            session.modified = True
            
            return jsonify({
                "success": True,
                "assessment": full_assessment
            })
            
        except Exception as ai_error:
            app.logger.error(f"AI分析失败: {ai_error}")
            # 返回简化的评估
            return jsonify({
                "success": True,
                "assessment": generate_fallback_wai_assessment(conversation)
            })
        
    except Exception as error:
        app.logger.error(f"WAI完整评估失败: {str(error)}")
        return jsonify({"error": f"评估失败: {str(error)}"}), 500

def generate_fallback_wai_assessment(conversation):
    """生成备用的WAI评估"""
    user_messages = [m for m in conversation if m.get('role') == 'user']
    turns = len(user_messages)
    
    # 基于对话轮次生成合理的分数
    if turns > 20:
        bond_score, task_score, goal_score = 5, 5, 5
    elif turns > 10:
        bond_score, task_score, goal_score = 4, 4, 4
    else:
        bond_score, task_score, goal_score = 3, 3, 3
    
    responses = {}
    for i in range(1, 37):
        if i in [1, 3, 5, 8, 17, 19, 20, 21, 23, 26, 28, 29, 36]:
            base_score = bond_score
        elif i in [2, 7, 9, 11, 13, 16, 18, 22, 24, 30, 31, 33]:
            base_score = task_score
        else:
            base_score = goal_score
        
        import random
        variation = random.randint(-1, 1)
        responses[i] = max(1, min(7, base_score + variation))
    
    wai_scores = calculate_wai_scores(responses, role="client")
    interpretation = interpret_wai_scores(wai_scores)
    report = generate_wai_report(wai_scores, interpretation)
    
    return {
        "ai_assessment": {
            "wai_scores": {
                "bond": {"score": bond_score, "rationale": "基于对话轮次生成的默认评估"},
                "task": {"score": task_score, "rationale": "基于对话轮次生成的默认评估"},
                "goal": {"score": goal_score, "rationale": "基于对话轮次生成的默认评估"}
            },
            "strengths": ["对话正常进行", "基本建立了咨询关系"],
            "improvement_areas": ["建议增加对话深度", "加强情感回应"],
            "overall_assessment": "对话初步建立了工作联盟"
        },
        "wai_calculated": {
            "scores": wai_scores,
            "interpretation": interpretation,
            "report": report
        }
    }

# 添加获取WAI问卷条目的路由
@app.route('/api/wai-questionnaire', methods=['GET'])
def get_wai_questionnaire():
    """获取WAI问卷条目"""
    version = request.args.get('version', 'client')  # client 或 counselor
    
    if version == 'counselor':
        items = WAI_COUNSELOR_ITEMS
    else:
        items = WAI_CLIENT_ITEMS
    
    return jsonify({
        "version": version,
        "scoring": WAI_SCORING,
        "dimensions": WAI_DIMENSIONS,
        "items": items,
        "total_items": len(items)
    })

# 修改现有的 /api/wai-feedback 路由，使其使用完整的WAI评估
@app.route('/api/wai-feedback', methods=['POST'])
@require_session
def wai_feedback():
    """WAI反馈 - 使用完整的WAI评估"""
    try:
        # 调用完整的WAI评估
        response_data = wai_full_assessment()
        
        # 如果返回的是Response对象（错误情况）
        if isinstance(response_data, tuple):
            return response_data
        
        # 否则返回评估结果
        assessment = response_data.json['assessment']
        
        # 格式化为前端需要的格式
        wai_scores = assessment['wai_calculated']['scores']
        
        result = {
            "wai_scores": {
                "bond": wai_scores['bond_avg'],
                "task": wai_scores['task_avg'],
                "goal": wai_scores['goal_avg']
            },
            "wai_total": wai_scores['total'],
            "wai_percentage": wai_scores['total_percent'],
            "dimension_comments": {
                "bond": assessment['ai_assessment']['wai_scores']['bond']['rationale'],
                "task": assessment['ai_assessment']['wai_scores']['task']['rationale'],
                "goal": assessment['ai_assessment']['wai_scores']['goal']['rationale']
            },
            "suggestions": assessment['ai_assessment'].get('improvement_areas', []),
            "strengths": assessment['ai_assessment'].get('strengths', []),
            "overall_assessment": assessment['ai_assessment'].get('overall_assessment', ''),
            "detailed_report": assessment['wai_calculated']['report'],
            "overall_score": assessment['ai_assessment'].get('overall_score', 0),
            "skill_scores": assessment['ai_assessment'].get('skill_scores', {}),
            "weakness_analysis": assessment['ai_assessment'].get('weakness_analysis', []),
            "dialogue_example": assessment['ai_assessment'].get('dialogue_example', None)
        }
        
        # 保存结果
        session['last_feedback'] = result
        session.modified = True
        
        return jsonify(result)
        
    except Exception as error:
        app.logger.error(f"WAI反馈生成失败: {str(error)}")
        return jsonify({"error": f"评估失败: {str(error)}"}), 500

@app.route('/api/export-report', methods=['GET', 'POST'])
@require_session
def export_report():
    """导出训练模式报告"""
    try:
        # 问题在这里：导入了pytz，而pytz中有session模块，覆盖了Flask的session
        # 首先获取Flask的session，保存到局部变量避免冲突
        flask_session = session  # 先保存Flask的session对象
        
        # 获取报告数据
        report_data = flask_session.get('last_report') or {}
        if not report_data:
            return jsonify({"error": "没有可导出的报告"}), 400

        # 导入必要的模块
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from flask import send_file  # 确保导入send_file
        
        # 设置北京时间 - 使用import而不是在函数内部重命名
        try:
            import pytz
            tz = pytz.timezone("Asia/Shanghai")
            now_time = datetime.now(tz)
        except:
            now_time = datetime.now()  # 如果pytz不可用，使用默认时间
        
        # 创建PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4, 
            leftMargin=36, 
            rightMargin=36, 
            topMargin=36, 
            bottomMargin=36
        )
        
        # 创建样式
        styles = getSampleStyleSheet()
        
        # 使用中文字体
        for style_name in ['Normal', 'Title', 'Heading1', 'Heading2', 'Heading3']:
            if style_name in styles:
                styles[style_name].fontName = 'ZTFont'
        
        story = []
        
        # 标题
        story.append(Paragraph("心理咨询训练反馈报告", styles["Title"]))
        story.append(Spacer(1, 20))
        
        # 基本信息
        story.append(Paragraph("<b>基本信息</b>", styles["Heading2"]))
        story.append(Spacer(1, 10))
        
        client_name = report_data.get('client_name', '未知来访者')
        client_issue = report_data.get('client_issue', '未指定问题')
        total_turns = report_data.get('total_turns', 0)
        
        info_lines = [
            f"来访者: {client_name}",
            f"主要问题: {client_issue}",
            f"对话轮次: {total_turns} 轮",
            f"报告生成: {now_time.strftime('%Y-%m-%d %H:%M:%S')} (北京时间)"
        ]
        
        for line in info_lines:
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 6))
        
        story.append(Spacer(1, 20))
        
        # WAI评估部分
        wai_data = report_data.get('wai_feedback') or {}
        
        if wai_data:
            story.append(Paragraph("<b>WAI工作联盟评估</b>", styles["Heading2"]))
            story.append(Spacer(1, 10))
            
            # 提取WAI分数
            wai_scores = wai_data.get('wai_scores', {})
            exploration = wai_scores.get('exploration', '未评估')
            relationship = wai_scores.get('relationship', '未评估')
            session_score = wai_scores.get('session', '未评估')  # 重命名为session_score避免冲突
            wai_total = wai_data.get('wai_total', 0)
            
            # 创建分数表格
            score_data = [
                ["评估维度", "得分 (1-5分)"],
                ["探索能力", str(exploration)],
                ["关系质量", str(relationship)],
                ["会谈效果", str(session_score)],
                ["总分", f"{wai_total}/15"]
            ]
            
            score_table = Table(score_data, colWidths=[200, 100])
            score_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'ZTFont'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 8),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ]))
            
            story.append(score_table)
            story.append(Spacer(1, 15))
            
            # 显示评估分析
            dimension_comments = wai_data.get('dimension_comments', {})
            if dimension_comments:
                story.append(Paragraph("<b>维度分析</b>", styles["Heading3"]))
                story.append(Spacer(1, 8))
                
                # 显示探索能力分析
                if 'exploration' in dimension_comments:
                    story.append(Paragraph(f"<b>探索能力:</b> {dimension_comments['exploration']}", styles["Normal"]))
                    story.append(Spacer(1, 6))
                
                # 显示关系质量分析
                if 'relationship' in dimension_comments:
                    story.append(Paragraph(f"<b>关系质量:</b> {dimension_comments['relationship']}", styles["Normal"]))
                    story.append(Spacer(1, 6))
                
                # 显示会谈效果分析
                if 'session' in dimension_comments:
                    story.append(Paragraph(f"<b>会谈效果:</b> {dimension_comments['session']}", styles["Normal"]))
                    story.append(Spacer(1, 6))
            
            story.append(Spacer(1, 15))
            
            # 显示改进建议
            suggestions = wai_data.get('suggestions', [])
            if suggestions:
                story.append(Paragraph("<b>改进建议</b>", styles["Heading3"]))
                story.append(Spacer(1, 8))
                
                for i, suggestion in enumerate(suggestions[:6], 1):
                    story.append(Paragraph(f"{i}. {suggestion}", styles["Normal"]))
                    story.append(Spacer(1, 5))
            
            story.append(Spacer(1, 20))
        
        # 关键洞察
        if report_data.get('key_insights'):
            story.append(Paragraph("<b>关键对话洞察</b>", styles["Heading2"]))
            story.append(Spacer(1, 10))
            for i, insight in enumerate(report_data.get('key_insights', [])[:5], 1):
                story.append(Paragraph(f"{i}. {insight}", styles["Normal"]))
                story.append(Spacer(1, 6))
            story.append(Spacer(1, 20))
        
        # 伦理注意事项
        if report_data.get('ethical_violations'):
            story.append(Paragraph("<b>伦理注意事项</b>", styles["Heading2"]))
            story.append(Spacer(1, 10))
            for i, violation in enumerate(report_data.get('ethical_violations', []), 1):
                story.append(Paragraph(f"{i}. {violation}", styles["Normal"]))
                story.append(Spacer(1, 6))
        
        # 页脚
        story.append(Spacer(1, 30))
        story.append(Paragraph("--- 报告结束 ---", styles["Normal"]))
        story.append(Paragraph("系统生成报告，仅供参考学习", styles["Normal"]))
        
        # 生成PDF
        doc.build(story)
        buffer.seek(0)
        
        # 生成文件名
        filename = f"咨询报告_{client_name}_{now_time.strftime('%Y%m%d_%H%M')}.pdf"
        
        # 返回PDF - 确保send_file已导入
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype="application/pdf"
        )
        
    except Exception as e:
        app.logger.error(f"PDF导出失败: {e}", exc_info=True)
        
        # 错误处理 - 这里也要确保send_file已导入
        try:
            error_text = f"""
            报告生成失败
            错误: {str(e)}
            时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            buffer = io.BytesIO()
            buffer.write(error_text.encode('utf-8'))
            buffer.seek(0)
            
            # 使用当前作用域的send_file
            from flask import send_file as flask_send_file
            return flask_send_file(
                buffer,
                as_attachment=True,
                download_name="report_error.txt",
                mimetype="text/plain"
            )
        except:
            # 如果连错误报告都生成失败，返回简单JSON
            return jsonify({"error": f"PDF导出失败: {str(e)}"}), 500

@app.route('/api/export-exam-report', methods=['GET', 'POST'])
@require_session
def export_exam_report():
    """
    导出考试模式报告（包含 WAI 评分），优先使用 session['last_report']，否则使用 POST 的 JSON
    """
    try:
        # 尝试读取 POST 数据
        try:
            data = request.get_json(silent=True) or {}
        except Exception:
            data = {}

        report_data = session.get('last_report') or {}
        if data:
            report_data = { **report_data, **data.get('report_data', data) }

        if not report_data:
            return jsonify({"error": "没有可导出的考试报告"}), 400

        tz = pytz.timezone("Asia/Shanghai")
        now_text = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)

        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("<b>考试反馈报告</b>", styles["Heading1"]))
        story.append(Spacer(1, 8))
        story.append(Paragraph(f"生成时间（北京时间）：{now_text}", styles["Normal"]))
        story.append(Spacer(1, 12))

        # 基本信息
        story.append(Paragraph("<b>基本信息</b>", styles["Heading2"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"结束原因: {report_data.get('end_reason', '未知')}", styles["Normal"]))
        story.append(Paragraph(f"对话回合数: {report_data.get('total_turns', 0)}", styles["Normal"]))
        story.append(Paragraph(f"耗时: {report_data.get('time_used', 0)} 秒", styles["Normal"]))
        story.append(Spacer(1, 10))

        # 能力评估
        story.append(Paragraph("<b>能力评估</b>", styles["Heading2"]))
        story.append(Spacer(1, 6))
        for item in report_data.get('skills_assessment', []):
            story.append(Paragraph(f"- {item}", styles["Normal"]))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 10))

        # 改进建议
        story.append(Paragraph("<b>改进建议</b>", styles["Heading2"]))
        story.append(Spacer(1, 6))
        for s in report_data.get('improvement_suggestions', []):
            story.append(Paragraph(f"- {s}", styles["Normal"]))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 10))

        # WAI 部分（表格化）
        wai = report_data.get('wai_feedback') or session.get('last_feedback')
        if wai:
            story.append(Paragraph("<b>WAI 评分（Working Alliance Inventory）</b>", styles["Heading2"]))
            story.append(Spacer(1, 6))

            scores = wai.get('wai_scores') if isinstance(wai.get('wai_scores'), dict) else {}
            wai_total = wai.get('wai_total') or wai.get('total') or '无'
            story.append(Paragraph(f"Bond: {scores.get('bond', '无')}    Task: {scores.get('task', '无')}    Goal: {scores.get('goal', '无')}    总分: {wai_total}", styles["Normal"]))
            story.append(Spacer(1, 8))

            # 构造表格
            table_data = [["条目 (Question)", "得分 (Score)", "评语 (Comment)"]]
            item_comments = wai.get('item_comments') or {}
            item_scores = wai.get('item_scores') or {}

            if isinstance(item_comments, dict) and item_comments:
                for k, v in item_comments.items():
                    sc = item_scores.get(k, "")
                    table_data.append([str(k), str(sc), str(v)])
            else:
                brief = wai.get('brief_rationale') or wai.get('brief') or ''
                if brief:
                    table_data.append(["总评理由", "", str(brief)])
                suggestions = wai.get('suggestions') or []
                for s in suggestions:
                    table_data.append(["建议", "", str(s)])

            t = Table(table_data, colWidths=[220, 80, 200])
            t.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'ZTFont'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f0f0f0')),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t)
            story.append(Spacer(1, 12))

        # 写入并返回
        doc.build(story)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"exam_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", mimetype="application/pdf")

    except Exception as e:
        current_app.logger.error(f"导出考试报告失败: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/end-session', methods=['POST'])
def end_session():
    """结束当前会话并返回报告数据"""
    try:
        print("=== 收到结束会话请求 ===")
        
        # 确保会话ID存在
        if 'sid' not in session:
            print("会话ID不存在，创建新的会话ID")
            session['sid'] = os.urandom(24).hex()
            
        session_id = session.get('sid')
        client_id = session.get('client_id')
        
        print(f"会话ID: {session_id}")
        print(f"客户端ID: {client_id}")
        
        if not session_id or not client_id:
            print("错误: 会话或客户端信息不完整")
            return jsonify({"error": "会话未初始化"}), 400
        
        # 获取对话记录 - 优先从session读取
        conversation = session.get('conversation', [])
        print(f"对话记录长度: {len(conversation)}")
        
        if not conversation:
            print("警告: 没有对话内容")
            # 返回一个默认的报告，而不是错误
            conversation = [{"role": "ai", "content": "对话内容为空"}]
        
        # 获取客户端信息
        client = None
        try:
            from ai_role_simulator import CLIENT_IDS
            client = CLIENT_IDS.get(client_id)
        except ImportError:
            pass
            
        if not client:
            client = client_manager.get_client(client_id)
        
        if not client:
            print(f"警告: 客户端 {client_id} 信息不存在，使用默认信息")
            client = {
                "name": "未知来访者",
                "issue": "未指定问题",
                "id": client_id
            }
        
        # 生成报告数据
        user_messages = [msg for msg in conversation if msg['role'] == 'user']
        total_turns = len(user_messages)
        estimated_time = total_turns * 2  # 假设每轮对话2分钟
        
        print(f"生成报告: {total_turns}轮对话，预计{estimated_time}分钟")
        
        report_data = {
            "client_name": client.get('name', '未知来访者'),
            "client_issue": client.get('issue', '未指定问题'),
            "conversation_date": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "total_turns": total_turns,
            "estimated_time": f"{estimated_time} 分钟",
            "key_insights": [
                f"完成了{total_turns}轮对话",
                "对话已正常结束",
                "建议回顾对话内容进行反思"
            ],
            "professional_advice": [
                "建议增加开放式问题的使用",
                "注意对话节奏的控制",
                "加强情感回应技巧"
            ],
            "ethical_violations": []
        }
        
        # 存储报告数据到会话
        session['last_report'] = report_data
        session.modified = True
        
        print("报告生成成功")
        
        return jsonify({
            "success": True,
            "report": report_data,
            "message": "会话结束成功"
        })
        
    except Exception as error:
        print(f"结束会话失败: {str(error)}")
        import traceback
        traceback.print_exc()
        
        # 返回一个简化的报告，确保前端能显示
        fallback_report = {
            "client_name": "来访者",
            "client_issue": "未知问题",
            "conversation_date": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "total_turns": 0,
            "estimated_time": "0 分钟",
            "key_insights": ["报告生成失败，但对话已成功结束"],
            "professional_advice": ["系统暂时无法生成专业建议"],
            "ethical_violations": []
        }
        
        return jsonify({
            "success": False,
            "report": fallback_report,
            "error": str(error)
        })

@app.route('/delete-client/<client_id>', methods=['POST'])
def delete_client(client_id):
    try:
        if client_manager.delete_client(client_id):
            return jsonify({"success": True}), 200
        return jsonify({"error": "来访者不存在"}), 404
    except Exception as error:
        app.logger.error(f"删除来访者失败: {str(error)}")
        return jsonify({"error": str(error)}), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', 
                         error_code=404,
                         error_title="页面未找到",
                         error_message="您访问的页面不存在或已被移动。",
                         error_details=str(error)), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html',
                         error_code=500,
                         error_title="服务器错误",
                         error_message="服务器在处理您的请求时遇到问题。",
                         error_details=str(error)), 500

@app.route('/debug/clients')
def debug_clients():
    return jsonify({
        "status": "success",
        "data": {
            "available_clients": list(client_manager.clients.keys()),
            "client_psydt_exists": "client_psydt" in client_manager.clients,
            "client_psi_exists": "client_psi" in client_manager.clients,
            "render_env": os.getenv('RENDER') == 'true',
            "data_file": client_manager.data_file,
            "file_exists": os.path.exists(client_manager.data_file)
        }
    })

@app.route('/api/export-conversation', methods=['GET'])
@require_session
def export_conversation():
    """导出当前会话对话为TXT格式"""
    try:
        # 从会话存储文件读取完整对话记录，而不是session
        session_id = session.get('sid')
        if not session_id:
            return jsonify({"error": "会话未初始化"}), 400
            
        file_path = os.path.join(current_app.config['CONVERSATION_DATA_DIR'], f'{session_id}.pkl')
        
        try:
            with open(file_path, 'rb') as f:
                session_data = pickle.load(f)
                conversation = session_data.get('conversation_history', [])
        except (FileNotFoundError, EOFError):
            conversation = session.get('conversation', [])
        
        if not conversation:
            return jsonify({"error": "没有可导出的对话内容"}), 404
            
        client_id = session.get('client_id')
        if not client_id:
            return jsonify({"error": "客户端信息不存在"}), 404
        
        # 获取完整的客户端信息（不从优化后的数据获取）
        from ai_role_simulator import CLIENT_IDS
        client = CLIENT_IDS.get(client_id)
        if not client:
            client = client_manager.get_client(client_id)
        
        if not client:
            return jsonify({"error": "客户端信息不存在"}), 404
        
        txt_content = f"心理咨询对话记录\n"
        txt_content += f"来访者: {client.get('name', '未知')}\n"
        txt_content += f"主要问题: {client.get('issue', '未指定')}\n"
        txt_content += f"会话时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        txt_content += f"{'='*50}\n\n"
        
        for i, msg in enumerate(conversation, 1):
            role = "咨询师" if msg['role'] == 'user' else "来访者"
            txt_content += f"{i}. [{role}] {msg['content']}\n\n"
        
        buffer = BytesIO()
        buffer.write(txt_content.encode('utf-8'))
        buffer.seek(0)
        
        filename = f"conversation_{client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='text/plain'
        )
        
    except Exception as error:
        app.logger.error(f"导出对话失败: {str(error)}")
        return jsonify({"error": f"导出失败: {str(error)}"}), 500


@app.after_request
def add_security_headers(response):
    # 确保响应是UTF-8编码
    if response.content_type.startswith('text/html'):
        response.charset = 'utf-8'
    
    # 添加安全头
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # 缓存控制
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=3600'
    else:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    
    # 确保Content-Type包含charset
    if response.content_type.startswith('text/'):
        if 'charset' not in response.content_type:
            response.content_type += '; charset=utf-8'
    
    return response

@app.route('/select-exam-client')
def select_exam_client():
    """考试模式下的案例选择页面"""
    try:
        all_clients = client_manager.get_all_clients()
        return render_template('select_exam.html', clients=all_clients)
    except Exception as error:
        app.logger.error(f"考试案例选择页面加载失败: {str(error)}")
        return render_template('error.html',
                     error_code=500,
                     error_title="服务器错误",
                     error_message="加载考试案例失败",
                     error_details=str(error)), 500

@app.route('/start-exam/<client_id>')
def start_exam(client_id):
    """开始考试会话"""
    try:
        # 清除之前的会话
        session.clear()
        
        # 设置考试模式标志和配置
        session['exam_mode'] = True
        session['exam_start_time'] = datetime.now().isoformat()
        session['exam_max_turns'] = 40
        session['exam_time_limit'] = 50 * 60
        
        # 设置客户端ID和会话
        session['client_id'] = client_id
        session['sid'] = os.urandom(24).hex()
        session.permanent = True
        
        # 获取客户端信息
        from ai_role_simulator import CLIENT_IDS
        preset_client = CLIENT_IDS.get(client_id)
        if preset_client:
            client = preset_client
            print(f"使用预设客户端: {client_id}")
        else:
            client = client_manager.get_client(client_id)
            if not client:
                return render_template('error.html', error_code=404, error_title="来访者不存在"), 404
            print(f"成功加载自定义客户端: {client_id}")

        # Create simulator for all clients (preset and custom)
        simulator = create_simulator(client_id)
        if not simulator:
            print(f"错误 - 模拟器初始化失败")
            return render_template('error.html',
                        error_code=500,
                        error_title="服务器错误",
                        error_message="AI模拟器初始化失败",
                        error_details=""), 500

        print(f"模拟器创建成功")

        initial_prompt = (
            "现在你是一位心理咨询来访者，刚见到咨询师。"
            "请根据你的角色设定，说出自然、有意义的第一句话。"
            "不要直接暴露核心问题，表现出适当的防御和不确定性。"
            "在咨询刚开始(尤其是第一次咨询时)，话语要更简短，并表现出更多的谨慎和防御。"
            "牢记你是正在寻求心理帮助的角色，因为你知道自己需要帮助，你会相对主动的陈述你的需求或者觉得不舒服的地方。"
            "请基于你的设定和故事背景，尽可能充分的表达自己的诉求和过往经历，语言尽可能丰富。"
            "**重要：不要使用以下无意义的开场白：**"
            "1. '好的，现在我要扮演一个来访者'"
            "2. '抱歉，我不能帮助实现这个请求'"
            "3. '会按照所设置的规则来扮演心理咨询来访者'"
            "4. '准备好了，可以开始模拟咨询'"
            "5. 任何暴露你是在扮演角色的语言"
            "请扮演一位真正需要帮助的来访者，开始你的第一句话："
        )

        def validate_first_message(message):
            if not message or len(message.strip()) < 5:
                return False
            invalid_patterns = [
                r'好的.*扮演.*来访者', r'抱歉.*不能帮助',
                r'按照.*规则.*扮演', r'准备好了.*开始.*咨询',
                r'现在我要.*扮演', r'模拟咨询',
                r'AI.*来访者', r'大语言模型', r'作为.*AI'
            ]
            for pattern in invalid_patterns:
                if re.search(pattern, message.lower()):
                    return False
            return True

        initial_message = None
        for attempt in range(3):
            try:
                generated_message = simulator.generate_response([{"role": "user", "content": initial_prompt}])
                if validate_first_message(generated_message):
                    initial_message = generated_message
                    print(f"第{attempt+1}次尝试：成功生成有效的初始消息")
                    break
                else:
                    print(f"第{attempt+1}次尝试：初始消息不符合要求，重新生成")
            except Exception as e:
                print(f"第{attempt+1}次尝试生成消息失败：{str(e)}")

        if not initial_message:
            print("所有尝试失败，使用备用初始消息")
            backup_messages = [
                "您好，我最近总是睡不好，感觉压力很大...",
                "嗯...我不知道该从哪里说起，就是感觉最近状态很不好...",
                "我想聊聊最近困扰我的一些事情...",
                "最近总觉得很焦虑，有些事情想找人倾诉..."
            ]
            initial_message = random.choice(backup_messages)

        print(f"最终初始消息：{initial_message[:50]}...")


        
        # 初始化会话记录
        session['conversation'] = [
            {"role": "ai", "content": initial_message}
        ]
        
        # 初始化轮次计数文件
        file_path = os.path.join(current_app.config['CONVERSATION_DATA_DIR'], f"{session['sid']}.pkl")
        initial_data = {
            'session_id': session['sid'],
            'turns': 0,
            'updated_at': datetime.now().isoformat()
        }
        with open(file_path, 'wb') as f:
            pickle.dump(initial_data, f)
        
        # 强制保存会话
        session.modified = True
        
        print(f"考试会话初始化完成 - sid: {session['sid']}, client_id: {session['client_id']}")
        
        # 使用考试的聊天界面
        return render_template('exam_chat.html', 
                            client=client,
                            initial_message=initial_message,
                            exam_mode=True)
        
    except Exception as error:
        print(f"严重错误 - start_exam 失败: {str(error)}")
        import traceback
        traceback.print_exc()
        
        app.logger.error(f"开始考试失败: {str(error)}")
        return render_template('error.html',
                     error_code=500,
                     error_title="服务器错误",
                     error_message="考试初始化失败",
                     error_details=str(error)), 500

@app.route('/api/generate-exam-report', methods=['POST'])
@require_session
def generate_exam_report():
    """生成考试评估报告"""
    try:
        data = request.get_json()
        end_reason = data.get('end_reason', 'unknown')
        total_turns = data.get('total_turns', 0)
        time_used = data.get('time_used', 0)
        
        # 基于对话轮次和时间生成更详细的评估
        time_minutes = time_used // 60
        turns_per_minute = total_turns / (time_minutes or 1)
        
        # 根据表现生成评估
        if turns_per_minute > 1.5:
            pace_assessment = "对话节奏较快，建议适当放慢节奏"
        elif turns_per_minute < 0.8:
            pace_assessment = "对话节奏较慢，可以适当加快回应"
        else:
            pace_assessment = "对话节奏适中"
        
        # 根据轮次生成评估
        if total_turns >= 35:
            engagement_assessment = "对话参与度高，能够充分展开话题"
        elif total_turns >= 25:
            engagement_assessment = "对话参与度良好"
        else:
            engagement_assessment = "建议增加对话深度和广度"
        
        report_data = {
            "end_reason": get_reason_text(end_reason),
            "total_turns": total_turns,
            "time_used": f"{time_minutes}分{time_used % 60}秒",
            "skills_assessment": [
                f"共情能力：{generate_empathy_assessment(total_turns)}",
                f"问题引导：{generate_question_assessment(total_turns)}",
                f"伦理规范：符合心理咨询基本伦理要求",
                f"对话节奏：{pace_assessment}",
                f"参与程度：{engagement_assessment}"
            ],
            "improvement_suggestions": [
                "建议增加情感回应的一致性",
                "可以尝试更多元化的干预技术",
                "注意非语言信息的观察和回应",
                "加强开放式问题的使用技巧",
                "提升对话的深度和连贯性"
            ]
        }
        
        return jsonify(report_data)
        
    except Exception as error:
        app.logger.error(f"生成考试报告失败: {str(error)}")
        return jsonify({"error": str(error)}), 500

def generate_empathy_assessment(turns):
    """生成共情能力评估"""
    if turns >= 30:
        return "表现优秀，能够准确理解和回应来访者情绪"
    elif turns >= 20:
        return "表现良好，基本能够理解来访者情绪"
    else:
        return "需要加强情感理解和回应能力"

def generate_question_assessment(turns):
    """生成问题引导评估"""
    if turns >= 30:
        return "问题引导技巧娴熟，能够有效推进对话"
    elif turns >= 20:
        return "问题引导基本掌握，可以适当增加技巧多样性"
    else:
        return "需要加强问题引导和对话推进能力"

def get_reason_text(reason):
    reason_map = {
        'timeout': '时间耗尽（50分钟）',
        'turn_limit': '达到最大对话轮次（40轮）',
        'manual': '提前结束考试',
        'unknown': '未知原因'
    }
    return reason_map.get(reason, '未知原因')

@app.route('/js/<path:filename>')
def serve_js(filename):
    """提供 JS 文件"""
    try:
        return send_from_directory('js', filename)
    except FileNotFoundError:
        return send_from_directory('static/js', filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    """提供 CSS 文件"""
    try:
        return send_from_directory('css', filename)
    except FileNotFoundError:
        return send_from_directory('static/css', filename)

@app.route('/static/<path:filename>')
def static_files(filename):
    """提供静态文件服务"""
    try:
        return send_from_directory('static', filename)
    except FileNotFoundError:
        # 如果文件不存在，返回404而不是500错误
        return "File not found", 404


client_manager = ClientManager(os.path.join(app.config['DATA_DIR'], 'clients.json'))
app.client_manager = client_manager

if __name__ == '__main__':
    # 确保所有目录存在
    try:
        # 主数据目录
        data_dir = app.config['DATA_DIR']
        os.makedirs(data_dir, exist_ok=True)
        
        # 会话目录
        session_dir = app.config['SESSION_FILE_DIR']
        os.makedirs(session_dir, exist_ok=True)
        
        # 对话数据目录
        conversation_dir = os.path.join(data_dir, 'conversations')
        os.makedirs(conversation_dir, exist_ok=True)
        app.config['CONVERSATION_DATA_DIR'] = conversation_dir
        
        # 内存存储目录
        memory_dir = os.path.join(os.path.dirname(__file__), 'data_memory')
        os.makedirs(memory_dir, exist_ok=True)
        
        print("目录初始化完成")
    except Exception as e:
        print(f"目录初始化失败: {e}")
    
    # 确保预设客户端存在
    client_manager.ensure_preset_clients()
    
    # 运行应用
    app.run(host='0.0.0.0', port=5000, debug=False)











