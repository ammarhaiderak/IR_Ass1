# Mini Search Engine using Python
Information Retrieval

In this project actually we have created an inverted index from a corpus of about 4000 documents. 
Postings are saved for each term in the document. Stop Words are eliminated, "Snow Ball Stemming" is applied on the words 
and for parsing the html document we have used 'Regex' library in python to correctly filter out the words for further 
processing. Once the inverted index is ready the documents are scored based on the set of queries
and 2 scoring functions are applied namely "Okapi BM25" and "Dirichlet Smoothing". Last but not the least for evaluation 
purpose "Mean Average Precision" or MAP is computed.


For this project you need the following resources:
1. corpus
2. relevance judgements.qrel
3. Topics.xml

required resource available at: https://drive.google.com/open?id=1psqQn9q6U1JY3zCG98J_mO2H-2pfjML6

note: corpus 'folder' and 2,3 should be in the working directory 

corpus: contains list of html documents on which the inverted index is created
relevence judgement.qrel: the Human Graded documents for a set of queries are available in this document.
Topics.xml: queries with topic/query id are available in this document.


How to run the program?
Just these follow simple steps
1. for command based interfaces like linux change current directory where solution.py is present 
2. type in "./solution.py --make {corpus folder name}"  this command will create inverted index for all documents in corpus
3. then to lookup for a specific term in the corpus(actually inverted index) type in "./solution.py --term <word to lookup>"
4. Now to apply scoring function you need to run query.py file
5. type in "./query.py --score {scoring function}"    scoring functions={'okapi','dirichlet'}
6. to evaluate the scored/ranked documents use this command "./query.py --evalauate relevance\ judgements.qrel"

note: if you need to rescore the documents you may use "--force True" parameter at compile time



Thank You!
