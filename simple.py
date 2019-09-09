#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 00:31:36 2019

@author: ammar
"""
from os import walk
from html.parser import HTMLParser
#from nltk.stem import PorterStemmer
import re
import nltk
import sys
sno = nltk.stem.SnowballStemmer('english')




inverted_index_list=[]     #termid , docid pairs

term_list2=[]




def swap(first,second):
    return second,first
    



def addtoInvertedIndex2(listofterms,docid):
    global inverted_index_list
    
    
    pos=0
    for term in listofterms:
        obj={
                'docid':docid,
                'termid':term,
                'pos':pos
                
            }
        if obj not in inverted_index_list:
            inverted_index_list.append(obj)
        pos=pos+1
    

def assigntermids():
    global inverted_index_list
    
    for _tuple in inverted_index_list:
        _tuple['termid']=term_list2.index(_tuple['termid'])
    




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
        stemmedlist.insert(count,sno.stem(word))
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
    

def writeterms(terms_list):
    f_desc=open('terms2.txt','w')
    term_id=0
    for term in terms_list:
        f_desc.write(term+'\t'+str(term_id)+'\n')
        term_id=term_id+1
    f_desc.close()

    



def makedoctxt(doc_directory):
    listoffiles=None
    index=0
    for dirpath,dirnames,filenames in walk(doc_directory):
        #print(filenames)
        listoffiles=filenames
        index=index+1
        
    #writing the file docs.txt
    maketxtfile(listoffiles,'docs2.txt')

    return listoffiles





def sortbytermids():
    global inverted_index_list
    
    i=0
    invind_size=len(inverted_index_list)
    
    
    
    while i<invind_size:
        j=i+1
        while j<invind_size:
            if inverted_index_list[i]['termid']>inverted_index_list[j]['termid']:
                inverted_index_list[i],inverted_index_list[j]=swap(inverted_index_list[i],inverted_index_list[j])
            j=j+1
        i=i+1
    



def writeinvind2():
    global inverted_index_list
    with open('invind2.txt','w') as f:
         for t in inverted_index_list:
             f.write(str(t['termid'])+','+str(t['docid'])+','+str(t['pos'])+'\n')




def loadterms():
    global term_list2
    with open('terms2.txt','r') as f2:
        for l in f2:
            #print(l,end='')
            start=l.find('\t')
          #  end=l.find('\n')
            #print(str(start)+','+str(end))
            term=l[0:start]
            term_list2.append(term)
            #print(l[start+1:end])

    



def loadinvind2():
    global inverted_index_list
    
    loadterms()
    
    if len(inverted_index_list)>=1:
        print('inv index already loaded')
        return 0
    
    with open('invind2.txt','r') as f:
        for l in f:
            vals=l.split(',')
            
            vals[2]=vals[2][0:len(vals[2])-1]
            inverted_index_list.append({'docid':vals[1],'termid':vals[0],'pos':vals[2]})  
                    
                



def findterm(term):
    global term_list2
    
    result=[]
    termid=term_list2.index(term)
    docs=[]
    if termid is not None:
       for x in inverted_index_list:      
           if int(x['termid'])>termid:
               break
                   
           
           if int(x['termid'])==termid:
              result.append(x)  
              if x['docid'] not in docs:
                  docs.append(x['docid'])
    
    corpuscount=len(result)
    doccount=len(docs)
    
    
    
    
    
    print(result)
    return termid,corpuscount,doccount
    
    
    
    





def makeinvind2(doc_directory):          #without dictionary
    listoffiles=makedoctxt(doc_directory)
    doc_id=0
    global term_list2
    
    
    #with open('terms.txt','w') as f1:
    for filename in listoffiles:
        parser = MyHTMLParser()
        with open(doc_directory+'/'+filename,'r',encoding='utf-8',errors='ignore') as f:
        #f=open(doc_directory+'/'+filename,'r') 
        #with open('testdir2/'+listoffiles[0],'r') as f:
            contents=f.read()
            parser.feed(str(contents))
            text=parser.getstringofdata()                   #fetches text
            tokenized_list=re.findall('[A-Za-z]{1,}',text)  #regex tokenizing
            #print(tokenized_list)
            stemmed_list=stemthewords(tokenized_list)       #stemming
            no_stopwords=nostopwords(stemmed_list)           #ignoring stopwords
            
            addtoInvertedIndex2(no_stopwords,doc_id)
            term_list2.extend(no_stopwords)
            
        doc_id=doc_id+1
   
    term_list2=unique(term_list2)      #filter outs the duplicates
    writeterms(term_list2)
    
   # print(term_list2)
    
    
    assigntermids()                 #replaces the terms with termids in invind
    sortbytermids()    
    writeinvind2()

    

makeinvind2('testdir')

loadinvind2()


a,b,c=findterm('upton')

print ('termid: ',a,'\n' ,'corpuscount: ',b,'\n','doccount: ',c,'\n')










