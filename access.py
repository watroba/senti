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
import counties
import collections

#Code
#appkeys are now stored
#fn to get appkeys from twitter through Twython

class TwyAccess(object):
    #class to group/organize methods    
    def __init__(self,oauthversion):
        self.appkeys()
        self.oauthversion = oauthversion
        
    def appkeys(self):
        try:
            f = open('appkeys.key','r')    #open '*.key' file where keys are stored
        except OSError:                    #if .key does not exist
            f = open('appkeys.key','w')    #open w/ 'w' to create/write to file
            self.APP_KEY=input("Enter the app key: ") #manual entry required for now
            self.APP_SECRET=input("Enter the app secret: ") #manual entry req'd for now
            f.write(self.__APP_KEY)               #write appkey to file
            f.write('\n')                  #newline to separate keys
            f.write(self.__APP_SECRET)            #write appsecret to file
        else:                              #if no problems opening
            self.__APP_KEY=f.readline().strip()   #read first line, strip all whitespace
            self.__APP_SECRET=f.readline().strip()#read next line, strip all whitespace
        finally:                           #always execute this code
            f.close()                      #close file
            
    #fn to get an oauth2 token using keys in vars above/store keys
    def oauth2(self):
        twitter = Twython(self.__APP_KEY, self.__APP_SECRET, oauth_version=2) #Twython object, v.2
        ACCESS_TOKEN = twitter.obtain_access_token() #obtain oauth v2 access token
        
        #create token file, unencrypted 
        f = open('token.key','w')           #create key file for token
        f.write(ACCESS_TOKEN)               #write the token
        f.close()                           #close file
        
    #fn to get oauth1 tokens using keys/store keys
    def oauth1(self):        
    
        twitter = Twython(self.__APP_KEY, self.__APP_SECRET)  #create twython object, v.1
        auth = twitter.get_authentication_tokens()  #get oauth v.1 tokens
        OAUTH_TOKEN = auth['oauth_token']           #pull out of auth
        OAUTH_TOKEN_SECRET = auth['oauth_token_secret'] #pull out of auth
        
        with open('token2a.key','w') as f:         #open file to store tokens key
            f.write(OAUTH_TOKEN)                #write token to file
            f.write('\n')                       #newline to separate tokens
            f.write(OAUTH_TOKEN_SECRET)         #write token secret to file
        
        print(auth['auth_url'])             #print auth_url to screen
        #user must follow and allow access to complete authorization, see oauth doc
        oauth_verifier = input('Enter pin: ')   #user inputs pin req'd for auth
        
        #reinstantiate twitter as twython object (authorized)
        twitter = Twython(self.__APP_KEY, self.__APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        final_tokens = twitter.get_authorized_tokens(oauth_verifier) #final step
        fot = final_tokens['oauth_token']           #final oauth token
        fots = final_tokens['oauth_token_secret']   #final oauth secret token 
        #final tokens can be saved and used repeatedly in new objects
        #twythonobj->authentication->verify->twythonobj2->authorization->storekeys
        
        with open('token2f.key','w') as r: #open final key file - create if not there
            r.write(fot)                #write final oauth v.1 token
            r.write('\n')               #newline to separate 
            r.write(fots)               #write final oauth v.1 secret token
    
    #fn to access oauth2 tokens
    def authrv2(self):
        try:                            #attempt following code
            f = open('token.key','r')   #open key file for oauth v.2 token
        except OSError:                 #if file does not exist error, do following
            self.oauth2() #get ouath v.2 keys/create key file in fn
            f = open('token.key','r')   #open key file for oauth v.2 token take dos
        finally:                        #always execute following code
            ACCESS_TOKEN = f.readline().strip();    #read line, strip whitespace
            f.close()                   #close file
        return ACCESS_TOKEN             #return access token
    
    #fn to access oauth1 tokens
    def authrv1(self):
        try:                            #attempt following code
            f = open('token2f.key','r') #open final key file for oauth v1 tokens
        except:                         #if file does not exist error, do following
            self.oauth1() #get oauth v.1 keys/create key file in fn
            f = open('token2f.key','r') #open key file for oauth v.1 tokens take dos
        finally:                        #always execute following code
            OAUTH_TOKEN = f.readline().strip()  #read line, strip whitespace
            OAUTH_TOKEN_SECRET = f.readline().strip()   #read next line, strip ws
            f.close()                   #close file
        return (OAUTH_TOKEN, OAUTH_TOKEN_SECRET)    #return tuple of keys
    #------------------------------------------------------------------------------
    #class for handling twython streams
    class Streamers(TwythonStreamer):   #parameter of TwythonStreamer type
        def on_success(self, data):     #if successful connection, pass datastream
            if 'text' in data:          #if text field of data is populated:
                print(data['text'].encode('utf-8')) #print text encoded in utf-8
                
        def on_error(self, status_code, data):  #if unsuccessful connection attempt
            print(status_code)          #print the code for the error
            self.disconnect()           #autodisconnect to prevent ban
    
    #fn for queries (add dict parameter in for calls from main())
    def query(self, Q, GEO):     #query using oauth v.2
        
        ACCESS_TOKEN = self.authrv2() #get oauth v.2 access token
        qtwitter = Twython(self.__APP_KEY,access_token=ACCESS_TOKEN)   #create twythonobj
        
        try:    #attempt following code
                #get tweets from given parameters
            results = qtwitter.search(q =Q,result_type ='recent',count = '100',
                                      lang='en',geo=GEO)  #GEO [lat,long,radius(mi/km)]
        except TwythonError as e:   #if error in search of TwythonError type:
            print(e)                #return error
        else:   #if successful, do following
            with io.open('data.dat','a+',encoding='utf-8') as d:    #unicode frmt
                for result in results['statuses']:          #iterate through result
                    print(result['text'])                   #print result
                    d.write(result['text'])                 #write result to file
                    d.write("\n")                           #write newline to file
        
    def queryv1(self, Q, GEO):
        
        auth = self.authrv1() #get oauth v.1 tokens
        OAUTH_TOKEN = auth[0]               #oauth token from auth tuple
        OAUTH_TOKEN_SECRET = auth[1]        #oauth token secret from auth tuple
        
        #create object from all keys
        qtwitter = Twython(self.__APP_KEY,self.__APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
    
        try:                        #attempt following code
            results = qtwitter.search(q =Q,result_type ='recent',count = '100',
                                      lang='en',geo=GEO)  #GEO [lat,long,radius(mi/km)]
        except TwythonError as e:   #if error of TwythonError type
            print(e)                #output error
        else:                       #if successful
            with io.open('data2.dat','a+',encoding='utf-8') as d:    #unicode frmt
                for result in results['statuses']:          #iterate through result
                    print(result['text'])                   #print result
                    d.write(result['text'])                 #write result to file
                    d.write("\n")                           #write newline to file


#------------------------------------------------------------------------------
#main fn
def main():
    twya = TwyAccess(2)
    
    #area initialization
    radius = 5.02   #avg radius of AR county
    unit = 'mi'     #unit of miles
    
    #query setup and geo initialization
    Q = 'a OR e OR i OR o OR u'
    GEO = str(35.4406)+','+str(-93.0176)+','+str(radius)+unit

    #clear data file
    with io.open('data.dat','w+',encoding='utf-8') as d:
        d.close()   
        
    #query looping over counties in order alphabetically     
    for key in counties.od:
        lat = counties.od[key][3]
        long = counties.od[key][4]
        GEO = str(lat)+','+str(long)+','+str(radius)+unit
        
        #print county name
        with io.open('data.dat','a+',encoding='utf-8') as d:
            d.write(counties.od[key][0]+':'+'\n')
        
        #query 
        twya.query(Q, GEO)
        
        with io.open('data.dat','a+',encoding='utf-8') as d:
            d.write('-------'+'\n')
            
   
#call main() if not used as lib   
 
#if __name__== '__main__':
#    main()
    