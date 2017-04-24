'''
Created on Oct 18, 2016

@author: Joseph Watroba & Jared Presley
'''
#import modules
import sys                                                                      #for system stuff
import time                                                                     #for wait() fn
import io                                                                       #processing unicode from twitter
from twython import Twython                                                     #google Twython
from twython.exceptions import TwythonError                                     #self explanatory
from twython import TwythonStreamer                                             #4streams
'''
import counties
import collections
from CleanAnalysis import (POS_tagging,StopWordsFilter,tagger,expandContractions)
from nltk.stem import WordNetLemmatizer                                         #Multiple options
from nltk.corpus import wordnet
from ratings import csvd
import csv
from logging import raiseExceptions
'''

class TwyAccess(object):
    #class to group/organize methods    
    def __init__(self,oauthversion):
        self.appkeys()
        self.oauthversion = oauthversion
        
    def appkeys(self):
        try:
            f = open('appkeys.key','r')                                         #open '*.key' file where keys are stored
        except OSError:                    
            f = open('appkeys.key','w')    
            self.APP_KEY=input("Enter the app key: ") 
            self.APP_SECRET=input("Enter the app secret: ") 
            f.write(self.__APP_KEY)               
            f.write('\n')                 
            f.write(self.__APP_SECRET)            
        else:                              
            self.__APP_KEY=f.readline().strip()   
            self.__APP_SECRET=f.readline().strip()
        finally:                          
            f.close()                      
            
    #fn to get an oauth2 token using keys in vars above/store keys
    def oauth2(self):
        twitter = Twython(self.__APP_KEY, self.__APP_SECRET, oauth_version=2)   #Twython object, v.2
        ACCESS_TOKEN = twitter.obtain_access_token()                            #obtain oauth v2 access token
        
        #create token file, unencrypted 
        f = open('token.key','w')                                               #create key file for token
        f.write(ACCESS_TOKEN)                                                   #write the token
        f.close()                                                               #close file
        
    #fn to get oauth1 tokens using keys/store keys
    def oauth1(self):        
    
        twitter = Twython(self.__APP_KEY, self.__APP_SECRET)                    #create twython object, v.1
        auth = twitter.get_authentication_tokens()                              #get oauth v.1 tokens
        OAUTH_TOKEN = auth['oauth_token']                                       #pull out of auth
        OAUTH_TOKEN_SECRET = auth['oauth_token_secret']                         #pull out of auth
        
        with open('token2a.key','w') as f:                                      #open file to store tokens key
            f.write(OAUTH_TOKEN)                                                #write token to file
            f.write('\n')                                                       #newline to separate tokens
            f.write(OAUTH_TOKEN_SECRET)                                         #write token secret to file
        
        print(auth['auth_url'])                                                 #print auth_url to screen
                                                                                #user must follow and allow access to complete authorization, see oauth doc
        oauth_verifier = input('Enter pin: ')
        
        #reinstantiate twitter as twython object (authorized)
        twitter = Twython(self.__APP_KEY, self.__APP_SECRET, OAUTH_TOKEN,
                          OAUTH_TOKEN_SECRET)
        final_tokens = twitter.get_authorized_tokens(oauth_verifier)            #final step
        fot = final_tokens['oauth_token']                                       #final oauth token
        fots = final_tokens['oauth_token_secret']                               #final oauth secret token 
                                                                                #final tokens can be saved and used repeatedly in new objects
                                                                                #twythonobj->authentication->verify->twythonobj2->authorization->storekeys
        
        with open('token2f.key','w') as r: 
            r.write(fot)                
            r.write('\n')                
            r.write(fots)               
    
    #fn to access oauth2 tokens
    def authrv2(self):
        try:                            
            f = open('token.key','r')   
        except OSError:                 
            self.oauth2()
            f = open('token.key','r')   
        finally:                        
            ACCESS_TOKEN = f.readline().strip();    
            f.close()                   
        return ACCESS_TOKEN             
    
    #fn to access oauth1 tokens
    def authrv1(self):
        try:                           
            f = open('token2f.key','r') 
        except:                         
            self.oauth1() 
            f = open('token2f.key','r') 
        finally:                       
            OAUTH_TOKEN = f.readline().strip()  
            OAUTH_TOKEN_SECRET = f.readline().strip()   
            f.close()                  
        return (OAUTH_TOKEN, OAUTH_TOKEN_SECRET)    
    '''
    class Streamers(TwythonStreamer):                                           #parameter of TwythonStreamer type
        def on_success(self, data):                                             #if successful connection, pass datastream
            if 'text' in data:                                                  #if text field of data is populated:
                print(data['text'].encode('utf-8'))                             #print text encoded in utf-8
                
        def on_error(self, status_code, data):                                  #if unsuccessful connection attempt
            print(status_code)                                                  #print the code for the error
            self.disconnect()                                                   #autodisconnect to prevent ban
    '''
 
    def query(self, Q, GEO):                                                    #query using oauth v.2
        
        ACCESS_TOKEN = self.authrv2() 
        qtwitter = Twython(self.__APP_KEY,access_token=ACCESS_TOKEN) 
        for i in range(0,10):
            try:    #attempt following code
                    #get tweets from given parameters
                results = qtwitter.search(q =Q,result_type ='recent',count = '100',
                                          lang='en',geo=GEO)                        #GEO [lat,long,radius(mi/km)]
            except TwythonError as e:   
                if e.error_code == 500:
                    time.sleep(10*i)
                print(e)                
            else:   
                return results
        

    def queryv1(self, Q, GEO):
        
        auth = self.authrv1()                                                   #get oauth v.1 tokens
        OAUTH_TOKEN = auth[0]                                                   #oauth token from auth tuple
        OAUTH_TOKEN_SECRET = auth[1]                                            #oauth token secret from auth tuple
        
        #create object from all keys
        qtwitter = Twython(self.__APP_KEY,self.__APP_SECRET,OAUTH_TOKEN,
                           OAUTH_TOKEN_SECRET)
    
        try:                        
            results = qtwitter.search(q =Q,result_type ='recent',count = '100',
                                      lang='en',geo=GEO)                        #GEO [lat,long,radius(mi/km)]
        except TwythonError as e:                                               #if error of TwythonError type
            print(e)                                                            #output error
        else:                       
            with io.open('data2.dat','a+',encoding='utf-8') as d:               #unicode frmt
                for result in results['statuses']:                              #iterate through result
#                    print(result['text'])                                       #print result #testing only
                    d.write(result['text'])                                     #write result to file
                    d.write("\n")                                               #write newline to file

