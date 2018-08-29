#!/user/bin/python3
#coding=utf-8
"""
最大匹配方法进行汉语分词
"""
import pickle
import codecs

SAVE_FILE_NAME = "../output/textCNResult.txt" # 保存的文件名
FILE_NAME = "../data/textCN.txt"    # 需要处理的文件名

with open("../output/dict_set.pkl", "rb") as file:
    DICT_SET = pickle.load(file)    # 载入之前load_dict.py保存的pickle文件

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

def cut(string):
    """
    Forward Maximum Matching(FMM) method to cut the Chinese sentences
    Args:
        string <str>: the sentence you wan to cut
    Returns:
        <str>: a string, consists of cut-words, concating by whitespaces
    """
    string = string.strip() # 消除句末的'\r\n'
    words = []
    start_pos = 0
    if start_pos + DICT_SET["max_length"] <= len(string):   # 确定待处理词的起始末尾位置
        end_pos = start_pos + DICT_SET["max_length"]
    else:
        end_pos = len(string)

    while len("".join(words)) < len(string):    # 若words中未包含string中的所有内容，则循环
        current_word = string[start_pos:end_pos]
        if current_word in DICT_SET["dict"] or len(current_word) == 1:  # 当前词在词表中出现过或当前词为单个字符时，添加至words中
            words.append(current_word)
            start_pos = end_pos # 更新下一个待分词的起始位置
            if start_pos + DICT_SET["max_length"] <= len(string):   # 更新下一个待分词的末尾位置
                end_pos = start_pos + DICT_SET["max_length"]
            else:
                end_pos = len(string)
        else:
            end_pos -= 1    # 待分词的长度减一

    return " ".join(words)

def main():
    with codecs.open(SAVE_FILE_NAME, 'a', "utf-8") as save_file:
        cnt = 1
        for line in read_lines(FILE_NAME):
            save_file.write(cut(line) + "\n")
            print("\rProcess: {}/803".format(cnt), end="")
            cnt += 1

if __name__ == '__main__':
    main()
