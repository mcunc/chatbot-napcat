# 🤖 chatbot-napcat – 基于 NapCat 的聊天 QQ 机器人
---

一款基于 NapCat 构建的 QQ 机器人，对接 dify 和 xyit平台。 支持与AI大模型聊天

[QQ交流群](https://qm.qq.com/q/ngLB6lVX3i)


## 🚀 主要功能

- ✅ 入群欢迎消息  
- 🚪 退群提醒  
- 🤝 自动添加好友  
- 🤖 AI模型聊天  
- 💨 清空历史记录  
- 🧩 配合提示词实现单群多人互动


\[开发中功能\]

暂无


## 🛠️ 部署指南

### 环境要求
安装python > 3.9

### 安装步骤
1. 下载本项目最新源码：
   ```
   git clone https://github.com/xyit2025/chatbot-napcat.git
   ```
2. 安装依赖库
3. 运行 main.py

### AI平台
1. dify: [https://dify.ai/](https://dify.ai/)  
你可以使用dify云平台或私有部署dify 并编写你的AI工作流

2. xyit 官网页面编写中，了解详情请加Q群：[https://qm.qq.com/q/D9CbFJMc6I](971108214)
你可以使用xyit体验我们训练好的AI模型

## 配置
配置文件：
```toml

        #napcat配置
bot_qq = 123456 #机器人q号
root_qq = 1234567 # 管理员q号
ws_uri = "loacalhost:3001" # ws 地址, 可自定义端口, 默认 3001
webui_uri = "loacalhost:6099" # webui 地址, 可自定义端口, 默认 6099
webui_token =  "napcat" # webui 令牌, 默认 napcat
ws_token = "" # ws_uri 令牌, 默认留空
ws_listen_ip = "localhost" # ws_uri 监听 ip, 默认 localhost 监听本机，监听全部则配置 0.0.0.0
remote_mode = false # 是否远程模式, 即 NapCat 服务不在本机运行 ps：ncatbot官方已废弃该参数

# 功能配置
allowed_groups = "all" # 授权群聊，all为全部，eg：[123456789, 987654321]
allowed_users = "all" # 授权用户，all为全部，eg：[123456789, 987654321]
ai_service = "xyit" # ai平台 支持 “dify” “xyit"
friend_auto = false # 好友自动同意
group_auto = true
group_welcome = false # 入群欢迎
group_welcome_message = "!at 欢迎加入本群，使用@bot /help获取此bot帮助" # 入群消息 !at 为@加群用户
group_leave = false # 退群提醒
group_leave_message = "用户{userid}退群了" # 退群消息 ，{userid}为退群用户id

# dify配置 ai_service选择dify时需配置
dify_ip= "" # ip:端口
dify_token = "" # token

# xyit配置 ai_service选择xyit时需配置
xyit_ip = "ai.openapi.xyit.net" # ip 此项一般不需用修改
xyit_appID = "" # appID
xyit_appKEY = "" # appKEY
xyit_model = "maoniang" # 模型名称

```

## 参与开发
由于部分原因，我们的代码均在私有git开发。
如希望参与开发请联系我们