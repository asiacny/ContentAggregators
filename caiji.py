# -*- coding:utf-8 -*-
import os
import re
import time
import json
import requests
import base64
import requests
import datetime
from threading import Thread
from lxml import etree

#理论python和前端js会自动转义，但如果采集名称因引号或其它需转义的字符报错，请将相应采集名修改如下
#hot_name = .replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").replace("\"", "").replace("\'", "").strip()

#采集数据保存目录,为了安全请修改本程序名字,或移动到其他目录,并修改以下路径,默认与程序同目录
dir = os.path.dirname(os.path.abspath(__file__)) + "/json/"
#dir = "webrootdir/json/"
#dir = "/tmp/json/"

try:
    os.mkdir(dir)
except:
    print("json文件夹已经存在！")

#字符替换加密(默认为大小写反转),修改此处顺序和添加数字替换可实现不同密码加密(并同时修改get/index.php内密码)
def multiple_replace(text):
    dic = {"a":"A", "b":"B", "c":"C", "d":"D", "e":"E", "f":"F", "g":"G", "h":"H", "i":"I", "j":"J", "k":"K", "l":"L", "m":"M", "n":"N", "o":"O", "p":"P", "q":"Q", "r":"R", "s":"S", "t":"T", "u":"U", "v":"V", "w":"W", "x":"X", "y":"Y", "z":"Z", "A":"a", "B":"b", "C":"c", "D":"d", "E":"e", "F":"f", "G":"g", "H":"h", "I":"i", "J":"j", "K":"k", "L":"l", "M":"m", "N":"n", "O":"o", "P":"p", "Q":"q", "R":"r", "S":"s", "T":"t", "U":"u", "V":"v", "W":"w", "X":"x", "Y":"y", "Z":"z"}
    pattern = "|".join(map(re.escape, list(dic.keys())))
    return re.sub(pattern, lambda m: dic[m.group()], text) 

#UTC时间转本地时间（+8:00）
def utc2local(utc_st):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st

def parse_baidu(name):
    jsondict= {}
    if name == 'now':
        jsondict["title"] = "百度实时热点"
        url = "http://top.baidu.com/buzz?b=1"
    if name == 'today':
        jsondict["title"] = "百度今日热点"
        url = "http://top.baidu.com/buzz?b=341"
    if name == 'week':
        jsondict["title"] = "百度七日热点"
        url = "http://top.baidu.com/buzz?b=42"
    fname = dir + "baidu_" + name + ".json"
    r = requests.get(url)
    r.encoding='gb2312'
    soup = etree.HTML(r.text.replace("<tr >", "<tr class=\"hideline\">"))
    list = []
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    for soup_a in soup.xpath("//tr[@class='hideline']"):
        blist = {}
        hot_name = soup_a.xpath("./td[2]/a[1]/text()")[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_a.xpath("./td[2]/a[1]/@href")[0]
        hot_num = soup_a.xpath("./td[@class='last']/span/text()")[0]
        group = name
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        blist["num"]=hot_num
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#知乎热榜
def parse_zhihu_hot():
    fname = dir + "zhihu_hot.json"
    zhihu_all = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Host': 'www.zhihu.com'
    }
    r = requests.get(zhihu_all, headers=headers).text
    data = json.loads(r)
    news = data['data']
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "知乎全站热榜"
    for n in news:
        blist = {}
        hot_name = n['target']['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = n['target']['url'].replace("api.zhihu.com/questions/", "www.zhihu.com/question/")
        group = "zhihu_hot"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#微博热点排行榜
def parse_weibo():
    fname = dir + "weibo.json"
    weibo_ssrd = "https://s.weibo.com/top/summary?cate=realtimehot"
    weibo = "https://s.weibo.com"
    r = requests.get(weibo_ssrd)
    r.encoding='utf-8'
    soup = etree.HTML(r.text)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "微博热点排行榜"
    for soup_a in soup.xpath("//td[@class='td-02']"):
        blist = {}
        hot_name = soup_a.xpath("./a/text()")[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = weibo + soup_a.xpath("./a/@href")[0]
        try:
            hot_num = soup_a.xpath("./span/text()")[0]
        except IndexError:
            hot_num = ''
        if "javascript:void(0)" in hot_url:
            str_list = ""
        else:
            group = "weibo"
            hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
            blist["name"]=hot_name
            blist["url"]=hot_url
            if hot_num:
                blist["num"]=hot_num
            list.append(blist)
            jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

def parse_tieba():
    fname = dir + "tieba.json"
    tb_url = "http://tieba.baidu.com/hottopic/browse/topicList"
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Host': 'tieba.baidu.com'
    }
    r = requests.get(tb_url, headers=headers).text
    data = json.loads(r)
    news = data['data']['bang_topic']['topic_list']
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "贴吧热度榜单"
    for n in news:
        blist = {}
        hot_name = n['topic_desc'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = n['topic_url'].replace("&amp;", "&")
        group = "tieba"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#V2EX热帖
def parse_v2ex():
    url = "https://www.v2ex.com/?tab=hot"
    fname = dir + "v2ex.json"
    r = requests.get(url)
    soup = etree.HTML(r.text)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "V2EX热帖"
    for soup_a in soup.xpath("//span[@class='item_title']/a"):
        blist = {}
        hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = "https://www.v2ex.com" + soup_a.get('href')
        group = "v2ex"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#豆瓣讨论精选
def parse_douban():
    url = "https://www.douban.com/group/explore"
    headers = {
        'Host': 'www.douban.com',
        'Referer': 'https://www.douban.com/group/explore'
    }
    fname = dir + "douban.json"
    r = requests.get(url, headers=headers)
    soup = etree.HTML(r.text)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "豆瓣讨论精选"
    for soup_a in soup.xpath("//div[@class='channel-item']/div[@class='bd']/h3/a"):
        blist = {}
        hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_a.get('href')
        group = "douban"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#天涯热帖
def parse_tianya():
    url = "http://bbs.tianya.cn/hotArticle.jsp"
    headers = {
        'Host': 'bbs.tianya.cn',
        'Referer': 'http://bbs.tianya.cn/hotArticle.jsp'
    }
    fname = dir + "tianya.json"
    r = requests.get(url, headers=headers)
    soup = etree.HTML(r.text)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "天涯热帖"
    for soup_a in soup.xpath("//div[@class='mt5']/table/tbody/tr/td[@class='td-title']/a"):
        blist = {}
        hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = 'http://bbs.tianya.cn' + soup_a.get('href')
        group = "tianya"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#抽屉新热榜
def parse_chouti():
    url = "https://dig.chouti.com/link/hot"
    headers = {
        'Referer': 'https://dig.chouti.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    fname = dir + "chouti.json"
    r = requests.get(url, headers=headers).text
    data = json.loads(r)
    news = data['data']
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(str(data['data'][0]['time_into_pool'])[0:10])))
    jsondict["time"] = list_time
    jsondict["title"] = "抽屉新热榜"
    for n in news:
        blist = {}
        hot_url = n['originalUrl']
        if 'chouti.com' not in hot_url:
            hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
            group = "chouti"
            hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
            blist["name"]=hot_name
            blist["url"]=hot_url
            list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#虎嗅网资讯
def parse_huxiu():
    url = "https://www-api.huxiu.com/v1/article/list"
    headers = {
        'Referer': 'https://www.huxiu.com/article',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    fname = dir + "huxiu.json"
    r = requests.get(url, headers=headers).text
    data = json.loads(r)
    news = data['data']['dataList']
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data['data']['dataList'][0]['dateline'])))
    jsondict["time"] = list_time
    jsondict["title"] = "虎嗅网资讯"
    for n in news:
        blist = {}
        hot_url = n['share_url']
        hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        group = "huxiu"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#煎蛋网
def parse_jandan():
    url = "https://jandan.net/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Referer': 'https://jandan.net/'
    }
    fname = dir + "jandan.json"
    r = requests.get(url, headers=headers)
    soup = etree.HTML(r.text)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "煎蛋网"
    for soup_a in soup.xpath("//div[@class='post f list-post']/div[@class='indexs']/h2/a"):
        blist = {}
        hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_a.get('href')
        group = "jandan"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#知乎日报
def parse_zhihu_daily():
    url = "https://daily.zhihu.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Referer': 'https://daily.zhihu.com/'
    }
    fname = dir + "zhihu_daily.json"
    r = requests.get(url, headers=headers).text.replace(" class=\"home\"", "")
    soup = etree.HTML(r)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "知乎日报"
    for soup_a in soup.xpath("//div[@class='box']/a"):
        blist = {}
        hot_name = soup_a.xpath('./span/text()')[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = "https://daily.zhihu.com" + soup_a.get('href')
        group = "zhihu_daily"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#黑客派-好玩
def parse_hacpai(name):
    jsondict= {}
    if name=="play":
        jsondict["title"] = "黑客派-好玩"
        group = "hacpai_play"
        url = "https://hacpai.com/domain/play"
    if name=="hot":
        jsondict["title"] = "黑客派-热议"
        group = "hacpai_hot"
        url = "https://hacpai.com/recent/hot"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Referer': 'https://hacpai.com/'
    }
    fname = dir + "hacpai_"+name+".json"
    r = requests.get(url, headers=headers)
    soup = etree.HTML(r.text)
    list = []
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    for soup_a in soup.xpath("//h2[@class='article-list__title article-list__title--view fn__flex-1']/a[@data-id]"):
        blist = {}
        hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_a.get('href')
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#猫扑热帖
def parse_mop():
    url = "https://www.mop.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "mop.json"
    r = requests.get(url, headers=headers)
    r.encoding='utf-8'
    soup = etree.HTML(r.text.replace("<h3>", "").replace("</h3>", ""))
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "猫扑热帖"
    for soup_a in soup.xpath("//div[@class='swiper-wrapper']")[0]:
        blist = {}
        hot_name = soup_a.xpath("./a/div/h2/text()")[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_a.xpath("./a/@href")[0]
        group = "mop"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    for soup_b in soup.xpath("//div[@class='shuffling-two']/a"):
        blist = {}
        hot_name = soup_b.xpath("./div/p/text()")[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_b.get('href')
        group = "mop"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    for soup_c in soup.xpath("//div[@class='mop-hot']/div[1]/div/div/div/div/div[2]/a"):
        blist = {}
        hot_name = soup_c.text.replace("\r", "").replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_c.get('href')
        group = "mop"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#果壳-科学人
def parse_guokr():
    url = "https://www.guokr.com/scientific/"
    url2 = "https://www.guokr.com/beta/proxy/science_api/articles?retrieve_type=by_category&page=1"
    url3 = "https://www.guokr.com/beta/proxy/science_api/articles?retrieve_type=by_category&page=2"
    headers = {
        'Referer': 'https://www.guokr.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "guokr.json"
    r = requests.get(url, headers=headers)
    r.encoding='utf-8'
    soup = etree.HTML(r.text.replace("<span class=\"split\">|</span>", ""))
    r2 = requests.get(url2, headers=headers).text
    data2 = json.loads(r2)
    r3 = requests.get(url3, headers=headers).text
    data3 = json.loads(r3)
    list = []
    jsondict= {}
    list_time = soup.xpath("//div[@class='article-info']/text()")[1].replace("\"", "").strip()
    jsondict["time"] = list_time
    jsondict["title"] = "果壳-科学人"
    for soup_a in soup.xpath("//a[@class='article-title']"):
        blist = {}
        hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_a.get('href')
        group = "guokr"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    for n in data2:
        blist = {}
        hot_url = "https://www.guokr.com/article/" + str(n['id']) + "/"
        hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        group = "guokr"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    for n in data3:
        blist = {}
        hot_url = "https://www.guokr.com/article/" + str(n['id']) + "/"
        hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        group = "guokr"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#IT之家
def parse_ithome():
    url = "https://www.ithome.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "ithome.json"
    r = requests.get(url, headers=headers)
    r.encoding='utf-8'
    soup = etree.HTML(r.text)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "IT之家"
    for soup_a in soup.xpath("//div[@class='bx']/ul/li/a"):
        blist = {}
        hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_a.get('href')
        group = "ithome"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#央视要闻
def parse_cctv():
    url = "http://news.cctv.com/data/index.json"
    headers = {
        'Referer': 'https://news.cctv.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "cctv.json"
    r = requests.get(url, headers=headers).text
    data = json.loads(r)
    list = []
    jsondict= {}
    list_time = data['updateTime']
    jsondict["time"] = list_time
    jsondict["title"] = "央视要闻"
    for n in data['rollData']:
        blist = {}
        hot_url = n['url']
        hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        group = "cctv"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#cnBeta
def parse_cnbeta():
    url = "https://www.cnbeta.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "cnbeta.json"
    r = requests.get(url, headers=headers)
    r.encoding='utf-8'
    soup = etree.HTML(r.text)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "cnBeta"
    for soup_a in soup.xpath("//div[@class='items-area']/div/dl/dt/a"):
        blist = {}
        hot_name = soup_a.xpath("./span/text()")
        if hot_name:
            hot_name = hot_name[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        else:
            hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_a.get('href').replace("//hot", "https://hot").strip()
        group = "cnbeta"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#联合早报-中港台
def parse_zaobao():
    url = "https://www.zaobao.com.sg/realtime/china"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "zaobao.json"
    r = requests.get(url, headers=headers)
    r.encoding='utf-8'
    soup = etree.HTML(r.text)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "联合早报-中港台"
    for soup_a in soup.xpath("//a[@target='_self']"):
        blist = {}
        hot_name = soup_a.xpath("./div/span/text()")[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = "https://www.zaobao.com.sg" + soup_a.get('href').strip()
        group = "zaobao"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#微信公众号热门文章
def parse_weixin():
    url = "https://weixin.sogou.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "weixin.json"
    fname2 = dir + "weixin_hot.json"
    r = requests.get(url, headers=headers)
    r.encoding='utf-8'
    soup = etree.HTML(r.text)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "微信公众号搜索热词"
    for soup_a in soup.xpath("//ol[@class='hot-news']/li"):
        blist = {}
        hot_name = soup_a.xpath("./a/text()")[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_a.xpath("./a/@href")[0]
        hot_num = soup_a.xpath("./span/span/@style")[0].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").replace("width:", "").replace("%", "").strip()
        group = "weixin"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        blist["num"]=hot_num
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))
    list = []
    jsondict= {}
    jsondict["time"] = list_time
    jsondict["title"] = "微信公众号热门文章"
    for soup_a in soup.xpath("//div[@class='txt-box']/h3/a"):
        blist = {}
        hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_a.get('href')
        group = "weixin"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname2,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#澎湃新闻
def parse_thepaper():
    url = "https://www.thepaper.cn/load_chosen.jsp"
    headers = {
        'Referer': 'https://www.thepaper.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "thepaper.json"
    r = requests.get(url, headers=headers)
    r.encoding='utf-8'
    soup = etree.HTML(r.text)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "澎湃新闻"
    for soup_a in soup.xpath("//div[@class='news_li']/h2/a"):
        blist = {}
        hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = "https://www.thepaper.cn/" + soup_a.get('href')
        group = "thepaper"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#纽约时报中文网-国际简报
def parse_nytimes():
    url = "https://m.cn.nytimes.com/world"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "nytimes.json"
    r = requests.get(url, headers=headers)
    r.encoding='utf-8'
    soup = etree.HTML(r.text)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "纽约时报中文网-国际简报"
    for soup_a in soup.xpath("//li[@class='regular-item']/a"):
        blist = {}
        hot_name = soup_a.get('title').replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_a.get('href')
        group = "nytimes"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#新京报-排行
def parse_bjnews():
    url = "http://www.bjnews.com.cn/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "bjnews.json"
    r = requests.get(url, headers=headers)
    r.encoding='utf-8'
    soup = etree.HTML(r.text)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "新京报-排行"
    for soup_a in soup.xpath("//li/h3/a"):
        blist = {}
        hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_a.get('href')
        group = "bjnews"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#奇客的资讯
def parse_solidot():
    url = "https://www.solidot.org/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "solidot.json"
    r = requests.get(url, headers=headers)
    r.encoding='utf-8'
    soup = etree.HTML(r.text)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "奇客的资讯"
    for soup_a in soup.xpath("//div[@class='bg_htit']/h2/a"):
        blist = {}
        hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = "https://www.solidot.org" + soup_a.get('href')
        group = "solidot"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#新浪科技
def parse_sinatech():
    url = "https://feed.mix.sina.com.cn/api/roll/get?pageid=372&lid=2431&k=&num=50&page=1"
    headers = {
        'Referer': 'http://tech.sina.com.cn/roll/rollnews.shtml#pageid=372&lid=2431&k=&num=50&page=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "sinatech.json"
    r = requests.get(url, headers=headers).text
    data = json.loads(r)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data['result']['data'][0]['ctime'])))
    jsondict["time"] = list_time
    jsondict["title"] = "新浪科技"
    for n in data['result']['data']:
        blist = {}
        hot_url = n['url']
        hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        group = "sinatech"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#全球主机交流论坛
def parse_hostloc():
    url = "https://www.hostloc.com/forum.php?mod=forumdisplay&fid=45&filter=author&orderby=dateline"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    cookies = {'hkCM_2132_saltkey': 'YUW6N18j', 'hkCM_2132_lastvisit': '1565188564', 'hkCM_2132_visitedfid': '45', 'L7DFW': 'f64d0d1c0e4afb6b8913e5cf1d39cbf2', 'hkCM_2132_sid': 'svW2eC', 'hkCM_2132_st_t': '0%7C1565195462%7Cc9e8fe0fa2043784ed064e22c9180fb3', 'hkCM_2132_forum_lastvisit': 'D_45_1565195462', 'hkCM_2132_lastact': '1565195463%09home.php%09misc', 'hkCM_2132_sendmail': '1'}
    fname = dir + "hostloc.json"
    r = requests.get(url, headers=headers, cookies=cookies).text.replace("<th class=\"lock\">", "<abc>")
    soup = etree.HTML(r)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "全球主机交流论坛"
    for soup_a in soup.xpath("//th/a[@onclick='atarget(this)']"):
        blist = {}
        hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = "https://www.hostloc.com/" + soup_a.get('href')
        group = "hostloc"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#什么值得买-今日热门文章
def  parse_smzdm_article(name):
    jsondict= {}
    if name=="today":
        id="1"
        jsondict["title"] = "什么值得买热门文章(日榜)"
    if name=="week":
        id="7"
        jsondict["title"] = "什么值得买热门文章(周榜)"
    if name=="month":
        id="30"
        jsondict["title"] = "什么值得买热门文章(月榜)"
    url = "https://post.smzdm.com/rank/json_more/?unit="+id+"&p=1"
    url2 = "https://post.smzdm.com/rank/json_more/?unit="+id+"&p=2"
    headers = {
        'Referer': 'https://post.smzdm.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "smzdm_article_"+name+".json"
    r = requests.get(url, headers=headers).text
    data = json.loads(r)
    r2 = requests.get(url2, headers=headers).text
    data2 = json.loads(r2)
    list = []
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    for n in data['data']:
        blist = {}
        hot_url = n['article_url']
        hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        group = "smzdm_article"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    for n in data2['data']:
        blist = {}
        hot_url = n['article_url']
        hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        group = "smzdm_article"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#知乎每日精选-编辑推荐
def parse_zhihu_good():
    url = "https://www.zhihu.com/node/ExploreRecommendListV2"
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'authority': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/explore/recommendations',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    d = {'method': 'next', 'params': '{"limit":40,"offset":0}'}
    fname = dir + "zhihu_good.json"
    r = requests.post(url, data=d, headers=headers)
    r.encoding='utf-8'
    json_data = ""
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    jsondict["title"] = "知乎每日精选-编辑推荐"
    for json_d in json.loads(r.text)['msg']:
        json_data = json_data + json_d
    soup = etree.HTML(json_data)
    for soup_a in soup.xpath("//div[@class='zm-item']/h2/a"):
        blist = {}
        hot_name = soup_a.text.replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        hot_url = soup_a.get('href').replace("/question/", "https://www.zhihu.com/question/")
        group = "zhihu_good"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#AppStore排行榜
def parse_itunes(name,country):
    if country=="cn":
        country2="(国区)"
    if country=="us":
        country2="(美区)"
    jsondict= {}
    if name=="free":
        name2="FreeApplications"
        jsondict["title"] = "AppStore免费排行榜"+country2
    if name=="paid":
        name2="PaidApplications"
        jsondict["title"] = "AppStore付费排行榜"+country2
    if name=="revenue":
        name2="AppsByRevenue"
        jsondict["title"] = "AppStore收入排行榜"+country2
    url = "https://itunes.apple.com/WebObjects/MZStoreServices.woa/ws/charts?cc="+country+"&g=36&limit=100&name="+name2
    headers = {
        'Referer': 'https://www.apple.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    fname = dir + "itunes_"+name+"_"+country+".json"
    r = requests.get(url, headers=headers)
    r.encoding='utf-8'
    data = json.loads(r.text)
    str_list="https://itunes.apple.com/"+country+"/lookup?id="
    list = []
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    for n in data['resultIds']:
        str_list = str_list + n + ","
    r = requests.get(str_list, headers=headers)
    r.encoding='utf-8'
    data = json.loads(r.text)
    for n in data['results']:
        blist = {}
        hot_url = n['trackViewUrl']
        hot_name = n['trackName'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        releaseNotes = n.get('releaseNotes')
        if releaseNotes:
            releaseNotes = releaseNotes.replace("<", "").replace(">", "")
        else:
            releaseNotes=""
        version = n.get('version')
        uptime=utc2local(datetime.datetime.strptime(n.get('currentVersionReleaseDate'),'%Y-%m-%dT%H:%M:%SZ'))
        hot_num = n['genres'][0]
        group = "itunes_free"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        blist["num"]=hot_num
        blist["description"]="最新版本:  "+version+"\n更新时间:  "+str(uptime)+" (北京时间)\n\n"+releaseNotes
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))

#头条推荐
def parse_toutiao(name):
    url = "https://www.toutiao.com/api/pc/feed/?category=__all__&min_behot_time=" + str(int(time.time()))
    headers = {
        'Referer': 'https://www.toutiao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    cookies = {'tt_webid': '6722913290500539908', 'WEATHER_CITY': '%E5%8C%97%E4%BA%AC', '__tasessionId': 'ccyrlpfcb1565300241329', 'tt_webid': '6722913290500539908', 'csrftoken': '36c38d5c3a8001b9d598c09f79c8c653'}
    fname = dir + "toutiao_" + name + ".json"
    r = requests.get(url, headers=headers, cookies=cookies).text
    data = json.loads(r)
    list = []
    jsondict= {}
    list_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jsondict["time"] = list_time
    if name == 'a':
        jsondict["title"] = "头条1"
    if name == 'b':
        jsondict["title"] = "头条2"
    if name == 'c':
        jsondict["title"] = "头条3"
    if name == 'd':
        jsondict["title"] = "头条4"
    if name == 'e':
        jsondict["title"] = "头条5"
    if name == 'f':
        jsondict["title"] = "头条5"
    if name == 'g':
        jsondict["title"] = "头条5"
    if name == 'h':
        jsondict["title"] = "头条5"
    if name == 'i':
        jsondict["title"] = "头条5"
    if name == 'j':
        jsondict["title"] = "头条5"
    for n in data['data']:
        blist = {}
        hot_url = "https://www.toutiao.com" + n['source_url']
        hot_name = n['title'].replace("\\n", "").replace("\n", "").replace("\\r", "").replace("\r", "").strip()
        group = "toutiao"
        hot_url = "get/?url=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_url.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1]) + "&group=" + group + "&title=" + multiple_replace(base64.urlsafe_b64encode(base64.urlsafe_b64encode(hot_name.encode("utf-8")).decode("utf-8").encode("utf-8")).decode("utf-8").replace("=", "")[::-1])
        blist["name"]=hot_name
        blist["url"]=hot_url
        list.append(blist)
    jsondict["data"]=list
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(json.dumps(jsondict, ensure_ascii=False, indent=2, separators=(',',':')))


#单线程运行,错误测试用,错误会直接退出并显示错误日志
def error_run():
    parse_smzdm_article("today")
    parse_smzdm_article("week")
    parse_smzdm_article("month")
    parse_hostloc()
    parse_sinatech()
    parse_solidot()
    parse_bjnews()
    parse_nytimes()
    parse_thepaper()
    parse_weixin()
    parse_zaobao()
    parse_cnbeta()
    parse_cctv()
    parse_ithome()
    parse_guokr()
    parse_mop()
    parse_hacpai("play")
    parse_hacpai("hot")
    parse_zhihu_daily()
    parse_jandan()
    parse_huxiu()
    parse_chouti()
    parse_tianya()
    parse_douban()
    parse_v2ex()
    parse_tieba()
    parse_weibo()
    parse_baidu("now")
    parse_baidu("today")
    parse_baidu("week")
    parse_zhihu_hot()
    parse_zhihu_good()
    parse_itunes("free","cn")
    parse_itunes("paid","cn")
    parse_itunes("revenue","cn")
    parse_itunes("free","us")
    parse_itunes("paid","us")
    parse_itunes("revenue","us")
    parse_toutiao("a")
    parse_toutiao("b")
    parse_toutiao("c")
    parse_toutiao("d")
    parse_toutiao("e")
    parse_toutiao("f")
    parse_toutiao("g")
    parse_toutiao("h")
    parse_toutiao("i")
    parse_toutiao("j")
    print("单线程错误测试通过")

#多线程抓取
def thread_run():
    threads = []
    ts2 = Thread(target=parse_hostloc)
    ts3 = Thread(target=parse_sinatech)
    ts4 = Thread(target=parse_solidot)
    ts5 = Thread(target=parse_bjnews)
    ts6 = Thread(target=parse_nytimes)
    ts7 = Thread(target=parse_thepaper)
    ts8 = Thread(target=parse_weixin)
    ts9 = Thread(target=parse_zaobao)
    ts10 = Thread(target=parse_cnbeta)
    ts11 = Thread(target=parse_cctv)
    ts12 = Thread(target=parse_ithome)
    ts13 = Thread(target=parse_guokr)
    ts14 = Thread(target=parse_mop)
    ts16 = Thread(target=parse_hacpai, args=("play",))
    ts17 = Thread(target=parse_hacpai, args=("hot",))
    ts18 = Thread(target=parse_zhihu_daily)
    ts19 = Thread(target=parse_jandan)
    ts20 = Thread(target=parse_huxiu)
    ts21 = Thread(target=parse_chouti)
    ts22 = Thread(target=parse_tianya)
    ts23 = Thread(target=parse_douban)
    ts24 = Thread(target=parse_v2ex)
    ts25 = Thread(target=parse_tieba)
    ts26 = Thread(target=parse_weibo)
    ts27 = Thread(target=parse_baidu, args=("now",))
    ts28 = Thread(target=parse_baidu, args=("today",))
    ts29 = Thread(target=parse_baidu, args=("week",))
    ts30 = Thread(target=parse_zhihu_hot)
    ts31 = Thread(target=parse_zhihu_good)
    ts32 = Thread(target=parse_itunes, args=("free","cn",))
    ts33 = Thread(target=parse_itunes, args=("paid","cn",))
    ts34 = Thread(target=parse_itunes, args=("revenue","cn",))
    ts35 = Thread(target=parse_itunes, args=("free","us",))
    ts36 = Thread(target=parse_itunes, args=("paid","us",))
    ts37 = Thread(target=parse_itunes, args=("revenue","us",))
    ts38 = Thread(target=parse_smzdm_article, args=("today",))
    ts39 = Thread(target=parse_smzdm_article, args=("week",))
    ts40 = Thread(target=parse_smzdm_article, args=("month",))
    threads.append(ts2)
    threads.append(ts3)
    threads.append(ts4)
    threads.append(ts5)
    threads.append(ts6)
    threads.append(ts7)
    threads.append(ts8)
    threads.append(ts9)
    threads.append(ts10)
    threads.append(ts11)
    threads.append(ts12)
    threads.append(ts13)
    threads.append(ts14)
    threads.append(ts16)
    threads.append(ts17)
    threads.append(ts18)
    threads.append(ts19)
    threads.append(ts20)
    threads.append(ts21)
    threads.append(ts22)
    threads.append(ts23)
    threads.append(ts24)
    threads.append(ts25)
    threads.append(ts26)
    threads.append(ts27)
    threads.append(ts28)
    threads.append(ts29)
    threads.append(ts30)
    threads.append(ts31)
    threads.append(ts32)
    threads.append(ts33)
    threads.append(ts34)
    threads.append(ts35)
    threads.append(ts36)
    threads.append(ts37)
    threads.append(ts38)
    threads.append(ts39)
    threads.append(ts40)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("多线程采集完成")

#单线程运行,错误测试用,错误会直接退出并显示错误日志
#error_run()

#因头条接口短时间请求时相同内容太多，故取消并发分时采集，此处的首次更新并发是为了避免前端内容太少或浏览器控制台报错(强迫症)
def thread_toutiao():
    threads = []
    ts1 = Thread(target=parse_toutiao, args=("a",))
    ts2 = Thread(target=parse_toutiao, args=("b",))
    ts3 = Thread(target=parse_toutiao, args=("c",))
    ts4 = Thread(target=parse_toutiao, args=("d",))
    ts5 = Thread(target=parse_toutiao, args=("e",))
    ts6 = Thread(target=parse_toutiao, args=("f",))
    ts7 = Thread(target=parse_toutiao, args=("g",))
    ts8 = Thread(target=parse_toutiao, args=("h",))
    ts9 = Thread(target=parse_toutiao, args=("i",))
    ts10 = Thread(target=parse_toutiao, args=("j",))
    threads.append(ts1)
    threads.append(ts2)
    threads.append(ts3)
    threads.append(ts4)
    threads.append(ts5)
    threads.append(ts6)
    threads.append(ts7)
    threads.append(ts8)
    threads.append(ts9)
    threads.append(ts10)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("首次运行采集头条完成")

if __name__ == "__main__":
    try:
        t1 = time.time()
        thread_toutiao() #首次运行头条抓取
        print("耗时:", time.time() - t1)
    except:
        print("头条采集出现一个错误，请及时更新规则！")
    while True:
        try:
            t1 = time.time()
            thread_run()
            print("耗时:", time.time() - t1)
        except:
            print("采集出现一个错误，请及时更新规则！")
        print ("完成时间:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("全部完成，10分钟后将再次采集")
        time.sleep(60)
        parse_toutiao("a")
        time.sleep(60)
        parse_toutiao("b")
        time.sleep(60)
        parse_toutiao("c")
        time.sleep(60)
        parse_toutiao("d")
        time.sleep(60)
        parse_toutiao("e")
        time.sleep(60)
        parse_toutiao("f")
        time.sleep(60)
        parse_toutiao("g")
        time.sleep(60)
        parse_toutiao("h")
        time.sleep(60)
        parse_toutiao("i")
        time.sleep(60)
        parse_toutiao("j") #每隔600秒也即十分钟更新一次
