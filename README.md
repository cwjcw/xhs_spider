# xhs_spider
使用爬虫抓取小红书信息，并通过企业微信发送给自己
# wechat.py
## 配置
        以下信息是需要自己进行配置的
        self.CORPID = ""  # 企业ID，网上教程很多，很好找
        self.CORPSECRET = ""  # 应用Secret，网上教程很多，很好找
        self.AGENTID = ""  # 应用Agentid，网上教程很多，很好找
        self.TOUSER = userid  # 接收消息的userid，作为新建类的一个参数，不同的id用"|"隔开
        self.ACCESS_TOKEN_PATH = "access_token.conf"  # 存放access_token的路径
## 函数
里面有两个函数，
send_message(message),只需要填入需要发送的文本即可，仅可用于发送文本
send_file(file),填入需要发送的路径即可


