import logging
import toml

class request:
    def __init__(self,msg):
        self.time = msg.time
        self.self_id = msg.self_id
        self.request_type = msg.request_type
        self.sub_type = msg.sub_type
        self.group_id = msg.group_id
        self.user_id = msg.user_id
        self.comment = msg.comment
        self.flag = msg.flag

    def main(self):
        if self.request_type == "friend":
            friend_auto = self.get_info()
            if friend_auto:
                return True
            else:
                return False


    def get_info(self):
        try:
            with open("./config.toml", "r", encoding="utf-8") as f:
                config = toml.load(f)
                friend_auto = config.get("friend_auto")
            return friend_auto
        except Exception as e:
            logging.error(f"读取配置文件错误：{e}")
            return False

    def get_allow_group(self):
        try:
            with open("./config.toml", "r", encoding="utf-8") as f:
                config = toml.load(f)
                allow_group = config.get("allowed_groups")
            return allow_group
        except Exception as e:
            logging.error(f"读取配置文件错误：{e}")
            return []
