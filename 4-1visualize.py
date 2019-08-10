import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import re
import nltk

from gensim.models import word2vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
data = pd.read_csv("train.csv").sample(50000,random_state=23)
stop_words = nltk.corpus.stopwords.words()
def clean_sentence(val):   #数据处理，把单词提取出来
    regex = re.compile('([^\s\w]|_)+')
    sentence = regex.sub('',val).lower()   #找到所有的字母、数字
    sentence = sentence.split(" ")

    for word in list(sentence):
        if word in stop_words:
            sentence.remove(word)
    sentence = " ".join(sentence)
    return sentence
def clean_dataframe(data):
    data = data.dropna(how="any")   #删除空白
    for col in ['question1','question2']:
        data[col] = data[col].apply(clean_sentence)
    return data
def build_corpus(data):    #建立语料库
    corpus = []
    for col in ['question1','question2']:
        for sentence in data[col].iteritems():
            word_list = sentence[1].split(" ")
            corpus.append(word_list)
    return corpus
def tsne_plot(model):  #对模型做图形化输出
    labels = []
    tokens = []
    for word in model.wv.vocab:   #对于model中的所有词
        tokens.append(model[word])   #把word中的词向量添加到tokens中
        labels.append(word)   #把单词添加到labels中
    tsne_model = TSNE(perplexity=40,n_components=2,init='pca',n_iter=2500,random_state=23)  #建立TSNE模型
    new_values = tsne_model.fit_transform(tokens)   #new_values为训练后的数据
    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
    plt.figure(figsize=(16,16))
    for i in range(len(x)):
        plt.scatter(x[i],y[i])
        plt.annotate(labels[i],xy=(x[i],y[i]),xytext=(5,2),textcoords='offset points',ha='right',va='bottom')
        #xy为被注释的坐标点，xytext为注释文本的坐标点，textcoords为注释文本的坐标系属性,offset points表示相对于被注释点xy的偏移量,
    plt.show()

corpus = build_corpus(data)
model = word2vec.Word2Vec(corpus,size=100,window=20,min_count=200,workers=4) #建立模型，过滤200以下的数字，100层的神经网络
print(model.wv['trump'])  #输出单词trump在模型中的向量表示



