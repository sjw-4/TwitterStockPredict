import combinedData
import kmeans
import utils

import numpy as np

#listOfData [{text, date, time, ticker, volumeRatio, startPrice, tenMinSD, nextHourDelta, oneHourPrice}, {}, ..., {}]

#starting vectors for train
trainingVec = [[-1] * 2 + [0] * 6, [1] * 8, [1] * 2 + [-1] * 6]     #Nothing(0), buy(1), sell(2)

class TweetClassifier:
    def __init__(self, listOfData, name=None):
        if name != None:
            self.filePath = "Data/TweetData/tc_" + name + ".json"
            self.classifiedTweets = utils.loadData(self.filePath)
        else:
            self.filePath = None
            self.classifiedTweets = []      #list of dictionaries containing 'text' and 'category'

        self.minMax = []
        self.k_means = None
        self.listOfData = listOfData

        if self.classifiedTweets == []:
            self.normalizedTweets = np.array(self.__normalizeTweetData(self.__createTweetsArray(listOfData)))
            self.__classifyTweets()
            if self.filePath != None:
                utils.saveData(self.filePath, self.classifiedTweets)

    def __createTweetsArray(self, listOfData):
        tweetsArray = []
        for tweet in listOfData:
            tweetArray = []
            tweetArray.append(tweet['volumeRatio'])
            tweetArray.append(tweet['tenMinSD'])
            tweetArray.append(tweet['nextHourDelta'][0])
            tweetArray.append(tweet['nextHourDelta'][1])
            tweetArray.append(tweet['nextHourDelta'][2])
            tweetArray.append(tweet['nextHourDelta'][3])
            tweetArray.append(tweet['nextHourDelta'][4])
            tweetArray.append(tweet['nextHourDelta'][5])
            tweetsArray.append(tweetArray)
        return tweetsArray

    def __normalizeTweetData(self, tweetsArray):
        #find min and max values in tweetsArray
        self.minMax = [(100000,-100000)] * len(tweetsArray[0])
        for tweet in tweetsArray:
            for i in range(len(tweet)):
                if tweet[i] > self.minMax[i][1]:
                    self.minMax[i] = (self.minMax[i][0], tweet[i])
                if tweet[i] < self.minMax[i][0]:
                    self.minMax[i] = (tweet[i], self.minMax[i][1])
        
        #normalize tweetsArray
        normalizedTweets = []
        for tweet in tweetsArray:
            normalizedTweet = []
            for i in range(len(tweet)):
                normalizedTweet.append(2 * (tweet[i] - self.minMax[i][0]) / (self.minMax[i][1] - self.minMax[i][0]) - 1)
            normalizedTweets.append(normalizedTweet)
        return normalizedTweets

    def __classifyTweets(self):
        self.k_means = kmeans.KMeans(self.normalizedTweets, _n_clusters=3, _maxIters=40)
        self.k_means.train(trainingVec)
        print(self.k_means.printCentroids())

        for i in range(len(self.normalizedTweets)):
            newTweet = {}
            newTweet['text'] = self.listOfData[i]['text']
            newTweet['category'] = self.k_means.predict(self.normalizedTweets[i])
            self.classifiedTweets.append(newTweet)