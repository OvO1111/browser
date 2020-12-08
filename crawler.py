# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import re
import os
import urllib, urllib.request
from urllib.parse import urljoin, urlparse
import sys, threading, time
from queue import Queue
import queue


def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def get_page(page):
    request = urllib.request.Request(page)
    content = urllib.request.urlopen(request, timeout=20).read()
    time.sleep(0.5)
    return content


def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content)
    for i in soup.findAll('a', {'href': re.compile('^http|^/')}):
        link = i.get('href', '')
        link = urljoin(page, link)
        links.append(link)
    return links


'''def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)  # 将网页存入文件
    f.close()'''


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
            # add_page_to_folder(page, content)
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
    seed = 'https://comp-sync.webapp.163.com/g37'
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
