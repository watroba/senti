#The following code contains a rough version of the preprocessing of tweets.
#In order to operate, the code requires nltk and applicable nltk data, as well as Python
#3.4 or later to operate.

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class exampleTweet:         #Class of example Tweets
    def __init__(self,ex):  #"Constructor class", ready for more arguments if necessary
        self.ex = ex        #ex means example

tweet1 = exampleTweet("This is the first example tweet. This tweet is an unhappy tweet. It contains some examples of being not happy.")
tweet2 = exampleTweet("This is the second example tweet. This is a very happy tweet. It contains some examples of being not sad.")





#print(tweet1.ex)  #Testing example tweets
#print(tweet2.ex)

#class tokenizer:                                   
#    def __init__(self, tweet1):                            #work in progress
#        pass
    
#    def splitter(self, tweet1):
#        self.tags = word_tokenize(exampleTweet)

#tags1 = tokenizer(tweet1)
#print(tags1)




tags1 = word_tokenize(tweet1.ex)    #Tokenizing tweet1
tags2 = word_tokenize(tweet2.ex)    #Tokenizing tweet2
#print(tags1)   #Testing tokenizer
#print(tags2)

stopWords = set(stopwords.words("english")) #Defines the set of "stop words", or irrelevant words


#Filtering stop words fron tags1
ftags1 = [] #Empty list for now
for w in tags1:                 
        if w not in stopWords:
            ftags1.append(w)


#Filtering stop words from tags2 (same as above in one line)
ftags2 = [x for x in tags2 if not x in stopWords] 

#print(ftags1)
#print(ftags2)

############################################################################################################################
########### Currently filtering stop words removes the word "not", fundamentally altering the meaning of parts of 
########### the example tweets. In the future, the list of stop words will need to be altered to remove "not" from the list
############################################################################################################################


def POS_tagging():  #Tagging tokens with parts of speech in ftags1
    try:
        for i in ftags1:                     #Currently only for ftags1(tweet1)
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            #print(tagged)

    except Exception as e:
            print(str(e))

POS_tagging()
#The potential exists to remove parts of speech deemed unessecarry for sentiment evaluation

#In order to test, remove desired commented print commands