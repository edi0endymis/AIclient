import regex
from typing import List, Dict, Any, Optional, Callable
import json
import logging
from dataclasses import dataclass


@dataclass
class ConversationState:
    """对话状态跟踪器"""
    current_stage: str = "defensive"
    key_memories: List[str] = None
    last_summary: str = ""
    turn_count: int = 0  # 新增对话轮次计数器


try:
    from .data import base_profile, dynamic_state, interaction_rules
except ImportError:
    base_profile = {}
    dynamic_state = {}
    interaction_rules = {}

class AIRoleSimulator:
    def __init__(
        self,
        generate_fn: Callable[[List[Dict[str, str]]], str],
        model_name: str = "generic-model",
        system_prompt: Optional[str] = None,
        role_data: Optional[Dict[str, Any]] = None,
        enable_memory_compression: bool = True,
        max_turns: int = 100  # 新增最大轮次参数
    ):
        self.generate_fn = generate_fn
        self.model_name = model_name
        self.role_data = role_data or {
            "base_profile": base_profile,
            "dynamic_state": dynamic_state,
            "interaction_rules": interaction_rules
        }
        self.conversation_state = ConversationState()
        self.enable_compression = enable_memory_compression
        self.max_turns = max_turns  # 存储最大轮次
        self.logger = logging.getLogger(self.__class__.__name__)

        self.system_prompt = """你正在模拟心理咨询来访者{name}，请严格遵守以下规则：
        
    1. 基础背景：
    - 姓名：{name}
    - 年龄：{age}
    - 性别：{gender}
    - 当前阶段：{current_stage}
    - 主要问题：{main_issue}

    2. 行为规范：
    - 要相对主动表达，因为作为来访者，你是来主动寻求帮助、支持和建议的
    - 根据当前阶段调整回应方式：
      * 防御期：简短回应(10-30字)，可表现犹豫但必须回答
      * 试探期：中等长度(30-60字)，分享具体经历
      * 开放期：详细探讨(60-100字)，深入表达感受
    - 风格：{style}
    - 情绪表达要真实：愤怒、困惑、悲伤等要自然流露

    3. 阻抗行为规则：
    - 在咨询师回复不自然、机械或缺乏共情时表现出阻抗
    - 阻抗表现形式：简短回应、转移话题、否认问题严重性

    4. 禁止行为：
    - 不能使用专业术语
    - 不能给出对于用户的建议或分析
    - 不要忘记自己是心理咨询中的来访者

    当前是第{interaction_count}次咨询，请根据以上设定回应。"""

    def _compress_history(self, messages: List[Dict]) -> List[Dict]:
        """智能压缩历史对话（优化版）"""
        if len(messages) <= 8:  # 调整压缩阈值为8轮
            return messages
        
        compressed = [messages[0]]  # 保留初始消息
        stage_groups = []
        current_group = []
        
        # 按阶段分组
        for msg in messages[1:]:
            if msg['role'] == 'user' and 'stage_transition' in msg.get('metadata', {}):
                if current_group:
                    stage_groups.append(current_group)
                    current_group = []
            current_group.append(msg)
        
        if current_group:
            stage_groups.append(current_group)
        
        # 对每个阶段组进行智能压缩
        for group in stage_groups:
            if len(group) > 4:  # 调整组压缩阈值为4轮
                summary = self._generate_stage_summary(group)
                compressed.append({
                    'role': 'system',
                    'content': f'[阶段摘要]: {summary}',
                    'metadata': {'compressed': True}
                })
                # 保留最近2轮详细对话
                compressed.extend(group[-2:])
            else:
                compressed.extend(group)
                
        return compressed

    def _generate_stage_summary(self, messages: List[Dict]) -> str:
        """生成阶段摘要（优化版）"""
        user_messages = [m['content'] for m in messages if m['role'] == 'user']
        ai_responses = [m['content'] for m in messages if m['role'] == 'assistant']
        
        summary = f"讨论了: {user_messages[0]}...等{len(user_messages)}个话题"
        if ai_responses:
            summary += f" | 回应重点: {ai_responses[-1][:50]}..."
        return summary
    
    def _generate_system_prompt(self):
        """生成系统提示（增强版）"""
        base = self.role_data.get("base_profile", {})
        dynamic = self.role_data.get("dynamic_state", {})
        rules = self.role_data.get("interaction_rules", {})
        
        current_stage = "防御期"  # 默认值
        
        try:
            consult_record = dynamic.get("咨询记录", {})
            if consult_record:
                stage = consult_record.get("当前阶段", "防御期")
                if isinstance(stage, str):
                    current_stage = stage
                elif isinstance(stage, dict):  # 兼容旧版结构
                    current_stage = next(iter(stage.keys())), "防御期"
        except Exception as e:
            self.logger.warning(f"获取咨询阶段失败: {str(e)}")
            current_stage = "防御期"  
        
        # 添加对话轮次信息
        stage_info = f"{current_stage} (第{self.conversation_state.turn_count}轮)"
        main_issue = dynamic.get("心理特征", {}).get("核心情绪", ["未指定问题"])[0]
        interaction_count = dynamic.get("咨询记录", {}).get("总次数", 0)
        
        return self.system_prompt.format(
            name=base.get("姓名", "匿名"),
            age=base.get("年龄", 30),
            gender=base.get("性别", "未知"),
            current_stage=stage_info,
            
            main_issue=dynamic.get("心理特征", {}).get("核心情绪", [""])[0],
            style=rules.get("风格", "自然"),
            interaction_count=dynamic.get("咨询记录", {}).get("总次数", 0),
            memories=", ".join(self.conversation_state.key_memories or [])[:200],  # 限制记忆长度
            summary=self.conversation_state.last_summary[:150]  # 限制摘要长度
        )
    
    def generate_response(self, messages, clean_response=True):
        # 更新对话轮次计数器
        self.conversation_state.turn_count += 1
        
        # 每10轮自动压缩记忆（原为5轮）
        if self.enable_compression and self.conversation_state.turn_count % 10 == 0:
            messages = self._compress_history(messages)
        
        # 确保至少有用户输入
        if not messages or not any(m['role'] == 'user' for m in messages):
            messages.insert(0, {"role": "user", "content": "请开始咨询"})
        
        # 更新交互次数
        if "dynamic_state" not in self.role_data:
            self.role_data["dynamic_state"] = {}
        if "咨询记录" not in self.role_data["dynamic_state"]:
            self.role_data["dynamic_state"]["咨询记录"] = {}
        self.role_data["dynamic_state"]["咨询记录"]["总次数"] = \
            self.role_data["dynamic_state"]["咨询记录"].get("总次数", 0) + 1
        
        try:
            response = self.generate_fn([
                {"role": "system", "content": self._generate_system_prompt()},
                *messages
            ])
            
            # 基本清理
            response = response.strip()
            if not response or response.lower() in ["不知道", "不清楚"]:
                response = "等会，请让我想想怎么说。"
            
            # 每20轮生成摘要（新增）
            if self.conversation_state.turn_count % 20 == 0:
                self.conversation_state.last_summary = self._generate_stage_summary(messages[-10:])
            
            return response
        except Exception as e:
            self.logger.error(f"生成响应失败: {str(e)}")
            return "啊。这个问题...(生成响应失败)"

    def update_interaction_count(self) -> None:
        """更新交互次数（保持不变）"""
        if "dynamic_state" not in self.role_data:
            self.role_data["dynamic_state"] = {}
        self.role_data["dynamic_state"]["交互次数"] = \
            self.role_data["dynamic_state"].get("交互次数", 0) + 1

    def get_role_data(self) -> Dict[str, Any]:
        """获取角色数据（保持不变）"""
        return self.role_data


class Simulator(AIRoleSimulator):
    """Simulator 别名类，保持向后兼容性"""
    pass

# 确保 __all__ 包含 Simulator
__all__ = ['AIRoleSimulator', 'Simulator', 'ConversationState']
