'''
Created on Oct 18, 2016

@author: Joseph Watroba (W)
(Jared Presley (P) is my +1) -W
'''
#import modules
import sys          #for system stuff
import time         #for wait() fn
import io           #processing unicode from twitter
from twython import Twython #google Twython
from twython.exceptions import TwythonError #self explanatory
from twython import TwythonStreamer #4streams

#Code
#appkeys are now stored
def appkeys():
    try:
        f = open('appkeys.key','r')
    except OSError:
        f = open('appkeys.key','w')
        APP_KEY=input("Enter the app key: ")
        APP_SECRET=input("Enter the app secret: ")
        f.write(APP_KEY)
        f.write('\n')
        f.write(APP_SECRET)
        f.close()
    else:
        APP_KEY=f.readline().strip()
        APP_SECRET=f.readline().strip()
    
    return(APP_KEY,APP_SECRET)

#fn to get an oauth2 token using keys in vars above/store keys
def oauth2(APP_KEY, APP_SECRET):    
    twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()
    
    #create token file, crypto needed
    f = open('token.key','w')
    f.write(ACCESS_TOKEN)
    f.close()
    
#fn to get oauth1 tokens using keys/store keys
def oauth1(APP_KEY, APP_SECRET): 

    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens()
    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

    f = open('token2a.key','w')
    f.write(OAUTH_TOKEN)
    f.write('\n')
    f.write(OAUTH_TOKEN_SECRET)
    f.close()
    
    print(auth['auth_url'])
    oauth_verifier = input('Enter pin: ')
    
    #DO NOT FORGET TO REINSTANTIATE WITH OAUTH TOKENS! Took me WAY too long -W
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    final_tokens = twitter.get_authorized_tokens(oauth_verifier)
    fot = final_tokens['oauth_token']
    fots = final_tokens['oauth_token_secret']    
    
    r = open('token2f.key','w')
    r.write(fot)
    r.write('\n')
    r.write(fots)
    r.close()

#fn to access oauth2 tokens
def authrv2(APP_KEY, APP_SECRET):
    try: 
        f = open('token.key','r')
    except OSError:
        oauth2(APP_KEY, APP_SECRET)
        f = open('token.key','r')
    finally:
        ACCESS_TOKEN = f.readline().strip();
        f.close()
    return ACCESS_TOKEN

def authrv1(APP_KEY, APP_SECRET):
    try: 
        f = open('token2f.key','r')
    except:
        oauth1(APP_KEY, APP_SECRET)
        f = open('token2f.key','r')
    finally:
        OAUTH_TOKEN = f.readline().strip()
        OAUTH_TOKEN_SECRET = f.readline().strip()
        f.close()
    return (OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#class for handling twython streams
class Streamers(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print(data['text'].encode('utf-8'))
            
    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()
#fn for queries (add dict parameter in for calls from main())
def query(APP_KEY, APP_SECRET):
    
    ACCESS_TOKEN = authrv2(APP_KEY, APP_SECRET) 
    qtwitter = Twython(APP_KEY,access_token=ACCESS_TOKEN)
    
    try:
        #replace txt inside () with variable parameters for looping/ease
        results = qtwitter.search(q ='tech',result_type ='recent',count = '100',geo='35.2951,-93.1387,1mi')
    except TwythonError as e:
        #if an error, wait for 15 min (in sec) for limit to reset, try again
        print(e)
    else:
        #change w to w+ to append file instead of overwriting
        d = io.open('data.txt','w',encoding='utf-8')
        #iterate through search results getting only text
        for result in results['statuses']:
            print(result['text'])
            d.write(result['text'])
            d.write("\n")
            
        d.close()
    
def queryv1(APP_KEY, APP_SECRET):
    
    auth = authrv1(APP_KEY, APP_SECRET)
    OAUTH_TOKEN = auth[0]
    OAUTH_TOKEN_SECRET = auth[1]
    
    qtwitter = Twython(APP_KEY,APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)

    try:
        results = qtwitter.search(q ='a',result_type ='recent',count = '100',geo='35.2951,-93.1387,1mi')
    except TwythonError as e:
        print(e)
    else: 
        d = io.open('data2.txt','w',encoding='utf-8')
        for result in results['statuses']:
            print(result['text'])
            d.write(result['text'])
            d.write("\n")
            
        d.close()

#------------------------------------------------------------------------------
#main fn
def main():
    
    #call to run query instead
    #query()
    
    #Twython oauth1 test
    queryv1()
    
#call main() if not used as lib    
if __name__== '__main__':
    main()
    
