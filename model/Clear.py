from model.logger import setup_logger
import toml
import sqlite3



logger = setup_logger()
class Clear:
    def __init__(self, user_id,group_id):
        self.user_id = user_id
        self.group_id = group_id

    def main(self):
        with open("config.toml", "r", encoding="utf-8"):
            config = toml.load("config.toml")
            clean_all_success_message = config.get("clean_all_success_message")
            clean_one_success_message = config.get("clean_one_success_message")
            clean_one_notfound_message = config.get("clean_one_notfound_message")
            clean_fail_message = config.get("clean_fail_message")
            clean_nopermissoin_message = config.get("clean_nopermissoin_message")

        if "{group_id}" in clean_one_success_message:
            clean_one_success_message.replace("{group_id}", self.group_id)
        if "{group_id}" in clean_one_notfound_message:
            clean_one_notfound_message.replace("{group_id}", self.group_id)

        if self.is_root():
            if self.group_id == "all":
                try:
                    with sqlite3.connect("uuid.db") as conn:
                        cursor = conn.cursor()
                        # 清空表中所有数据
                        cursor.execute("DELETE FROM groups;")  # 假设表名为 uuid_table，请根据实际表名修改
                        conn.commit()
                        logger.info("已清空所有群组数据")
                        return clean_all_success_message
                except sqlite3.Error as e:
                    if 'conn' in locals():
                        conn.close()
                    logger.error(f"数据库操作失败: {e}")
                    return clean_fail_message
            else:
                try:
                    with sqlite3.connect("uuid.db") as conn:
                        cursor = conn.cursor()
                        # 删除指定 group_id 对应的数据行
                        cursor.execute("DELETE FROM groups WHERE group_openid = ?", (self.group_id,))
                        conn.commit()
                        if cursor.rowcount > 0:
                            logger.info(f"✅ 已成功删除 group_id = {self.group_id} 的数据")
                            return clean_one_success_message
                        else:
                            logger.info(f"⚠️ 没有找到 group_id = {self.group_id} 的数据")
                            return  clean_one_notfound_message
                except sqlite3.Error as e:
                    if 'conn' in locals():
                        conn.close()
                    logger.error(f"❌ 数据库操作失败: {e}")
                    return clean_fail_message

        else:
            return clean_nopermissoin_message

    def is_root(self):
        with open("./config.toml", "r", encoding="utf-8") as f:
            config = toml.load(f)
            root = config.get("root_qq")
        if self.user_id == root:
            return True
        else:
            return False
