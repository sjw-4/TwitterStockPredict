import json as js
import os
import re
from enum import IntEnum

#Gloabl Vars
DATE_FORMAT = '%Y-%m-%d'    #format used for the date
TIME_FORMAT = '%H:%M:%S'    #format used for the time

class Categories(IntEnum):
    NOTHING = 0
    BUY = 1
    SELL = 2

DO_OUTPUT = False
stopwordList = 'stopwords.txt'
stopwords = []

def loadData(jsonPath):
    if DO_OUTPUT: print("Loading data: " + jsonPath)
    data = []
    if os.path.exists(jsonPath):
        with open(jsonPath, 'r') as jf:
            data = js.load(jf)
    return data

def saveData(jsonPath, data):
    if DO_OUTPUT: print("Saving data: " + jsonPath)
    with open(jsonPath, 'w') as jf:
        js.dump(data, jf)

def cleanTextCorpus( words):
        if stopwords == []:
            if DO_OUTPUT:
                print("Loading stopwords")
            f = open(stopwordList, 'r')
            lines = f.readlines()
            for line in lines:
                stopwords.append(line.strip())
        newWords = []
        regex = re.compile('[^a-zA-Z]')
        for word in words:
            wordF = word.strip().lower()
            wordF = regex.sub('', wordF)
            if len(wordF) > 2 and wordF not in stopwords:
                newWords.append(wordF)
        return newWords
