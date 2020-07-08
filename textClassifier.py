import utils

import math
import operator

#NOTE: Lines 13-20 and 34 have been commented out due to issues loading saved
#       training data

class TextClassifier:
    def __init__(self, _trainingData, _name=None):
        self.trainingData = _trainingData
        self.filePath = "Data/NB_" + _name + ".json"

        #if _name != None and utils.loadData(self.filePath) != []:
        #    tempData = utils.loadData(self.filePath)
        #    self.n_doc_total = tempData[0]
        #    self.n_doc = tempData[1]
        #    self.freq = tempData[2]
        #    self.wordCount = tempData[3]
        #    self.uWords = tempData[4]
        #else:
        #total number of documents in the training set
        self.n_doc_total = 0
        #total number of documents in each category
        self.n_doc = {c: 0  for c in utils.Categories}
        #frequency of words in each category
        self.freq = {c: {} for c in utils.Categories}
        #total word count in each category
        self.wordCount = {c: 0 for c in utils.Categories}
        #total number of unique words
        self.uWords = 0
        self.__train()
        if self.filePath != None:
            tempData = [self.n_doc_total, self.n_doc, self.freq, self.wordCount, self.uWords]
            #utils.saveData(self.filePath, tempData)                    
        
    #parses training documents to generate and save trained data
    def __train(self):
        uniqueWordsDict = {}
        for doc in self.trainingData:
            curCat = doc["category"]
            self.n_doc_total += 1
            self.n_doc[curCat] += 1
            cleanDoc = utils.cleanTextCorpus(doc["text"].lower().split())
            for word in cleanDoc:
                if word not in self.freq[curCat]:
                    self.freq[curCat][word] = 0
                self.freq[curCat][word] += 1
                self.wordCount[curCat] += 1
                uniqueWordsDict[word] = 1
        self.uWords = len(uniqueWordsDict)
    
    #predict
    def predict(self, pDoc):
        #holds all the words in a document
        xWords = pDoc.lower().split()
        xWords = utils.cleanTextCorpus(xWords)

        #create dictionary to hold final nbPredictions
        nbProb = {c: 0.0 for c in utils.Categories}

        #create dictionary and calculate prior probabilities
        prior = {c: 0.0 for c in utils.Categories}
        for c in utils.Categories:
            prior[c] = self.n_doc[c] / self.n_doc_total

        #create dictionary to hold likelihoods and calculate
        likelihood = {c: 0.0 for c in utils.Categories}
        posteriori = {c: 0.0 for c in utils.Categories}
        for c in utils.Categories:
            for xWord in xWords:
                countWC = 1
                if xWord in self.freq[c]:
                    countWC += self.freq[c][xWord]
                likelihood[c] += math.log(countWC / (self.wordCount[c] + self.uWords + 1))
            posteriori[c] = likelihood[c] + math.log(prior[c])

        return max(posteriori.items(), key=operator.itemgetter(1))[0]