import random
import numpy as np
import re
import pandas as pd
import jieba
from collections import Counter
human = """
human = 称谓  娱乐
称谓 = 小爱 | 天猫精灵  | 小度 | 小冰
娱乐 = 打开空调 | 播放音乐 | 讲故事 | 读小说 | 打开电视
"""
machine ="""
machine_language = 问候 称呼 时间 对象  娱乐
问候 = 晚上好 |  早上好 | 你好 | 您好 | 你们好 | 好的 | OK
称呼 = 帅哥 | 美女 | 先生 
时间 = 正在 | 马上 | 等会 | 十分钟后 | 一小时后
对象 = 为您 | 为你 | 为你们
娱乐 = 打开空调 | 打开电视 | 开台灯 | 播放音乐 | 讲故事 | 读小说 
"""
class language_generate():   #句子生成类
    def create_grammar(self,grammar,split='=',linesplit='\n'):   #返回一个字典
        gram = {}
        for line in grammar.split(linesplit):
            if not line.strip():
                continue
            exp,stmt = line.split(split)
            gram[exp.strip()] = [e.split() for e in stmt.split('|')]
        return gram
    def generate(self,simple_gram,target):   #生成句子
        if target not in simple_gram:
            return target
        expanded = []
        for t in random.choice(simple_gram[target]):
            res = self.generate(simple_gram,t)
            expanded.append(res)
        return ''.join(e if e!='/n' else '\n' for e in expanded if e!='null')
    def generate_n(self,simple_gram,target,n):    #一次性生成n个句子
        sentences = []
        for i in range(n):
            if target not in simple_gram:
                sentences.append(target)
            tmp = self.generate(simple_gram,target)
            sentences.append(tmp)
        return sentences

class txt_analysis():    #文本生成类
    def token(self,string):
        return re.findall('\w+',string)
    def cut(self,string):
        return list(jieba.cut(string))



if __name__=="__main__":
    g = language_generate()
    gram = g.create_grammar(machine)
    # for i in range(20):
    #     language = g.generate(gram,target='machine_language')
    #     print(language)
    l = g.generate_n(gram,target="machine_language",n=10)
    for line in l:
        print(line)

    filename = "D:\PycharmProjects\数据分析\自然语言处理（高民权）\Data\movie_comments.csv"
    content = pd.read_csv(filename,encoding='utf-8')   #总共有4个列属性，分别为link、name、comment、star
    # comment = content["comment"]
    # print(len(comment))    #总共有261497条评论
    comments = content["comment"].tolist()    #把所有评论行成列表
    txt_ana = txt_analysis()
    comments_clean = [''.join(txt_ana.token(str(a))) for a in comments]    #把去除标点的文字再串联起来
    with open("comments.txt",'w',encoding='utf-8') as f:
        for comment in comments_clean:
            f.write(comment+'\n')
    Token_string = []
    for i,line in enumerate((open('comments.txt',encoding='utf-8'))):
        Token_string += txt_ana.cut(line)
    #print(Token_string)

    words_count = Counter(Token_string)
    print(words_count.most_common(100))   #

    Token_str = [str(t) for t in Token_string]
    Token_2_gram = [''.join(Token_str[i:i+2]) for i in range(len(Token_str[:-2]))]

    word_count2 = Counter(Token_2_gram)


    def prob_1(word):
        return words_count[word]/len(Token_string)    #word出现的次数除以总的词的个数
    print(prob_1('电影'))    #打印出单词“电影”出现的频率
    def prob_2(word1,word2):    #两个单词连在一起出现的概率
        if word1+word2 in word_count2:
            return word_count2[word1+word2]/len(Token_2_gram)
        else:
            return 1/len(Token_2_gram)
    def prob_3(sentence):    #一个句子出现的概率
        words = txt_ana.cut(sentence)
        sentence_pro = 1
        for i,word in enumerate(words[:-1]):
            next_ = words[i+1]
            probability = prob_2(word,next_)
            sentence_pro *= probability
        return sentence_pro
    print("句子出现的概率为：",prob_3("吴京的电影太垃圾了"))
    print("另一个句子出现的概率为：",prob_3(("包子馒头稀饭牛奶西瓜")))

    def generate_best(simple_grammar,target,n):    #生成n个句子，再选出最合理的那个句子
        gram_dic = g.create_grammar(simple_grammar)
        sentences = g.generate_n(gram_dic,target,n)
        result = []
        for s in sentences:
            s_pro = prob_3(s)
            result.append((s_pro,s))
        result = sorted(result,key=lambda x: x[0])
        return result[-1][1]

    #测试
    best_sentence = generate_best(machine,target="machine_language",n=20)    #求出最合理的句子
    print("10句中最合理的句子为：",best_sentence)





