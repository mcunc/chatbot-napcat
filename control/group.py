import logging
from model import ai_model
from model.Clear import Clear
import toml
from model.logger import setup_logger

logger = setup_logger()
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
        try:
           with open("config.toml", "r", encoding="utf-8") as f:
               config = toml.load(f)
               self.permission_denied_message = config.get("permission_denied_message")
               self.error_message = config.get("error_message")
               self.help_message = config.get("help_message")
               self.command_isnone_message = config.get("command_none_message")
               self.command_notfound_message = config.get("command_notfound_message")
               self.status_message = config.get("status_message")
               self.chatmessage_isnone_message = config.get("chatmessage_isnone_message")
        except Exception as e:
           logger.error(f"读取配置文件出现错误{e}")

   def main(self):
       is_at = self.is_at()
       if is_at is None:
           return None
       else:
           permission = self.check_permission()
           if permission is None:
               return self.error_message
           elif permission:
               return self.menu(is_at)
           else:
               return self.permission_denied_message

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
           logger.error(str(e))
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
            return self.help_message
        elif command.startswith("/cat"):#  留此指令接口为了方便qq官bot通过审核
            # 排除 " /cat "" /cat"未传参情况
            parts = command.split("/cat ", 1)
            if len(parts) > 1:
                chat_content = parts[1].strip()
                if chat_content:
                    answer = ai_model.main(chat_content, self.user_id,self.group_id)
                    return answer
                else:
                    return self.chatmessage_isnone_message
            else:
                return self.chatmessage_isnone_message
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
            return self.status_message
        elif command.startswith("/"):
            return self.command_notfound_message
        elif command == "":
            return self.command_isnone_message
        elif command is None:
            return self.command_isnone_message
        else:
            answer = ai_model.main(command, self.user_id, self.group_id)
            return answer