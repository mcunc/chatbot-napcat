import toml
from model.logger import setup_logger
from http import HTTPStatus
from dashscope import Application
from model.sql_tools import init_db
from model.sql_tools import get_uuid
from model.sql_tools import add_uuid


logger = setup_logger()
def main(message, group_openid):
    with open('./config.toml', 'r', encoding='utf-8') as f:
        config = toml.load(f)

        error_message = config.get("error_message")

        # aliyun
        aliyun_app_id = config.get("aliyun_app_id")
        aliyun_api_key = config.get("aliyun_api_key")
        init_db()

    uuid = get_uuid(group_openid)

    if uuid == "":
        logger.info("未找到 UUID")
    else:
        logger.info(f"找到 UUID: {uuid}")

    # 发送请求
    response = Application.call(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=aliyun_api_key,
        app_id=aliyun_app_id,
        prompt= message,
        session_id = group_openid
    )


    # 检查响应状态码
    if response.status_code != HTTPStatus.OK:
        logger.info(f"请求失败！状态码: {response.status_code}")
        logger.info(f"错误信息: {response.message}")  # 打印错误信息
        return error_message
    else:
        logger.info("请求成功！返回结果：")
        print(f"message: {response.output.text}, session_id: {response.output.session_id}")  # test
        # 存储uuid
        if uuid == "":
            uuid = response.output.session_id
            add_uuid(group_openid, uuid)

        # 提取 answer 值
        answer = response.output.text
        return answer



