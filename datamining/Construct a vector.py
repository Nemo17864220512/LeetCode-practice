# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 16:41:46 2018

@author: Nemo
"""

import os
from textblob import TextBlob 
from textblob import Word 


#获取文件名
def Return_File_Name(Rootdir):
    name = []
    
    for root,dirs,files in os.walk(Rootdir):#root遍历的文件夹
        for file in files:
            name.append(os.path.join(root,file))
        for dirname in dirs:
            Return_File_Name(dirname)
    
    return name

Rootdir = "D:\训练集"
name = Return_File_Name(Rootdir)


print(len(name))

#构建字符串
def Get_str(name):
    s = ""

    for i in range(len(name)):
        
        fopen = open(name[i], 'r',errors='replace')
        
        for eachLine in fopen:
            s += eachLine
        fopen.close()
    
    return s
    
    
str1 = Get_str(name)

#规范化
def Tokenization_Stemmer(str1):
    
    zen = TextBlob(str1)
    
    zen = zen.words  #分词
    
    zen = zen.lemmatize() #名词单复数变原型
    
    zen = list(zen)    
    #动词分词和动名词 变 原型
    for i in range(len(zen)):
        w = Word(zen[i])
        zen[i] = w.lemmatize("v")
    #所有单词变换为小写
    for i in range(len(zen)):
        zen[i] = zen[i].lower()        
    zen = sorted(zen)            
    return zen

#停用词    
def stop_word():
    s = ""
    fopen = open("E:\停用词", 'r',errors='replace')
        
    for eachLine in fopen:
        s += eachLine
    fopen.close()
    
    stop_word = s.split()
   
    return stop_word

#构建向量
def construct_vecter(list1):
    Vecter_list = []
    num = 1
    for i in range(len(list1) - 1):
        if list1[i] == list1[i + 1]:
            num += 1
            if i == len(list1) - 1 and num >= 5:
                Vecter_list.append(list1[i])
        else:
            if num >= 5 and list1[i].isalpha():
                Vecter_list.append(list1[i])
                num = 1
    Vecter_list = list(set(Vecter_list) ^ set(stop_word()))
    Vecter_list = sorted(Vecter_list)
    return Vecter_list

"""

vector = construct_vecter(Tokenization_Stemmer(str1))

filename = "D:\向量"

with open(filename,'w') as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    for i in range(len(vector)):
        f.write(vector[i])
        f.write(" ")
    f.close()
"""        
print(len(construct_vecter(Tokenization_Stemmer(str1))))





 















 