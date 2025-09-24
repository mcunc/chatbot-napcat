import sqlite3
from model.logger import setup_logger



logger = setup_logger()
def init_db():
    try:
        with sqlite3.connect("uuid.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS groups
                           (
                               id           INTEGER PRIMARY KEY AUTOINCREMENT,
                               group_openid TEXT UNIQUE NOT NULL,
                               uuid         TEXT        NOT NULL
                           )
                           ''')
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"数据库初始化失败: {e}")


def get_uuid(group_openid):
    try:
        with sqlite3.connect("uuid.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT uuid FROM groups WHERE group_openid = ?", (group_openid,))
            result = cursor.fetchone()
            return result[0] if result else ""
    except sqlite3.Error as e:
        logger.error(f"数据库查询错误: {e}")
        return ""

def add_uuid(group_openid, uuid):
    try:
        with sqlite3.connect("uuid.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO groups (group_openid, uuid) VALUES (?, ?)",
                           (group_openid, uuid))
    except sqlite3.Error as e:
        logger.error(f"数据库插入错误: {e}")