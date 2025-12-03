from .simulator import AIRoleSimulator, Simulator, ConversationState
from .adapter import (
    convert_psydt_to_standard, 
    convert_patientpsi_to_standard,
    convert_psydt_lxwn_to_standard,
    convert_patientpsi_lxwn_to_standard,
    convert_psydt_mqq_to_standard,
    convert_patientpsi_mqq_to_standard,
    convert_psydt_sbjg_to_standard,
    convert_patientpsi_sbjg_to_standard,
    convert_psydt_sxsu_to_standard,
    convert_patientpsi_sxsu_to_standard,
    convert_psydt_syan_to_standard,
    convert_patientpsi_syan_to_standard
)
from .data import base_profile as djjo_base, dynamic_state as djjo_dynamic, interaction_rules as djjo_rules, cognitive_emotional_model as djjo_cognitive, conversation_profile as djjo_conversation, impedance_rules as djjo_impedance
from .data_PsyDT import client_profile as psydt_profile, dynamic_state as psydt_dynamic, interaction_rules as psydt_rules
from .data_PatientPsi import (
    self_worth, others, future, rules, assumptions,
    work, relationship, family, coping, style_params,
    events, status, notes
)

from .clients.lxwn.data_lxwn import base_profile as lxwn_base, dynamic_state as lxwn_dynamic, interaction_rules as lxwn_rules, cognitive_emotional_model as lxwn_cognitive, conversation_profile as lxwn_conversation, impedance_rules as lxwn_impedance
from .clients.lxwn.data_PsyDT_lxwn import client_profile as lxwn_psydt_profile, dynamic_state as lxwn_psydt_dynamic, interaction_rules as lxwn_psydt_rules
from .clients.lxwn.data_PatientPsi_lxwn import (
    self_worth as lxwn_self_worth, others as lxwn_others, future as lxwn_future, 
    rules as lxwn_rules_psi, assumptions as lxwn_assumptions,
    work as lxwn_work, relationship as lxwn_relationship, family as lxwn_family, 
    coping as lxwn_coping, style_params as lxwn_style_params,
    events as lxwn_events, status as lxwn_status, notes as lxwn_notes
)

from .clients.mqq.data_mqq import base_profile as mqq_base, dynamic_state as mqq_dynamic, interaction_rules as mqq_rules, cognitive_emotional_model as mqq_cognitive, conversation_profile as mqq_conversation, impedance_rules as mqq_impedance
from .clients.mqq.data_PsyDT_mqq import client_profile as mqq_psydt_profile, dynamic_state as mqq_psydt_dynamic, interaction_rules as mqq_psydt_rules
from .clients.mqq.data_PatientPsi_mqq import (
    self_worth as mqq_self_worth, others as mqq_others, future as mqq_future, 
    rules as mqq_rules_psi, assumptions as mqq_assumptions,
    work as mqq_work, relationship as mqq_relationship, family as mqq_family, 
    coping as mqq_coping, style_params as mqq_style_params,
    events as mqq_events, status as mqq_status, notes as mqq_notes
)

from .clients.sbjg.data_sbjg import base_profile as sbjg_base, dynamic_state as sbjg_dynamic, interaction_rules as sbjg_rules, cognitive_emotional_model as sbjg_cognitive, conversation_profile as sbjg_conversation, impedance_rules as sbjg_impedance
from .clients.sbjg.data_PsyDT_sbjg import client_profile as sbjg_psydt_profile, dynamic_state as sbjg_psydt_dynamic, interaction_rules as sbjg_psydt_rules
from .clients.sbjg.data_PatientPsi_sbjg import (
    self_worth as sbjg_self_worth, others as sbjg_others, future as sbjg_future, 
    rules as sbjg_rules_psi, assumptions as sbjg_assumptions,
    work as sbjg_work, relationship as sbjg_relationship, family as sbjg_family, 
    coping as sbjg_coping, style_params as sbjg_style_params,
    events as sbjg_events, status as sbjg_status, notes as sbjg_notes
)

from .clients.sxsu.data_sxsu import base_profile as sxsu_base, dynamic_state as sxsu_dynamic, interaction_rules as sxsu_rules, cognitive_emotional_model as sxsu_cognitive, conversation_profile as sxsu_conversation, impedance_rules as sxsu_impedance
from .clients.sxsu.data_PsyDT_sxsu import client_profile as sxsu_psydt_profile, dynamic_state as sxsu_psydt_dynamic, interaction_rules as sxsu_psydt_rules
from .clients.sxsu.data_PatientPsi_sxsu import (
    self_worth as sxsu_self_worth, others as sxsu_others, future as sxsu_future, 
    rules as sxsu_rules_psi, assumptions as sxsu_assumptions,
    work as sxsu_work, relationship as sxsu_relationship, family as sxsu_family, 
    coping as sxsu_coping, style_params as sxsu_style_params,
    events as sxsu_events, status as sxsu_status, notes as sxsu_notes
)

from .clients.syan.data_syan import base_profile as syan_base, dynamic_state as syan_dynamic, interaction_rules as syan_rules, cognitive_emotional_model as syan_cognitive, conversation_profile as syan_conversation, impedance_rules as syan_impedance
from .clients.syan.data_PsyDT_syan import client_profile as syan_psydt_profile, dynamic_state as syan_psydt_dynamic, interaction_rules as syan_psydt_rules
from .clients.syan.data_PatientPsi_syan import (
    self_worth as syan_self_worth, others as syan_others, future as syan_future, 
    rules as syan_rules_psi, assumptions as syan_assumptions,
    work as syan_work, relationship as syan_relationship, family as syan_family, 
    coping as syan_coping, style_params as syan_style_params,
    events as syan_events, status as syan_status, notes as syan_notes
)

__all__ = [
    'AIRoleSimulator',
    'base_profile',
    'dynamic_state', 
    'interaction_rules',
    'convert_psydt_to_standard',
    'convert_patientpsi_to_standard',
    'convert_psydt_lxwn_to_standard',
    'convert_patientpsi_lxwn_to_standard',
    'convert_psydt_mqq_to_standard',
    'convert_patientpsi_mqq_to_standard',
    'convert_psydt_sbjg_to_standard',
    'convert_patientpsi_sbjg_to_standard',
    'convert_psydt_sxsu_to_standard',
    'convert_patientpsi_sxsu_to_standard',
    'convert_psydt_syan_to_standard',
    'convert_patientpsi_syan_to_standard'
]
def convert_psydt_to_standard():
    key_events = [
        {"标签": event["事件"], "摘要": f"影响度: {event['影响度']}"}
        for event in psydt_dynamic.get("压力源", [])
    ]

    detailed_content = [
        {"标签": "核心信念", "内容": "\n".join(psydt_profile["心理特征"]["核心信念"])},
        {"标签": "情绪模式", "内容": str(psydt_profile["心理特征"]["情绪模式"])},
        {"标签": "咨询目标", "内容": "\n".join(psydt_profile["咨询目标"])}
    ]
    
    return {
        "base_profile": {
            "姓名": psydt_profile.get("姓名", "匿名"),
            "年龄": psydt_profile.get("年龄", 30),
            "性别": psydt_profile.get("性别", "未知"),
            "职业": psydt_profile.get("职业", {}),
            "家庭背景": psydt_profile.get("家庭结构", {}),
            "健康状况": psydt_profile.get("健康状况", {}),
            "关键事件": key_events,
            "具体内容": detailed_content
        },
        "dynamic_state": {
            "心理特征": {
                "核心情绪": [psydt_dynamic.get("情绪状态", {}).get("主导情绪", "")],
                "情绪强度": psydt_dynamic.get("情绪状态", {}).get("强度", 0),
                "防御机制": psydt_profile["心理特征"]["情绪模式"].get("防御机制", []),
                "认知特点": psydt_profile["心理特征"].get("认知特点", {})
            },
            "咨询进展": {
                "当前阶段": psydt_dynamic.get("咨询进展", {}).get("阶段", ""),
                "关键话题": psydt_dynamic.get("咨询进展", {}).get("关键话题", []),
                "阻抗表现": psydt_dynamic.get("咨询进展", {}).get("阻抗表现", [])
            },
            "近期压力源": psydt_dynamic.get("压力源", [])
        },
        "interaction_rules": {
            "阶段特征": psydt_rules.get("阶段特征", {}),
            "交互限制": {
                "禁忌话题": psydt_rules.get("交互限制", {}).get("绝对禁忌", []),
                "敏感话题": list(psydt_rules.get("交互限制", {}).get("敏感话题", {}).keys()),
                "阻抗策略": psydt_rules.get("阻抗策略", {})
            },
            "情绪引导": psydt_rules.get("情绪引导", {})
        },
        "cognitive_emotional_model": {
            "核心信念": psydt_profile["心理特征"].get("核心信念", []),
            "中间信念": {},
            "自动思维示例": {},
            "情绪反应模式": {},
            "行为应对策略": {}
        },
        "conversation_profile": {
            "初始风格": "戒备型",
            "风格梯度": {},
            "语言特点": [],
            "阻抗策略": []
        },
        "impedance_rules": {
            "触发条件": {},
            "表现形式": {},
            "强度等级": {},
            "阶段特异性": {},
            "处理原则": []
        }
    }

def convert_patientpsi_to_standard():
    """将PatientPsi格式转换为标准格式"""
    core_beliefs = "\n".join(self_worth + others + future)
    intermediate_beliefs = "\n".join(rules + assumptions)
    
    situational_content = [
        {"标签": "工作情境", "内容": str(work)},
        {"标签": "关系情境", "内容": str(relationship)},
        {"标签": "家庭情境", "内容": str(family)}
    ]
    
    return {
        "base_profile": {
            "姓名": "Djjo-PatientPsi",
            "年龄": 30,
            "性别": "女",
            "关键事件": [
                {"标签": event, "摘要": f"发生在{period}"} 
                for period, events_list in events.items() 
                for event in events_list
            ],
            "具体内容": [
                {"标签": "核心信念", "content": core_beliefs},
                {"标签": "中间信念", "content": intermediate_beliefs},
                {"标签": "行为模式", "content": str(coping)}
            ] + situational_content
        },

        "dynamic_state": {
            "心理特征": {
                "核心情绪": ["认知模型CCD"],
                "认知扭曲": self_worth,
                "行为模式": coping,
                "核心冲突": status.get("核心冲突", [])
            },
            "咨询记录": {
                "当前阶段": status.get("咨询进展", {}).get("阶段", "防御期"),
                "睡眠状况": status.get("睡眠质量", {}),
                "治疗注意事项": notes
            }
        },
        "interaction_rules": {
            "阶段设定": style_params.get("风格梯度", {}),
            "当前约束": {
                "禁忌话题": status.get("咨询进展", {}).get("禁忌话题", []),
                "对话特征": style_params.get("风格梯度", {}).get(
                    status.get("咨询进展", {}).get("阶段", "防御期"), {}
                ).get("特征", [])
            },
            "治疗建议": {
                "优先处理": [note for note in notes if note.startswith("优先")],
                "注意事项": [note for note in notes if note.startswith("!")]
            }
        },
        "cognitive_emotional_model": {
            "核心信念": self_worth,
            "中间信念": {
                "规则": rules,
                "假设": assumptions
            },
            "自动思维示例": {
                "工作情境": [],
                "关系情境": [],
                "家庭情境": []
            },
            "情绪反应模式": {
                "焦虑触发点": [],
                "典型情绪": []
            },
            "行为应对策略": {
                "回避行为": [],
                "过度补偿": []
            }
        },
        "conversation_profile": {
            "初始风格": "戒备型",
            "风格梯度": style_params.get("风格梯度", {}),
            "语言特点": [],
            "阻抗策略": []
        },
        "impedance_rules": {
            "触发条件": {},
            "表现形式": {},
            "强度等级": {},
            "阶段特异性": {},
            "处理原则": []
        }
    }

# lxwn
def convert_psydt_lxwn_to_standard():
    key_events = [
        {"标签": event["事件"], "摘要": f"影响度: {event['影响度']}"}
        for event in lxwn_dynamic.get("压力源", [])
    ]

    detailed_content = [
        {"标签": "核心信念", "内容": "\n".join(lxwn_psydt_profile["心理特征"]["核心信念"])},
        {"标签": "情绪模式", "内容": str(lxwn_psydt_profile["心理特征"]["情绪模式"])},
        {"标签": "咨询目标", "内容": "\n".join(lxwn_psydt_profile["咨询目标"])}
    ]
    
    return {
        "base_profile": {
            "姓名": lxwn_psydt_profile.get("姓名", "匿名"),
            "年龄": lxwn_psydt_profile.get("年龄", 25),
            "性别": lxwn_psydt_profile.get("性别", "未知"),
            "职业": lxwn_psydt_profile.get("职业", {}),
            "家庭背景": lxwn_psydt_profile.get("家庭结构", {}),
            "健康状况": lxwn_psydt_profile.get("健康状况", {}),
            "关键事件": key_events,
            "具体内容": detailed_content
        },
        "dynamic_state": {
            "心理特征": {
                "核心情绪": [lxwn_psydt_dynamic.get("情绪状态", {}).get("主导情绪", "")],
                "情绪强度": lxwn_psydt_dynamic.get("情绪状态", {}).get("强度", 0),
                "防御机制": lxwn_psydt_profile["心理特征"]["情绪模式"].get("防御机制", []),
                "认知特点": lxwn_psydt_profile["心理特征"].get("认知特点", {})
            },
            "咨询进展": {
                "当前阶段": lxwn_psydt_dynamic.get("咨询进展", {}).get("阶段", ""),
                "关键话题": lxwn_psydt_dynamic.get("咨询进展", {}).get("关键话题", []),
                "阻抗表现": lxwn_psydt_dynamic.get("咨询进展", {}).get("阻抗表现", [])
            },
            "近期压力源": lxwn_psydt_dynamic.get("压力源", [])
        },
        "interaction_rules": {
            "阶段特征": lxwn_psydt_rules.get("阶段特征", {}),
            "交互限制": {
                "禁忌话题": lxwn_psydt_rules.get("交互限制", {}).get("绝对禁忌", []),
                "敏感话题": list(lxwn_psydt_rules.get("交互限制", {}).get("敏感话题", {}).keys()),
                "阻抗策略": lxwn_psydt_rules.get("阻抗策略", {})
            },
            "情绪引导": lxwn_psydt_rules.get("情绪引导", {})
        },
        "cognitive_emotional_model": {
            "核心信念": lxwn_psydt_profile["心理特征"].get("核心信念", []),
            "中间信念": {},
            "自动思维示例": {},
            "情绪反应模式": {},
            "行为应对策略": {}
        },
        "conversation_profile": {
            "初始风格": "戒备型",
            "风格梯度": {},
            "语言特点": [],
            "阻抗策略": []
        },
        "impedance_rules": {
            "触发条件": {},
            "表现形式": {},
            "强度等级": {},
            "阶段特异性": {},
            "处理原则": []
        }
    }

def convert_patientpsi_lxwn_to_standard():
    """将PatientPsi格式转换为标准格式"""
    core_beliefs = "\n".join(lxwn_self_worth + lxwn_others + lxwn_future)
    intermediate_beliefs = "\n".join(lxwn_rules_psi + lxwn_assumptions)
    
    situational_content = [
        {"标签": "工作情境", "内容": str(lxwn_work)},
        {"标签": "关系情境", "内容": str(lxwn_relationship)},
        {"标签": "家庭情境", "内容": str(lxwn_family)}
    ]
    
    return {
        "base_profile": {
            "姓名": "lxwn-PatientPsi",
            "年龄": 25,
            "性别": "女",
            "关键事件": [
                {"标签": lxwn_events, "摘要": f"发生在{period}"} 
                for period, events_list in lxwn_events.items() 
                for lxwn_events in events_list
            ],
            "具体内容": [
                {"标签": "核心信念", "content": core_beliefs},
                {"标签": "中间信念", "content": intermediate_beliefs},
                {"标签": "行为模式", "content": str(lxwn_coping)}
            ] + situational_content
        },

        "dynamic_state": {
            "心理特征": {
                "核心情绪": ["认知模型CCD"],
                "认知扭曲": lxwn_self_worth,
                "行为模式": lxwn_coping,
                "核心冲突": lxwn_status.get("核心冲突", [])
            },
            "咨询记录": {
                "当前阶段": lxwn_status.get("咨询进展", {}).get("阶段", "防御期"),
                "睡眠状况": lxwn_status.get("睡眠质量", {}),
                "治疗注意事项": lxwn_notes
            }
        },
        "interaction_rules": {
            "阶段设定": lxwn_style_params.get("风格梯度", {}),
            "当前约束": {
                "禁忌话题": lxwn_status.get("咨询进展", {}).get("禁忌话题", []),
                "对话特征": lxwn_style_params.get("风格梯度", {}).get(
                    lxwn_status.get("咨询进展", {}).get("阶段", "防御期"), {}
                ).get("特征", [])
            },
            "治疗建议": {
                "优先处理": [note for note in lxwn_notes if note.startswith("优先")],
                "注意事项": [note for note in lxwn_notes if note.startswith("!")]
            }
        },
        "cognitive_emotional_model": {
            "核心信念": lxwn_self_worth,
            "中间信念": {
                "规则": lxwn_rules_psi,
                "假设": lxwn_assumptions
            },
            "自动思维示例": {
                "工作情境": [],
                "关系情境": [],
                "家庭情境": []
            },
            "情绪反应模式": {
                "焦虑触发点": [],
                "典型情绪": []
            },
            "行为应对策略": {
                "回避行为": [],
                "过度补偿": []
            }
        },
        "conversation_profile": {
            "初始风格": "戒备型",
            "风格梯度": lxwn_style_params.get("风格梯度", {}),
            "语言特点": [],
            "阻抗策略": []
        },
        "impedance_rules": {
            "触发条件": {},
            "表现形式": {},
            "强度等级": {},
            "阶段特异性": {},
            "处理原则": []
        }
    }

# mqq
def convert_psydt_mqq_to_standard():
    key_events = [
        {"标签": event["事件"], "摘要": f"影响度: {event['影响度']}"}
        for event in mqq_dynamic.get("压力源", [])
    ]

    detailed_content = [
        {"标签": "核心信念", "内容": "\n".join(mqq_psydt_profile["心理特征"]["核心信念"])},
        {"标签": "情绪模式", "内容": str(mqq_psydt_profile["心理特征"]["情绪模式"])},
        {"标签": "咨询目标", "内容": "\n".join(mqq_psydt_profile["咨询目标"])}
    ]
    
    return {
        "base_profile": {
            "姓名": mqq_psydt_profile.get("姓名", "匿名"),
            "年龄": mqq_psydt_profile.get("年龄", 25),
            "性别": mqq_psydt_profile.get("性别", "未知"),
            "职业": mqq_psydt_profile.get("职业", {}),
            "家庭背景": mqq_psydt_profile.get("家庭结构", {}),
            "健康状况": mqq_psydt_profile.get("健康状况", {}),
            "关键事件": key_events,
            "具体内容": detailed_content
        },
        "dynamic_state": {
            "心理特征": {
                "核心情绪": [mqq_psydt_dynamic.get("情绪状态", {}).get("主导情绪", "")],
                "情绪强度": mqq_psydt_dynamic.get("情绪状态", {}).get("强度", 0),
                "防御机制": mqq_psydt_profile["心理特征"]["情绪模式"].get("防御机制", []),
                "认知特点": mqq_psydt_profile["心理特征"].get("认知特点", {})
            },
            "咨询进展": {
                "当前阶段": mqq_psydt_dynamic.get("咨询进展", {}).get("阶段", ""),
                "关键话题": mqq_psydt_dynamic.get("咨询进展", {}).get("关键话题", []),
                "阻抗表现": mqq_psydt_dynamic.get("咨询进展", {}).get("阻抗表现", [])
            },
            "近期压力源": mqq_psydt_dynamic.get("压力源", [])
        },
        "interaction_rules": {
            "阶段特征": mqq_psydt_rules.get("阶段特征", {}),
            "交互限制": {
                "禁忌话题": mqq_psydt_rules.get("交互限制", {}).get("绝对禁忌", []),
                "敏感话题": list(mqq_psydt_rules.get("交互限制", {}).get("敏感话题", {}).keys()),
                "阻抗策略": mqq_psydt_rules.get("阻抗策略", {})
            },
            "情绪引导": mqq_psydt_rules.get("情绪引导", {})
        },
        "cognitive_emotional_model": {
            "核心信念": mqq_psydt_profile["心理特征"].get("核心信念", []),
            "中间信念": {},
            "自动思维示例": {},
            "情绪反应模式": {},
            "行为应对策略": {}
        },
        "conversation_profile": {
            "初始风格": "戒备型",
            "风格梯度": {},
            "语言特点": [],
            "阻抗策略": []
        },
        "impedance_rules": {
            "触发条件": {},
            "表现形式": {},
            "强度等级": {},
            "阶段特异性": {},
            "处理原则": []
        }
    }

def convert_patientpsi_mqq_to_standard():
    """将PatientPsi格式转换为标准格式"""
    core_beliefs = "\n".join(mqq_self_worth + mqq_others + mqq_future)
    intermediate_beliefs = "\n".join(mqq_rules_psi + mqq_assumptions)
    
    situational_content = [
        {"标签": "工作情境", "内容": str(mqq_work)},
        {"标签": "关系情境", "内容": str(mqq_relationship)},
        {"标签": "家庭情境", "内容": str(mqq_family)}
    ]
    
    return {        
        "base_profile": {
            "姓名": "mqq-PatientPsi",
            "年龄": 25,
            "性别": "女",
            "关键事件": [
                {"标签": mqq_events, "摘要": f"发生在{period}"} 
                for period, events_list in mqq_events.items() 
                for mqq_events in events_list
            ],
            "具体内容": [
                {"标签": "核心信念", "content": core_beliefs},
                {"标签": "中间信念", "content": intermediate_beliefs},
                {"标签": "行为模式", "content": str(mqq_coping)}
            ] + situational_content
        },

        "dynamic_state": {
            "心理特征": {
                "核心情绪": ["认知模型CCD"],
                "认知扭曲": mqq_self_worth,
                "行为模式": mqq_coping,
                "核心冲突": mqq_status.get("核心冲突", [])
            },
            "咨询记录": {
                "当前阶段": mqq_status.get("咨询进展", {}).get("阶段", "防御期"),
                "睡眠状况": mqq_status.get("睡眠质量", {}),
                "治疗注意事项": mqq_notes
            }
        },
        "interaction_rules": {
            "阶段设定": mqq_style_params.get("风格梯度", {}),
            "当前约束": {
                "禁忌话题": mqq_status.get("咨询进展", {}).get("禁忌话题", []),
                "对话特征": mqq_style_params.get("风格梯度", {}).get(
                    mqq_status.get("咨询进展", {}).get("阶段", "防御期"), {}
                ).get("特征", [])
            },
            "治疗建议": {
                "优先处理": [note for note in mqq_notes if note.startswith("优先")],
                "注意事项": [note for note in mqq_notes if note.startswith("!")]
            }
        },
        "cognitive_emotional_model": {
            "核心信念": mqq_self_worth,
            "中间信念": {
                "规则": mqq_rules_psi,
                "假设": mqq_assumptions
            },
            "自动思维示例": {
                "工作情境": [],
                "关系情境": [],
                "家庭情境": []
            },
            "情绪反应模式": {
                "焦虑触发点": [],
                "典型情绪": []
            },
            "行为应对策略": {
                "回避行为": [],
                "过度补偿": []
            }
        },
        "conversation_profile": {
            "初始风格": "戒备型",
            "风格梯度": mqq_style_params.get("风格梯度", {}),
            "语言特点": [],
            "阻抗策略": []
        },
        "impedance_rules": {
            "触发条件": {},
            "表现形式": {},
            "强度等级": {},
            "阶段特异性": {},
            "处理原则": []
        }
    }

# sbjg
def convert_psydt_sbjg_to_standard():
    key_events = [
        {"标签": event["事件"], "摘要": f"影响度: {event['影响度']}"}
        for event in sbjg_dynamic.get("压力源", [])
    ]

    detailed_content = [
        {"标签": "核心信念", "内容": "\n".join(sbjg_psydt_profile["心理特征"]["核心信念"])},
        {"标签": "情绪模式", "内容": str(sbjg_psydt_profile["心理特征"]["情绪模式"])},
        {"标签": "咨询目标", "内容": "\n".join(sbjg_psydt_profile["咨询目标"])}
    ]
    
    return {
        "base_profile": {
            "姓名": sbjg_psydt_profile.get("姓名", "匿名"),
            "年龄": sbjg_psydt_profile.get("年龄", 25),
            "性别": sbjg_psydt_profile.get("性别", "未知"),
            "职业": sbjg_psydt_profile.get("职业", {}),
            "家庭背景": sbjg_psydt_profile.get("家庭结构", {}),
            "健康状况": sbjg_psydt_profile.get("健康状况", {}),
            "关键事件": key_events,
            "具体内容": detailed_content
        },
        "dynamic_state": {
            "心理特征": {
                "核心情绪": [sbjg_psydt_dynamic.get("情绪状态", {}).get("主导情绪", "")],
                "情绪强度": sbjg_psydt_dynamic.get("情绪状态", {}).get("强度", 0),
                "防御机制": sbjg_psydt_profile["心理特征"]["情绪模式"].get("防御机制", []),
                "认知特点": sbjg_psydt_profile["心理特征"].get("认知特点", {})
            },
            "咨询进展": {
                "当前阶段": sbjg_psydt_dynamic.get("咨询进展", {}).get("阶段", ""),
                "关键话题": sbjg_psydt_dynamic.get("咨询进展", {}).get("关键话题", []),
                "阻抗表现": sbjg_psydt_dynamic.get("咨询进展", {}).get("阻抗表现", [])
            },
            "近期压力源": sbjg_psydt_dynamic.get("压力源", [])
        },
        "interaction_rules": {
            "阶段特征": sbjg_psydt_rules.get("阶段特征", {}),
            "交互限制": {
                "禁忌话题": sbjg_psydt_rules.get("交互限制", {}).get("绝对禁忌", []),
                "敏感话题": list(sbjg_psydt_rules.get("交互限制", {}).get("敏感话题", {}).keys()),
                "阻抗策略": sbjg_psydt_rules.get("阻抗策略", {})
            },
            "情绪引导": sbjg_psydt_rules.get("情绪引导", {})
        },
        "cognitive_emotional_model": {
            "核心信念": sbjg_psydt_profile["心理特征"].get("核心信念", []),
            "中间信念": {},
            "自动思维示例": {},
            "情绪反应模式": {},
            "行为应对策略": {}
        },
        "conversation_profile": {
            "初始风格": "戒备型",
            "风格梯度": {},
            "语言特点": [],
            "阻抗策略": []
        },
        "impedance_rules": {
            "触发条件": {},
            "表现形式": {},
            "强度等级": {},
            "阶段特异性": {},
            "处理原则": []
        }
    }

def convert_patientpsi_sbjg_to_standard():
    """将PatientPsi格式转换为标准格式"""
    core_beliefs = "\n".join(sbjg_self_worth + sbjg_others + sbjg_future)
    intermediate_beliefs = "\n".join(sbjg_rules_psi + sbjg_assumptions)
    
    situational_content = [
        {"标签": "工作情境", "内容": str(sbjg_work)},
        {"标签": "关系情境", "内容": str(sbjg_relationship)},
        {"标签": "家庭情境", "内容": str(sbjg_family)}
    ]
    
    return {
        "base_profile": {
            "姓名": "sbjg-PatientPsi",
            "年龄": 22,
            "性别": "女",
            "关键事件": [
                {"标签": sbjg_events, "摘要": f"发生在{period}"} 
                for period, events_list in sbjg_events.items() 
                for sbjg_events in events_list
            ],
            "具体内容": [
                {"标签": "核心信念", "content": core_beliefs},
                {"标签": "中间信念", "content": intermediate_beliefs},
                {"标签": "行为模式", "content": str(sbjg_coping)}
            ] + situational_content
        },

        "dynamic_state": {
            "心理特征": {
                "核心情绪": ["认知模型CCD"],
                "认知扭曲": sbjg_self_worth,
                "行为模式": sbjg_coping,
                "核心冲突": sbjg_status.get("核心冲突", [])
            },
            "咨询记录": {
                "当前阶段": sbjg_status.get("咨询进展", {}).get("阶段", "防御期"),
                "睡眠状况": sbjg_status.get("睡眠质量", {}),
                "治疗注意事项": sbjg_notes
            }
        },
        "interaction_rules": {
            "阶段设定": sbjg_style_params.get("风格梯度", {}),
            "当前约束": {
                "禁忌话题": sbjg_status.get("咨询进展", {}).get("禁忌话题", []),
                "对话特征": sbjg_style_params.get("风格梯度", {}).get(
                    sbjg_status.get("咨询进展", {}).get("阶段", "防御期"), {}
                ).get("特征", [])
            },
            "治疗建议": {
                "优先处理": [note for note in sbjg_notes if note.startswith("优先")],
                "注意事项": [note for note in sbjg_notes if note.startswith("!")]
            }
        },
        "cognitive_emotional_model": {
            "核心信念": sbjg_self_worth,
            "中间信念": {
                "规则": sbjg_rules_psi,
                "假设": sbjg_assumptions
            },
            "自动思维示例": {
                "工作情境": [],
                "关系情境": [],
                "家庭情境": []
            },
            "情绪反应模式": {
                "焦虑触发点": [],
                "典型情绪": []
            },
            "行为应对策略": {
                "回避行为": [],
                "过度补偿": []
            }
        },
        "conversation_profile": {
            "初始风格": "戒备型",
            "风格梯度": sbjg_style_params.get("风格梯度", {}),
            "语言特点": [],
            "阻抗策略": []
        },
        "impedance_rules": {
            "触发条件": {},
            "表现形式": {},
            "强度等级": {},
            "阶段特异性": {},
            "处理原则": []
        }
    }

# sxsu
def convert_psydt_sxsu_to_standard():
    key_events = [
        {"标签": event["事件"], "摘要": f"影响度: {event['影响度']}"}
        for event in sxsu_dynamic.get("压力源", [])
    ]

    detailed_content = [
        {"标签": "核心信念", "内容": "\n".join(sxsu_psydt_profile["心理特征"]["核心信念"])},
        {"标签": "情绪模式", "内容": str(sxsu_psydt_profile["心理特征"]["情绪模式"])},
        {"标签": "咨询目标", "内容": "\n".join(sxsu_psydt_profile["咨询目标"])}
    ]
    
    return {
        "base_profile": {
            "姓名": sxsu_psydt_profile.get("姓名", "匿名"),
            "年龄": sxsu_psydt_profile.get("年龄", 25),
            "性别": sxsu_psydt_profile.get("性别", "未知"),
            "职业": sxsu_psydt_profile.get("职业", {}),
            "家庭背景": sxsu_psydt_profile.get("家庭结构", {}),
            "健康状况": sxsu_psydt_profile.get("健康状况", {}),
            "关键事件": key_events,
            "具体内容": detailed_content
        },
        "dynamic_state": {
            "心理特征": {
                "核心情绪": [sxsu_psydt_dynamic.get("情绪状态", {}).get("主导情绪", "")],
                "情绪强度": sxsu_psydt_dynamic.get("情绪状态", {}).get("强度", 0),
                "防御机制": sxsu_psydt_profile["心理特征"]["情绪模式"].get("防御机制", []),
                "认知特点": sxsu_psydt_profile["心理特征"].get("认知特点", {})
            },
            "咨询进展": {
                "当前阶段": sxsu_psydt_dynamic.get("咨询进展", {}).get("阶段", ""),
                "关键话题": sxsu_psydt_dynamic.get("咨询进展", {}).get("关键话题", []),
                "阻抗表现": sxsu_psydt_dynamic.get("咨询进展", {}).get("阻抗表现", [])
            },
            "近期压力源": sxsu_psydt_dynamic.get("压力源", [])
        },
        "interaction_rules": {
            "阶段特征": sxsu_psydt_rules.get("阶段特征", {}),
            "交互限制": {
                "禁忌话题": sxsu_psydt_rules.get("交互限制", {}).get("绝对禁忌", []),
                "敏感话题": list(sxsu_psydt_rules.get("交互限制", {}).get("敏感话题", {}).keys()),
                "阻抗策略": sxsu_psydt_rules.get("阻抗策略", {})
            },
            "情绪引导": sxsu_psydt_rules.get("情绪引导", {})
        },
        "cognitive_emotional_model": {
            "核心信念": sxsu_psydt_profile["心理特征"].get("核心信念", []),
            "中间信念": {},
            "自动思维示例": {},
            "情绪反应模式": {},
            "行为应对策略": {}
        },
        "conversation_profile": {
            "初始风格": "戒备型",
            "风格梯度": {},
            "语言特点": [],
            "阻抗策略": []
        },
        "impedance_rules": {
            "触发条件": {},
            "表现形式": {},
            "强度等级": {},
            "阶段特异性": {},
            "处理原则": []
        }
    }

def convert_patientpsi_sxsu_to_standard():
    """将PatientPsi格式转换为标准格式"""
    core_beliefs = "\n".join(sxsu_self_worth + sxsu_others + sxsu_future)
    intermediate_beliefs = "\n".join(sxsu_rules_psi + sxsu_assumptions)
    
    situational_content = [
        {"标签": "工作情境", "内容": str(sxsu_work)},
        {"标签": "关系情境", "内容": str(sxsu_relationship)},
        {"标签": "家庭情境", "内容": str(sxsu_family)}
    ]
    
    return {
        "base_profile": {
            "姓名": "sxsu-PatientPsi",
            "年龄": 30,
            "性别": "男",
            "关键事件": [
                {"标签": sxsu_events, "摘要": f"发生在{period}"} 
                for period, events_list in sxsu_events.items() 
                for sxsu_events in events_list
            ],
            "具体内容": [
                {"标签": "核心信念", "content": core_beliefs},
                {"标签": "中间信念", "content": intermediate_beliefs},
                {"标签": "行为模式", "content": str(sxsu_coping)}
            ] + situational_content
        },

        "dynamic_state": {
            "心理特征": {
                "核心情绪": ["认知模型CCD"],
                "认知扭曲": sxsu_self_worth,
                "行为模式": sxsu_coping,
                "核心冲突": sxsu_status.get("核心冲突", [])
            },
            "咨询记录": {
                "当前阶段": sxsu_status.get("咨询进展", {}).get("阶段", "防御期"),
                "睡眠状况": sxsu_status.get("睡眠质量", {}),
                "治疗注意事项": sxsu_notes
            }
        },
        "interaction_rules": {
            "阶段设定": sxsu_style_params.get("风格梯度", {}),
            "当前约束": {
                "禁忌话题": sxsu_status.get("咨询进展", {}).get("禁忌话题", []),
                "对话特征": sxsu_style_params.get("风格梯度", {}).get(
                    sxsu_status.get("咨询进展", {}).get("阶段", "防御期"), {}
                ).get("特征", [])
            },
            "治疗建议": {
                "优先处理": [note for note in sxsu_notes if note.startswith("优先")],
                "注意事项": [note for note in sxsu_notes if note.startswith("!")]
            }
        },
        "cognitive_emotional_model": {
            "核心信念": sxsu_self_worth,
            "中间信念": {
                "规则": sxsu_rules_psi,
                "假设": sxsu_assumptions
            },
            "自动思维示例": {
                "工作情境": [],
                "关系情境": [],
                "家庭情境": []
            },
            "情绪反应模式": {
                "焦虑触发点": [],
                "典型情绪": []
            },
            "行为应对策略": {
                "回避行为": [],
                "过度补偿": []
            }
        },
        "conversation_profile": {
            "初始风格": "戒备型",
            "风格梯度": sxsu_style_params.get("风格梯度", {}),
            "语言特点": [],
            "阻抗策略": []
        },
        "impedance_rules": {
            "触发条件": {},
            "表现形式": {},
            "强度等级": {},
            "阶段特异性": {},
            "处理原则": []
        }
    }

# syan
def convert_psydt_syan_to_standard():
    key_events = [
        {"标签": event["事件"], "摘要": f"影响度: {event['影响度']}"}
        for event in syan_dynamic.get("压力源", [])
    ]

    detailed_content = [
        {"标签": "核心信念", "内容": "\n".join(syan_psydt_profile["心理特征"]["核心信念"])},
        {"标签": "情绪模式", "内容": str(syan_psydt_profile["心理特征"]["情绪模式"])},
        {"标签": "咨询目标", "内容": "\n".join(syan_psydt_profile["咨询目标"])}
    ]
    
    return {
        "base_profile": {
            "姓名": syan_psydt_profile.get("姓名", "匿名"),
            "年龄": syan_psydt_profile.get("年龄", 25),
            "性别": syan_psydt_profile.get("性别", "未知"),
            "职业": syan_psydt_profile.get("职业", {}),
            "家庭背景": syan_psydt_profile.get("家庭结构", {}),
            "健康状况": syan_psydt_profile.get("健康状况", {}),
            "关键事件": key_events,
            "具体内容": detailed_content
        },
        "dynamic_state": {
            "心理特征": {
                "核心情绪": [syan_psydt_dynamic.get("情绪状态", {}).get("主导情绪", "")],
                "情绪强度": syan_psydt_dynamic.get("情绪状态", {}).get("强度", 0),
                "防御机制": syan_psydt_profile["心理特征"]["情绪模式"].get("防御机制", []),
                "认知特点": syan_psydt_profile["心理特征"].get("认知特点", {})
            },
            "咨询进展": {
                "当前阶段": syan_psydt_dynamic.get("咨询进展", {}).get("阶段", ""),
                "关键话题": syan_psydt_dynamic.get("咨询进展", {}).get("关键话题", []),
                "阻抗表现": syan_psydt_dynamic.get("咨询进展", {}).get("阻抗表现", [])
            },
            "近期压力源": syan_psydt_dynamic.get("压力源", [])
        },
        "interaction_rules": {
            "阶段特征": syan_psydt_rules.get("阶段特征", {}),
            "交互限制": {
                "禁忌话题": syan_psydt_rules.get("交互限制", {}).get("绝对禁忌", []),
                "敏感话题": list(syan_psydt_rules.get("交互限制", {}).get("敏感话题", {}).keys()),
                "阻抗策略": syan_psydt_rules.get("阻抗策略", {})
            },
            "情绪引导": syan_psydt_rules.get("情绪引导", {})
        },
        "cognitive_emotional_model": {
            "核心信念": syan_psydt_profile["心理特征"].get("核心信念", []),
            "中间信念": {},
            "自动思维示例": {},
            "情绪反应模式": {},
            "行为应对策略": {}
        },
        "conversation_profile": {
            "初始风格": "戒备型",
            "风格梯度": {},
            "语言特点": [],
            "阻抗策略": []
        },
        "impedance_rules": {
            "触发条件": {},
            "表现形式": {},
            "强度等级": {},
            "阶段特异性": {},
            "处理原则": []
        }
    }

def convert_patientpsi_syan_to_standard():
    """将PatientPsi格式转换为标准格式"""
    core_beliefs = "\n".join(syan_self_worth + syan_others + syan_future)
    intermediate_beliefs = "\n".join(syan_rules_psi + syan_assumptions)
    
    situational_content = [
        {"标签": "工作情境", "内容": str(syan_work)},
        {"标签": "关系情境", "内容": str(syan_relationship)},
        {"标签": "家庭情境", "内容": str(syan_family)}
    ]
    
    return {
        "base_profile": {
            "姓名": "syan-PatientPsi",
            "年龄": 21,
            "性别": "女",
            "关键事件": [
                {"标签": syan_events, "摘要": f"发生在{period}"} 
                for period, events_list in syan_events.items() 
                for syan_events in events_list
            ],
            "具体内容": [
                {"标签": "核心信念", "content": core_beliefs},
                {"标签": "中间信念", "content": intermediate_beliefs},
                {"标签": "行为模式", "content": str(syan_coping)}
            ] + situational_content
        },

        "dynamic_state": {
            "心理特征": {
                "核心情绪": ["认知模型CCD"],
                "认知扭曲": syan_self_worth,
                "行为模式": syan_coping,
                "核心冲突": syan_status.get("核心冲突", [])
            },
            "咨询记录": {
                "当前阶段": syan_status.get("咨询进展", {}).get("阶段", "防御期"),
                "睡眠状况": syan_status.get("睡眠质量", {}),
                "治疗注意事项": syan_notes
            }
        },
        "interaction_rules": {
            "阶段设定": syan_style_params.get("风格梯度", {}),
            "当前约束": {
                "禁忌话题": syan_status.get("咨询进展", {}).get("禁忌话题", []),
                "对话特征": syan_style_params.get("风格梯度", {}).get(
                    syan_status.get("咨询进展", {}).get("阶段", "防御期"), {}
                ).get("特征", [])
            },
            "治疗建议": {
                "优先处理": [note for note in syan_notes if note.startswith("优先")],
                "注意事项": [note for note in syan_notes if note.startswith("!")]
            }
        },
        "cognitive_emotional_model": {
            "核心信念": syan_self_worth,
            "中间信念": {
                "规则": syan_rules_psi,
                "假设": syan_assumptions
            },
            "自动思维示例": {
                "工作情境": [],
                "关系情境": [],
                "家庭情境": []
            },
            "情绪反应模式": {
                "焦虑触发点": [],
                "典型情绪": []
            },
            "行为应对策略": {
                "回避行为": [],
                "过度补偿": []
            }
        },
        "conversation_profile": {
            "初始风格": "戒备型",
            "风格梯度": syan_style_params.get("风格梯度", {}),
            "语言特点": [],
            "阻抗策略": []
        },
        "impedance_rules": {
            "触发条件": {},
            "表现形式": {},
            "强度等级": {},
            "阶段特异性": {},
            "处理原则": []
        }
    }

CLIENT_IDS = {
    'client_djjo': {
        'name': 'Djjo',
        'issue': '综合',
        'role_data': {
            'base_profile': djjo_base,
            'dynamic_state': djjo_dynamic,
            'interaction_rules': djjo_rules,
            'cognitive_emotional_model': djjo_cognitive,
            'conversation_profile': djjo_conversation,
            'impedance_rules': djjo_impedance
        }
    },
    'client_psydt': {
        'name': 'Djjo-PsyDT',
        'issue': '综合-标准化后',
        'role_data': convert_psydt_to_standard()
    },
    'client_psi': {
        'name': 'Djjo-PatientPsi',
        'issue': '综合-认知模型CCD',
        'role_data': convert_patientpsi_to_standard()
    },

        # 新增来访者配置
    'client_lxwn': {
        'name': 'lxwn',
        'issue': '人际与亲密关系',
        'role_data': {
            'base_profile': lxwn_base,
            'dynamic_state': lxwn_dynamic,
            'interaction_rules': lxwn_rules,
            'cognitive_emotional_model': lxwn_cognitive,
            'conversation_profile': lxwn_conversation,
            'impedance_rules': lxwn_impedance
        }
    },
    'client_lxwn_psydt': {
        'name': 'lxwn-PsyDT',
        'issue': '人际与亲密关系-标准化后',
        'role_data': convert_psydt_lxwn_to_standard()
    },
    'client_lxwn_psi': {
        'name': 'lxwn-PatientΨ',
        'issue': '人际与亲密关系-认知模型CCD',
        'role_data': convert_patientpsi_lxwn_to_standard()
    },

        'client_mqq': {
        'name': 'mqq',
        'issue': '行为与成瘾',
        'role_data': {
            'base_profile': mqq_base,
            'dynamic_state': mqq_dynamic,
            'interaction_rules': mqq_rules,
            'cognitive_emotional_model': mqq_cognitive,
            'conversation_profile': mqq_conversation,
            'impedance_rules': mqq_impedance
        }
    },
    'client_mqq_psydt': {
        'name': 'mqq-PsyDT',
        'issue': '行为与成瘾-标准化后',
        'role_data': convert_psydt_lxwn_to_standard()
    },
    'client_mqq_psi': {
        'name': 'mqq-PatientΨ',
        'issue': '行为与成瘾-认知模型CCD',
        'role_data': convert_patientpsi_lxwn_to_standard()
    },

        'client_sbjg': {
        'name': 'sbjg',
        'issue': '适应障碍',
        'role_data': {
            'base_profile': sbjg_base,
            'dynamic_state': sbjg_dynamic,
            'interaction_rules': sbjg_rules,
            'cognitive_emotional_model': sbjg_cognitive,
            'conversation_profile': sbjg_conversation,
            'impedance_rules': sbjg_impedance
        }
        
    },
    'client_sbjg_psydt': {
        'name': 'sbjg-PsyDT',
        'issue': '适应障碍-标准化后',
        'role_data': convert_psydt_sbjg_to_standard()
    },
    'client_sbjg_psi': {
        'name': 'sbjg-PatientΨ',
        'issue': '适应障碍-认知模型CCD',
        'role_data': convert_patientpsi_sbjg_to_standard()
    },

        'client_sxsu': {
        'name': 'sxsu',
        'issue': '自我认知',
        'role_data': {
            'base_profile': sxsu_base,
            'dynamic_state': sxsu_dynamic,
            'interaction_rules': sxsu_rules,
            'cognitive_emotional_model': sxsu_cognitive,
            'conversation_profile': sxsu_conversation,
            'impedance_rules': sxsu_impedance
        }
    },
    'client_sxsu_psydt': {
        'name': 'sxsu-PsyDT',
        'issue': '自我认知-标准化后',
        'role_data': convert_psydt_sxsu_to_standard()
    },
    'client_sxsu_psi': {
        'name': 'sxsu-PatientΨ',
        'issue': '自我认知-认知模型CCD',
        'role_data': convert_patientpsi_sxsu_to_standard()
    },

        'client_syan': {
        'name': 'syan',
        'issue': '心境障碍',
        'role_data': {
            'base_profile': syan_base,
            'dynamic_state': syan_dynamic,
            'interaction_rules': syan_rules,
            'cognitive_emotional_model': syan_cognitive,
            'conversation_profile': syan_conversation,
            'impedance_rules': syan_impedance
        }
    },
    'client_syan_psydt': {
        'name': 'syan-PsyDT',
        'issue': '心境障碍-标准化后',
        'role_data': convert_psydt_syan_to_standard()
    },
    'client_syan_psi': {
        'name': 'syan-PatientΨ',
        'issue': '心境障碍-认知模型CCD',
        'role_data': convert_patientpsi_syan_to_standard()
    }

} 

try:
    # 测试导入是否成功
    test_data = {
        'base_profile': djjo_base,
        'dynamic_state': djjo_dynamic,
        'interaction_rules': djjo_rules,
        'cognitive_emotional_model': djjo_cognitive,
        'conversation_profile': djjo_conversation,
        'impedance_rules': djjo_impedance
    }
    print("Djjo数据导入成功")
except ImportError as e:
    print(f"数据导入失败: {e}")
    # 使用空字典作为后备
    djjo_base = {}
    djjo_dynamic = {}
    djjo_rules = {}
    djjo_cognitive = {}
    djjo_conversation = {}
    djjo_impedance = {}

def get_client(client_id):
    """获取指定客户端数据"""
    return CLIENT_IDS.get(client_id)

__version__ = '3.2.0'
