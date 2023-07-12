# -*- coding: utf-8 -*-
import hashlib
import json

import pandas as pd
import urllib3
import requests
from bs4 import BeautifulSoup
import time
import re

urllib3.disable_warnings()


class XHSContent:

    def __init__(self, url, Authorization):
        self.url = url
        self.Authorization = Authorization

    def header(self):
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-cn',
            'Connection': 'keep-alive',
            'Host': 'www.xiaohongshu.com',
            'Referer': "https://servicewechat.com/wxffc08ac7df482a27/346/page-frame.html",
            'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 "
                          "(KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
            'Authorization': self.Authorization
        }
        return headers

    def get_x_sign(self):
        x_sign = "X"
        m = hashlib.md5()
        m.update((self.url + "WSUDD").encode())
        x_sign = x_sign + m.hexdigest()
        return x_sign

    def html_header(self):
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-cn',
            'Connection': 'keep-alive',
            'Host': 'www.xiaohongshu.com',
            'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 "
                          "(KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
            'X-Sign': self.get_x_sign(),
        }
        return headers

    def getHtmlSession(self):
        ses = requests.session()
        html = ses.get(self.url, headers=self.html_header(), verify=False)
        soup = BeautifulSoup(html.content, 'html.parser')
        return soup

    def getdata(self):
        soup = self.getHtmlSession()
        # print(f'soup is {soup}')
        script_tag = soup.find('script', {'type': 'application/ld+json'})
        if script_tag is None:
            print('无内容')
            return '无内容'
        else:
            json_ld_str = script_tag.string
            # print(f'json is {json_ld_str}')
            cleaned_data = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', json_ld_str)
            cleaned_data = cleaned_data.replace('\n', '').replace('\r\n', '').replace('\t', '')
            json_ld = json.loads(cleaned_data)
            print(json_ld['description'])
            return json_ld['description']

    # def run(self):
    #     with open('xhs.csv', mode='a') as f:
    #         for url in self.urls:
    #             print(url)
    #             description = self.getdata(url)
    #             print(description)
    #             f.write(description + '\n')
    #             time.sleep(30)


if __name__ == "__main__":
    urls = ['https://www.xiaohongshu.com/explore/64ac08f0000000000f00c2ea',
            'https://www.xiaohongshu.com/explore/64adc895000000001c00cf3b']

    content = []
    for url in urls:
        xhs_content = XHSContent(url, 'Authorization')
        # print(url)
        entire_data = xhs_content.getdata()
        a_list = [url, entire_data]
        content.append(a_list)
        print(content)
        time.sleep(15)
    pd_data = pd.DataFrame(content)
    pd_data.to_csv('test.csv', encoding='utf-8-sig', index=False)
    print(pd_data)
