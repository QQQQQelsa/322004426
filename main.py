import re
import jieba
import numpy
import jieba.analyse
import math
import os
from simhash import Simhash
import argparse

def short_analyse(o_file, c_file):
    jieba.setLogLevel(jieba.logging.INFO)
    o_list = []
    c_list = []
    try:
        with open(o_file, 'r', encoding='utf-8') as f:
            o_lines = f.readlines()
        for line in o_lines:
            pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
            target = pattern.sub("", line)
            for data in jieba.lcut(target):
                o_list.append(data)
    except FileNotFoundError:
        print(f"{o_file}这个路径下没有文件")
        raise FileNotFoundError

    try:
        abs_c_file = os.path.abspath(c_file)
        print(f"抄袭论文的绝对地址为: {abs_c_file}")

        with open(c_file, 'r', encoding='utf-8') as f:
            c_lines = f.readlines()
        for line in c_lines:
            pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
            target = pattern.sub("", line)
            for data in jieba.lcut(target):
                c_list.append(data)

    except FileNotFoundError:
        print(f"{c_file}这个路径下没有文件")
        raise FileNotFoundError

    all_words = list(set(o_list).union(set(c_list)))
    la = []
    lb = []
    # 转换为向量的形式
    for word in all_words:
        la.append(o_list.count(word))
        lb.append(c_list.count(word))

    # 计算余弦相似度
    laa = numpy.array(la)
    lbb = numpy.array(lb)
    cos = (numpy.dot(laa, lbb.T)) / ((math.sqrt(numpy.dot(laa, laa.T))) * (math.sqrt(numpy.dot(lbb, lbb.T))))
    return cos


def long_analyse(fname):
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"{fname}这个路径下并不存在文件")

    tags = jieba.analyse.extract_tags(content, 15)
    return tags


def compute_sim(o_file, c_file):
    i = set(o_file).intersection(set(c_file))
    j = set(o_file).union((set(c_file)))
    return round(len(i) / len(j), 2)


def long_ans(o_file, c_file):
    a1 = long_analyse(o_file)
    a2 = long_analyse(c_file)
    return compute_sim(a1, a2)


def save_data(a_file, cos, long_similarity, simhash_similarity, o_file, c_file):
    try:
        # 以追加模式('a')打开文件，确保结果不会覆盖之前的数据
        with open(a_file, 'a', encoding='utf-8') as f:
            f.write("========================================\n")
            f.write(f"原文本的绝对地址: {o_file}\n")
            f.write(f"被抄袭文本的绝对地址: {c_file}\n")
            f.write(f"短文本分析的相似度为: {cos}\n")
            f.write(f"长文本分析的相似度为: {long_similarity}\n")
            f.write(f"Simhash分析的相似度为: {simhash_similarity}\n")
            f.write("========================================\n\n")
    except FileNotFoundError:
        print(f"{a_file}这个路径下没有文件")


def simhash_demo(text_a, text_b):

    try:
        with open(text_a, 'r', encoding='utf-8') as f:
            content_a = f.read()

    except FileNotFoundError:
        print(f"{text_a}这个路径下文件不存在")
        raise FileNotFoundError

    try:
        with open(text_b, 'r', encoding='utf-8') as f:
            content_b = f.read()

    except FileNotFoundError:
        print(f"{text_b}这个路径下文件不存在")
        raise FileNotFoundError

    a_simhash = Simhash(content_a)
    b_simhash = Simhash(content_b)
    max_hashbit = max(len(bin(a_simhash.value)), len(bin(b_simhash.value)))
    # 汉明距离
    distince = a_simhash.distance(b_simhash)
    similar = 1 - distince / max_hashbit
    return similar

