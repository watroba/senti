#!/usr/bin/env python

'''
Created on Mar 29, 2017

@author: Joseph
'''
import sys                                                                      #for system stuff
import time                                                                     #for wait() fn
import io   
from access import TwyAccess
import counties
import collections
from CleanAnalysis import (POS_tagging,StopWordsFilter,tagger,expandContractions)
from nltk.stem import WordNetLemmatizer                                         #Multiple options
from nltk.corpus import wordnet
from ratings import csvd
import csv
from logging import raiseExceptions

def conv(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    elif treebank_tag.startswith('S'):
        return wordnet.ADJ_SAT
    else:
        return wordnet.NOUN
    
'''
def moody(VAD,VAD_AVG):
    v,a,d=VAD
    vc,ac,dc=VAD_AVG
    
    if(v>=vc):
        if(a>=ac):
            if(d>=dc):
                return 'exuberant'
            elif(d<dc):
                return 'dependent'
            else:
                return 'ERROR'
        elif(a<ac):
            if(d>=dc):
                return 'relaxed'
            elif(d<dc):
                return 'docile'
            else:
                return 'ERROR'
        else:
            return 'ERROR'
    elif(v<vc):
        if(a>=ac):
            if(d>=dc):
                return 'hostile'
            elif(d<dc):
                return 'anxious'
            else:
                return 'ERROR'
        elif(a<ac):
            if(d>=dc):
                return 'disdainful'
            elif(d<dc):
                return 'bored'
            else:
                return 'ERROR'
        else:
            return 'ERROR'
    else:
        return 'ERROR'
'''    
   
    
#------------------------------------------------------------------------------
#main fn
if __name__== '__main__':
    twya = TwyAccess(2)                                                         #TwyAccess class init
    lem = WordNetLemmatizer()                                                   #Lemmatizer class init
    
    Tavg={}                                                                     #Averages for counties
    Aavg=0
    Davg=0
    Vavg=0
    i=0    
    tchk = time.time()

    #area initialization
    radius = 5.02   #avg radius of AR county
    unit = 'mi'     #unit of miles
    
    #query setup and geo initialization
    Q = 'a OR e OR i OR o OR u'
    GEO = str(35.4406)+','+str(-93.0176)+','+str(radius)+unit
        
    #query looping over counties in order alphabetically 
    while True: #infinite loop
        #prevent excessive twitter api access
        if (time.time()<tchk+2):
            time.sleep((tchk+2)-time.time())
        else:
            tchk=time.time()
            #run rest of code
            #rest of code:
            for key in counties.od:
                lat = counties.od[key][3]
                long = counties.od[key][4]
                GEO = str(lat)+','+str(long)+','+str(radius)+unit
        
                print(key)
                results = twya.query(Q, GEO)
                for result in results['statuses']:
                    tagged =(POS_tagging(StopWordsFilter(tagger(
                        expandContractions(result['text'].lower())))))
                    for tag in tagged:
                        tag[0] = (lem.lemmatize(tag[0][0], pos=conv(tag[0][1])))
                        if tag[0] in csvd:
                            V,A,D = csvd[tag[0]]
                            Vavg+=V
                            Aavg+=A
                            Davg+=D
                            i+=1
                            print(i)
        
                Tavg[key]=Vavg/i,Aavg/i,Davg/i
        
            with open('countyVADdata.csv','a+',newline='') as csvfile:
                cout = csv.writer(csvfile,dialect='excel')
                for key in counties.od:
                    print(key+':'+str(Tavg[key][0])+' '+str(Tavg[key][1])+' '+
                          str(Tavg[key][2])+'\n')
                    cout.writerow([time.time(),key,Tavg[key][0],Tavg[key][1],
                                   Tavg[key][2]])
            #end rest of code