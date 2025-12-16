# wai_questionnaire.py
"""
工作同盟量表 (Working Alliance Inventory) 问卷数据
包含当事人版和咨询员版
"""

WAI_CLIENT_ITEMS = [
    {
        "id": 1,
        "category": "bond",
        "text": "我和_____相处时觉得不自在。",
        "reverse": True
    },
    {
        "id": 2,
        "category": "task",
        "text": "_____和我同意我需做某些事以改善我的状况。",
        "reverse": False
    },
    {
        "id": 3,
        "category": "bond",
        "text": "我担心咨询的效果。",
        "reverse": True
    },
    {
        "id": 4,
        "category": "goal",
        "text": "我在咨询中所做的事情使我得到新的方式来看自己的问题。",
        "reverse": False
    },
    {
        "id": 5,
        "category": "bond",
        "text": "_____和我彼此相互了解。",
        "reverse": False
    },
    {
        "id": 6,
        "category": "goal",
        "text": "_____了解我的咨询目标。",
        "reverse": False
    },
    {
        "id": 7,
        "category": "task",
        "text": "我对自己在咨询中所做的事感到困惑。",
        "reverse": True
    },
    {
        "id": 8,
        "category": "bond",
        "text": "我相信_____喜欢我。",
        "reverse": False
    },
    {
        "id": 9,
        "category": "task",
        "text": "我期望_____和我能澄清我们咨询的目的。",
        "reverse": True
    },
    {
        "id": 10,
        "category": "goal",
        "text": "我并不同意_____认为我应从咨询中所得到的。",
        "reverse": True
    },
    {
        "id": 11,
        "category": "task",
        "text": "我相信_____和我花费在咨询上的时间并不有效。",
        "reverse": True
    },
    {
        "id": 12,
        "category": "goal",
        "text": "_____并不了解我想要在咨询中获得什么。",
        "reverse": True
    },
    {
        "id": 13,
        "category": "task",
        "text": "我明白我在咨询中的责任。",
        "reverse": False
    },
    {
        "id": 14,
        "category": "goal",
        "text": "这几次咨询的目标对我而言是重要的。",
        "reverse": False
    },
    {
        "id": 15,
        "category": "goal",
        "text": "我发现_____和我在咨询中所处理的事与我所关心的事无关。",
        "reverse": True
    },
    {
        "id": 16,
        "category": "task",
        "text": "我在咨询中所做的事将有助于我达到自己所希望的改变。",
        "reverse": False
    },
    {
        "id": 17,
        "category": "bond",
        "text": "我相信_____是真诚地关心我的福祉。",
        "reverse": False
    },
    {
        "id": 18,
        "category": "task",
        "text": "我明白_____期望我在每次咨询中做什么。",
        "reverse": False
    },
    {
        "id": 19,
        "category": "bond",
        "text": "_____和我彼此相互尊重。",
        "reverse": False
    },
    {
        "id": 20,
        "category": "bond",
        "text": "我觉得_____对我的感觉并不完全真诚。",
        "reverse": True
    },
    {
        "id": 21,
        "category": "bond",
        "text": "我自信_____有能力协助我。",
        "reverse": False
    },
    {
        "id": 22,
        "category": "task",
        "text": "_____和我正朝向彼此同意的目标努力。",
        "reverse": False
    },
    {
        "id": 23,
        "category": "bond",
        "text": "我觉得_____欣赏我。",
        "reverse": False
    },
    {
        "id": 24,
        "category": "task",
        "text": "_____和我都同意目前我所做的事是重要的。",
        "reverse": False
    },
    {
        "id": 25,
        "category": "goal",
        "text": "几次咨询结果，我较以前更清楚我可以如何改变。",
        "reverse": False
    },
    {
        "id": 26,
        "category": "bond",
        "text": "_____和我相互信任。",
        "reverse": False
    },
    {
        "id": 27,
        "category": "goal",
        "text": "_____和我的问题的认定有不同看法。",
        "reverse": True
    },
    {
        "id": 28,
        "category": "bond",
        "text": "我和_____的关系对我非常重要。",
        "reverse": False
    },
    {
        "id": 29,
        "category": "bond",
        "text": "我感觉到假如我说了或做了不当的事，_____将不再与我咨询。",
        "reverse": True
    },
    {
        "id": 30,
        "category": "task",
        "text": "_____和我共同设定我的咨询目标。",
        "reverse": False
    },
    {
        "id": 31,
        "category": "task",
        "text": "我对我在咨询中所做的事感到挫折。",
        "reverse": True
    },
    {
        "id": 32,
        "category": "goal",
        "text": "_____和我对有益于我的改变方向已具有共识。",
        "reverse": False
    },
    {
        "id": 33,
        "category": "task",
        "text": "_____要我做的事对我没多大意义。",
        "reverse": True
    },
    {
        "id": 34,
        "category": "goal",
        "text": "我不知道可期望从咨询结果中得到什么。",
        "reverse": True
    },
    {
        "id": 35,
        "category": "goal",
        "text": "我相信我们目前对我的问题的处理方向是对的。",
        "reverse": False
    },
    {
        "id": 36,
        "category": "bond",
        "text": "我觉得_____关心我，即使我所做的事他并不赞同。",
        "reverse": False
    }
]

WAI_COUNSELOR_ITEMS = [
    {
        "id": 1,
        "category": "bond",
        "text": "我和_____相处时觉得不自在。",
        "reverse": True
    },
    {
        "id": 2,
        "category": "task",
        "text": "_____和我同意采取某些步骤以改进他的状况。",
        "reverse": False
    },
    {
        "id": 3,
        "category": "bond",
        "text": "我担心咨询的效果。",
        "reverse": True
    },
    {
        "id": 4,
        "category": "goal",
        "text": "当事人和我对目前所进行的咨询活动之有效性都觉得有信心。",
        "reverse": False
    },
    {
        "id": 5,
        "category": "bond",
        "text": "我觉得我确实了解_____。",
        "reverse": False
    },
    {
        "id": 6,
        "category": "goal",
        "text": "_____和我对其咨询目标具有共识。",
        "reverse": False
    },
    {
        "id": 7,
        "category": "task",
        "text": "_____对我们在咨询中所做的事感到困惑。",
        "reverse": True
    },
    {
        "id": 8,
        "category": "bond",
        "text": "我相信_____喜欢我。",
        "reverse": False
    },
    {
        "id": 9,
        "category": "task",
        "text": "我感到有必要为_____澄清我们咨询的目的。",
        "reverse": True
    },
    {
        "id": 10,
        "category": "goal",
        "text": "我有点不同意_____对咨询目标的看法。",
        "reverse": True
    },
    {
        "id": 11,
        "category": "task",
        "text": "我相信_____和我花费在咨询上的时间不够有效。",
        "reverse": True
    },
    {
        "id": 12,
        "category": "goal",
        "text": "我对我们在咨询中要达成的事感到疑虑。",
        "reverse": True
    },
    {
        "id": 13,
        "category": "task",
        "text": "我很清楚同时也明白指出_____在咨询中的责任。",
        "reverse": False
    },
    {
        "id": 14,
        "category": "goal",
        "text": "我们咨询中所做的事对_____无多大意义。",
        "reverse": True
    },
    {
        "id": 15,
        "category": "goal",
        "text": "_____并不知道可期望从咨询结果中得到什么。",
        "reverse": True
    },
    {
        "id": 16,
        "category": "goal",
        "text": "_____相信我们目前处理他的问题的方式是对的。",
        "reverse": False
    },
    {
        "id": 17,
        "category": "bond",
        "text": "我尊重_____，即使他所做的事情我并不赞同。",
        "reverse": False
    },
    {
        "id": 18,
        "category": "task",
        "text": "我明白我在咨询中的责任。",
        "reverse": False
    },
    {
        "id": 19,
        "category": "bond",
        "text": "_____和我彼此相互尊重。",
        "reverse": False
    },
    {
        "id": 20,
        "category": "bond",
        "text": "我觉得_____对我的感觉并不完全真诚。",
        "reverse": True
    },
    {
        "id": 21,
        "category": "bond",
        "text": "我自信我有能力协助_____。",
        "reverse": False
    },
    {
        "id": 22,
        "category": "task",
        "text": "_____和我正朝向彼此同意的目标努力。",
        "reverse": False
    },
    {
        "id": 23,
        "category": "bond",
        "text": "我欣赏_____这个人。",
        "reverse": False
    },
    {
        "id": 24,
        "category": "task",
        "text": "我们同意_____应该做的重要事情。",
        "reverse": False
    },
    {
        "id": 25,
        "category": "goal",
        "text": "几次咨询结果下来_____较以前更清楚他可以如何改变。",
        "reverse": False
    },
    {
        "id": 26,
        "category": "bond",
        "text": "_____和我已建立互信。",
        "reverse": False
    },
    {
        "id": 27,
        "category": "goal",
        "text": "_____和我对他的问题的认定有不同看法。",
        "reverse": True
    },
    {
        "id": 28,
        "category": "bond",
        "text": "我们的关系对_____是重要的。",
        "reverse": False
    },
    {
        "id": 29,
        "category": "bond",
        "text": "_____担心假如他说了或做了不当的事，我将不再与他咨询。",
        "reverse": True
    },
    {
        "id": 30,
        "category": "task",
        "text": "_____和我共同设定了咨询的目标。",
        "reverse": False
    },
    {
        "id": 31,
        "category": "task",
        "text": "_____对我要他在咨询中所做的事感到挫折。",
        "reverse": True
    },
    {
        "id": 32,
        "category": "goal",
        "text": "_____和我对有益于他的改变方向已具有共识。",
        "reverse": False
    },
    {
        "id": 33,
        "category": "goal",
        "text": "我们咨询中所做的事对_____无多大意义。",
        "reverse": True
    },
    {
        "id": 34,
        "category": "goal",
        "text": "_____并不知道可期望从咨询结果中得到什么。",
        "reverse": True
    },
    {
        "id": 35,
        "category": "goal",
        "text": "_____相信我们目前处理他的问题的方式是对的。",
        "reverse": False
    },
    {
        "id": 36,
        "category": "bond",
        "text": "我尊重_____，即使他所做的事情我并不赞同。",
        "reverse": False
    }
]

# WAI维度解释
WAI_DIMENSIONS = {
    "bond": {
        "name": "情感联结",
        "description": "指咨询师与来访者之间的信任、关心、接纳等情感连接",
        "client_items": [1, 3, 5, 8, 17, 19, 20, 21, 23, 26, 28, 29, 36],
        "counselor_items": [1, 3, 5, 8, 17, 19, 20, 21, 23, 26, 28, 29, 36],
        "max_score": 91  # 13项 × 7分
    },
    "task": {
        "name": "任务合作",
        "description": "指咨询师与来访者对咨询过程中需要完成的任务达成的一致",
        "client_items": [2, 7, 9, 11, 13, 16, 18, 22, 24, 30, 31, 33],
        "counselor_items": [2, 7, 9, 11, 13, 18, 22, 24, 30, 31, 33, 18],
        "max_score": 84  # 12项 × 7分
    },
    "goal": {
        "name": "目标一致",
        "description": "指咨询师与来访者对咨询目标的共识程度",
        "client_items": [4, 6, 10, 12, 14, 15, 25, 27, 32, 34, 35],
        "counselor_items": [4, 6, 10, 12, 14, 15, 16, 25, 27, 32, 33, 34, 35],
        "max_score": 77  # 11项 × 7分（客户端版）
    }
}

# 评分标准
WAI_SCORING = {
    1: "从未",
    2: "甚少",
    3: "偶尔",
    4: "有时",
    5: "时常",
    6: "经常",
    7: "总是"
}

# 解释指南
WAI_INTERPRETATION = {
    "high": {
        "range": "6-7分",
        "description": "工作联盟关系良好",
        "interpretation": "咨询师与来访者建立了良好的信任关系，对咨询目标和任务有高度共识"
    },
    "medium": {
        "range": "4-5分",
        "description": "工作联盟关系中等",
        "interpretation": "基本建立了工作联盟，但某些方面需要进一步加强"
    },
    "low": {
        "range": "1-3分",
        "description": "工作联盟关系薄弱",
        "interpretation": "需要重点关注联盟建立，可能存在信任问题或目标不一致"
    }
}

def calculate_wai_scores(responses, role="client"):
    """
    计算WAI量表得分
    
    Args:
        responses: 字典，键为题目ID，值为得分(1-7)
        role: "client" 或 "counselor"
    
    Returns:
        包含各维度得分和总分的字典
    """
    scores = {
        "bond": 0,
        "task": 0,
        "goal": 0,
        "total": 0
    }
    
    # 根据角色选择题目列表
    items = WAI_CLIENT_ITEMS if role == "client" else WAI_COUNSELOR_ITEMS
    
    for item in items:
        item_id = item["id"]
        category = item["category"]
        reverse = item["reverse"]
        
        if item_id in responses:
            score = responses[item_id]
            # 如果是反向题，需要反转分数
            if reverse:
                score = 8 - score  # 7分制下，8 - 原始分 = 反转分
            
            scores[category] += score
    
    scores["total"] = scores["bond"] + scores["task"] + scores["goal"]
    
    # 计算平均分
    scores["bond_avg"] = round(scores["bond"] / len(WAI_DIMENSIONS["bond"][f"{role}_items"]), 2)
    scores["task_avg"] = round(scores["task"] / len(WAI_DIMENSIONS["task"][f"{role}_items"]), 2)
    scores["goal_avg"] = round(scores["goal"] / len(WAI_DIMENSIONS["goal"][f"{role}_items"]), 2)
    scores["overall_avg"] = round(scores["total"] / 36, 2)
    
    # 计算百分比
    scores["bond_percent"] = round((scores["bond"] / WAI_DIMENSIONS["bond"]["max_score"]) * 100, 1)
    scores["task_percent"] = round((scores["task"] / WAI_DIMENSIONS["task"]["max_score"]) * 100, 1)
    scores["goal_percent"] = round((scores["goal"] / WAI_DIMENSIONS["goal"]["max_score"]) * 100, 1)
    scores["total_percent"] = round((scores["total"] / (36 * 7)) * 100, 1)  # 36题，每题最高7分
    
    return scores

def interpret_wai_scores(scores):
    """解释WAI得分"""
    interpretation = {}
    
    for dimension in ["bond", "task", "goal"]:
        avg_score = scores.get(f"{dimension}_avg", 0)
        percent = scores.get(f"{dimension}_percent", 0)
        
        if avg_score >= 6:
            level = "high"
        elif avg_score >= 4:
            level = "medium"
        else:
            level = "low"
        
        interpretation[dimension] = {
            "level": level,
            "description": WAI_INTERPRETATION[level]["description"],
            "interpretation": WAI_INTERPRETATION[level]["interpretation"],
            "suggestion": generate_suggestion(dimension, level),
            "score": avg_score,
            "percent": percent
        }
    
    return interpretation

def generate_suggestion(dimension, level):
    """根据维度和等级生成建议"""
    suggestions = {
        "bond": {
            "high": "继续保持良好的情感连接，注意维护信任关系",
            "medium": "加强情感回应，增加共情表达，建立更深层的信任",
            "low": "优先建立基本信任，减少防御，增加情感支持"
        },
        "task": {
            "high": "继续保持任务共识，确保咨询方向的一致性",
            "medium": "澄清咨询任务，增加来访者对任务的认同感",
            "low": "重新协商咨询任务，确保来访者理解并认同咨询过程"
        },
        "goal": {
            "high": "继续保持目标共识，定期回顾目标进展",
            "medium": "澄清咨询目标，确保双方对目标有共同理解",
            "low": "重新设定咨询目标，确保目标具体、可达成、来访者认同"
        }
    }
    
    return suggestions.get(dimension, {}).get(level, "暂无具体建议")

def generate_wai_report(scores, interpretation, conversation_context=None):
    """生成WAI评估报告"""
    report = {
        "基本信息": {
            "评估工具": "工作同盟量表(WAI)",
            "评估维度": "情感联结、任务合作、目标一致",
            "评分标准": "1-7分制（1=从未，7=总是）"
        },
        "维度得分": {
            "情感联结": {
                "原始分": scores["bond"],
                "平均分": scores["bond_avg"],
                "百分比": f"{scores['bond_percent']}%",
                "等级": interpretation["bond"]["level"],
                "解释": interpretation["bond"]["interpretation"]
            },
            "任务合作": {
                "原始分": scores["task"],
                "平均分": scores["task_avg"],
                "百分比": f"{scores['task_percent']}%",
                "等级": interpretation["task"]["level"],
                "解释": interpretation["task"]["interpretation"]
            },
            "目标一致": {
                "原始分": scores["goal"],
                "平均分": scores["goal_avg"],
                "百分比": f"{scores['goal_percent']}%",
                "等级": interpretation["goal"]["level"],
                "解释": interpretation["goal"]["interpretation"]
            }
        },
        "总体评估": {
            "总分": scores["total"],
            "总平均分": scores["overall_avg"],
            "总百分比": f"{scores['total_percent']}%",
            "工作联盟强度": get_overall_strength(scores["total_percent"])
        },
        "专业建议": [
            interpretation["bond"]["suggestion"],
            interpretation["task"]["suggestion"],
            interpretation["goal"]["suggestion"]
        ]
    }
    
    # 如果提供了对话上下文，添加对话分析
    if conversation_context:
        report["对话分析"] = analyze_conversation_for_wai(conversation_context, scores)
    
    return report

def get_overall_strength(percent):
    """根据百分比确定工作联盟强度"""
    if percent >= 80:
        return "强"
    elif percent >= 60:
        return "中等"
    elif percent >= 40:
        return "弱"
    else:
        return "很弱"

def analyze_conversation_for_wai(conversation, scores):
    """分析对话内容，提供与WAI相关的见解"""
    analysis = {
        "情感联结表现": [],
        "任务合作表现": [],
        "目标一致表现": [],
        "需要改进的方面": []
    }
    
    # 这里可以根据对话内容进行更详细的分析
    # 目前先基于分数提供一般性分析
    
    if scores["bond_avg"] < 4:
        analysis["需要改进的方面"].append("情感联结有待加强，需增加信任建立")
    
    if scores["task_avg"] < 4:
        analysis["需要改进的方面"].append("任务合作需要改善，澄清咨询任务")
    
    if scores["goal_avg"] < 4:
        analysis["需要改进的方面"].append("目标一致性需提升，明确咨询目标")
    
    return analysis