import codecs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_recall_fscore_support
import numpy as np

def get_corpus(filename):
    copus = []
    label = []
    with codecs.open(filename, "r", "utf-8") as f:
        for line in f:
            line = line.strip()
            label.append(line.split("\t")[0])
            copus.append(line.split("\t")[1])
    return label, copus

def get_stopworods(filename):
    stopwords = []
    with codecs.open(filename, "r", "utf-8") as f:
        for line in f:
            stopwords.append(line.strip())
    return stopwords


if __name__ == '__main__':
    train_labels, train_copuses = get_corpus("train.txt")
    test_labels, test_copuses = get_corpus("test.txt")
    pip = Pipeline([
        ('vect', CountVectorizer(stop_words=get_stopworods("hlt_stop_words.txt"))),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB())
    ])
    pip.fit(train_copuses, train_labels)
    predicted = pip.predict(test_copuses)
    acc = np.mean(predicted == test_labels)
    # precision = np.sum(predicted == test_labels)/(np.sum(predicted == test_labels) + )
    # recall = np.sum(predicted == test_labels)/
    precision, recall, fscore, _ = precision_recall_fscore_support(test_labels, predicted, average="macro") # 1 vs others
    print("Precision = {:.5f}".format(precision))
    print("Recall = {:.5f}".format(recall))
    print("F1 = {:.5f}".format(fscore))
