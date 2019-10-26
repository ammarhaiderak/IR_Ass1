#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 17:02:11 2019

@author: ammar
"""
import pathlib
import math
import solution             #loads inverted index already created
import re
import nltk
import argparse
import operator
sno = nltk.stem.SnowballStemmer('english')
import csv

invind=solution.inverted_index
totalcorpuscount=solution.totalcorpuscount


import xml.etree.ElementTree as ET          #for xml parsing


queries=[]

'''
query= {
number: ' ',
words:[],
}

'''

docs=[]


def avgdoclen():
    return float(totalcorpuscount)/len(docs)


def doclength(fname):
    num_words = 0
 
    with open(fname, 'r',errors='ignore') as f:
        for line in f:
            words = line.split()
            num_words += len(words)
    #      print("Number of words:")
    #     print(num_words)
    return num_words



def loaddocs():
    with open('docs.txt') as fd:
         lis=fd.readlines() 
         for r in lis:
             splitted=r.split('\t')
             docs.append(splitted[0])


def loadqueries():

    tree = ET.parse('topics.xml')
    root = tree.getroot()
    #print(root)
    for child in root.iter('topic'):
        #print(child.attrib['number'])
        for c in child.iter('query'):
         #   print(c.text)
            l=re.findall('[A-Za-z\']{1,}',c.text)
            index=0
            l=solution.nostopwords(l)            
            for w in l:
                temp=sno.stem(w)
                temp=temp.lower() 
                #temp=solution.nostopwords(temp)                       
                l[index]=temp
                index=index+1
            obj={
                'number':child.attrib['number'],
                'words':l,
            }        
            queries.append(obj)        
            

            


def scoringfunct1(did,q):       #Okapi BM25
    
    k1=1.2
    k2=500
    b=0.75
    K=k1*((1-b)+b* (doclength('corpus/'+docs[did])/(avgdoclen())))
    
    number=q['number']
    words=q['words']
        
    D=len(docs)     #no of Documents in corpus
    

    score=0
    count=0
    for w in words:
         
     
        temp=invind.get(w)                        
        temp2=temp.get('doclist')
        df=len(temp2)
        tfq=words.count(w) #term frequency in query

        tf=0
        for d in temp2:
            if int(d.get('docid'))==did:
               tf=tf+1
        
        if tf==0:
            count+=1        
        
        
        A=math.log((D+0.5)/(df+0.5))
        B=((1+k1)*tf)/(K+tf)  
        C=((1+k2)*tfq)/(k2+tfq)

        score+=A*B*C             
        
    if count>=2:
       score=-9999
    return score


def scoringfunct2(did,q):         #dirichlet smooting
    
    
    mu=avgdoclen()
        
    q1=q        #uss carl vinson
    number=q1['number']
    words=q1['words']
    prob=0
    
    count=0
    for w in words:
        #print(w)
        temp=invind.get(w)                        
        temp2=temp.get('doclist')        
    
        
        doccount=temp.get('doccount')       #freq of doc having this term
        corpcount=temp.get('corpuscount')   #freq of term in corp
    
        
        

        corpdist=float(corpcount)/float(totalcorpuscount)    
    
        tf=0
        for d in temp2:
            if int(d.get('docid'))==did:
               tf=tf+1
        
        if tf==0:
            count+=1        



        doclen=doclength('corpus/'+docs[did])     # total words in document
        
        docdist=float(tf)/float(doclen)    
            
        
        N=doclen
        

        lembda=float(N)/float(N+mu) 
        #print('tf: '+str(tf))   
        
        if prob==0:     #for first time
            prob=math.log(docdist*lembda+corpdist*(1-lembda))
        else:
            prob+=math.log(docdist*lembda+corpdist*(1-lembda))

        #print(prob)
        #print('docdist: ',docdist,'\n','corpdist: ',corpdist)    
    
#    print(prob) 

    if count>=2:        #for checking if more than 1 words of query are not in the document d 
       prob=-9999

    return prob
        


 #  count=0    
   # for w in words:
    #    if count==1:
                   
                               
                

def callscoringfunct(typ,did,q):
    val=None    
    if typ=='dirichlet':
       val=scoringfunct2(did,q)    
    elif typ=='okapi':
       val=scoringfunct1(did,q)
    return val




def scoredocs(scorefunct,end):

    
    path = pathlib.Path('scored')
    if path.exists():
        with open('scored','r+') as scored:
             v=int(scored.read())
             if v==1:
                return 'already scored'
    
    retrieved={}    
    
    print(scorefunct+' Smoothing \n')
    
    for j in range(0,end):
        for i in range(0,len(docs)):
            m2=callscoringfunct(scorefunct,i,queries[j])    #scoringfuncttype,docid,queryid/topic 
            if m2!=-9999:                                   #not considering irrelevent documents              
               retrieved[i]=round(m2,4)
    
        
        sorted_x = sorted(retrieved.items(), key=operator.itemgetter(1),reverse=True)
        #sorting retrieved dictionary based on score in descending order

        #print(sorted_x)
        
        rank=1
        qnum=queries[j]['number']
        print('Making table for results for query ',qnum,'...')
            
        with open(scorefunct+'/query_'+str(qnum)+'.csv', mode='w+') as queryresult:
            result_writer = csv.writer(queryresult, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            result_writer.writerow(['topic','doc','rank','score','run'])            
            for s in sorted_x:            
                result_writer.writerow([qnum,docs[s[0]],str(rank),str(s[1]),'run1'])                
                #print(qnum+'\t'+docs[s[0]]+'\t'+str(rank)+'\t'+str(s[1])+'\trun1'+'\n')
                rank+=1
    
    with open('scored','w') as scored:
         scored.write('1')
    
    return 'scoring complete'
            
     
        


#ma=0        #max prob
#mi=0        #min prob
#print(totalcorpuscount)

#loaddocs()


def evaluate(qrelfile,end,scorefunct):
    
    avgprec=0    
    
    with open(scorefunct+'/evalresults.txt','w') as evalresult:
        for j in range(0,end):
        
            q=queries[j]['number']
            print('evaluating on query ',q)
            

            relscores={}                                    #relevance scores for query q
            #202 0 clueweb12-0900tw-23-04411 0
            with open(qrelfile,'r') as qrel:
                 for line in qrel:
                     l=line.split(' ')
                     
                     if l[0]==q:
                        relscores[l[2]]={'topic':l[0],'score':l[3][0:len(l[3])-1]}      #key is docname
                        #.append({'topic':l[0],'docname':l[2],'score':l[3][0:len(l[3])-1]})
            

            '''
            for r in relscores:
                print(relscores[r])          
            '''
            
            graded={}
            

            totalrelevant=0

            relvdocs=[]         #names of documents that are relevent , just to simplify/speedup calculations of MAP
            with open(scorefunct+'/query_'+str(q)+'.csv','r') as f:       #there is a file of results for each query with name query_<topic>
                 for line in f:
                     l=line.split(',')
                     docname=l[1]
                     detail=relscores.get(docname)             
                     score=-9999    
                     if detail is not None:                 #if grade is provided for doc otherwise -9999 which is NR
                        score=int(detail['score'])
                     
                     grade='NR'
                     if score>0:
                        grade='R'
                        totalrelevant+=1
                        relvdocs.append(docname)

                     graded[docname]={'grade':grade,'precision':None,'recall':None }      
             
            if totalrelevant==0:
               totalrelevant=1      #to avoid divide by zero error


            retcount=0        #retrieved count
            relcount=0        #currently relevent docs  
            
            for r in graded:                    #computing precision and recall
                grade=graded[r]['grade']
                retcount+=1

                if grade=='R':
                   relcount+=1
                
                
                graded[r]['recall']=relcount/totalrelevant        
                graded[r]['precision']=relcount/retcount
                
                #retcount+=1 
                    
            

            keys=[*graded.keys()]       #list of keys i.e doc names
            pat5=keys[4]
            pat10=keys[9]
            pat20=keys[19]
            pat30=keys[29]

            pat5=graded[pat5]['precision']
            pat10=graded[pat10]['precision']
            pat20=graded[pat20]['precision']
            pat30=graded[pat30]['precision']
           
            
            prec_sum=0  #precision sum
            for doc in relvdocs:                #sums precision of relevant docs only
                prec_sum+=graded[doc]['precision']
            
            
            MAP=prec_sum/totalrelevant
            
            avgprec+=MAP
            
            '''
            for r in graded:
                print(graded[r])            
            '''               
                    
            
            print('P@5:',pat5,'\tP@10: ',pat10,'\tP@20:',pat20,'\tP@30:',pat30,'\tMAP:',MAP)                  
            evalresult.write('query:'+q+'\tP@5:'+str(pat5)+'\tP@10: '+str(pat10)+'\tP@20:'+str(pat20)+'\tP@30:'+str(pat30)+'\tMAP:'+str(MAP)+'\n')            

             
        print('Average AP for all queries: ',avgprec/len(queries))
        
        evalresult.write('Average AP for all queries: '+str(avgprec/len(queries)))



def resetflag():
    with open('scored','w') as f:
         f.write('0')



def main():

   
    #print(queries)
    loaddocs()
    loadqueries()

    parser = argparse.ArgumentParser()

    parser.add_argument("--score",dest="score", type=str,default="dirichlet",help="scoring function",choices=['dirichlet','okapi'])
    
    parser.add_argument("--evaluate",dest="eval", type=str,default=None,help="evalute scored docs for passed query")
    
    parser.add_argument("--force",dest="force", type=bool,default=False,help="Forcibly recompute scores")
            
    args=parser.parse_args()
    
    
    if args.force:
       resetflag()

    end=len(queries)

    print(scoredocs(args.score,end))    
        
    if args.eval is not None:
       evaluate(args.eval,end,args.score)      
    
    
           
     
    #print('docid: ',i,' score: ',m2)




if __name__=='__main__':
    main()


