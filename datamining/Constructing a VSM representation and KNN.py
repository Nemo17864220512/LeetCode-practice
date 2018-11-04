# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:49:33 2018

@author: Nemo
"""
import os
from textblob import TextBlob 
from textblob import Word
import math

#获得字典
def Get_dictionary():
    s = ""
    list1 = []
    fopen = open("D:\向量", 'r',errors='replace')
    
    for eachLine in fopen:
        s += eachLine
    fopen.close()
    list1 = s.split()
    
    return list1

dic = Get_dictionary()

Rootdir_train = "D:\训练集" #文件的总文件名
Rootdir_test = "D:\测试集"
#获取文件名
def Return_File_Name(Rootdir):
    name = []
    
    for root,dirs,files in os.walk(Rootdir):#root遍历的文件夹
        for file in files:
            name.append(os.path.join(root,file))
    for dirname in dirs:
        Return_File_Name(dirname)
    
    return name

#文件地址
name_train = Return_File_Name(Rootdir_train)
name_test = Return_File_Name(Rootdir_test)



#对一个文件进行分词，规范化
def Tokenization_Stemmer(str1):
    
    zen = TextBlob(str1)    
    zen = zen.words    
    zen = zen.lemmatize()
    
    zen = list(zen)
    for i in range(len(zen)):
        w = Word(zen[i])
        zen[i] = w.lemmatize("v")
    for i in range(len(zen)):
        zen[i] = zen[i].lower()
        
    zen = sorted(zen)
     
    return zen


#获得每一个文件中每个单词的TF值，返回一个字典,key为单词，value值为key出现次数
def Get_TF(filename):
    s = ""
    fopen = open(filename, 'r',errors='replace')
    
    for eachLine in fopen:
        s += eachLine
    fopen.close()
    
    List = Tokenization_Stemmer(s)
    len_list = len(List)
    a = {}
    for i in List:
        a[i] = round( List.count(i)/len_list , 5 ) #保留5位小数    
    return a

#遍历所有文件，获得每个文件的字典表示，并把这些字典添加到一个链表中
def Get_Mat_TF(name):
    List = []
    for i in range(len(name)):
        List.append(Get_TF(name[i]))
    return List
  
Mat_tf_train = Get_Mat_TF(name_train)
Mat_tf_test = Get_Mat_TF(name_test)

#获得向量中每个单词的IDF值    
def Get_Idf(Mat_tf,dic):
    a = {}
    for i in range(len(dic)):
        num = 0
        for j in range(len(Mat_tf)):
            if dic[i] in Mat_tf[j].keys():
                num += 1
        a[dic[i]] = num
    
    return a

dic_idf = Get_Idf(Mat_tf_train,dic)    

#计算TF-IDF值   
def Get_Tfidf(Mat_tf,dic_idf,name):
    
    for i in range(len(Mat_tf)):
        for key in Mat_tf[i]:
            if key in dic_idf.keys():
                Mat_tf[i][key] = Mat_tf[i][key] * math.log(len(name) / (dic_idf[key] + 1))
            else:
                Mat_tf[i][key] = 0
    
    return Mat_tf

mat_train_tfidf = Get_Tfidf(Mat_tf_train,dic_idf,name_train)
mat_test_tfidf = Get_Tfidf(Mat_tf_test,dic_idf,name_test)

print("矩阵完成")

#计算两个向量之间的cos值
def Cos_value(dic1,dic2):
    sum_dic1 = 0
    sum_dic2 = 0
    
    for i in dic1.values():
        sum_dic1 += i * i
    sum_dic1 = pow(sum_dic1,0.5)

    
    for i in dic2.values():
        sum_dic2 += i * i
    sum_dic2 = pow(sum_dic2,0.5)
        
    sum1 = 0
    for key1 in dic1.keys():
        if key1 in dic2.keys():
            sum1 += dic1[key1] * dic2[key1]

    return sum1 / (sum_dic1 + sum_dic2)

#返回前K个预测中出现次数最多的类的名字。
def return_maxname(a1):
    b = {}
    for i in range(len(a1)):
        if a1[i][0][7:-7] in b.keys():
            b[a1[i][0][7:-7]] += 1
        else:
            b[a1[i][0][7:-7]] = 1
    
    return max(b,key=b.get)
    


#返回分类成功的的概率
def Knn(mat_train_tfidf,mat_test_tfidf,name_train,name_test,k):
  
    num = 0
    
    for i in range(len(mat_test_tfidf)):
        
        a = {}
        
        for j in range(len(mat_train_tfidf)):
            
            a[name_train[j]] = Cos_value(mat_test_tfidf[i],mat_train_tfidf[j])
        
        sort_a = sorted(a.items(),key = lambda x:x[1],reverse = True)
        sort_a = sort_a[:k]
        
        if return_maxname(sort_a) in name_test[i]: 
            num += 1
  
    return (num/len(mat_test_tfidf))

k = 15
print(Knn(mat_train_tfidf,mat_test_tfidf,name_train,name_test,k))
            
        
                








