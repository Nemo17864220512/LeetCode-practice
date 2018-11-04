# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:32:02 2018

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


#获得每一个文件中每个单词的TF值，返回一个字典和包含全部单词的列表
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
    List = sorted(list(set(List)))
    
    return List,a




#获得TF矩阵
def Get_matrix(name,dic):  
    #第一个数字为列数     
    List = [[ 0 for i in range(len(dic)) ] for i in range(len(name))]
    
    for i in range(len(name)):
        list1 = []
        a = {}
        list1,a = Get_TF(name[i])
        for j in range(len(dic)):
            if dic[j] in list1:
                List[i][j] = a[dic[j]]
                    
    return List



mat_train = Get_matrix(name_train,dic)
mat_test = Get_matrix(name_test,dic)
#print(mat)



#获得字典里每个词的IDF值存到列表里
def Get_IDF(mat_tf):
    list_idf = []
        
    for j in range(len(mat_tf[0])):
        num = 0
        for i in range(len(mat_tf)):
            if float(mat_tf[i][j]) != 0:
                num += 1
        list_idf.append(num)        
    return list_idf

list_idf = Get_IDF(mat_train)


#获得TF-IDF矩阵
def Get_Tf_Ifd_Matrix(mat,name,list_idf):
    
    for i in range(len(name)):
        list1 = []
        a = {}
        list1,a = Get_TF(name[i])
        for j in range(len(mat[0])):
            if dic[j] in list1:
                mat[i][j] = a[dic[j]]
        
    return mat


def Get_Tf_Idf_Mat(mat,name,list_idf,dic):
    List = []
    for i in range(len(name)):
        a = {}
        for j in range(len(mat[i])):
            if mat[i][j] != 0:
                a[dic[j]] = mat[i][j] * math.log(len(name)/(list_idf[j] + 1))
        
        List.append(a)
    
    return List

mat_train_tfidf = Get_Tf_Idf_Mat(mat_train,name_train,list_idf,dic)
mat_test_tfidf = Get_Tf_Idf_Mat(mat_test,name_test,list_idf,dic)



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

def return_maxname(a1):
    b = {}
    for i in range(len(a1)):
        if a1[i][0][7:-7] in b.keys():
            b[a1[i][0][7:-7]] += 1
        else:
            b[a1[i][0][7:-7]] = 1
    
    return max(b,key=b.get)
    




k = 10
num = 0 
for i in range(len(mat_test_tfidf)):
    
    a = {}
    
    for j in range(len(mat_train_tfidf)):
        
        a[name_train[j]] = Cos_value(mat_test_tfidf[i],mat_train_tfidf[j])
    
    sort_a = sorted(a.items(),key = lambda x:x[1],reverse = True)
    sort_a = sort_a[:k]
    
    if return_maxname(sort_a) in name_test[i]: 
        num += 1
    
print(num/len(mat_test_tfidf))


        
    
    
        
        
        
            
    
                
        







































