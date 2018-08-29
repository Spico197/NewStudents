#!/user/bin/python3
#coding=utf-8
"""
载入字典文件，并将其保存为pickle文件，方便后续调用
保存的数据：
    dict_set = {
        "max_length": 0,
        "line_number": 0,
        "dict": set()
    }
"""
import codecs
import pickle

DICT_FILE_NAME = "CN.dict"
DICT_FILE_ENCODING = "utf-8"
DICT_FILE_SAVE_NAME = "dict_set.pkl"

def main():
    dict_set = {
        "max_length": 0,
        "line_number": 0,
        "dict": set()
    }
    with codecs.open(DICT_FILE_NAME, 'r', DICT_FILE_ENCODING) as dict_file:
        cnt = 0
        for line in dict_file:
            if cnt == 0:
                dict_set["line_number"], dict_set["max_length"] = map(int, line.strip().split())    # 获取行号和最大长度
            elif 1 <= cnt <= dict_set["line_number"]:
                dict_set["dict"].add(line.strip())
            else:
                break
            print("\rProcess: {}/{}".format(cnt, dict_set["line_number"]), end="")
            cnt += 1
    with open(DICT_FILE_SAVE_NAME, "wb") as dict_set_file:
        pickle.dump(dict_set, dict_set_file)

if __name__ == '__main__':
    main()