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


term_id=0

inverted_index={
        }


#inverted_index_item={
#        'termid':None,
#        'doclist':[
#           {
#            'doc':'docid1',
#            'position':'position'                           
#           },
#           {
#            'doc':'docid',
#            'position':'position'                           
#           },
#           ...
#           ]
#       }


class MyHTMLParser(HTMLParser):
    stringofdata=''    
        
    #def handle_starttag(self, tag, attrs):
    #    print("Encountered a start tag:",tag)

    #def handle_endtag(self, tag):
    #    print("Encountered an end tag :",tag)
    
    def handle_data(self, data):
        #print("Encountered some data  :", data)
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
    lines=[]
    index=0
    with open('stoplist.txt','r') as f:
        for line in f:
           # print(line,end='')
            lines.insert(index,line)
            index=index+1
            
    list2=lines
    newlist=[]
    # traverse for all elements 
    for x in list1: 
        if x not in list2:
            x.lower()
            newlist.append(x) 
    return newlist



def maketxtfile(fileslist,filename):
    with open(filename,'w') as f:
        _id=0
        for doc_name in fileslist:
            f.write(doc_name+'\t'+str(_id)+'\n')
            _id=_id+1
    

def writeterms(f_desc,terms_list):
    global term_id
    for term in terms_list:
        f_desc.write(term+'\t'+str(term_id)+'\n')
        term_id=term_id+1

def addtoInvertedIndex(listofterms,docid):
    global inverted_index
    pos=0
    for term in listofterms:
        item={    
                'docid':docid,
                'position':pos
             }

        val=inverted_index.get(term)        
        if val is None:
            inverted_index[term]=[]
        inverted_index[term].append(item)
        pos=pos+1 




listoffiles=None


doc_directory = input("Enter name of the directory: ")  # Python 3
print(doc_directory) 

index=0
for dirpath,dirnames,filenames in walk(doc_directory):
    #print(filenames)
    listoffiles=filenames
    index=index+1

#print(listoffiles)
#print(index)
#python



#writing the file docs.txt
maketxtfile(listoffiles,'docs.txt')

doc_id=0

with open('terms.txt','w') as f1:
    for filename in listoffiles:
        parser = MyHTMLParser()
        with open(doc_directory+'/'+filename,'rb') as f:
        #f=open(doc_directory+'/'+filename,'r') 
        #with open('testdir2/'+listoffiles[0],'r') as f:
            contents=f.read()
            parser.feed(str(contents))
            text=parser.getstringofdata()                   #fetches text
            tokenized_list=re.findall('[A-Za-z]{1,}',text)  #regex tokenizing
        #print(filename+'\n')
        #print(tokenized_list)
            stemmed_list=stemthewords(tokenized_list)       #stemming
            unique_list=unique(stemmed_list)                #removing duplicates
            finallist=nostopwords(unique_list)              #ignoring stopwords
            writeterms(f1,finallist)            
            addtoInvertedIndex(finallist,doc_id)
        doc_id=doc_id+1
        #f.close()
        
        
        


#va=inverted_index.get('123')
#if va is None:
#    inverted_index['123']=[]
#inverted_index['123'].append({'item1':1,'item2':2})
#
#
#print(inverted_index)
#print(inverted_index['is'])
#
#print(finallist)
#print(unique_list)
#print(stemmed_list)
#print(tokenized_list)


