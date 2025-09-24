from ncatbot.core.notice import NoticeMessage
from ncatbot.core import BotClient, Request
from model.logger import setup_logger
import asyncio
from control.group import group
from control.private import private
from control.request import request
from control.notice import notice
import toml


logger = setup_logger()
with open("./config.toml", "r", encoding="utf-8") as f:
    config = toml.load(f)
    bt_uin = config.get("bot_qq")
    root = config.get("root_qq")
    ws_uri = config.get("ws_uri")
    web_uri = config.get("web_uri")
    webui_token = config.get("webui_token")
    ws_token = config.get("ws_token")
    ws_listen_ip = config.get("ws_listen_ip")
    remote_mode = config.get("remote_mode")

bot = BotClient()
api = bot.run_blocking(bt_uin=bt_uin, root=root, ws_uri=ws_uri, web_uri=web_uri, webui_token=webui_token, ws_token=ws_token, ws_listen_ip=ws_listen_ip, remote_mode=remote_mode)

@bot.group_event()
async def on_group_message(msg):
    logger.info(f"收到消息：{msg.raw_message}，来自{msg.group_id}群聊{msg.user_id}用户")
    if msg.user_id == 2854196310: # qq管家，防止刷屏。bot大战请看
        pass
    else:
        ctrl = group(msg)
        return_message = ctrl.main()
        if return_message is None:
            return
        else:
            logger.info(f"返回消息：{return_message}")
            await  bot.api.post_group_msg(group_id=msg.group_id, text=return_message, reply=msg.message_id)

@bot.private_event()
async def on_private_message(msg):
    logger.info(f"收到消息：{msg.raw_message}，来自{msg.user_id}用户")
    if msg.user_id == 2854196310: # qq管家，防止刷屏。
        pass
    else:
        ctrl = private(msg)
        return_message = ctrl.main()
        if return_message is None:
            return
        else:
            logger.info(f"返回消息：{return_message}")
            await  bot.api.post_private_msg(user_id=msg.user_id, text=return_message, reply=msg.message_id)


@bot.request_event()
async def on_request_event(msg: Request):
    logger.info(f"收到request事件：{msg.request_type}，来自{msg.group_id}群聊，{msg.user_id}用户，验证消息：{msg.comment}")
    ctrl = request(msg)
    accept_friend_application = ctrl.main()
    if accept_friend_application is True:
        await msg.reply(True, comment="请求已通过")
        logger.info("请求已通过")
    else:
        await msg.reply(False, comment="请求被拒绝")
        logger.info("请求被拒绝")



@bot.notice_event()
async  def on_notice_event(msg: NoticeMessage):
    logger.info(f"收到notice事件：{msg['notice_type']}，来自{msg['user_id']}用户")
    ctrl = notice(msg)
    return_message = ctrl.main()
    if return_message is None:
        return
    else:
        logger.info(f"返回消息：{return_message}")
        await  bot.api.post_group_msg(group_id=msg["group_id"], text=return_message)




asyncio.get_event_loop().run_forever()