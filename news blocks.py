# -*- coding: utf-8 -*-
__author__ = 'Zhao'


# 浙江大学新闻网的list进行相似度计算，并且进行k-means聚类


import operator
import re
import math
from decimal import getcontext


# import comp_char from cnsort


path = 'lib/'
fp = open(path + 'First.txt', encoding='utf-8')
ori = fp.readlines()
# ori is the list with out any operation


copy = []
new_list = []
for x in ori:
    x = re.sub(r'\n', '', x)
    copy.append(x)
    new_list.append(x)
# in this part we change the format in a into standard format and save as copy


fp.close()
# we close the file, then we can run the list totally in this program


copy.sort()


id = 0
dictionary = []
for element in copy:
    if element != '':
        dictionary.append([])
        dictionary[id].append(element)
        for ele in new_list:
            if ele == element and len(dictionary[id]) < 2:
                dictionary[id].append(new_list.index(ele))
        id += 1
# using new list to substitute original dictionary which contains lots of '' (it's hard to visualize.)


id = 0
for element in dictionary:
    print(id, " ", element, end=" / ")
    print(" ", copy[id])
    id += 1
print("----------")
path = 'scrapy/'
f = open(path + 'ori_news.txt')
ori = f.readlines()
# ori is the list with out any operation


text = []
for x in ori:
    x = re.sub(r'\n', '', x)
    text.append(x)
# in this part we change the format in a into standard format and save as copy


fp.close()
# we close the file, then we can run the list totally in this program


# ------------- upper is reading part including wordlist and text -------------


index = []
for x in ori:
    index.append([])


# ------------- upper is append a vacant list prepared to insert index -------------


for str_input in text:
    str_input = re.sub(r',', "", str_input)
    str_input = re.sub(r'，', "", str_input)
    str_input = re.sub(r'\.', "", str_input)
    str_input = re.sub(r'。', "", str_input)
    str_input = re.sub(r'——', "", str_input)
    str_input = re.sub(r'……', "", str_input)
    str_input = re.sub(r'！', "", str_input)
    str_input = re.sub(r'!', "", str_input)
    str_input = re.sub(r'\?', "", str_input)
    str_input = re.sub(r'？', "", str_input)
    str_input = re.sub(r';', "", str_input)
    str_input = re.sub(r'；', "", str_input)
    str_input = re.sub(r' ', "", str_input)
    str_input = re.sub(r'/', "", str_input)
    str_input = re.sub(r'、', "", str_input)
    str_input = re.sub(r'"', "", str_input)
    str_input = re.sub(r'\'', "", str_input)
    str_input = re.sub(r'<', "", str_input)
    str_input = re.sub(r'>', "", str_input)
    str_input = re.sub(r'《', "", str_input)
    str_input = re.sub(r'》', "", str_input)
    str_input = re.sub(r'\(', "", str_input)
    str_input = re.sub(r'\)', "", str_input)
    str_input = re.sub(r'（', "", str_input)
    str_input = re.sub(r'）', "", str_input)




    # change all the punctuation as blank, however, we may split falsely.
    # Words get around, the step can also split at wrong place, so, I do not fix this mistake.


# ------------- upper is transforming part -------------


temp_text = -1
for str_input in text:
    temp_text += 1
    str_head = 0
    str_tail = len(str_input)
    ptr = 5
    temp = 0  # 当前处理字段起始位置


    # result = []
    # ch_index = []


    exact_num = 0
    # we sort dictionary(the copy) in this program and each word has two characteristic number
    # using as index to look back on original dictionary
    while temp < str_tail - 1:
        flag = 0
        ptr = 5
        while flag != 1:
            in_put = str_input[temp:temp + ptr]  # 当前处理字段

            tail = len(dictionary) - 1
            head = 0
            half = int((tail + head) / 2)

            while tail != half and head != half:
                if operator.lt(dictionary[half][0], in_put):
                    # 如果字符组的一半比input小
                    head = half
                    half = int((tail + head) / 2)


                elif operator.gt(dictionary[half][0], in_put):
                    # 如果字符组的一半比input大
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
                        # print("exact_num = ",exact_num)
                        index[temp_text].append(exact_num * 1000000)
                        # index[temp_text].append(half) # 这个语句仅用于调试之后的Part A部分
                    break


            if ptr == 0 and temp <= len(str_input) - 1:
                # print(str_input[temp], end='/')
                # result.append(str_input[temp])
                # ch_index.append(-1)
                temp += 1
                flag = 1


            if flag == 0:
                ptr -= 1


    # ------ Part A 仅用于调试变量 具体用于探测特征变量 ------


    # print(text[temp_text])
    # for element in index[temp_text]:
    #     print(element,end=" ")
    #     # print(dictionary[element])
    # print("")
    # # print(index[temp_text])
    # print("------------------------------")


    # ------ Part A END ------


    if len(index[temp_text]) > 1:
        sum = 0
        for element in index[temp_text]:
            sum += element


        average = sum / len(index[temp_text])
        index[temp_text] = []
        index[temp_text].append(int(average))


        # ------ Part B 仅用于调试变量 具体用于探测特征变量 ------


        # print(text[temp_text])
        # print(index[temp_text])
        # print("-------------")
        # ------ Part B END ------


# ------------ Upper is first array for the title (the main class) ------------


path = 'lib/'
fp = open(path + 'Second.txt', encoding='utf-8')
ori = fp.readlines()
# ori is the list with out any operation


copy = []
new_list = []
for x in ori:
    x = re.sub(r'\n', '', x)
    copy.append(x)
    new_list.append(x)
# in this part we change the format in a into standard format and save as copy


fp.close()
# we close the file, then we can run the list totally in this program


copy.sort()


id = 0
dictionary = []
for element in copy:
    if element != '':
        dictionary.append([])
        dictionary[id].append(element)
        for ele in new_list:
            if ele == element and len(dictionary[id]) < 2:
                dictionary[id].append(new_list.index(ele))
        id += 1
# using new list to substitute original dictionary which contains lots of '' (it's hard to visualize.)


id = 0
for element in dictionary:
    print(id, " ", element, end=" / ")
    print(" ", copy[id])
    id += 1
print("----------")


# ------------- upper is reading part including the second wordlist -------------


temp_text = -1
for str_input in text:
    temp_text += 1
    # str_head = 0
    str_tail = len(str_input)
    ptr = 5
    temp = 0  # 当前处理字段起始位置


    while temp < str_tail - 1:
        flag = 0
        ptr = 5
        while flag != 1:
            in_put = str_input[temp:temp + ptr]  # 当前处理字段


            tail = len(dictionary) - 1
            head = 0
            half = int((tail + head) / 2)


            while tail != half and head != half:
                if operator.lt(dictionary[half][0], in_put):
                    # 如果字符组的一半比input小
                    head = half
                    half = int((tail + head) / 2)


                elif operator.gt(dictionary[half][0], in_put):
                    # 如果字符组的一半比input大
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
                        index[temp_text].append(exact_num * 1000)
                        # index[temp_text].append(half) # 这个语句仅用于调试之后的Part A部分
                    break


            if ptr == 0 and temp <= len(str_input) - 1:
                temp += 1
                flag = 1


            if flag == 0:
                ptr -= 1


    # ------ Part A 仅用于调试变量 具体用于探测特征变量 ------
    # print(text[temp_text])
    # for element in index[temp_text]:
    #     print(element,end=" ")
    #     # print(dictionary[element])
    # print("")
    # # print(index[temp_text])
    # print("------------------------------")


    # ------ Part A END ------


    if len(index[temp_text]) > 1:
        sum = 0
        for i in range(1, len(index[temp_text])):
            sum += index[temp_text][i]


        average = sum / len(index[temp_text])
        average += index[temp_text][0]
        index[temp_text] = []
        index[temp_text].append(int(average))


        # ------ Part B 仅用于调试变量 具体用于探测特征变量 ------


        # print(text[temp_text])
        # print(index[temp_text])
        # print("-------------")
        # ------ Part B END ------


# ------------ Upper is second array for the title (the second class) ------------


for element in index:
    if not element:
        element.append(0)


# ------------ 如果仍然没有结果 那么用0替代这个分组 --------------




list = [50000000, 150000000, 250000000, 350000000, 450000000, 50000, 150000, 250000, 350000, 450000]
# ------------ Start Clustering -------------
getcontext().prec = 4


k = int(input("please input k:\n"))
new_ori_set = [float(item[0]) for item in index]


centroid = []
if k <= 10:
    for i in range(0,k-1):
        centroid.append(list[i])
else:
    for element in list:
        centroid.append(element)


    step = (len(new_ori_set) - 0) / (k-10)


    # print(new_ori_set)


    temp = 0


    while temp < len(new_ori_set):
        centroid.append(new_ori_set[math.trunc(temp)])
        temp += step


print("original centroids: ", centroid, "\n")


class_i = [[] for i in range(len(centroid))]
class_text = [[] for i in range(len(centroid))]


# class_i is the null class for k centroid


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


    # class_i is the null class for k centroid


    for i in range(0, len(new_ori_set)):
        distance = float("inf")
        centroid_in_choose = 0
        for j in range(0, len(centroid)):
            if abs(new_ori_set[i] - centroid[j]) < distance:
                distance = abs(new_ori_set[i] - centroid[j])
                centroid_in_choose = j


        class_i[centroid_in_choose].append(new_ori_set[i])
        class_text[centroid_in_choose].append(i)


        # sort all the elements into proper class


    # ------------ 每次 Clustering 之后的结果输出 ------------


    # print("after %sth cluster: " % number, "\n")
    # print("centroid   class")
    # for i in range(0, len(class_i)):
    #     print(centroid[i], '     ', class_i[i])
    #
    # print("---------")


    # ------------ 每次 Clustering 之后的结果输出 END ------------


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
            # print("---------")
            # change the wrong centroid


# ------------ Clustering 最终结果输出 -----------


# print("THE CONCLUSION IS：")
# print("centroid   class")
# for i in range(0, len(class_i)):
#     print(centroid[i], '     ', [text[element] for element in class_text[i]])


# ------------ Clustering 最终结果输出 END -----------


# -------------- * UPPER IS CLUSTERING, CLUSTERING IS END.* --------------


# ------------ 输出到txt -------------


try:
    path = 'out/'
    f = open(path + "result.txt", "w+")
    f.write("cat\ttitle\n")
    for i in range(0, len(class_i)):
        for element in class_text[i]:
            f.write(str(i) + "\t" + text[element] + "\n")
    f.close()
    print("Print out %d classes successfully."%k)
except:
    print("Print out to txt ERROR.")
# ------------ 输出到txt END -------------
