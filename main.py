import os
os.environ['NCATBOT_CONFIG_PATH'] = 'ncatbot.yaml'
import toml
from ncatbot.core.event import PrivateMessageEvent, GroupMessageEvent, NoticeEvent, RequestEvent
from ncatbot.utils import ncatbot_config
from ncatbot.core import BotClient
from model.logger import setup_logger
from control.group import group
from control.private import private
from control.request import request
from control.notice import notice

logger = setup_logger()

with open("./config.toml", "r", encoding="utf-8") as f:
    config = toml.load(f)
    bt_uin = config.get("bot_qq")
    root = config.get("root_qq")
    ws_uri = config.get("ws_uri")
    webui_uri = config.get("webui_uri")
    webui_token = config.get("webui_token")
    ws_token = config.get("ws_token")
    ws_listen_ip = config.get("ws_listen_ip")
    enable_webui_interaction = config.get("enable_webui_interaction")

    ncatbot_config.set_bot_uin(bt_uin)
    ncatbot_config.set_root(root)
    ncatbot_config.set_webui_uri(webui_uri)
    ncatbot_config.set_webui_token(webui_token)
    ncatbot_config.set_ws_uri(ws_uri)
    ncatbot_config.set_ws_token(ws_token)
    ncatbot_config.set_ws_listen_ip(ws_listen_ip)
    ncatbot_config.enable_webui_interaction = enable_webui_interaction

bot = BotClient()

@bot.on_group_message()
async def on_group_message(msg: GroupMessageEvent):
    logger.info(f"收到消息：{msg.raw_message}，来自{msg.group_id}群聊{msg.user_id}用户")
    if msg.user_id == 2854196310: # qq管家，防止刷屏。bot大战请看
        pass
    else:
        ctrl = group(msg)
        return_message = ctrl.main()
        if return_message is None:
            return
        else:
            # logger.info(f"返回消息：{return_message}")
            await  msg.reply(text=return_message)

@bot.on_private_message()
async def on_private_message(msg: PrivateMessageEvent):
    logger.info(f"收到消息：{msg.raw_message}，来自{msg.user_id}用户")
    if msg.user_id == 2854196310: # qq管家，防止刷屏。
        pass
    else:
        ctrl = private(msg)
        return_message = ctrl.main()
        if return_message is None:
            return
        else:
            # logger.info(f"返回消息：{return_message}")
            await  msg.reply(text=return_message)


@bot.on_request(filter='friend')
async def on_request_event(msg: RequestEvent):
    logger.info(f"收到request事件：{msg.request_type}，来自{msg.group_id}群聊，{msg.user_id}用户，验证消息：{msg.comment}")
    logger.info(f"收到request请求，来自{msg.self_id}")
    ctrl = request(msg)
    accept_friend_application = ctrl.main()
    if accept_friend_application is True:
        await msg.reply(True)
        # logger.info("请求已通过")
    else:
        await msg.reply(False)
        # logger.info("请求被拒绝")



@bot.on_notice()
async  def on_notice_event(msg: NoticeEvent):
    logger.info(f"收到notice事件：{msg['notice_type']}，来自{msg['user_id']}用户")
    ctrl = notice(msg)
    return_message = ctrl.main()
    if return_message is None:
        return
    else:
        # logger.info(f"返回消息：{return_message}")
        await  bot.api.post_group_msg(group_id=msg["group_id"], text=return_message)


bot.run_frontend()

