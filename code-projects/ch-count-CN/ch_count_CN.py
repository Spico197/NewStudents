#!/user/bin/python3
#coding=utf-8
"""
汉字字频统计（utf-8输入，gbk输出）
方法：线性扫描，逐字比对
编码方式注解：
    GBK：简繁汉语、韩语日语字符集
    GB2312：简体中文字符集
    utf-8：变长编码（8bit为一个单位，可使用一至四个字节表示一个字符）字符集
    unicode：“大一统”字符集
"""
import time
import operator
import codecs

__author__ = "spico1026@gmail.com"

def read_lines(filename, encoding="utf-8"):
    """
    read a line from text which is named `filename`
    Args:
        filename <str>: file name u wnat to read from
        encoding <str>: file reading encoding
    Returns:
        a generator by `yield`
    """
    with codecs.open(filename, 'r', encoding) as file:
        for line in file:
            # if file is replaced by file.read(size), 
            # then we can process GB files.
            # but there's a peoblem. 'cause you may cut words from "chocalate" to "cho" and "calate"
            yield line

def dict2file(word_dict, filename, order=None, save_encoding="utf-8"):
    """
    save the dict to a .txt file, splited by '\t'
    Args:
        word_dict <dict>: the dict u want to save
        filename <str>: the file u want to save. if not exist: create; else overwrite.
    Returns:
        None
    Raises:
        ValueError
    """
    with codecs.open(filename, 'w', encoding=save_encoding) as save_file:
        save_file.write("character\tfrequency\n")
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
    open_filename = "textCN.txt"
    save_filename = "textCNFreq.txt"
    open_encoding = "utf-8"
    save_encoding = "gbk"

    ch_dict = {}
    cnt = 0
    start_time = time.time()
    for line in read_lines(open_filename, encoding=open_encoding):
        cnt += 1
        for ch in list(line.strip()):
            if u'\u4e00' <= ch <= u'\u9fa5': # unicode中汉字的区间编码
                if ch_dict.get(ch) is None:
                    ch_dict[ch] = 1
                else:
                    ch_dict[ch] += 1
        print("\rLine Process: {:3}/803".format(cnt), end="")
    end_time = time.time()
    dict2file(ch_dict, save_filename, order='-', save_encoding=save_encoding)
    save_time = time.time()
    print("\nProcess time: {0} seconds\nSave time: {1} seconds"
        .format(end_time - start_time, save_time - end_time))
