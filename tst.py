# -*- coding = utf-8 -*-
# coding: utf-8
__author__ = 518030910298

import sys, importlib, codecs
import urllib3
from bs4 import BeautifulSoup
import jieba.posseg as peg

reload(sys)

import operator
import re, math, os
from decimal import getcontext

# import comp_char from cnsort


def pick_charset(html):
    charset = None
    m = re.compile('<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?', re.I).search(html)
    if m and m.lastindex == 2:
        charset = m.group(2).lower()
    if not charset:
        charset = 'utf-8'
    return charset


p = re.compile('<title>.*</title>', re.DOTALL)
root = os.getcwd()
copy = []
text = []
index = []
dictionary = []

fp = codecs.open('./dictionary.txt', encoding='utf-8')
ori = fp.readlines()
# ori is the list with out any operation

for x in ori:
    x = re.sub(r'\n', '', x)
    copy.append(x)
    dictionary.append([0])

fp.close()
'''copy.sort()'''

id = 0

loop = 0
prev_index = 0
flags = 0
for i, element in enumerate(copy):
    if element != '' and re.sub(r'\D', '', element) == '' and loop == 0:
        prev_index += 1
        dictionary[i] = [element, prev_index]

    elif element != '':
        if loop == 0:
            prev_index += 1
        if not re.sub(r'\D', '', element) == '':
            loop = int(re.sub(r'\D', '', element))
        dictionary[i] = [re.sub(r'\d', '', element).strip(), prev_index]
        loop -= 1

flagCorrect = 1076
flags = 0

url = []
with codecs.open('title.txt', 'r', encoding='utf8') as titles:
    for roots, dirs, files in os.walk(root, topdown=False):
        for name in files:
            # flagCorrect = len(titles.readlines())
            flags = 1076
            if not (name.endswith('jpg') or name.endswith('png') or name.endswith('gif') or name.endswith('jpeg')):
                titles.seek(0)
                while flags:
                    line = titles.readline()
                    flags -= 1
                    if name in line:  # name = url as filename
                        line_cnt = re.sub(name, '', line).strip()  # web page title
                        text.append(line_cnt)  # titles
                        nameToUrl = re.split(r'\s+', name)
                        with open(root + '/index.txt', 'r') as urlLibrary:
                            urlLibrary.seek(0)
                            for line in urlLibrary:
                                if nameToUrl[0] in line:
                                    nameToUrl = re.split(r'\s+', line)
                            url.append(nameToUrl[0])
                        # url.append(re.sub(line_cn.strip('\t').strip('\n'), '', line_origin))  # filenames
                        index.append([])

                        break
                    if flagCorrect == 1:
                        print('Runtime Error')

temp_text = -1
dist = []
for str_input in text:
    temp_text += 1
    flags = 0
    distance = 0
    contents = []
    for dic_temp in dictionary:
        if (dic_temp[0] in str_input) or (dic_temp[0] in url[temp_text]):
            flags = 1
            index[temp_text].append(dic_temp[1])
            break

    if not flags:
        try:
            distance += 10
            http = urllib3.PoolManager(num_pools=5, headers={
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"})
            content = http.request('GET', url[temp_text]).data
            soup = BeautifulSoup(content, 'html.parser')
            chars = pick_charset(url[temp_text])
            for idx in soup.findAll('p'):
                idx = idx.get_text().decode(chars).lower()
                for idy in dictionary:
                    if idy[0] in idx:
                        text[temp_text] = text[temp_text] + idx.get_text()
                        index[temp_text].append(idy[1])

                        flags = idy

        except RuntimeError or TypeError:
            str_head = 0
            str_tail = len(str_input)
            ptr = 5
            temp = 0

            exact_num = 0
            while temp < str_tail - 1:
                flag = 0
                ptr = 5
                while flag != 1:
                    in_put = str_input[temp:temp + ptr]

                    tail = len(dictionary) - 1
                    head = 0
                    half = int((tail + head) / 2)

                    while tail != half and head != half:
                        if operator.lt(dictionary[half][0], in_put):  # less than
                            head = half
                            half = int((tail + head) / 2)

                        elif operator.gt(dictionary[half][0], in_put):  # greater than
                            tail = half
                            half = int((tail + head) / 2)

                        elif operator.eq(dictionary[half][0], in_put):
                            flag = 1
                            temp += len(in_put)
                            if tail != 11 and in_put != "":
                                exact_num = dictionary[half][1]
                                index[temp_text].append(exact_num)
                            break

                    if ptr == 0 and temp <= len(str_input) - 1:
                        temp += 1
                        flag = 1

                    if flag == 0:
                        ptr -= 1

            if len(index[temp_text]) > 1:
                sum = 0
                for element in index[temp_text]:
                    sum += element

                average = sum / len(index[temp_text])
                index[temp_text] = []
                index[temp_text].append(int(average))

for element in index:
    if not element:
        element.append(0)

list = [5e-1, 1.5e0, 2.5e0, 3.5e0, 4.5e0, 5e-1, 1.5e-1, 2.5e-1, 3.5e-1, 4.5e-1]
# ------------ Start Clustering -------------
getcontext().prec = 4

k = int(input("k"))  # cluster size
sets = [float(item[0]) for item in index]

centroid = []
if k <= 10:
    for i in range(0, k):
        centroid.append(list[i])
else:
    for element in list:
        centroid.append(element)

    step = (len(sets) - 0)/(k - 10)
    temp = 0
    while temp < len(sets):
        centroid.append(sets[math.trunc(temp)])
        temp += step

class_i = [[] for i in range(len(centroid))]
class_text = [[] for i in range(len(centroid))]

flag = 1
number = 0
times = 0
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
for item in res[::-1]:
    if len(item) <= 1 or len(item) > 3 or temp == item:
        res.remove(item)
    temp = item

print(res[:(k*3 if k*3 < len(res) else len(res))])

while flag == 1 and times < 50:
    number += 1
    flag = 0
    times += 1

    class_i = [[] for i in range(len(centroid))]
    class_text = [[] for i in range(len(centroid))]
    for i in range(0, len(sets)):
        distance = float("inf")
        centroid_in_choose = 0
        for j in range(0, len(centroid)):
            if abs(sets[i] - centroid[j]) < distance:
                distance = abs(sets[i] - centroid[j])
                centroid_in_choose = j

        class_i[centroid_in_choose].append(sets[i])
        class_text[centroid_in_choose].append(i)

    for i in range(0, len(class_i)):
        sum = 0
        for j in range(0, len(class_i[i])):
            sum += class_i[i][j]
        if sum != 0:
            new_centroid = round(sum / len(class_i[i]), 3)
        else:
            continue

        if new_centroid != centroid[i]:
            centroid[i] = new_centroid
            flag = 1


try:
    path = 'out'
    if not os.path.exists(path):  # 如果文件夹不存在则新建
        os.mkdir(path)
    f = codecs.open(path + "/result.txt", "w+", encoding='utf8')
    # f.write("title\tcategory\ttitle\n")
    printOut = 0
    out = ['其他', '篮球', '足球', '综合', '轮滑', '电竞']
    for i, content in enumerate(index):
        printOut += 1
        f.write(url[i] + '\t' + (out[content[0]] if centroid[math.floor(i*k/len(index))] < float('inf') else "None") + '\n')
    f.close()
except () as e:
    print("Print out to txt ERROR.")
