#The following code contains a rough version of the preprocessing of tweets.
#In order to operate, the code requires nltk and applicable nltk data, as well as Python
#3.4 or later to operate.

import nltk #Natural Launguage Toolkit
import yaml #Text file type used for dictionaries
from pprint import pprint
from nltk.tokenize import word_tokenize #There are multiple options for tokenizing
from nltk.corpus import stopwords
#from nltk.stem import PorterStemmer #There are also multiple stemmers
from nltk.stem import WordNetLemmatizer #Multiple options
import re #Regular expressions


def tagger(tweet):
    try:
        tags = word_tokenize(tweet)    #Tokenizing tweet1

        return tags
    except Exception as e:
        print(str(e))


def StopWordsFilter(tags):

    #Defines the set of "stop words", or irrelevant words (needs refinement)
    omitFromStopWords = set(('against','most','too','some','not','most','very','few','further','off','more','no'))
    punctuation = set(('!','.',',',':',';'))
    stopWords = set(stopwords.words("english"))
    alteredStopWords = set(stopwords.words("english")) - omitFromStopWords
    alteredStopWords = alteredStopWords | punctuation
    
    try:
        ftags = [i for i in tags if not i in alteredStopWords]
        return ftags

    except Exception as e:
        print(str(e))


class exampleTweet:         #Class of example Tweets
    def __init__(self,ex):  #"Constructor class", ready for more arguments if necessary
        self.ex = ex        



#class tokenizer:                                   
#    def __init__(self, tweet1):                            #work in progress
#        pass
    
#    def splitter(self, tweet1):
#        self.tags = word_tokenize(exampleTweet)

#tags1 = tokenizer(tweet1)
#print(tags1)



#Below I'm attempting to lemmatize the filtered tags. In theory, this should change synonymous words all to the same word.
#I believe that when implemented properly, this code should be placed AFTER the parts of speech tagging, as it is able to
#utilize parts of speech.

#lmtz = WordNetLemmatizer()

#for i in ftags1:
#   ftags1 = lmtz.lemmatize(i)
#print(ftags1)

#for i in ftags1:
#   print(lmtz.lemmatize(i))
#print(ftags1)


def POS_tagging(untagged):  #Tagging tokens with parts of speech in ftags1
    try:
        tagged = []
        for i in untagged:                     
            tagged.append(nltk.pos_tag(nltk.word_tokenize(i)))
        return tagged
        
    except Exception as e:
            print(str(e))
            

#The potential exists to remove parts of speech deemed unessecarry for sentiment evaluation

#lemmatization would ideally go here


#############################################################################################################################

##The following code was borrowed from http://fjavieralba.com/basic-sentiment-analysis-with-python.html (dictionary stuff)
#class DictionaryTagger(object):
#    def __init__(self, dictionary_paths):
#        files = [open(path, 'r') for path in dictionary_paths]
#        dictionaries = [yaml.load(dict_file) for dict_file in files]
#        map(lambda x: x.close(), files)
#        self.dictionary = {}
#        self.max_key_size = 0
#        for curr_dict in dictionaries:
#            for key in curr_dict:
#                if key in self.dictionary:
#                    self.dictionary[key].extend(curr_dict[key])
#                else:
#                    self.dictionary[key] = curr_dict[key]
#                    self.max_key_size = max(self.max_key_size, len(key))

#    def tag(self, postagged_sentences):
#        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

#    def tag_sentence(self, sentence, tag_with_lemmas=False):
#        """
#        the result is only one tagging of all the possible ones.
#        The resulting tagging is determined by these two priority rules:
#            - longest matches have higher priority
#            - search is made from left to right
#        """
#        tag_sentence = []
#        N = len(sentence)
#        if self.max_key_size == 0:
#            self.max_key_size = N
#        i = 0
#        while (i < N):
#            j = min(i + self.max_key_size, N) #avoid overflow
#            tagged = False
#            while (j > i):
#                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
#                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
#                if tag_with_lemmas:
#                    literal = expression_lemma
#                else:
#                    literal = expression_form
#                if literal in self.dictionary:
#                    #self.logger.debug("found: %s" % literal)
#                    is_single_token = j - i == 1
#                    original_position = i
#                    i = j
#                    taggings = [tag for tag in self.dictionary[literal]]
#                    tagged_expression = (expression_form, expression_lemma, taggings)
#                    if is_single_token: #if the tagged literal is a single token, conserve its previous taggings:
#                        original_token_tagging = sentence[original_position][2]
#                        tagged_expression[2].extend(original_token_tagging)
#                    tag_sentence.append(tagged_expression)
#                    tagged = True
#                else:
#                    j = j - 1
#            if not tagged:
#                tag_sentence.append(sentence[i])
#                i += 1
#        return tag_sentence

# ########################################################################################################################

contractions = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "couldn't've": "could not have",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hadn't've": "had not have",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'd've": "he would have",
  "he'll": "he will",
  "he'll've": "he will have",
  "he's": "he is",
  "how'd": "how did",
  "how'd'y": "how do you",
  "how'll": "how will",
  "how's": "how is",
  "I'd": "I would",
  "I'd've": "I would have",
  "I'll": "I will",
  "I'll've": "I will have",
  "I'm": "I am",
  "I've": "I have",
  "isn't": "is not",
  "it'd": "it had",
  "it'd've": "it would have",
  "it'll": "it will",
  "it'll've": "it will have",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "mightn't": "might not",
  "mightn't've": "might not have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "o'clock": "of the clock",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "shan't": "shall not",
  "sha'n't": "shall not",
  "shan't've": "shall not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "should've": "should have",
  "shouldn't": "should not",
  "shouldn't've": "should not have",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that'd've": "that would have",
  "that's": "that is",
  "there'd": "there had",
  "there'd've": "there would have",
  "there's": "there is",
  "they'd": "they would",
  "they'd've": "they would have",
  "they'll": "they will",
  "they'll've": "they will have",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'd've": "we would have",
  "we'll": "we will",
  "we'll've": "we will have",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what'll've": "what will have",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who'll've": "who will have",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "won't've": "will not have",
  "would've": "would have",
  "wouldn't": "would not",
  "wouldn't've": "would not have",
  "y'all": "you all",
  "y'alls": "you alls",
  "y'all'd": "you all would",
  "y'all'd've": "you all would have",
  "y'all're": "you all are",
  "y'all've": "you all have",
  "you'd": "you had",
  "you'd've": "you would have",
  "you'll": "you will",
  "you'll've": "you will have",
  "you're": "you are",
  "you've": "you have"
}



def expandContractions(tweets):
    c_re = re.compile('(%s)' % '|'.join(contractions.keys()))
    def replace(match):
        return contractions[match.group(0)]
    return c_re.sub(replace, tweets)


def main():
    if __name__ == '__main__':

        tweet1 = "This is the first example tweet. This tweet is an unhappy tweet. It contains some examples of sadness. Test contractions: can't, won't, wouldn't."
        tweet2 = "This is the second example tweet. This is a very happy tweet. It contains some examples of joyfullness."

        print("Raw example tweets: ")
        print(tweet1)  #Testing example tweets
        print(tweet2)
        print("\n\n")

        
        tweet1 = tweet1.lower()
        tweet2 = tweet2.lower()
        print("Tweets with all lowercase letters: ")
        print (tweet1)
        print (tweet2)
        print ("\n\n")


        tweet1 = expandContractions(tweet1)
        tweet2 = expandContractions(tweet2)
        print("Tweets with expanded contractions: ")
        print(tweet1)
        print(tweet2)
        print("\n\n")
        

        tags1 = tagger(tweet1)
        tags2 = tagger(tweet2)
        print("Tokenized Tweets: ")   #Tokenizing tweet2
        print(tags1)   #Testing tokenizer
        print(tags2)
        print("\n\n")


        ftags1 = StopWordsFilter(tags1)
        ftags2 = StopWordsFilter(tags2)
        print("Tweets with stop words romoved:")
        print(ftags1)
        print(ftags2)
        print("\n\n")


        tagged1 = POS_tagging(ftags1)
        tagged2 = POS_tagging(ftags2)
        print("Parts of speech tagged words: ")
        print(tagged1)
        print(tagged2)
        print("\n\n\n\n")



        


        #dictTagger = DictionaryTagger([ 'dicts/happy.yml', 'dicts/sad.yml'])

        #dictTagged = dictTagger.tag(tagged)

        
        #print("Dictionary-tagged tweets: ")
        #pprint(dictTagged)


main()