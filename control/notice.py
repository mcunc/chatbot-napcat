import toml
import logging
from model.logger import setup_logger

logger = setup_logger()
class notice:
    def __init__(self,msg):
        self.time = msg.time
        self.notice_type = msg.notice_type
        self.group_id = msg.group_id
        self.operator_id = msg.operator_id
        self.user_id = msg.user_id

    def main(self):
        if self.notice_type == "group_increase":
            return self.group_increase()
        elif self.notice_type == "group_decrease":
            return self.group_decrease()
        else:
            return None

    def group_increase(self):
        try:
            with open("./config.toml", "r", encoding="utf-8") as f:
                config = toml.load(f)
                group_welcome = config.get("group_welcome")
                print(group_welcome)
                group_welcome_message = config.get("group_welcome_message")
                print(group_welcome_message)
                if group_welcome:
                    if "!at" in group_welcome_message:
                        return group_welcome_message.replace("!at", f"[CQ:at,qq={self.user_id}]")
                    else:
                        return group_welcome_message
                else:
                    return None
        except Exception as e:
            logger.error(f"读取配置文件错误：{e}")
            return None

    def group_decrease(self):
        try:
            with open("./config.toml", "r", encoding="utf-8") as f:
                config = toml.load(f)
                group_leave = config.get("group_leave")
                group_leave_message = config.get("group_leave_message")
                if group_leave:
                    if "{userid}" in group_leave_message:
                        return group_leave_message.replace("{userid}", str(self.user_id))
                    else:
                        return group_leave_message
                else:
                    return None
        except Exception as e:
            logger.error(f"读取配置文件错误：{e}")
            return None