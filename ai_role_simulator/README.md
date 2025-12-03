# 通用AI角色模拟器

这是一个通用的AI角色模拟包，通过替换data.py或动态传入数据即可模拟不同角色。

## 安装

```bash
pip install -e .
```

## 使用方式

### 方式1：替换data.py

1. 创建你的角色数据文件`data.py`，必须包含:
   - `BASE_PROFILE`: 基础角色信息
   - `DYNAMIC_STATE`: 动态状态
   - `INTERACTION_RULES`: 交互规则

2. 使用示例:

```python
from openai import OpenAI
from ai_role_simulator import AIRoleSimulator

client = OpenAI(base_url="your-api-endpoint", api_key="your-api-key")
simulator = AIRoleSimulator(client)

messages = [{"role": "user", "content": "你好"}]
response = simulator.generate_response(messages)
print(response)
```

### 方式2：动态传入角色数据

```python
role_data = {
    "base_profile": {
        "姓名": "测试角色",
        "年龄": 25,
        "性别": "男"
    },
    "dynamic_state": {
        "当前阶段": "初始阶段",
        "交互次数": 0
    },
    "interaction_rules": {
        "风格": "正式"
    }
}

simulator = AIRoleSimulator(client, role_data=role_data)
```

## 高级定制

- 可以自定义系统提示模板
- 可以关闭自动清理回复内容
- 可以随时获取当前角色数据


## 异常处理

```python
try:
    response = simulator.generate_response(messages)
except ValueError as e:
    print(f"输入参数错误: {e}")
except RuntimeError as e:
    print(f"API调用失败: {e}")
