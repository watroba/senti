#!/usr/bin/env python

'''
Created on Mar 29, 2017

@author: Joseph
'''
import sys                                                                      #for system stuff
import time                                                                     #for wait() fn
import io   
from access import TwyAccess
import gui
import counties
import collections
from CleanAnalysis import (POS_tagging,StopWordsFilter,tagger,expandContractions)
from nltk.stem import WordNetLemmatizer                                         #Multiple options
from nltk.corpus import wordnet
from ratings import csvd
import csv
from logging import raiseExceptions
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
from nltk.app.wordnet_app import lemma_property

class worker (QObject):
   
    update_Label = pyqtSignal(str,'PyQt_PyObject','PyQt_PyObject')    
    
    def __init__(self, twya, lem, conv, Q = 'a OR e OR i OR o OR u',
                             radius= 5.02, unit='mi'):
        QThread.__init__(self)
        self.twya = twya
        self.Q = Q
        self.lem = lem
        self.conv = conv
        self.radius = radius
        self.unit = unit
        
        self.Vavg = 0
        self.Aavg = 0
        self.Davg = 0
        self.i = 0
    
    def _get_mood_per_county(self,GEO):
        Vavg, Aavg, Davg, i = 0,0,0,0
        
        results = self.twya.query(self.Q, GEO)
        for result in results['statuses']:
            tagged =(POS_tagging(StopWordsFilter(tagger(
                expandContractions(result['text'].lower())))))
            for tag in tagged:
                tag[0] = (self.lem.lemmatize(tag[0][0], pos=self.conv(tag[0][1])))
                if tag[0] in csvd:
                    V,A,D = csvd[tag[0]]
                    Vavg+=V
                    Aavg+=A
                    Davg+=D
                    i+=1
                    #print(i)
                    
        self.Vavg+=Vavg
        self.Aavg+=Aavg
        self.Davg+=Davg
        self.i+=i
        
        
        return Vavg/i,Aavg/i,Davg/i
        
    def run(self):
        while True:
            for key in counties.od:
                lat = counties.od[key][3]
                long = counties.od[key][4]
                GEO = str(lat)+','+str(long)+','+str(self.radius)+self.unit
                moodVal = self._get_mood_per_county(GEO)
                #print(moodVal[0])
                self.update_Label.emit(counties.od[key][0],moodVal,
                          (self.Vavg/self.i,self.Aavg/self.i,self.Davg/self.i))
                QThread.sleep(1)

class TSAprogram(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    twya = TwyAccess(2)
    def __init__(self, twya, lem, conv, Q, radius, unit):
        super(self.__class__, self).__init__()
        self.Q = Q
        self.lem = lem
        self.conv = conv
        self.radius = radius
        self.unit = unit
        
        self.setupUi(self)
        #self.keyPressEvent.connect(sys.exit())
        
        self.thread = QThread()
        self.w = worker(twya, lem, conv, Q, radius, unit)        
        self.w.update_Label.connect(self.setLabel)
        self.w.moveToThread(self.thread)
        self.thread.started.connect(self.w.run)
        
        self.thread.start()
    
    def moody(self,VAD,VAD_AVG):
        #print('moody')
        #return ":/Images/1f60c.relaxedsvg.png"
        v,a,d=VAD
        vc,ac,dc=VAD_AVG
        if(v>=vc):                                                              #positive emotion (high valence)
            if(a>=ac):                                                          #excited (high arousal)
                if(d>=dc):
                    return ":/Images/1f601exuberant.png"
                elif(d<dc):                                                     #"frequently seeks the sympathy, protection,love,advice,and reasuurance of other people
                    return ":/Images/1f605dependent.png"
            elif(a<ac):
                if(d>=dc):
                    return ":/Images/1f60c.relaxedsvg.png"
                elif(d<dc):
                    return ":/Images/1f610docile.png"
        elif(v<vc):
            if(a>=ac):
                if(d>=dc):
                    return ":/Images/1f621hostile.png"
                elif(d<dc):
                    return ":/Images/1f616anxious.png"
            elif(a<ac):
                if(d>=dc):
                    return ":/Images/1f61edisdainful.png"
                elif(d<dc):
                    return ":/Images/1f634bored.png"
        return 'ERROR'
    
    #@pyqtSlot(str,'PyQt_PyObject','PyQt_PyObject')
    def setLabel(self, name, moodVal,avgVal):
        for label in self.centralwidget.children():
            #print(name)
            #print(label.objectName())
            if label.objectName()==name:
                #print('made it inside')
                new = self.moody(moodVal,avgVal)
                #print(new)
                #label.setPixmap(self.moody(moodVal,avgVal))
                label.setPixmap(QtGui.QPixmap(new))
                #print('success')
                return

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
    
''' #find more info @ ftp://smtp.infomus.org/pub/BiologicalMotion/Survey-Karg/Mehrabian%20-%20Pleasure-Arousal.Dominance%20A%20General%20Framework%20for%20Describing%20and%20Measuring%20Individual%20Differences%20in%20Temperament.pdf
def moody(VAD,VAD_AVG):
    v,a,d=VAD
    vc,ac,dc=VAD_AVG
    
    if(v>=vc):                                                                  #positive emotion (high valence)
        if(a>=ac):                                                              #excited (high arousal)
            if(d>=dc):                                                          #in control (high dominance)
                #return 'exuberant'                                              #happy!
                #return 1 #(for signals/slots)
                return ":/Images/1f601exuberant.png"
            elif(d<dc):                                                         #not in control
                #return 'dependent'                                              #opposite of disdainful
                #return 2 #(s/s)                                                #"frequently seeks the sympathy, protection,love,advice,and reasuurance of other people
                return ":/Images/1f605dependent.png"
            else:
                return 'ERROR'
                #return 0 #(s/s)
        elif(a<ac):
            if(d>=dc):
                #return 'relaxed'
                #return 3 #(s/s)
                return ":/Images/1f60c.relaxedsvg.png"
            elif(d<dc):
                #return 'docile'
                #return 4 #(s/s)
                return ":/Images/1f610docile.png"
            else:
                return 'ERROR'
                #return 0 #(s/s)
        else:
            return 'ERROR'
            #return 0 #(s/s)
    elif(v<vc):
        if(a>=ac):
            if(d>=dc):
                #return 'hostile'
                #return 5 #(s/s)
                return ":/Images/1f621hostile.png"
            elif(d<dc):
                #return 'anxious'
                #return 6 #(s/s)
                return ":/Images/1f616anxious.png"
            else:
                return 'ERROR'
                #return 0  #(s/s)
        elif(a<ac):
            if(d>=dc):
                #return 'disdainful'                                             #shame, humiliation,
                #return 7 #(s/s)
                return ":/Images/1f61edisdainful.png"
            elif(d<dc):
                #return 'bored'
                #return 8 #(s/s)
                return ":/Images/1f634bored.png"
            else:
                return 'ERROR'
                #return 0 #(s/s)
        else:
            return 'ERROR'
            #return 0 #(s/s)
    else:
        return 'ERROR'
        #return 0  #(s/s)
'''    
def main():
    twya = TwyAccess(2)                                                         #TwyAccess class init
    lem = WordNetLemmatizer()                                                   #Lemmatizer class init
    radius = 5.02                                                               #avg radius of AR county
    unit = 'mi'                                                                 #unit of miles
    Q = 'a OR e OR i OR o OR u'
    #GEO = str(35.4406)+','+str(-93.0176)+','+str(radius)+unit
    
    app = QtWidgets.QApplication(sys.argv)
    form = TSAprogram(twya, lem, conv, Q, radius, unit)
    form.showFullScreen() 
    app.exec_()
    
if __name__ == '__main__':
    main()    
    
    