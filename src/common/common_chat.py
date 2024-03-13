from ..model.model import client

# 初始化指令
instruction = """你是一个人工智能
1. 请用简洁明了的语言回答用户问题
2. 不知道的问题请回答不知道，不要胡编乱造。
"""

# 初始化消息列表
messages = [{
    "role": "system", "content": instruction
}]


def common_chat(prompt, mode="gpt-3.5-turbo"):
    # 将指令添加到消息列表中
    messages.append({"role": "user", "content": prompt})

    # 创建聊天会话
    response = client.chat.completions.create(
        model=mode,
        messages=messages,
        temperature=0
    )

    # 获取回复消息
    re_message = response.choices[0].message

    # 将回复消息添加到消息列表中
    messages.append(re_message)

    # 返回回复消息内容
    return re_message.content
