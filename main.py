import XhsContent
import XhsTitle
import pandas as pd
import time
import random
from datetime import datetime
import wechat
import os
import logging

# fields = ['文章链接', '作者主页', '作者昵称', '文章标题', '获赞数量', '发布时间', '是否认证ID']
# 需要搜索的关键字
key = [""]
# 授权令牌，可通过charles获取，教程网上很多
authorization = "wxmp.XXXXX"
# 排序方式，共3种，general：综合排序，hot_desc：热度排序,create_time_desc：发布时间排序
sort = ["create_time_desc", 'general', 'hot_desc']
times = 0
# 对关键字和品牌做循环
for keyName in key:
    for sortedWay in sort:
        times = times + 1
        print(f'一共进行了{times}次循环')
        try:
            # 创建爬虫对象
            xhs_title = XhsTitle.XhsTitle(key_name=keyName, authorization=authorization, sorted_way=sortedWay)
            # 获取小程序的页面内容
            idList = xhs_title.getlist_by_name()
            # 获取解析后的内容
            xhs_basic = xhs_title.get_title_url(idList)
            # print(f'xhs_basic: {xhs_basic}')
            # 转换为DataFrame格式，方便后面进行操作
            pd_basic = pd.DataFrame(xhs_basic)
            # print(f'pd_basic转为dataframe: {pd_basic}')
            # 删除重复的"文章链接"列
            pd_basic.drop_duplicates('文章链接', inplace=True, keep='last')
            # print(f'去重后的pd_basic: {pd_basic}')
            # 获取文章链接,生成一个包含所有链接的列表
            links = [d['文章链接'] for d in xhs_basic]
            # print(links)
            # 把标题及链接等信息保存为csv文件
            # xhs_title.xhs_to_csv(xhs_basic, field=fields)

            # # 由于存在编码问题，因此要先对标题表的编码进行转换
            # with open('20230707hot_desc.csv', 'r', encoding='GB2312') as f:
            #     data = f.read()
            #
            # # 将内容写入新的无BOM的UTF-8文件
            # with open('2023070hot_desc.csv', 'w', encoding='utf-8') as f:
            #     f.write(data)

            # 通过Links获取文章内容，返回列表content
            content = []
            for url in links:
                # print(url)
                xhs_content = XhsContent.XHSContent(url, authorization)
                xhs = xhs_content.getdata()
                time.sleep(random.randint(20, 40))
                a_list = [url, xhs]
                content.append(a_list)

            # 把content转化为DataFrame格式
            pd_content = pd.DataFrame(content)
            # 原标题为0和1，把标题转为"文章链接"和"文章内容"
            pd_content = pd_content.rename(columns={0: "文章链接", 1: "文章内容"})
            # 把文章内容存入CSV文件
            # pd_content.to_csv(f'{today_str()}{keyName}{sortedWay}content.csv', index=False, encoding='utf-8-sig')
            # print(datetime.today(), pd_content)
            # 使用merge函数合并两个DataFrame
            # content_pd = pd.DataFrame(content)
            # content_pd = pd.DataFrame(data=list(zip(links, content)), columns=["文章链接", "文章内容"])
            xhs_pd = pd.merge(pd_basic, pd_content, on='文章链接', how='left')

            # 新建一列，用来记录抓取日期
            xhs_pd['抓取日期'] = pd.to_datetime('now').date()
            xhs_pd['品牌'] = keyName
            xhs_pd['抓取方式'] = sortedWay

            # 保存为csv文件
            xhs_pd.to_csv('xhs_db.csv', index=False, mode='a')
            # 每次间隔500 - 700秒，规避反爬虫机制
            time.sleep(random.randint(500, 700))
        except:
            logging.exception("Error occurred")
            continue


def duplicates(s, t):
    # 随机爬取，难保会抓到重复的内容，保存后去除重复的内容
    t = pd.read_excel(t)
    s = pd.read_csv(s)
    df = pd.concat([t, s], ignore_index=True)
    # print(len(df))
    # 去除重复内容，如有重复内容，保留最新的一条
    df.drop_duplicates(subset='文章链接', inplace=True, keep='last')
    # print(len(df))
    df.to_excel('xhs_db.xlsx', index=False)


def sent_file(sent_id, path):
    chat = wechat.WeChat(sent_id)
    chat.send_file(path)


if __name__ == "__main__":
    source = 'xhs_db.csv'
    target = 'xhs_db.xlsx'
    duplicates(source, target)
    sent_file('12345', 'xhs_db.xlsx')

    if os.path.exists(source):
        os.remove(source)
        print(f"文件 {source} 已成功删除")
    else:
        print(f"文件 {source} 不存在")
