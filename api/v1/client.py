from flask import Blueprint, request, jsonify
from flask import current_app as app
from datetime import datetime
import json
from ai_role_simulator import AIRoleSimulator
from openai import OpenAI
from .utils import validate_api_key, rate_limit

import logging

api_blueprint = Blueprint('client_api', __name__)

@api_blueprint.route('/client/response', methods=['GET', 'POST'])
@validate_api_key
@rate_limit
def get_client_response():
    # 处理GET请求
    app.logger.info(f"API请求 - 客户端IP: {request.remote_addr}, 方法: {request.method}")

    """
    获取AI来访者响应
    请求格式:
    {
        "client_id": "来访者ID",
        "conversation": [
            {"role": "user", "content": "你好，最近怎么样？"},
            {"role": "assistant", "content": "你好，最近我遇到了一些事..."}
        ],
         
        "api_key": "可选API密钥"
     
    }

    """
    if request.method == 'GET':
        client_id = request.args.get('client_id')
        if not client_id:
            return jsonify({"error": "缺少client_id参数"}), 400
            
        try:
            dialog_history = json.loads(request.args.get('dialog_history', '[]'))
        except json.JSONDecodeError:
            return jsonify({"error": "无效的对话历史格式"}), 400
            
        data = {
            "client_id": client_id,
            "conversation": dialog_history
        }
    else:
        data = request.get_json()
        if not data:
            return jsonify({"error": "无效的请求数据"}), 400
        
    if len(data.get('conversation', [])) > app.config.get('MAX_CONVERSATION_TURNS', 100):
        return jsonify({
            "error": "对话轮次超过限制",
            "max_turns": 100,
            "current_turns": len(data['conversation'])
        }), 400
    
    # 共用处理逻辑
    try:
        client = app.client_manager.get_client(data['client_id'])
        if not client:
            return jsonify({"error": "来访者不存在"}), 404

        openai_client = OpenAI(
            api_key=app.config['OPENAI_API_KEY'],
            base_url=app.config['OPENAI_API_BASE'] if app.config['OPENAI_API_BASE'] else None
        )
        app.logger.debug(f"生成响应 - 来访者ID: {data['client_id']}, 当前轮次: {len(data.get('conversation', []))}")


        def generate_fn(messages):
            try:
                response = openai_client.chat.completions.create(
                    model=app.config['OPENAI_MODEL'],
                    messages=messages,
                    max_tokens=200
                )
                return response.choices[0].message.content
            except Exception as e:
                app.logger.error(f"OpenAI API错误: {str(e)}")
                return "API调用错误"

        simulator = AIRoleSimulator(generate_fn, role_data=client["role_data"])
        response = simulator.generate_response(data['conversation'])
        return jsonify({
            "success": True,
            "response": response,
            "client_id": data['client_id'],
            "updated_state": client["role_data"]["dynamic_state"],  # 返回更新后的状态
            "current_turns": len(data['conversation']) + 1,
            "version": "1.1.0",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        app.logger.error(f"API处理错误 - 客户端IP: {request.remote_addr}, 错误: {str(e)}", exc_info=True) 
        return jsonify({
            "error": "内部服务器错误",
            "details": str(e)
        }), 500

    

@api_blueprint.route('/client/list', methods=['GET'])
def list_clients():
    try:
        clients = app.client_manager.get_all_clients()
        simplified_clients = []
        
        for client in clients:
            role_data = client["role_data"]
            current_stage = "防御期"
            
            if "咨询记录" in role_data.get("dynamic_state", {}):
                current_stage = role_data["dynamic_state"]["咨询记录"].get("当前阶段", "防御期")
            elif "status" in role_data.get("dynamic_state", {}):
                current_stage = role_data["dynamic_state"]["status"].get("咨询进展", {}).get("阶段", "防御期")
            elif "咨询进展" in role_data.get("dynamic_state", {}):
                current_stage = role_data["dynamic_state"]["咨询进展"].get("当前阶段", "防御期")
                
            simplified_clients.append({
                "id": client["id"],
                "name": client["name"],
                "issue": client["issue"],
                "created_at": client["created_at"],
                "current_stage": current_stage
            })
        
        return jsonify({
            "success": True,
            "clients": simplified_clients,
            "count": len(simplified_clients)
        })
    
    except Exception as e:
        app.logger.error(f"获取来访者列表错误: {str(e)}")
        return jsonify({
            "error": "内部服务器错误",
            "details": str(e)
        }), 500

@api_blueprint.route('/chat', methods=['POST'])
def chat():
    from code.memory.memory import Memory
    from code.memory.summary import SummaryMemory

    try:
        data = request.get_json(force=True)
    except:
        return jsonify({"error": "Invalid JSON"}), 400

    user_message = data.get("message", "").strip()
    client_id = data.get("client_id") or session.get("client_id", "anonymous")
    role = data.get("role", "default")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # 载入会话记录（使用 blueprint 的 session）
    conversation = session.get("conversation", [])
    conversation.append({"role": "user", "content": user_message})

    # 调用 AI 模拟器
    try:
        from ai_role_simulator.simulator import Simulator
        simulator = Simulator(role=role)
        ai_response = simulator.generate_response(conversation)
    except Exception as e:
        ai_response = f"[对话引擎错误: {e}]"

    # 写入 AI 回复
    conversation.append({"role": "assistant", "content": ai_response})
    session["conversation"] = conversation
    session.modified = True

    # ---------------------------------------------------------
    #              长时记忆 Memory + 摘要 SummaryMemory
    # ---------------------------------------------------------

    try:
        # 从 code 包加载 Memory 实现
        from code.memory.memory import Memory
        from code.memory.summary import SummaryMemory
        from code.memory.utils import now_timestamp
        namespace = f"client_{client_id or session.get('client_id','anonymous')}"

        mem = Memory(namespace=namespace)
        summary = SummaryMemory(namespace=f"{namespace}_summary")

        # 保存用户消息（已经在 conversation 中，但再次写入以保证历史）
        try:
            mem.add(message, metadata={"role": "user", "ts": now_timestamp()})
        except TypeError:
            mem.add(message)

        # 保存 AI 回复
        try:
            mem.add(ai_reply, metadata={"role": "assistant", "ts": now_timestamp()})
        except TypeError:
            mem.add(ai_reply)

        # 更新摘要（把 user + assistant 最新消息追加）
        try:
            summary.add_messages([
                {"role": "user", "content": message},
                {"role": "assistant", "content": ai_reply}
            ])
        except Exception:
            # 兼容旧接口
            summary.update(message)
            summary.update(ai_reply, role="assistant")

        # 把简短摘要写入 session['last_report']，以便 PDF 导出读取
        last_report = session.get('last_report', {})
        last_report['short_summary'] = summary.get_summary()
        session['last_report'] = last_report
        session.modified = True

    except Exception as __mem_e:
        # 记忆错误不应阻塞主流程，仅记录日志
        try:
            app.logger.warning(f"Memory integration error (client.chat): {__mem_e}")
        except Exception:
            pass
    # ---------- END 插入（client.py chat） ----------

    # ---------------------------------------------------------

    return jsonify({
        "status": "ok",
        "reply": ai_response,
        "client_id": client_id
    })

