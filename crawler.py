# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import re, operator
from jieba import posseg as peg
import os
import urllib3, urllib.request
from urllib.parse import urljoin, urlparse
import sys, threading, time
from queue import Queue
import queue


def pick_charset(html):
    charset = None
    m = re.compile('<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?', re.I).search(html)
    if m and m.lastindex == 2:
        charset = m.group(2).lower()
    if not charset:
        charset = 'utf-8'
    return charset


'''headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36", }


def pick_charset(html):
    charset = None
    m = re.compile('<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?', re.I).search(html)
    if m and m.lastindex == 2:
        charset = m.group(2).lower()
    return charset


def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def get_page(page):
    request = urllib.request.Request(page, headers)
    content = urllib.request.urlopen(request, timeout=20).read()
    time.sleep(0.5)
    return content


def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content, 'html.parser')
    for i in soup.findAll('a', {'href': re.compile('^http|^/')}):
        link = i.get('href', '')
        link = urljoin(page, link)
        links.append(link)
    return links


def get_title(content, page):
    charset = pick_charset(page)
    p = re.compile('<title>.*</title>', re.DOTALL)
    title = ""
    for line, cxt in enumerate(content):
        if "<title>" in cxt.decode(charset):
            title = re.findall(p, cxt)[0].decode("string_escape")
            title = str(title).strip('<title>').strip('</title>')

    return title


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
    try:
        filename = valid_filename(get_title(content, page))  # 将网址变成合法的文件名
    except AttributeError:
    filename = valid_filename(page)
    index = open(index_filename, 'a')
    index.write(str(page) + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content.decode('utf-8'))  # 将网页存入文件
    f.close()


def crawl():
    queue.put(seed)
    crawled = []
    graph = {}
    count = 5000
    while count:
        page = queue.get()
        if page not in crawled:
            print(page)
            content = get_page(page)
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            for link in outlinks:
                queue.put(link)
            if varLock.acquire():
                graph[page] = outlinks
                crawled.append(page)
                varLock.release()
            queue.task_done()
            count -= 1
            print(count)
    return graph, crawled


if __name__ == '__main__':
    seed = 'https://www.baidu.com'
    q = queue.Queue()
    queue = q

    start = time.clock()
    threads = []
    NUM = 3
    varLock = threading.Lock()

    for i in range(NUM):
        t = threading.Thread(target=crawl)
        t.setDaemon(True)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = time.clock()
    print(end - start)
'''
cxt1 = []
cxt2 = []
res = []
k = 2
inp_url = 'https://soccer.hupu.com/'
seed_url = 'https://baijiahao.baidu.com/s?id=1655661900636454426&wfr=spider&for=pc'
http = urllib3.PoolManager(num_pools=5, headers={
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"})
content = http.request('GET', inp_url).data
soup = BeautifulSoup(content, 'html.parser')
chars = pick_charset(inp_url)
for idx in soup.findAll():
    cut = peg.cut(re.sub(r'[a-zA-Z0-9]', '', idx.get_text()).lower())
    for word, flag in cut:
        if 'n' in flag and word not in cxt1:
            cxt1.append(word)
cxt1.sort()

http = urllib3.PoolManager(num_pools=5, headers={
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"})
content = http.request('GET', seed_url).data
soup = BeautifulSoup(content, 'html.parser')
chars = pick_charset(seed_url)
for idx in soup.findAll():
    cut = peg.cut(re.sub(r'[a-zA-Z0-9]', '', idx.get_text()).lower())
    for word, flag in cut:
        if 'n' in flag and word not in cxt2:
            cxt2.append(word)
cxt2.sort()
print(cxt1)
print(cxt2)

res = []
for str_input in (cxt1 if len(cxt1) >= len(cxt2) else cxt2):

    str_tail = len(str_input)
    ptr = 1
    temp = 0

    while temp < str_tail - 1:
        flag = 0
        ptr = 5
        while flag != 1:
            in_put = str_input[temp:temp + ptr]

            tail = len(cxt2) - 1
            head = 0
            half = int((tail + head) / 2)

            while tail != half and head != half:
                if operator.lt(cxt2[half], in_put):
                    head = half
                    half = int((tail + head) / 2)

                elif operator.gt(cxt2[half], in_put):
                    tail = half
                    half = int((tail + head) / 2)

                elif cxt2[half] in in_put if len(in_put) > len(cxt2[half]) else in_put in cxt2[half]:
                    flag = 1
                    temp += len(in_put)
                    if tail != 11 and in_put != "":
                        try:
                            result = cxt2[half]
                        except:
                            print(half)
                            result = 'None'

                        res.append(result)

                    break

            if ptr == 0 and temp <= len(str_input) - 1:
                temp += 1
                flag = 1

            if flag == 0:
                ptr -= 1

res.sort()
temp = ''
for index, item in enumerate(res[::-1]):
    if len(item) <= 1 or len(item) > 3 or temp == item:
        res.remove(item)
    temp = item

print(res[:(k*3 if k*3 < len(res) else len(res))])
# http://xueshu.baidu.com/usercenter/paper/show?paperid=1621590ab8ad8e9055cf9141cbff7ec5&site=xueshu_se
# https://blog.51cto.com/9499607/2089667
