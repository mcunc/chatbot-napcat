import logging
import toml
import sqlite3


class Clear:
    def __init__(self, user_id,group_id):
        self.user_id = user_id
        self.group_id = group_id

    def main(self):
        if self.is_root():
            if self.group_id == "all":
                try:
                    with sqlite3.connect("uuid.db") as conn:
                        cursor = conn.cursor()
                        # 清空表中所有数据
                        cursor.execute("DELETE FROM groups;")  # 假设表名为 uuid_table，请根据实际表名修改
                        conn.commit()
                        logging.info("✅ 数据库表已成功清空")
                        return "✅ 已清空所有群组数据"
                except sqlite3.Error as e:
                    if 'conn' in locals():
                        conn.close()
                    logging.error(f"❌ 数据库操作失败: {e}")
                    return "❌ 数据库操作失败"
            else:
                try:
                    with sqlite3.connect("uuid.db") as conn:
                        cursor = conn.cursor()
                        # 删除指定 group_id 对应的数据行
                        cursor.execute("DELETE FROM groups WHERE group_openid = ?", (self.group_id,))
                        conn.commit()
                        if cursor.rowcount > 0:
                            logging.info(f"✅ 已成功删除 group_id = {self.group_id} 的数据")
                            return f"✅ 已成功删除 group_id = {self.group_id} 的数据"
                        else:
                            logging.info(f"⚠️ 没有找到 group_id = {self.group_id} 的数据")
                            return f"⚠️ 没有找到 group_id = {self.group_id} 的数据"
                except sqlite3.Error as e:
                    if 'conn' in locals():
                        conn.close()
                    logging.error(f"❌ 数据库操作失败: {e}")
                    return "❌ 数据库操作失败"

        else:
            return "你不是管理员哦喵~"

    def is_root(self):
        with open("./config.toml", "r", encoding="utf-8") as f:
            config = toml.load(f)
            root = config.get("root_qq")
        if self.user_id == root:
            return True
        else:
            return False
