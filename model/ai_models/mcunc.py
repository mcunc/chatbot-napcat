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

        # mcunc
        mcunc_ip = config.get("mcunc_ip")
        mcunc_appID = config.get("mcunc_appID")
        mcunc_appKEY = config.get("mcunc_appKEY")
        mcunc_model = config.get("mcunc_model")

        init_db()

    uuid = get_uuid(group_openid)

    if uuid == "":
        logger.info("未找到 UUID")
    else:
        logger.info(f"找到 UUID: {uuid}")

    url = f"{mcunc_ip}/models/{mcunc_model}/"  # 替换为实际的 API 地址

    # 请求头
    headers = {
        "Content-Type": "application/json",
        "appID": mcunc_appID,  # 替换为你的 API 密钥
        "appKEY": mcunc_appKEY
    }

    # 请求体
    payload = {
        "query": message,  # 用户输入/提问内容
        "conversation_id": uuid,  # （选填）会话 ID，继续对话时需要传入
    }

    logger.info("请求平台：mcunc")


    # 发送 POST 请求
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # 检查响应状态码
        if response.status_code == 200:
            logger.info("请求成功！返回结果：")
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
            logger.info(f"请求失败！状态码: {response.status_code}")
            logger.info(f"错误信息: {response.text}")  # 打印错误信息
            return error_message

    except Exception as e:
        logger.info(f"请求过程中出现异常: {e}")
        return error_message
