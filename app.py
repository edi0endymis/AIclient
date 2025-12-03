from flask import Flask, render_template, request, jsonify, redirect, url_for, session, current_app, send_from_directory
from flask import send_file,current_app
from flask import make_response
from flask_session import Session
from flask_cors import CORS
import io
from io import BytesIO

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
import pytz
pdfmetrics.registerFont(TTFont('ZTFont', 'ZTwyrh.ttc'))


import json
import time
import os
import pickle
from datetime import datetime
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

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 确保JSON使用UTF-8
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
app.config['SESSION_COOKIE_SECURE'] = True  
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
Session(app)

# API健康检查端点
@app.route('/api/health')
def api_health():
    return jsonify({"status": "healthy", "version": "1.0.6"})

# 注册API蓝图
app.register_blueprint(api_blueprint, url_prefix='/api/v1')

# 确保目录存在
os.makedirs(app.config['DATA_DIR'], exist_ok=True)
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)


# ========== FINAL /api/chat ROUTE (Clean + Stable + Memory Enabled) ==========
@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        data = request.get_json(force=True) or {}
        user_message = data.get("message", "").strip()
        client_id = data.get("client_id", "")

        if not user_message:
            return jsonify({"error": "message is required"}), 400

        # 取当前 client_id，没有则从 session 拿
        if not client_id:
            client_id = session.get("client_id")
        if not client_id:
            return jsonify({"error": "client_id missing"}), 400

        # 从 simulator 获取响应
        try:
            from ai_role_simulator.simulator import Simulator
            sim = Simulator(client_id=client_id)
            ai_response = sim.generate_response(user_message)
        except Exception as e:
            current_app.logger.error(f"Simulator error: {e}")
            return jsonify({"error": "simulator internal error"}), 500

        # 写入记忆 + 摘要（关键）
        try:
            safe_integrate_memory(client_id, user_message, ai_response)
        except Exception as e:
            current_app.logger.warning(f"Memory integration failed: {e}")

        # 更新 session 消息记录（用于 UI 展示）
        msgs = session.get("messages", [])
        msgs.append({"role": "user", "content": user_message})
        msgs.append({"role": "assistant", "content": ai_response})
        session["messages"] = msgs
        session.modified = True

        return jsonify({
            "reply": ai_response,
            "client_id": client_id
        })

    except Exception as e:
        current_app.logger.error(f"/api/chat fatal error: {e}")
        return jsonify({"error": "internal server error"}), 500
# ========== END FINAL /api/chat ROUTE ==========


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
            return jsonify({"error": "会话未初始化，请重新开始咨询"}), 400
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
                return jsonify({"error": "会话未初始化", "code": "SESSION_NOT_INITIALIZED"}), 400
        
        if 'client_id' not in session:
            return jsonify({"error": "客户端未选择", "code": "CLIENT_NOT_SELECTED"}), 400
        
        return f(*args, **kwargs)
    return decorated_function

# 然后修改 require_session 装饰器：
def require_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'sid' not in session or 'client_id' not in session:
            # 尝试重新初始化会话
            client_id = request.args.get('client_id') or request.json.get('client_id')
            if client_id:
                session['sid'] = os.urandom(24).hex()
                session['client_id'] = client_id
                session.permanent = True
                session.modified = True
            else:
                return jsonify({"error": "会话未初始化，请重新开始咨询"}), 400
        return f(*args, **kwargs)
    return decorated_function

# app.py 中修改 create_simulator 函数
def create_simulator(client_id):
    print(f"创建模拟器 - 客户端ID: {client_id}")
    
    # 延迟导入，减少初始加载时间
    from ai_role_simulator import CLIENT_IDS
    
    # 首先尝试从 CLIENT_IDS 获取预设客户端
    preset_client = CLIENT_IDS.get(client_id)
    
    if preset_client:
        print(f"使用预设客户端: {client_id}")
        role_data = preset_client.get('role_data', {})
    else:
        # 如果不是预设客户端，从 client_manager 获取
        client = client_manager.get_client(client_id)
        if not client:
            print(f"错误 - 客户端 {client_id} 不存在")
            return None
        print(f"成功加载自定义客户端: {client_id}")
        role_data = client.get("role_data", {})
    
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
            # 使用默认的Djjo数据作为后备
            from ai_role_simulator.data import (
                base_profile as default_base,
                dynamic_state as default_dynamic, 
                interaction_rules as default_rules,
                cognitive_emotional_model as default_cognitive,
                conversation_profile as default_conversation,
                impedance_rules as default_impedance
            )
            default_data = {
                'base_profile': default_base,
                'dynamic_state': default_dynamic,
                'interaction_rules': default_rules,
                'cognitive_emotional_model': default_cognitive,
                'conversation_profile': default_conversation,
                'impedance_rules': default_impedance
            }
            display_role_data[key] = default_data[key]
    
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

            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = openai_client.chat.completions.create(
                        model=app.config['OPENAI_MODEL'],
                        messages=simplified_messages,
                        max_tokens=400,  # 增加到400个token，让回答更详细
                        timeout=40
                    )
                    return response.choices[0].message.content
                except Exception as api_error:
                    if attempt < max_retries - 1:
                        app.logger.warning(f"OpenAI API 尝试 {attempt + 1} 失败: {str(api_error)}，正在重试...")
                        import time
                        time.sleep(2)
                    else:
                        app.logger.error(f"OpenAI API 所有尝试失败: {str(api_error)}")
                        return "抱歉，我暂时无法回应，请稍后再试。"
                
        except Exception as error:
            app.logger.error(f"生成响应失败: {str(error)}")
            return "生成响应失败，请重试或联系开发者"
    
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
            return AIRoleSimulator(
                generate_fn, 
                role_data={},  # 使用空数据作为后备
                max_turns=70
            )
        except Exception as e2:
            print(f"备用模拟器也创建失败: {str(e2)}")
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
            session.permanent = True
            
            session['exam_mode'] = True
            session.modified = True
            
            # 初始化模拟器
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
                "不要直接暴露核心问题，表现出适当的防御和不确定性。"
                "在咨询刚开始(尤其是第一次咨询时)，话语要更简短，并表现出更多的谨和防御。"
                "牢记你是正在寻求心理帮助的角色，因为你知道自己需要帮助，你会相对主动的陈述你的需求或者觉得不舒服的地方。"
                "请基于你的设定和故事背景，尽可能充分的表达自己的诉求和过往经历，语言尽可能丰富。"
                "不要说:'会按照所设置的规则来扮演心理咨询来访者Djjo。如果有需要进一步调整我的行为，请随时告诉我。准备好了，可以开始模拟咨询。'，请扮演一位真正需要帮助的来访者，第一句话可以是'你好，嗯...我不知道从哪里开始'"
                
                "在以下情况出现时，在话语中表现出对咨询师的不信任、质疑、或敌意;"
                    "1,在咨询过程中，咨询师的回复没有让你感到共情、支持、被理解时,"
                    "2,在咨询师的回复机械、刻板、重复、不自然、或缺乏人情味时,"
                    "3,在咨询师一次提出多个问题，或说了其他让你难以回复的话时,"
                    "4,在咨询师只顾提问或提建议，而没有更多倾听和共情你的感受时,"
                    "5,在咨询师遗忘了你的基本情况或你从前提到过的关键信息时"
                    "6,根据你的对话风格配置文件，使用适当的阻抗策略，如简短回应、否认问题、转移话题等。"
            ) 
             
            try:
                initial_message = simulator.generate_response([{"role": "user", "content": initial_prompt}])
                print(f"初始消息生成成功: {initial_message[:50]}...")
            except Exception as e:
                print(f"初始消息生成失败: {str(e)}")
                initial_message = "您好,我最近总是睡不好..."
            
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
            # 如果不是预设客户端，从 client_manager 获取
            client = client_manager.get_client(client_id)
            if not client:
                print(f"错误 - 客户端 {client_id} 不存在")
                return render_template('error.html', error_code=404, error_title="来访者不存在"), 404
            print(f"成功加载自定义客户端: {client_id}")
        
        # 确保会话ID存在
        if 'sid' not in session:
            session['sid'] = os.urandom(24).hex()
            print(f"新会话ID已生成: {session['sid']}")

        processing_time = time.time() - start_time
        if processing_time > 10:
            app.logger.warning(f"会话启动处理时间较长: {processing_time:.2f}秒")
            
        # 设置客户端ID和会话永久性
        session['client_id'] = client_id
        session.permanent = True
        
        # 强制保存会话
        session.modified = True
        
        # 初始化模拟器
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
            "不要直接暴露核心问题，表现出适当的防御和不确定性。"
            "在咨询刚开始(尤其是第一次咨询时)，话语要更简短，并表现出更多的谨和防御。"
            "牢记你是正在寻求心理帮助的角色，因为你知道自己需要帮助，你会相对主动的陈述你的需求或者觉得不舒服的地方。"
            "请基于你的设定和故事背景，尽可能充分的表达自己的诉求和过往经历，语言尽可能丰富。"
            "不要说:'会按照所设置的规则来扮演心理咨询来访者Djjo。如果有需要进一步调整我的行为，请随时告诉我。准备好了，可以开始模拟咨询。'，请扮演一位真正需要帮助的来访者，第一句话可以是'你好，嗯...我不知道从哪里开始'"
            
            "在以下情况出现时，在话语中表现出对咨询师的不信任、质疑、或敌意;"
                "1,在咨询过程中，咨询师的回复没有让你感到共情、支持、被理解时,"
                "2,在咨询师的回复机械、刻板、重复、不自然、或缺乏人情味时,"
                "3,在咨询师一次提出多个问题，或说了其他让你难以回复的话时,"
                "4,在咨询师只顾提问或提建议，而没有更多倾听和共情你的感受时,"
                "5,在咨询师遗忘了你的基本情况或你从前提到过的关键信息时"
                "6,根据你的对话风格配置文件，使用适当的阻抗策略，如简短回应、否认问题、转移话题等。"
        ) 
         
        try:
            initial_message = simulator.generate_response([{"role": "user", "content": initial_prompt}])
            print(f"初始消息生成成功: {initial_message[:50]}...")
        except Exception as e:
            print(f"初始消息生成失败: {str(e)}")
            initial_message = "您好,我最近总是睡不好..."
        
        # 初始化会话记录
        session['conversation'] = [
            {"role": "ai", "content": initial_message}
        ]
        
        # 再次确保会话保存
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
                
# @app.route('/start-session/client_djjo')
# def handle_djjo():
#     return redirect('/start-session/client_djjo')

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


# ---------- WAI 评分：后端实现（新增） ----------
import json
try:
    # optional: 读取 docx 的库（非必须）
    from docx import Document
except Exception:
    Document = None

def load_wai_text():
    """
    尝试加载项目根目录下的 WAI.docx（或 WAI.txt），
    如不可用则返回一个简短的内置说明（fallback）。
    """
    try:
        base_paths = [
            os.path.join(app.root_path, 'WAI.docx'),
            os.path.join(app.root_path, 'WAI.txt'),
            os.path.join(os.getcwd(), 'WAI.docx'),
            '/mnt/data/WAI.docx'
        ]
        for p in base_paths:
            if p and os.path.exists(p):
                if p.lower().endswith('.docx') and Document is not None:
                    doc = Document(p)
                    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
                else:
                    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                        return f.read()
    except Exception as e:
        app.logger.warning(f"加载 WAI 文档失败: {e}")
    # fallback brief description (will still work)
    return (
        "WAI（Working Alliance Inventory）包含几个维度："
        "关系亲密度(Alliance/Bond)、目标一致性(Goals)、任务一致性(Tasks)等。"
        "要求对咨询师在对话中的行为进行评分（1-5），并给出简短理由与改进建议。"
    )

def make_wai_prompt(wai_text, conversation, mode='train', meta=None):
    """
    构建给模型的 prompt。要求模型返回 **JSON** 格式如下：
    {
      "wai_scores": {"bond":4,"task":3,"goal":5},
      "wai_total": 12,
      "item_comments": {"bond":"...","task":"...","goal":"..."},
      "suggestions": ["...","..."],
      "brief_rationale": "..."
    }
    """
    convo_text = ""
    for m in conversation:
        role = m.get('role', '')
        content = m.get('content', '')
        convo_text += f"{role.upper()}: {content}\n"

    meta_info = ""
    if meta:
        meta_info = "\n".join([f"{k}: {v}" for k, v in meta.items()])

    instruction = (
        "You are an expert clinical supervisor and psychotherapist trainer. "
        "Using the WAI guidance below, evaluate the CONSULTANT/THERAPIST's performance in the conversation. "
        "Output a JSON object only (no extra commentary) with these fields:\n"
        " - wai_scores: an object with numeric scores 1-5 for 'bond', 'task', 'goal'\n"
        " - wai_total: integer sum\n"
        " - item_comments: short 1-2 sentence justification for each item\n"
        " - suggestions: list of 3 brief actionable suggestions for the therapist\n"
        " - brief_rationale: one-sentence overall rationale\n"
        "If you cannot rate, return scores as null and explain in brief_rationale.\n\n"
        f"WAI reference (use for guidance):\n{wai_text}\n\n"
        f"Conversation (most recent last):\n{convo_text}\n\n"
        f"Meta:\n{meta_info}\n\n"
        "Return VALID JSON only. Use Chinese if the conversation is in Chinese; otherwise use English."
    )
    return instruction

@app.route('/api/wai-feedback', methods=['POST'])
@require_session
def wai_feedback():
    """
    通用 WAI 评分 API（训练/考试共用）。
    前端不需要传 conversation（会从 session/file 读取），可传 mode/meta。
    返回 JSON：{wai_scores, wai_total, item_comments, suggestions, brief_rationale, raw_text}
    """
    try:
        payload = request.get_json(force=True, silent=True) or {}
        mode = payload.get('mode', 'train')
        extra_meta = payload.get('meta', {})
        # 获取对话记录（优先文件，再 session）
        session_id = session.get('sid')
        conversation = load_conversation_from_file(session_id)
        if not conversation:
            conversation = session.get('conversation', [])

        if not conversation:
            return jsonify({"error": "没有对话内容"}), 400

        # 读取 WAI 文档（若存在）
        wai_text = load_wai_text()

        prompt = make_wai_prompt(wai_text, conversation, mode=mode, meta=extra_meta)

        # 调用 OpenAI via existing openai_client
        messages = [
            {"role": "system", "content": "You are a concise, structured evaluator."},
            {"role": "user", "content": prompt}
        ]

        # 调用模型
        try:
            resp = openai_client.chat.completions.create(
                model=app.config.get('OPENAI_MODEL'),
                messages=messages,
                max_tokens=800,
                timeout=60
            )
            text = resp.choices[0].message.content.strip()
        except Exception as e:
            app.logger.error(f"WAI 模型调用失败: {e}")
            return jsonify({"error": "模型调用失败", "detail": str(e)}), 500

        # 尝试解析 JSON（宽容处理）
        parsed = None
        try:
            parsed = json.loads(text)
        except Exception:
            # 有时模型会在文本前后附带 Markdown 或说明，尝试抽取 JSON 子串
            import re
            m = re.search(r'(\{.*\})', text, re.S)
            if m:
                try:
                    parsed = json.loads(m.group(1))
                except Exception:
                    parsed = None

        result = {
            "raw_text": text
        }
        if parsed and isinstance(parsed, dict):
            result.update(parsed)
        else:
            # 当解析失败时，放回 raw_text 并返回提醒
            result.update({
                "wai_scores": None,
                "wai_total": None,
                "item_comments": None,
                "suggestions": None,
                "brief_rationale": None,
                "note": "模型输出无法解析为JSON，请检查 raw_text 字段"
            })

        # 将 wai 评分保存到 session['last_feedback'] 以便后续导出
        session['last_feedback'] = result
        session.modified = True

        # 同时把最后反馈也写入 last_report（如果存在），以便 PDF 导出包含 WAI
        last_report = session.get('last_report', {})
        last_report['wai_feedback'] = result
        session['last_report'] = last_report
        session.modified = True

        return jsonify(result)

    except Exception as error:
        app.logger.error(f"WAI 评分失败: {str(error)}")
        return jsonify({"error": str(error)}), 500
# ---------- WAI 评分实现结束 ----------


@app.route('/api/export-report', methods=['POST'])
@require_session
def export_report():
    """
    导出训练模式报告（包含 WAI 评分），从 session['last_report'] 读取
    若前端 POST 了 report_data，则使用 POST 的数据（优先）
    """
    try:
        # 优先使用 POST 提交的数据（如果有）
        data = None
        try:
            data = request.get_json(silent=True) or {}
        except Exception:
            data = {}

        report_data = session.get('last_report') or {}
        # merge: POST data overrides session data if provided
        if data:
            report_data = { **report_data, **data.get('report_data', data) }

        if not report_data:
            return jsonify({"error": "没有可导出的报告"}), 400

        # PDF 基本信息
        tz = pytz.timezone("Asia/Shanghai")
        now_text = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

        # 使用内存缓冲生成 PDF
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)

        styles = getSampleStyleSheet()
        styles["Normal"].fontName = "ZTFont"
        styles["Heading1"].fontName = "ZTFont"
        styles["Heading2"].fontName = "ZTFont"

        story = []

        # 标题
        story.append(Paragraph("<b>训练反馈报告</b>", styles["Heading1"]))
        story.append(Spacer(1, 8))
        story.append(Paragraph(f"生成时间（北京时间）：{now_text}", styles["Normal"]))
        story.append(Spacer(1, 12))

        # 基本信息区
        story.append(Paragraph("<b>基本信息</b>", styles["Heading2"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"来访者: {report_data.get('client_name', '未知')}", styles["Normal"]))
        story.append(Paragraph(f"主要问题: {report_data.get('client_issue', '')}", styles["Normal"]))
        story.append(Paragraph(f"对话时间: {report_data.get('conversation_date', '')}", styles["Normal"]))
        story.append(Paragraph(f"对话轮次: {report_data.get('total_turns', 0)}", styles["Normal"]))
        story.append(Paragraph(f"预计用时: {report_data.get('estimated_time', '')}", styles["Normal"]))
        story.append(Spacer(1, 12))

        # 关键洞察
        story.append(Paragraph("<b>关键洞察（Key Insights）</b>", styles["Heading2"]))
        story.append(Spacer(1, 6))
        for insight in report_data.get('key_insights', []):
            story.append(Paragraph(f"- {insight}", styles["Normal"]))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 8))

        # 专业建议
        story.append(Paragraph("<b>专业建议（Professional Advice）</b>", styles["Heading2"]))
        story.append(Spacer(1, 6))
        for suggestion in report_data.get('professional_advice', []):
            story.append(Paragraph(f"- {suggestion}", styles["Normal"]))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 10))

        # 如果有 WAI 评分，则加入表格化的量表展示
        wai = report_data.get('wai_feedback') or session.get('last_feedback')
        if wai:
            story.append(Paragraph("<b>WAI 评分（Working Alliance Inventory）</b>", styles["Heading2"]))
            story.append(Spacer(1, 6))

            # 简要分数（Bond / Task / Goal / Total）
            scores = wai.get('wai_scores') if isinstance(wai.get('wai_scores'), dict) else {}
            wai_total = wai.get('wai_total', wai.get('total') or '无')
            story.append(Paragraph(f"Bond: {scores.get('bond', '无')}    Task: {scores.get('task', '无')}    Goal: {scores.get('goal', '无')}    总分: {wai_total}", styles["Normal"]))
            story.append(Spacer(1, 8))

            # 构造表格：如果有 item-level 数据则尽量展示
            # table header
            table_data = [["条目 (Question)", "得分 (Score)", "评语 (Comment)"]]

            # item_scores 或 item_comments：先尝试 item_comments（WAI 后端一般返回 item_comments）
            item_comments = wai.get('item_comments') or {}
            item_scores = wai.get('item_scores') or {}

            # 如果 item_comments 是 dict，按 key 列表显示
            if isinstance(item_comments, dict) and len(item_comments) > 0:
                for k, v in item_comments.items():
                    score_val = item_scores.get(k, "")
                    table_data.append([str(k), str(score_val), str(v)])
            else:
                # 尝试把 short items（如果提供了 list）
                items = wai.get('items') or wai.get('questions') or []
                scores_list = wai.get('item_values') or []
                comments_list = wai.get('item_comments_list') or []
                if isinstance(items, list) and items:
                    for idx, itm in enumerate(items):
                        sc = scores_list[idx] if idx < len(scores_list) else ""
                        cm = comments_list[idx] if idx < len(comments_list) else ""
                        table_data.append([str(itm), str(sc), str(cm)])
                else:
                    # fallback: 把 brief_rationale / suggestions / raw_text 显示为单行
                    brief = wai.get('brief_rationale') or wai.get('brief', '')
                    if brief:
                        table_data.append(["总评理由", "", str(brief)])
                    # suggestions as separate rows
                    suggestions = wai.get('suggestions') or []
                    for s in suggestions:
                        table_data.append(["建议", "", str(s)])

            # 创建表格并添加样式
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

        # 伦理注意事项（如果有）
        if report_data.get('ethical_violations'):
            story.append(Paragraph("<b>伦理注意事项</b>", styles["Heading2"]))
            story.append(Spacer(1, 6))
            for ev in report_data.get('ethical_violations', []):
                story.append(Paragraph(f"- {ev}", styles["Normal"]))
                story.append(Spacer(1, 4))

        # 结束并写入 PDF
        doc.build(story)

        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"training_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", mimetype="application/pdf")

    except Exception as e:
        current_app.logger.error(f"导出训练报告失败: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/export-exam-report', methods=['POST'])
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
        styles["Normal"].fontName = "ZTFont"
        styles["Heading1"].fontName = "ZTFont"
        styles["Heading2"].fontName = "ZTFont"

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
@require_session
def end_session():
    """结束当前会话并返回报告数据"""
    try:
        # 确保会话ID存在
        if 'sid' not in session:
            session['sid'] = os.urandom(24).hex()
            
        session_id = session.get('sid')
        client_id = session.get('client_id')
        
        if not session_id or not client_id:
            return jsonify({"error": "会话未初始化"}), 400
        
        # 获取对话记录 - 优先从文件读取
        conversation = load_conversation_from_file(session_id)
        if not conversation:
            # 如果没有文件记录，使用会话中的记录
            conversation = session.get('conversation', [])
        
        if not conversation:
            return jsonify({"error": "没有对话内容"}), 400
        
        # 获取客户端信息
        from ai_role_simulator import CLIENT_IDS
        client = CLIENT_IDS.get(client_id)
        if not client:
            client = client_manager.get_client(client_id)
        
        if not client:
            return jsonify({"error": "客户端信息不存在"}), 404
        
        # 生成报告数据
        total_turns = len([msg for msg in conversation if msg['role'] == 'user'])
        estimated_time = total_turns * 2  # 假设每轮对话2分钟
        
        report_data = {
            "client_name": client.get('name', '未知来访者'),
            "client_issue": client.get('issue', '未指定问题'),
            "conversation_date": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "total_turns": total_turns,
            "estimated_time": f"{estimated_time} 分钟",
            "key_insights": [
                "第3轮对话中，咨询师的共情回应让来访者开始开放心扉",
                "第8轮对话中，直接的问题让来访者表现出防御性",
                "来访者在谈到家庭话题时表现出明显的情绪波动"
            ],
            "professional_advice": [
                "建议更多使用开放式问题，减少封闭式提问",
                "在敏感话题上可以更加渐进地探索",
                "注意非语言信号的观察，适时给予情感支持"
            ],
            "ethical_violations": [
                "第12轮对话中可能存在双重关系风险的建议",
                "需要注意保密原则的边界"
            ]
        }
        
        # 存储报告数据到会话
        session['last_report'] = report_data
        session.modified = True
        
        # 清理会话数据（保留client_id和sid以便后续操作）
        session.pop('conversation', None)
        
        return jsonify({
            "success": True,
            "report": report_data
        })
        
    except Exception as error:
        app.logger.error(f"结束会话失败: {str(error)}")
        return jsonify({"error": str(error)}), 500

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

        # 初始化模拟器
        simulator = create_simulator(client_id)
        if not simulator:
            print(f"错误 - 模拟器初始化失败")
            return render_template('error.html',
                         error_code=500,
                         error_title="服务器错误",
                         error_message="AI模拟器初始化失败"), 500
        
        print(f"模拟器创建成功")
        
        # 使用与训练模式完全相同的初始提示
        initial_prompt = (
            "现在你是一位心理咨询来访者，刚见到咨询师。"
            "不要直接暴露核心问题，表现出适当的防御和不确定性。"
            "在咨询刚开始(尤其是第一次咨询时)，话语要更简短，并表现出更多的谨和防御。"
            "牢记你是正在寻求心理帮助的角色，因为你知道自己需要帮助，你会相对主动的陈述你的需求或者觉得不舒服的地方。"
            "请基于你的设定和故事背景，尽可能充分的表达自己的诉求和过往经历，语言尽可能丰富。"
            "不要说:'会按照所设置的规则来扮演心理咨询来访者Djjo。如果有需要进一步调整我的行为，请随时告诉我。准备好了，可以开始模拟咨询。'，请扮演一位真正需要帮助的来访者，第一句话可以是'你好，嗯...我不知道从哪里开始'"
            
            "在以下情况出现时，在话语中表现出对咨询师的不信任、质疑、或敌意;"
                "1,在咨询过程中，咨询师的回复没有让你感到共情、支持、被理解时,"
                "2,在咨询师的回复机械、刻板、重复、不自然、或缺乏人情味时,"
                "3,在咨询师一次提出多个问题，或说了其他让你难以回复的话时,"
                "4,在咨询师只顾提问或提建议，而没有更多倾听和共情你的感受时,"
                "5,在咨询师遗忘了你的基本情况或你从前提到过的关键信息时"
                "6,根据你的对话风格配置文件，使用适当的阻抗策略，如简短回应、否认问题、转移话题等。"
        ) 
         
        try:
            initial_message = simulator.generate_response([{"role": "user", "content": initial_prompt}])
            print(f"初始消息生成成功: {initial_message[:50]}...")
        except Exception as e:
            print(f"初始消息生成失败: {str(e)}")
            initial_message = "您好,我最近总是睡不好..."
        
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
    Config.init_dirs()  # 确保所有目录存在
    app.run(host='0.0.0.0', port=5000, debug=False)











