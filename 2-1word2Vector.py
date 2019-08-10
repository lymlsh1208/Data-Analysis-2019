import jieba
from gensim.models import word2vec
from time import time
import os
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)

def cut_words():
    file = open("C:/Users/lym/zhwiki_jian_20190720","r",encoding="utf-8")
    target = open("C:/Users/lym/zhwiki_jian_20190720_curwords.txt","w",encoding="utf-8")
    line_num = 1
    line = file.readline()
    while line:
        print("-------processing-------",line_num,"--article--------")
        #line_seg = file.readline()
        line_cut = " ".join(jieba.cut(line))
        target.writelines(line_cut)
        line_num += 1
        line = file.readline()

    print("----------Complicated----------")
    file.close()
    target.close()
def create_Model():
    begin = time()
    sentences = word2vec.Text8Corpus("C:/Users/lym/zhwiki_jian_20190720_curwords.txt")   #导入已经切分好的语料
    model = word2vec.Word2Vec(sentences,sg=0,min_count=50,size=300,seed=1,iter=8,workers=15)
    #min_count在较大的语料中，可以忽略出现次数较小的单词
    #size 用来设置神经网络的层数，word2vec中的默认值是设置为100层
    # workers参数用于设置并发训练时候的线程数
    model.save("word2vec_wikicorpus.model")
    model.wv.save_word2vec_format("word2vec_wikicorpus.model.bin",binary = True)
    end = time()
    print("Total processing time:%d seconds" %(end-begin))

if __name__=="__main__":
    create_Model()
