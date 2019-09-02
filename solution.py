#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 22:39:58 2019

@author: ammar
"""

from os import walk
from html.parser import HTMLParser
from nltk.stem import PorterStemmer
import re


ps=PorterStemmer()



class MyHTMLParser(HTMLParser):
    stringofdata='empty'    
        
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:",tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :",tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)
        self.stringofdata=self.stringofdata+data
    def getstringofdata(self):
        return self.stringofdata
    
parser = MyHTMLParser()



def stemthewords(list_of_words):
    stemmedlist=[]
    count=0
    for word in list_of_words:
        stemmedlist.insert(count,ps.stem(word))
        count=count+1
    return stemmedlist
    
def unique(list1): 
  
    # intilize a null list 
    unique_list = [] 
      
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list


def nostopwords(list1): 
    with open('stoplist.txt','r') as f:
        lines=f.readlines()
    
    list2=lines
    newlist=[]
    # traverse for all elements 
    for x in list1: 
        if x not in list2: 
            newlist.append(x) 
    return newlist







listoffiles=None

index=0
for dirpath,dirnames,filenames in walk('testdir2'):
    #print(filenames)
    listoffiles=filenames
    index=index+1

print(listoffiles)
print(index)



#for filename in listoffiles:
    #with open('testdir/'+filename,'r') as f:
    with open('testdir2/'+listoffiles[0],'r') as f:
        contents=f.read()
        print(filename)
        #print(contents)
        parser.feed(contents)
        text=parser.getstringofdata()
        tokenized_list=re.findall('[A-Za-z]{1,}',text)
        stemmed_list=stemthewords(tokenized_list)
        unique_list=unique(stemmed_list)
        no_stopwords=nostopwords(unique_list)
        
        
        

print(no_stopwords)
print(unique_list)
print(stemmed_list)
print(tokenized_list)


