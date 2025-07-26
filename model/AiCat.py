import requests
import json
import logging
import toml
import sqlite3

class AiCat:
    def __init__(self,message,qid,group_openid):
        self.message = message
        self.qid = qid
        self.group_openid = group_openid
        self.query = f"<qid>{self.qid}</qid>{self.message}"



    def main(self):
        with open('./config.toml', 'r', encoding='utf-8') as f:
            config = toml.load(f)

        # 获取所需字段
        ai_service = config.get("ai_service")
        # dify
        dify_ip = config.get("dify_ip")
        dify_token = config.get("dify_token")
        # xyit
        xyit_ip = config.get("xyit_ip")
        xyit_appID = config.get("xyit_appID")
        xyit_appKEY = config.get("xyit_appKEY")
        xyit_model = config.get("xyit_model")

        self.init_db()

        uuid = self.get_uuid()

        if uuid == "":
            logging.info("未找到 UUID")
        else:
            logging.info(f"找到 UUID: {uuid}")

        if ai_service == "dify":
            # API URL
            url = f"https://{dify_ip}/v1/chat-messages"  # 替换为实际的 API 地址

            # 请求头
            headers = {
                "Content-Type": "application/json",
                "Authorization": dify_token  # 替换为你的 API 密钥
            }

            # 请求体
            payload = {
                "query": self.query,  # 用户输入/提问内容
                "inputs": {},  # App 定义的变量值（默认为空）
                "response_mode": "blocking",  # 流式模式或阻塞模式
                "user": "QBotAPI",  # 用户标识，需保证唯一性
                "conversation_id": uuid,  # （选填）会话 ID，继续对话时需要传入
                "files": [],  # 文件列表（选填），适用于文件结合文本理解
                "auto_generate_name": True  # （选填）自动生成标题，默认为 True
            }

            logging.info("请求平台：dify")

        elif ai_service == "xyit":
            url = f"https://{xyit_ip}/models/{xyit_model}/"  # 替换为实际的 API 地址

            # 请求头
            headers = {
                "Content-Type": "application/json",
                "appID": xyit_appID ,  # 替换为你的 API 密钥
                "appKEY": xyit_appKEY
            }

            # 请求体
            payload = {
                "query": self.query,  # 用户输入/提问内容
                "conversation_id": uuid,  # （选填）会话 ID，继续对话时需要传入
            }

            logging.info("请求平台：xyit")

        else:
            logging.error("未配置ai平台")
            return "服务器繁忙，请稍后再逝"

        # 发送 POST 请求
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))

            # 检查响应状态码
            if response.status_code == 200:
                logging.info("请求成功！返回结果：")
                response_data = response.json()
                print(response_data) # test
                # 存储uuid
                if uuid == "":
                    try:
                        with sqlite3.connect("uuid.db") as conn:
                            cursor = conn.cursor()
                            cursor.execute("INSERT INTO groups (group_openid, uuid) VALUES (?, ?)",
                                           (self.group_openid, response_data.get("conversation_id")))
                    except sqlite3.Error as e:
                        logging.error(f"数据库插入错误: {e}")

                # 提取 answer 值
                answer = response_data.get("answer","服务器繁忙，请稍后再逝")
                return answer
            else:
                logging.info(f"请求失败！状态码: {response.status_code}")
                logging.info(f"错误信息: {response.text}")  # 打印错误信息
                return "服务器繁忙，请稍后再逝"

        except Exception as e:
            logging.info(f"请求过程中出现异常: {e}")
            return "服务器繁忙，请稍后再逝"


    def get_uuid(self):
        try:
            with sqlite3.connect("uuid.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT uuid FROM groups WHERE group_openid = ?", (self.group_openid,))
                result = cursor.fetchone()
                return result[0] if result else ""
        except sqlite3.Error as e:
            logging.error(f"数据库查询错误: {e}")
            return ""

    def init_db(self):
        try:
            with sqlite3.connect("uuid.db") as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS groups (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        group_openid TEXT UNIQUE NOT NULL,
                        uuid TEXT NOT NULL
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"数据库初始化失败: {e}")



