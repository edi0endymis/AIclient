from .data_PsyDT import client_profile as data_PsyDT_client_profile
from .data_PsyDT import dynamic_state as data_PsyDT_dynamic_state
from .data_PsyDT import interaction_rules as data_PsyDT_interaction_rules
from .data_PatientPsi import (
    self_worth, others, future, rules, assumptions,
    work, relationship, family, coping, style_params,
    events, status, notes
)

def convert_psydt_to_standard():
    key_events = [
        {"标签": event["事件"], "摘要": f"影响度: {event['影响度']}"}
        for event in data_PsyDT_dynamic_state.get("压力源", [])
    ]

    detailed_content = [
        {"标签": "核心信念", "内容": "\n".join(data_PsyDT_client_profile["心理特征"]["核心信念"])},
        {"标签": "情绪模式", "内容": str(data_PsyDT_client_profile["心理特征"]["情绪模式"])},
        {"标签": "咨询目标", "内容": "\n".join(data_PsyDT_client_profile["咨询目标"])}
    ]
    
    return {
        "base_profile": {
            "姓名": data_PsyDT_client_profile.get("姓名", "匿名"),
            "年龄": data_PsyDT_client_profile.get("年龄", 30),
            "性别": data_PsyDT_client_profile.get("性别", "未知"),
            "职业": data_PsyDT_client_profile.get("职业", {}),
            "家庭背景": data_PsyDT_client_profile.get("家庭结构", {}),
            "健康状况": data_PsyDT_client_profile.get("健康状况", {}),
            "关键事件": key_events,
            "具体内容": detailed_content
        },
        "dynamic_state": {
            "心理特征": {
                "核心情绪": [data_PsyDT_dynamic_state.get("情绪状态", {}).get("主导情绪", "")],
                "情绪强度": data_PsyDT_dynamic_state.get("情绪状态", {}).get("强度", 0),
                "防御机制": data_PsyDT_client_profile["心理特征"]["情绪模式"].get("防御机制", []),
                "认知特点": data_PsyDT_client_profile["心理特征"].get("认知特点", {})
            },
            "咨询进展": {
                "当前阶段": data_PsyDT_dynamic_state.get("咨询进展", {}).get("阶段", ""),
                "关键话题": data_PsyDT_dynamic_state.get("咨询进展", {}).get("关键话题", []),
                "阻抗表现": data_PsyDT_dynamic_state.get("咨询进展", {}).get("阻抗表现", [])
            },
            "近期压力源": data_PsyDT_dynamic_state.get("压力源", [])
        },
        "interaction_rules": {
            "阶段特征": data_PsyDT_interaction_rules.get("阶段特征", {}),
            "交互限制": {
                "禁忌话题": data_PsyDT_interaction_rules.get("交互限制", {}).get("绝对禁忌", []),
                "敏感话题": list(data_PsyDT_interaction_rules.get("交互限制", {}).get("敏感话题", {}).keys())
            },
            "情绪引导": data_PsyDT_interaction_rules.get("情绪引导", {})
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
            "姓名": "Djjo-PatientΨ",
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



