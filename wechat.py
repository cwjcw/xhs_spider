import requests
import time
import json


class WeChat():
    def __init__(self, userid):
        """
        配置初始信息
        """
        self.CORPID = ""  # 企业ID
        self.CORPSECRET = ""  # 应用Secret
        self.AGENTID = ""  # 应用Agentid
        self.TOUSER = userid  # 接收消息的userid
        self.ACCESS_TOKEN_PATH = "access_token.conf"  # 存放access_token的路径

    def _get_access_token(self):
        """
        调用接口返回登录信息access_token
        """
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.CORPID}&corpsecret={self.CORPSECRET}"
        res = requests.get(url=url)
        return json.loads(res.text)['access_token']

    def _save_access_token(self, cur_time):
        """
        将获取到的access_token保存到本地
        """
        with open(self.ACCESS_TOKEN_PATH, "w") as f:
            access_token = self._get_access_token()
            # 保存获取时间以及access_token
            f.write("\t".join([str(cur_time), access_token]))
        return access_token

    def get_access_token(self):
        cur_time = time.time()
        try:
            with open(self.ACCESS_TOKEN_PATH, "r") as f:
                t, access_token = f.read().split()
                # 判断access_token是否有效
                if 0 < cur_time - float(t) < 7200:
                    return access_token
                else:
                    return self._save_access_token(cur_time)
        except:
            return self._save_access_token(cur_time)

    def send_message(self, message):
        """
        发送文本消息
        """
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.get_access_token()}"
        # print(self.get_access_token())
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
            },
        }
        send_message = (bytes(json.dumps(send_values), 'utf-8'))
        res = requests.post(url, send_message)
        # print(res.text)
        return res.json()['errmsg']

    def _upload_file(self, file):
        """
        先将文件上传到临时媒体库
        """
        url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={self.get_access_token()}&type=file"
        data = {"file": open(file, "rb")}
        res = requests.post(url, files=data)
        return res.json()['media_id']

    def send_file(self, file):
        """
        发送文件
        """
        media_id = self._upload_file(file)  # 先将文件上传至临时媒体库
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.get_access_token()}"
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "file",
            "agentid": self.AGENTID,
            "file": {
                "media_id": media_id
            },
        }
        send_message = (bytes(json.dumps(send_values), 'utf-8'))
        res = requests.post(url, send_message)
        return res.json()['errmsg']
