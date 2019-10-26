#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 22:39:58 2019

@author: ammar
"""

from os import walk
from html.parser import HTMLParser
#from nltk.stem import PorterStemmer
import re
import nltk
import sys
import datetime
sno = nltk.stem.SnowballStemmer('english')

#ps=PorterStemmer()

term_id=0

inverted_index={}
totalcorpuscount=0

terms_list=[]

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
    f_desc=open('terms.txt','w')
    term_id=0
    for term in terms_list:
        f_desc.write(term+'\t'+str(term_id)+'\n')
        term_id=term_id+1
    f_desc.close()

    
def addtoInvertedIndex(listofterms,docid):      #dictionary
    global inverted_index
    pos=0
    for term in listofterms:
        item={    
                'docid':docid,
                'position':pos
             }

        val=inverted_index.get(term)   
        
        if val is None:
            inverted_index[term]={}
            inverted_index[term]['doclist']=[]
        inverted_index[term]['doclist'].append(item)
        pos=pos+1 




def writeinvindfile():
    global inverted_index
    term_id=0
    with open('term_index.txt','w') as f:
        for i in inverted_index:
            _tuple=inverted_index[i]['doclist']
            #print(i)
            #print(_tuple)
            c_wordcount=len(_tuple)     #wordcount in corpus
            #docscount for term
            templist=[]
            pairs=''                 #docid&pos pair
            for inner_tuple in _tuple:      #each _tuple is a list of <docid,pos> pairs
                # c_wordcount=len(inner_tuple)
                pairs=pairs+' '+(str(inner_tuple.get('docid'))+','+str(inner_tuple.get('position')))+' '
                if inner_tuple.get('docid') not in templist:
                    templist.append(inner_tuple.get('docid'))
            p2=str(pairs)
          #  p2=p2[start:end]
            
            
            d_count=len(templist)
            #f.write(i+' '+c_wordcount+' '+d_count)
    #        print(p2)
   #         print('word '+str(i)+' in documents: ')
  #          print(d_count)
 #           print('word '+str(i)+' in whole corpus: ')
#            print(c_wordcount)
            finalline=str(term_id)+'\t'+str(c_wordcount)+'\t'+str(d_count)+'\t'+p2+'\n'
            term_id=term_id+1
            f.write(finalline)
        
           #print(c_wordcount)
           # print(d_count)



def makedoctxt(doc_directory):
    listoffiles=None
    index=0
    for dirpath,dirnames,filenames in walk(doc_directory):
        #print(filenames)
        listoffiles=filenames
        index=index+1
        
    #writing the file docs.txt
    maketxtfile(listoffiles,'docs.txt')

    return listoffiles



def makeinvind(doc_directory):
    
    print('start_time: ',datetime.datetime.now(),'\n')

    listoffiles=makedoctxt(doc_directory)
    doc_id=0
    
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
            #unique_list=unique(no_stopwords)                #removing duplicates
            #writeterms(f1,unique_list)             
            addtoInvertedIndex(no_stopwords,doc_id)
        doc_id=doc_id+1
        
    
    keys=[*inverted_index.keys()]
    writeterms(keys)
    global terms_list
    terms_list=keys
    
    
    
    writeinvindfile()
    
    print('Inverted Index Successfully made!')
    print('endtime :',datetime.datetime.now(),'\n')


   


def loadterms():
    global terms_list
    with open('terms.txt','r') as f2:
        for l in f2:
            #print(l,end='')
            start=l.find('\t')
          #  end=l.find('\n')
            #print(str(start)+','+str(end))
            term=l[0:start]
            terms_list.append(term)
            #print(l[start+1:end])



def loadinvertedindex():
    loadterms()
    global terms_list,inverted_index,totalcorpuscount

    with open('term_index.txt') as f:
        for l in f:
            tab=l.split('\t')
            pairs=re.findall('\d{1,},\d{1,}',tab[3])
            #print(tab)
            term=terms_list[int(tab[0])]    
            res=inverted_index.get(term)
            if res is None:
                inverted_index[term]={}
                inverted_index[term]['doclist']=[]
                
            inverted_index[term]['corpuscount']=tab[1]
            inverted_index[term]['doccount']=tab[2]
            totalcorpuscount=totalcorpuscount+int(tab[1])            


            for _tuple in pairs:
                t={'docid':None,'position':None}
                vals=_tuple.split(',')
                t['docid']=vals[0]
                t['position']=vals[1]
                inverted_index[term]['doclist'].append(t)   
                
    #print(inverted_index)        
    
    

        


    
        
    

def parsecommand():
    global terms_list
    
    args=sys.argv
    if len(args)<=1:
        print('Type in the correct Command!')
        return False
    
    term=None
    arg=str(args[1])
    if  arg == '--term':
       term=str(args[2])
       loadinvertedindex()         #using index_file.txt
       
       v=inverted_index.get(sno.stem(term))
       corpuscount=v.get('corpuscount')
       doccount=v.get('doccount')
       termid=terms_list.index(sno.stem(term))
       
       
       print ('termid: ',termid,'\n' ,'corpuscount: ',corpuscount,'\n','doccount: ',doccount,'\n')
       print(v)
           
       
       return True
   
       if v is not None:
           print(v)
       else:
           print('No such term found!')
   
           return False
           
    elif arg == '--make':
        doc_directory=str(args[2])      #corpus directory
        makeinvind(doc_directory)   #using corpus
        return True
    else:
       print('No argument like '+str(args[1]))
       return False
    
    


## main

if __name__=="__main__":
    print('\'Welcome to Mini Search Engine\'')
    print('COMMANDS\n')
    print('1. --term <term to search> \n')
    print('2. --make <corpus directory> \n')
    parsecommand()
else:
    print('called from program')
    print('loading inverted index...')    
    loadinvertedindex()

    #command=input('Enter respective command: ')
 

#print(inverted_index)



#termid occurence_in_corpus documents <docid,pos>

#1	4	3	 0,2  0,3  1,1  2,2 


         #   inverted_index[]
        #    print(t)
        #print(pairs)






#print(len(inverted_index['ali']))        





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


