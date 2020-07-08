import stockHist as sh
import tweetHist as th
import utils

class CombinedData:
    def __init__(self, _username, _ticker):
        self.username = _username
        self.ticker = _ticker

        self.jsonPath = 'Data/CombinedData/' + self.username + '.json'

        #listOfData [{text, date, time, ticker, volumeRatio, startPrice, tenMinSD, nextHourDelta, oneHourPrice}, {}, ..., {}]
        self.listOfData = utils.loadData(self.jsonPath)
        if self.listOfData == []:
            self.tweets = th.TweetData(self.username).tweets
            self.__loadStockData()
            utils.saveData(self.jsonPath, self.listOfData)
    
    def __loadStockData(self):
        for tweet in self.tweets:
            stockData = sh.StockInfo(self.ticker, tweet['date'], tweet['time']).getData()
            if stockData != None:
                stockData['text'] = tweet['text']
                self.listOfData.append(stockData)
    
    def getData(self):
        return self.listOfData