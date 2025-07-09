import logging
from model.AiCat import AiCat
from model.Clear import Clear
import toml

class group:
   def __init__(self, msg):
        self.user_id = msg.user_id
        self.group_id = msg.group_id
        self.message_id = msg.message_id
        self.message_type = msg.message_type
        self.raw_message = msg.raw_message
        self.sender = msg.sender
        self.message = msg.message
        self.self_id = msg.self_id
        self.time = msg.time

   def main(self):
       is_at = self.is_at()
       if is_at is None:
           return None
       else:
           permission = self.check_permission()
           if permission is None:
               return "服务器繁忙，请稍后再逝"
           elif permission:
               return self.menu(is_at)
           else:
               return "此bot未在该群启用"

   def is_at(self):
       for seg in self.message:
           if seg['type'] == 'at' and seg['data'].get('qq') == str(self.self_id):
               texts = [s['data']['text'].strip() for s in self.message if s['type'] == 'text']
               full_text = ' '.join(texts).strip()
               return full_text

       return None

   def check_permission(self):
       try:
           with open("./config.toml", "r", encoding="utf-8") as f:
               config = toml.load(f)
               allowed_groups = config.get("allowed_groups", [])
       except Exception as e:
           logging.error(str(e))
           return None

           # 检查当前群是否在允许列表中
       if allowed_groups == "all":
           return True
       elif self.group_id in allowed_groups:
           return True
       else:
           return False

   def menu(self,command):
        if command.startswith("/help"):
            return " 直接输入聊天内容即可 \n /help -- 获取帮助 \n /clear [群号 / private:Q号]  (all 为全部，不填为本 群/用户)  \n /status -- 查看bot状态 "
        elif command.startswith("/cat"):#  留此指令接口为了方便通过审核
            # 排除 " /cat "" /cat"未传参情况
            parts = command.split("/cat ", 1)
            if len(parts) > 1:
                chat_content = parts[1].strip()
                if chat_content:
                    cat = AiCat(chat_content, self.user_id,self.group_id)
                    answer = AiCat.main(cat)
                    return answer
                else:
                    return "你似乎没有提供想和我聊的内容喵~  \n 格式：/cat <提问内容>"
            else:
                return "你似乎没有提供想和我聊的内容喵~  \n 格式：/cat <提问内容>"
        elif command.startswith("/clear"):
            parts = command.split("/clear ", 1)
            if len(parts) > 1:
                group_id = parts[1].strip()
                if group_id:
                    clear = Clear(self.user_id,group_id)
                    return clear.main()
                else:
                    clear = Clear(self.user_id, self.group_id)
                    return  clear.main()
            else:
                clear = Clear(self.user_id, self.group_id)
                return clear.main()
        elif command.startswith("/status"):
            return "---猫娘 QBOT---\n Q bot 运行正常 \n 版本: 2.0 pre \n © 融玩文化 | 无尽创意MCUNC"
        elif command.startswith("/"):
            return "指令不存在，输入/help查看帮助"
        elif command == "":
            return "你似乎没有提供想和我聊的内容喵~  \n 直接输入聊天内容即可"
        elif command is None:
            return "你似乎没有提供想和我聊的内容喵~  \n 直接输入聊天内容即可"
        else:
            cat = AiCat(command, self.user_id,self.group_id)
            answer = AiCat.main(cat)
            return answer