#!/user/bin/python3
#coding=utf-8
"""
评价最大匹配法进行汉语分词的效果
"""
import codecs

RESULT_FILENAME = "../output/textCNResult.txt"
TEST_FILENAME = "../data/textCN.gold"

def main():
    true_rec_num = 0
    rec_num = 0
    test_set_num = 0

    with codecs.open(RESULT_FILENAME, 'r', "utf-8") as result_file, codecs.open(TEST_FILENAME, 'r', "utf-8") as test_file:
        for result_line, test_line in zip(result_file, test_file):
            result_line_set = set(result_line.strip().split())
            test_line_set = set(test_line.strip().split())
            true_rec_num += len(result_line_set & test_line_set)
            rec_num += len(result_line_set)
            test_set_num += len(test_line_set)

    precision = true_rec_num/rec_num
    recall = true_rec_num/test_set_num
    f_score = precision*recall*2/(precision + recall)
    print("Precision = {}/{} = {:.2f}%".format(true_rec_num, rec_num, precision*100))
    print("Recall = {}/{} = {:.2f}%".format(true_rec_num, test_set_num, recall*100))
    print("F-score = Precision*Recall*2/(Precision + Recall) = {:.2f}%".format(f_score*100))

if __name__ == '__main__':
    main()