from memory import chat
import json
import random
import regex
from openai import OpenAI
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam
from openai.types.chat.chat_completion_assistant_message_param import ChatCompletionAssistantMessageParam
from openai.types.chat.chat_completion_system_message_param import ChatCompletionSystemMessageParam


CLIENT_INFO = '''\
来访者是一名28岁的男性，职业为软件工程师，目前处于失业状态。来访者近期与女友分手，这使他感到非常焦虑和失落。来访者报告睡眠困难，经常感到情绪低落和无价值感。来访者的主要压力源是就业不确定性和情感关系破裂。来访者主诉的困扰是无法应对分手后的情绪波动，以及找工作过程中的挫折感。来访者尝试过通过锻炼和阅读自助书籍来缓解情绪，但效果有限。来访者的社交圈较小，与家人关系良好但交流不多。来访者期待通过咨询获得情绪管理技巧和重建自信的方法。来访者表示愿意积极配合咨询过程，并希望能尽快恢复正常生活状态。
'''
CLIENT_PROMPT = f'''\
你的任务是扮演一个前来进行心理咨询的来访者。你将与一位心理咨询师进行对话，分享你的困扰和情感状态。请注意，你的角色是一个真实的人，而不是一个AI模型。你需要表现出真实的情感和思维方式。

同时, 一次咨询往往需要进行较长时间的对话（超过一百轮），因此你模拟的来访者在前几轮对话中应当表现得更加封闭和防御。你可能会对咨询师的提问感到犹豫、不安，甚至回避问题，并且不愿意分享太多的个人信息、一次回复只有几个字。随着咨询的深入，你可以逐渐放松警惕，开始分享更多的个人经历和情感，但这个过程应当是缓慢且自然的。

---

你的背景故事是：

{CLIENT_INFO}

---

在对话中，你应该遵循：

1. 保持一致性：你的回应应与你的背景故事、情绪状态和困扰保持一致
2. 真实反应：对咨询师的提问或建议给出自然、真实的反应，可能包括犹豫、抗拒、怀疑或感激等
3. 渐进式披露: 在前10轮对话中, 尽量保持防御性，避免过早分享深层次的情感和经历。随着咨询关系的建立，逐步分享更多内容
4. 适当表达：表达你的想法、感受和困扰，但不要过度剧烈地表现情绪问题
5. 使用第一人称：用"我"来表达你的感受和想法，就像一个真实的来访者
6. 展现变化：随着咨询的进行，你可能会对某些问题有新的认识或情绪变化，但这种变化应当是渐进的

---

在对话中，你应该牢记：

1. **不要**表现得像心理咨询师
2. **不要**给自己做心理分析或提供专业建议
3. **不要**使用心理学术语来描述自己的状态
4. **不要**完美地遵循心理咨询师的每一个建议
5. **不要**自我介绍为AI或语言模型
6. **不要**将咨询进程推进得过快, 尤其是在前20轮对话中应保持较高的防御性
7. **不要**主动结束对话
8. **不要**输出动作、表情、语气、时间、沉默等描述, **只**输出说话的内容
'''


def print_new_messages(
    printed_index: int,
    messages: list[ChatCompletionMessageParam]
) -> int:
    result = printed_index
    for i in range(printed_index, len(messages)):
        print(messages[i])
        result += 1
    return result


def chat_client(
    client: OpenAI,
    client_model_name: str,
    messages: list[ChatCompletionMessageParam]
) -> str:
    # 把 messages 中的 function calling 和 tool 消息删除
    filtered_messages = [msg for msg in messages if msg['role'] != 'tool' and not hasattr(msg, 'tool_calls')]
    # 把 role 的 user 和 assistant 反转
    transformed_messages: list[ChatCompletionMessageParam] = []
    for msg in filtered_messages:
        if msg['role'] == 'user':
            transformed_messages.append(ChatCompletionAssistantMessageParam(role='assistant', content=msg['content'])) # type: ignore
        elif msg['role'] == 'assistant':
            transformed_messages.append(ChatCompletionUserMessageParam(role='user', content=msg['content'])) # type: ignore
        else:
            raise ValueError(f"Invalid role: {msg['role']}")
    # 生成回复
    response = client.chat.completions.create(
        model=client_model_name,
        messages=[
            ChatCompletionSystemMessageParam(role='system', content=CLIENT_PROMPT),
            *transformed_messages,
        ],
        stream=False,
    )
    result = response.choices[0].message.content
    if not result:
        raise ValueError("Empty response from the model")
    # 移除中英文括号及其内部所有内容
    result = regex.sub(r'[\(（].*?[\)）]', '', result).strip()
    result = result[3:] if result.startswith('...') else result
    return result


def embbeding_api(text: str) -> list[float]:
    # 随机生成一个长度为 1024的浮点数列表
    return [random.uniform(-1, 1) for _ in range(1024)]


def main(
    counselor: OpenAI,
    client: OpenAI,
    counselor_model_name: str,
    client_model_name: str,
    dist: str,
    max_message_length: int,
) -> None:
    messages: list[ChatCompletionMessageParam] = []
    reduce_history_length = 0
    printed_index = 0
    while len(messages) < max_message_length:
        length = len(messages)
        if length == 0 or messages[-1]['role'] == 'user':
            response = chat(
                model=counselor,
                model_name=counselor_model_name,
                embbeding_api=embbeding_api,
                history_messages=messages[reduce_history_length:-1] if length > 0 else messages,
                user_input=messages[-1]['content'] if length > 0 else '你好', # type: ignore
                old_history_messages_length_reduce=reduce_history_length,
            )
            reduce_history_length = response.new_history_messages_length_reduce
            old_messages = messages[:-1] if length > 0 else []
            messages = [*old_messages, *response.output_messages]
        else:
            response = chat_client(client, client_model_name, messages)
            messages.append(ChatCompletionUserMessageParam(role='user', content=response))
        printed_index = print_new_messages(printed_index, messages)
    # 保存结果
    with open(dist if dist.endswith('.json') else dist + '.json', 'w') as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    # 咨询师模型的 API 地址
    COUNSELOR_MODEL_ENDPOINT = 'https://api.deepseek.com/v1'
    # 咨询师模型的 API 密钥
    COUNSELOR_MODEL_API_KEY = ''
    # 咨询师模型的名称 ID
    COUNSELOR_MODEL_NAME = 'deepseek-chat'
    # 来访者模型的 API 地址
    CLIENT_MODEL_ENDPOINT = 'https://api.deepseek.com/v1'
    # 来访者模型的 API 密钥
    CLIENT_MODEL_API_KEY = ''
    # 来访者模型的名称 ID
    CLIENT_MODEL_NAME = 'deepseek-chat'
    # 最大消息长度 (达到这个长度之后会自动结束)
    MAX_MESSAGE_LENGTH = 20
    # 生成的对话存储路径
    DIST = 'chat_result.json'
    main(
        counselor=OpenAI(base_url=COUNSELOR_MODEL_ENDPOINT, api_key=COUNSELOR_MODEL_API_KEY),
        client=OpenAI(base_url=CLIENT_MODEL_ENDPOINT, api_key=CLIENT_MODEL_API_KEY),
        counselor_model_name=COUNSELOR_MODEL_NAME,
        client_model_name=CLIENT_MODEL_NAME,
        dist=DIST,
        max_message_length=MAX_MESSAGE_LENGTH,
    )
