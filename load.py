# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
from nltk.corpus import brown
from nltk.corpus import stopwords
from os.path import join
from pymongo import MongoClient 
from sklearn.feature_extraction.text import TfidfVectorizer
import codecs
import json
import jieba
import logging
import os
import nltk
import numpy as np
import re
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
jieba.set_dictionary('C:/Users/BIG DATA/Desktop/dict.txt.big.txt')  #切換至中文繁體字庫
jieba.load_userdict('C:/Users/BIG DATA/Desktop/dict.key.txt')	#關鍵詞字庫
path = 'C:\Users\BIG DATA\Desktop'


# 讀取資料庫資料
client = MongoClient('10.120.28.9',27017)
database = client['ZB105-4']
collection =database['All']


# 將Q資料存入陣列,original是Q資料原貌
original=[]
for post in collection.find(): 
	summary = post['Q'].encode('utf-8')
	original.append(summary)
#存成Q.json
with open(path+'\Q.json','wb') as f:
    json.dump((original),f,indent=4)

	
# 將A資料存入陣列,original是Q資料原貌	
answer=[]
for post in collection.find(): 
    summary = post['A'].encode('utf-8')
    answer.append(summary)
output = 'C:\Users\BIG DATA\Desktop\A.json'
with open(path+'\A.json','wb') as f:
    json.dump((answer),f,indent=4)

	
# 進行切字,QAlist_Q_words是切字後資料
QAlist_Q_words=[]
QAlist_words=[]
for i in range(0,len(original)):
	words = jieba.cut(original[i], cut_all=False)
	for word in words:
		utf8type = word.encode('utf-8')
		QAlist_words.append(utf8type)
	QAlist_Q_words.append(QAlist_words)
	QAlist_words=[]

	
# 去標點符號,delete_punctuations去完標點符號再由utf-8轉unicode
delete_punctuations=[]
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', 'Q', 'A', 'n', '\\',
                      ' ', '{', '}', '"','？', '！','。','、','；','：','〈','〉','《','》','【','】','﹝','﹞','「','」',
                       '　','『','』','“','”','〝','〞','‘','’','q','a','B','C','D']
delete_punctuations=[[word.decode('utf-8') for word in document if not word in english_punctuations] for document in QAlist_Q_words]

# 去停用字,最後查詢用陣列:bank_questions
chinese_stopwords = stopwords.words('chinese.txt')
bank_questions=[]
bank_questions = [[word for word in document if not word in chinese_stopwords] for document in delete_punctuations]


	
#讀取新聞資料
courses = [line.strip() for line in file('C:/Users/BIG DATA/Desktop/newsList.txt')]
	
#進行新聞切字,newslist_words:新聞切字後陣列
jieba.load_userdict('C:/Users/BIG DATA/Desktop/tagList.txt')     #新聞專用字典
newslist_words=[]
newslist_word=[]
for i in range(0,len(courses)):
	words = jieba.cut(courses[i], cut_all=False)
	for word in words:
		newslist_word.append(word)
		newslist_words.append(newslist_word)
		newslist_word=[]


#合併陣列
QA_and_news = []
QA_and_news.extend(loaddata.bank_questions)
QA_and_news.extend(loadnewsdata.newslist_words)


#建立向量特徵-dictionary&.save
dictionary = corpora.Dictionary(QA_and_news)
dictionary.save(path+"\dictionary.saved")

#Q-news向量化
Qnews_corpus = [dictionary.doc2bow(new) for new in QA_and_news]
#Q-向量化&QCorpus.json
bank_questions_corpus = [dictionary.doc2bow(bank_question) for bank_question in loaddata().bank_questions]
with open(path+'\QCorpus.json','wb') as f:
    json.dump((bank_questions_corpus),f,indent=4)
	
#LSI建立,取用Qnews_corpus
tfidf = models.TfidfModel(victory().Qnews_corpus)
Qnews_corpus_tfidf = tfidf[victory().Qnews_corpus]
lsi = models.LsiModel(Qnews_corpus_tfidf, id2word=dictionary, num_topics=10)
lsi.save(path+"\lsi.saved")
