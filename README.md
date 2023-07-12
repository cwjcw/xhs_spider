# xhs_spider
使用爬虫抓取小红书信息，并通过企业微信发送给自己

# wechat.py
使用企业微信发送消息和文件
## 配置
        以下信息是需要自己进行配置的
        self.CORPID = ""  # 企业ID，网上教程很多，很好找
        self.CORPSECRET = ""  # 应用Secret，网上教程很多，很好找
        self.AGENTID = ""  # 应用Agentid，网上教程很多，很好找
        self.TOUSER = userid  # 接收消息的userid，作为新建类的一个参数，不同的id用"|"隔开
        self.ACCESS_TOKEN_PATH = "access_token.conf"  # 存放access_token的路径
## 函数
里面有两个函数，
### send_message(message)
只需要填入需要发送的文本即可，仅可用于发送文本
### send_file(file)
填入需要发送的路径即可

# XhsTitle.py
通过微信的小红书小程序进行信息抓取
## 建立爬虫对象
    # 建立爬虫对象，包含3个参数
    xhs_spider = XhsTitle(keyName, authorization, sortedWay)
    # 需要搜索的关键字
    keyName = "输入需要搜索的关键字"
    # 授权令牌，可通过charles获取，教程网上很多，wxmp开头的一段文本
    authorization = "wxmp.XXXXX"
    # 排序方式，共3种，general：综合排序，hot_desc：热度排序,create_time_desc：发布时间排序
    sortedWay = "general"
## 函数
    # 获取小程序的页面内容
    idList = xhs_spider.getlist_by_name()
    # 获取解析后的信息-需要抓取文章内容的话，也是从xhs_title里面获取内容的链接
    xhs_title = xhs_spider.get_title_url(idList)
    # 获取文章链接,会生成一个列表
    links = [d['文章链接'] for d in xhs_title]
    # 输出到csv，最后会生成一个文件名包含KeyName, sortedWay,以及当天日期的csv文件
    xhs_spider.xhs_to_csv(xhs_title, fields, path='path.csv')

