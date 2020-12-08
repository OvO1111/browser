# -*- coding = utf-8 -*-
__author__ = 518030910298

"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
"""

import operator
import re, math, os
from decimal import getcontext
# import comp_char from cnsort

root = os.getcwd()
copy = []
new_list = []
dictionary = []
text = []
index = []

try:
    with open('keywords.txt') as fp:
        ori = fp.readlines()
        for x in ori:
            x = re.sub(r'\n', '', x)
            copy.append(x)
            new_list.append(x)
        copy.sort()
        id = 0

        for element in copy:
            if element != '':
                dictionary.append([])
                dictionary[id].append(element)
                for ele in new_list:
                    if ele == element and len(dictionary[id]) < 2:
                        dictionary[id].append(new_list.index(ele))
                id += 1

        id = 0
        for element in dictionary:
            print(id, " ", element, end=" / ")
            print(" ", copy[id])
            id += 1
        print("----------")

    for roots, dirs, files in os.walk(root, topdown=False):
        for name in files:
            if not name.endswith('jpg') or name.endswith('png') or name.endswith('gif'):
                with open(os.path.join(roots, name)) as fp:
                    ori = fp.readlines()

                    for items in ori:
                        items = re.sub(r'\n', '', items)
                        text.append(items)
                        index.append([])

                for str_input in text:
                    str_input = re.sub(r',，\.。_\?？；;/\'<>《》\(\)（）！!、——·', '', str_input)

except ValueError:
    print('ERROR')

temp_text = -1
for str_input in text:
    temp_text += 1
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
                if operator.lt(dictionary[half][0], in_put):
                    head = half
                    half = int((tail + head) / 2)

                elif operator.gt(dictionary[half][0], in_put):
                    tail = half
                    half = int((tail + head) / 2)

                elif operator.eq(dictionary[half][0], in_put):
                    flag = 1
                    temp += len(in_put)
                    if tail != 11 and in_put != "":
                        try:
                            exact_num = dictionary[half][1]
                        except:
                            print(half)
                        index[temp_text].append(exact_num * 1000000)
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

list = [5e7, 1.5e8, 2.5e8, 3.5e8, 4.5e8, 5e4, 1.5e5, 2.5e5, 3.5e5, 4.5e5]
# ------------ Start Clustering -------------
getcontext().prec = 4

k = len(dictionary)  # cluster size
sets = [float(item[0]) for item in index]

centroid = []
if k <= 10:
    for i in range(10):
        centroid.append(list[i])
else:
    for element in list:
        centroid.append(element)

    step = (len(sets) - 0)/(k - 10)
    temp = 0
    while temp < len(sets):
        centroid.append(sets[math.trunc(temp)])
        temp += step

print("original centroids: ", centroid, "\n")
class_i = [[] for i in range(len(centroid))]
class_text = [[] for i in range(len(centroid))]

flag = 1
number = 0
times = 0
# sign if k never change or this program runs more than 100 times
while flag == 1 and times < 100:
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
            # print("change centroid ", centroid[i], "as ", end="")
            centroid[i] = new_centroid
            # print(centroid[i])
            flag = 1

try:
    path = 'out/'
    f = open(path + "result.txt", "w+")
    f.write("cat\ttitle\n")
    for i in range(0, len(class_i)):
        for element in class_text[i]:
            f.write(str(i) + "\t" + text[element] + "\n")
    f.close()
    print(f"Print out {k} classes successfully.")
except:
    print("Print out to txt ERROR.")
