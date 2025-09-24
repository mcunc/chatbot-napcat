import requests
import json
from model.logger import setup_logger
import toml
from model.sql_tools import init_db
from model.sql_tools import get_uuid
from model.sql_tools import add_uuid


logger = setup_logger()
def main(message, group_openid):
    with open('./config.toml', 'r', encoding='utf-8') as f:
        config = toml.load(f)

        error_message = config.get("error_message")

        # dify
        dify_ip = config.get("dify_ip")
        dify_token = config.get("dify_token")
        init_db()

    uuid = get_uuid(group_openid)

    if uuid == "":
        logging.info("未找到 UUID")
    else:
        logging.info(f"找到 UUID: {uuid}")

    url = f"{dify_ip}/v1/chat-messages"  # 替换为实际的 API 地址

    # 请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": dify_token  # 替换为你的 API 密钥
    }

    # 请求体
    payload = {
        "query": message,  # 用户输入/提问内容
        "inputs": {},  # App 定义的变量值（默认为空）
        "response_mode": "blocking",  # 流式模式或阻塞模式
        "user": "chatbot_napcat",  # 用户标识，需保证唯一性
        "conversation_id": uuid,  # （选填）会话 ID，继续对话时需要传入
        "files": [],  # 文件列表（选填），适用于文件结合文本理解
        "auto_generate_name": True  # （选填）自动生成标题，默认为 True
    }

    logging.info("请求平台：dify")


    # 发送 POST 请求
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # 检查响应状态码
        if response.status_code == 200:
            logging.info("请求成功！返回结果：")
            response_data = response.json()
            print(response_data)  # test
            # 存储uuid
            if uuid == "":
                uuid = response_data.get("conversation_id")
                add_uuid(group_openid, uuid)

            # 提取 answer 值
            answer = response_data.get("answer", error_message)
            return answer
        else:
            logging.info(f"请求失败！状态码: {response.status_code}")
            logging.info(f"错误信息: {response.text}")  # 打印错误信息
            return error_message

    except Exception as e:
        logging.info(f"请求过程中出现异常: {e}")
        return error_message


