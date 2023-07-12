import hashlib
from urllib import parse

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import csv

# 定义当天日期
today = datetime.today()
today_str = today.strftime('%Y%m%d')
class XhsTitle:
    def __init__(self, key_name, authorization, sorted_way):
        self.key_name = key_name
        self.authorization = authorization
        self.sorted_way = sorted_way
        self.host = 'https://www.xiaohongshu.com'

    @staticmethod
    def get_x_sign(api):
        x_sign = "X"
        m = hashlib.md5()
        m.update((api + "WSUDD").encode())
        x_sign = x_sign + m.hexdigest()
        return x_sign

    def spider(self, d_page, sort_by='general'):
        url = f'/fe_api/burdock/weixin/v2/search/notes?keyword={parse.quote(self.key_name)}&sortBy={sort_by}' \
              f'&page={d_page + 1}&pageSize=20&prependNoteIds=&needGifCover=true'
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x1800262c) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com',
            'Authorization': self.authorization,
            'X-Sign': self.get_x_sign(url)
        }
        resp = requests.get(url=self.host + url, headers=headers, timeout=5)
        if resp.status_code == 200:
            res = json.loads(resp.text)
            return res['data']['notes'], res['data']['totalCount']
        else:
            print(f'Fail:{resp.text}')

    def getlist_by_name(self, page_range=5):
        notes = []
        # 目前是每次小程序搜索，出来100条结果，然后分5页进行抓取
        for i in range(0, page_range):
            tmp = self.spider(d_page=i, sort_by=self.sorted_way)
            if len(tmp[0]) <= 0:
                break
            else:
                notes.extend(tmp[0])
            print(tmp[0])
        return notes

    @staticmethod
    def get_info(ids):
        infolist = []
        for id in ids:
            url = f"https://www.xiaohongshu.com/explore/{id}"
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                "Connection": "keep-alive",
                "Host": "www.xiaohongshu.com",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 "
                              "(KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1"
            }
            resp = requests.get(url, headers=headers)
            resp.encoding = resp.apparent_encoding
            html = resp.text
            soup = BeautifulSoup(html, 'lxml')
            json_str = soup.find(attrs={'type': 'application/ld+json'}).text
            json_str = json_str.replace('\n', '').replace('\r\n', '')
            info_dic = json.loads(json_str, strict=False)
            info_dic['link'] = url
            if info_dic['name'] != '':
                infolist.append(info_dic)
        return infolist

    @staticmethod
    def get_title_url(xhs_data):
        new_data = []
        for item in xhs_data:
            new_data.append({
                '文章链接': f"https://www.xiaohongshu.com/explore/{item['id']}",
                '作者主页': f'https://www.xiaohongshu.com/user/profile/{item["user"]["id"]}',
                '作者昵称': item['user']['nickname'],
                '文章标题': item['title'],
                '获赞数量': item['likes'],
                '发布时间': item['time'],
                '是否认证ID': item['user']['officialVerified']
            })

        return new_data

    def xhs_to_csv(self, data, field, path='x'):
        if path == 'x':
            with open(f'{today_str}{self.key_name}{self.sorted_way}.csv', 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=field)
                writer.writeheader()
                writer.writerows(data)
            print(f'保存成功，文件名为：{today_str}{self.key_name}{self.sorted_way}.csv')
        else:
            with open(path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=field)
                writer.writeheader()
                writer.writerows(data)
            print(f'保存成功，文件名为：{path}')


if __name__ == "__main__":
    # 以下3个均为class XHS的参数
    # 需要搜索的关键字
    keyName = "铂爵旅拍"
    # 授权令牌，可通过charles获取，教程网上很多
    authorization = "wxmp.eeb9954d-2ac7-4d88-beeb-2afb98566d74"
    # 排序方式，共3种，general：综合排序，hot_desc：热度排序,create_time_desc：发布时间排序
    sortedWay = "general"
    fields = ['文章链接', '作者主页', '作者昵称', '文章标题', '获赞数量', '发布时间', '是否认证ID']
    # 建立爬虫对象
    xhs_spider = XhsTitle(keyName, authorization, sortedWay)
    # 获取小程序的页面内容
    idList = xhs_spider.getlist_by_name()
    # 获取解析后的内容-需要抓取内容的话，也是从xhs_title里面获取内容的链接
    xhs_title = xhs_spider.get_title_url(idList)
    # 获取文章链接,会生成一个列表
    links = [d['文章链接'] for d in xhs_title]
    # 输出到csv，最后会生成一个文件名包含KeyName, sortedWay,以及当天日期的csv文件
    xhs_spider.xhs_to_csv(xhs_title, fields, path=r'C:\Users\Administrator\PycharmProjects\pythonProject\test\basic.csv')
