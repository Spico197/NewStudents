#!/user/bin/python3
#coding=utf-8

## 
# 英文词频统计
# 1、文件的输入输出√
# 2、大文本情况下的Python处理（如何不加载至内存中而进行处理）√
# 3、专有名词（带`.`等特殊符号）的处理√P.S.全部lowercase处理√
# 4、词性的转换，如将does替换成do，将chocalates替换成单数的chocalate（复数变单数，时态变为现在时）√
# 5、行末被切断的词的还原√
# 6、数字的处理（数字和标点符号的混合组合，如1/2, 123,456）√
# 7、年份日期的处理：如20th，90s——在这里暂且将6和7合并为一种解决办法，即若单词中包含数字，则丢弃该单词√
# 8、输出时的排序√
# 9、以's或'等类似字符开头的单词√
# 10、类似全是标点符号的字符，如``, --等√
# 11、进度条的实现√
#

__author__ = "spico1026@gmail.com"

import time
import operator
import pickle

NUMBERS_SET = set("0123456789")
LETTERS_SET = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
PUCTUATIONS_SET = set("~`!@#$%^&*()_+-=1234567890\\|]}[{'\";:/?.>,<")

class Variant(object):
    """
    Variant Lemmatisation Class, which supports word-variants finding
    """
    def __init__(self):
        """get the lemmatisation from **12dict**"""
        self.variants = {}
        self.find_query = {}
        print("------------------------- pkl files loading -------------------------")
        with open("../output/variants.pkl", "rb") as variants_file:
            self.variants = pickle.load(variants_file)
        with open("../output/find_query.pkl", "rb") as find_query_file:
            self.find_query = pickle.load(find_query_file)
        print("------------------------- end of loading -------------------------")

    def get_head(self, word):
        """
        get the head word
        Args:
            word <str>: the word that u want to find its headword
        Returns:
            head_word <str>
        """
        if self.find_query.get(word) != None:
            return self.find_query[word]
        else:
            return word

va = Variant()

def read_lines(filename):
    """
    read a line from text which is named `filename`
    Args:
        filename <str>: file name u wnat to read from
    Returns:
        a generator by `yield`
    """
    with open(filename, 'r') as file:
        for line in file:
            # if file is replaced by file.read(size), 
            # then we can process GB files.
            # but there's a peoblem. 'cause you may cut words from "chocalate" to "cho" and "calate"
            yield line

def line_process(line, former_last="", method="specific"):
    """
    strip a line and split this line by whitespaces and return a list of words
    Args:
        line <str>: a line of string from the text'
        former_last <str>: a word split by '\n' and concat by '-' from the former line's last word
        method <str>: three methods provided: 
            specific: focus on the details: the first character mustn't be "'"; there is not number in words; there must have a to z or A to Z characters;
            quick: less focus on the details. just judge if it is a single number or single punctuation;
            rough: return the split result without characters check;
            detail: add lemmasation variant process based on the specific mode.
    Returns:
        word_list <list>: a list of words after being splited
        last_word <str>: a word that connecting with the first word of the next line
    Raises:
        ValueError
    """
    word_list_origin = (former_last + line).strip().lower().split()
    if word_list_origin[-1][-1] == '-': # 如果最后一个单词的最后一个字母是通配符，则返回
        last_word = word_list_origin[-1]
    else:
        last_word = ""
    word_list = []
    if method == "specific": 
        for item in word_list_origin:
            if len(set(item) & {"'"}) == 0 and len(NUMBERS_SET & set(item)) == 0:
                if len(set(item) & LETTERS_SET) != 0:
                    word_list.append(item)
            """ old style
            if len(item) != 1 or item not in PUCTUATIONS_SET: # 单个字符且该字符为标点符号或数字
                # TODO: 此处有一个问题：即语料中所有的标点符号前后都有空格，但遇到一般语料时该如何处理？即"I love u."或"i.e. | for e.g.,"
                if item[0] != "'": # 开头为:"'"的词，例如"'s | 'll"等等
                    # TODO: 此处还有一个问题：如何将"'ll"的词变换为"will"？
                    if len(NUMBERS_SET & set(item)) == 0: # 取交集，判断单词中是否存在数字。只要有数字，则舍弃
                        if len(set(item) & LETTERS_SET) != 0: # 判断单词中是否存在字母，若存在，则继续
                            word_list.append(item)
            """
    elif method == "quick":
        for item in word_list_origin:
            if len(item) != 1 or item not in PUCTUATIONS_SET: # 单个字符且该字符为标点符号或数字
                word_list.append(item)
    elif method == "rough":
        word_list = word_list_origin
    elif method == "detail":
        for item in word_list_origin:
            if len(set(item) & {"'"}) == 0 and len(NUMBERS_SET & set(item)) == 0:
                if len(set(item) & LETTERS_SET) != 0:
                    word_list.append(va.get_head(item))
    else:
        raise ValueError
    return word_list, last_word

def dict2file(word_dict, filename, order=None):
    """
    save the dict to a .txt file, splited by '\t'
    Args:
        word_dict <dict>: the dict u want to save
        filename <str>: the file u want to save. if not exist: create; else overwrite.
    Returns:
        None
    Raises:

    """
    with open(filename, 'w') as save_file:
        save_file.write("word\tfrequency\n")
        if order == None:
            for (key, value) in word_dict.items():
                save_file.write("{0}\t{1}\n".format(key, value))
        elif order == '+':
            words_order_list = sorted(word_dict.items(), key=operator.itemgetter(1), reverse=False)
            for (key, value) in words_order_list:
                save_file.write("{0}\t{1}\n".format(key, value))
        elif order == '-':
            words_order_list = sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)
            for (key, value) in words_order_list:
                save_file.write("{0}\t{1}\n".format(key, value))
        else:
            raise ValueError

if __name__ == "__main__":
    filename = "../data/textEN.txt"
    method = "detail"
    words = {}
    last_word = ""
    print("------------------------- line process, method={} -------------------------".format(method))
    start_time = time.time()
    cnt = 0
    for line in read_lines(filename):
        words_list, last_word = line_process(line, last_word, method)
        cnt += 1
        for word in words_list:
            if words.get(word) == None:
                words[word] = 1
            else:
                words[word] += 1
        print("\rLine Process: {:6}/100000".format(cnt), end="")
    end_time = time.time()
    print("\n------------------------- end of line process -------------------------")
    print("Time spend: {0:.3} s; Next we will save the file."
        .format(end_time - start_time))
    dict2file(words, "../output/textENfrequency.txt", order='-')
    total_end_time = time.time()
    print("Save time spend: {0:.3} s; Total time spend: {1:.3} s"
        .format(total_end_time - end_time, total_end_time - start_time))
