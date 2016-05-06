# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
from load import loaddata
from nltk.corpus import brown
from nltk.corpus import stopwords
import jieba
import logging
import nltk
import load

#Query
target = '房貸要如何申請?最近的利率優惠如何?'
#1. get jieba
jieba_target = list(jieba.cut(target,cut_all=False))
jieba_target_stopword=[]
for i in range(0,len(jieba_target)):
    if jieba_target[i] not in loaddata().chinese_stopwords:
        jieba_target_stopword.append(jieba_target[i])
#2. get vec
vec_target = dictionary.doc2bow(jieba_target_stopword)
#3. get lda score
score_target = lsi[vec_target]

#sims是LSI的結果
index = similarities.MatrixSimilarity(lsi[bank_questions_corpus])
sims = index[score_target]


###建立權重分數
#建立權重陣列
tier1=[]
tier2=[]
tier3=[]
for i in range(1,4):
    fid = open('C:/Users/BIG DATA/Desktop/weight/tier%d.txt' %(i),'r')
    while 1:
        line = fid.readline().decode('utf-8').strip()
        if i == 1:
            tier1.append(line)
        if i == 2:
            tier2.append(line)
        if i == 3:
            tier3.append(line)
        if not line:
            break
        pass # do something
    fid.close()

#去空白
tier1.pop()
tier2.pop()
tier3.pop()

#建立權重字典
dic = {}
for word in tier3:
    dic[word] = 0.3 
for word in tier2:
    dic[word] = 0.5
for word in tier1:
    dic[word] = 1 
	
#Query的關鍵字權重字典-dic_Q
dic_Q={}
Qtier1words=[]
Qtier2words=[]
Qtier3words=[]
for i in range(0,len(jieba_target)):
    for j in range(0,len(tier1)):
        if jieba_target[i] == tier1[j]:
            Qtier1words.append(jieba_target[i])
    for k in range(0,len(tier2)):
        if jieba_target[i] == tier2[k]:
            Qtier2words.append(jieba_target[i])
    for l in range(0,len(tier3)):
        if jieba_target[i] == tier3[l]:
            Qtier3words.append(jieba_target[i])

for word in Qtier3words:
    dic_Q[word] = 0.3 
for word in Qtier2words:
    dic_Q[word] = 0.5
for word in Qtier1words:
    dic_Q[word] = 1
    
#sims分數+權重分數
for i in range(0,loaddata().bank_questions):
    for key in dic_Q:
        if key in loaddata().bank_questions[i]:
            sims[i] += dic[key]

#分數前10名的推薦答案			
sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
for i,s in sort_sims[0:10]:
    print loaddata().original[i], s