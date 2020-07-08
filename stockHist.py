import utils

import yfinance as yf
import pandas as pd
import datetime as dt
import statistics as st

#To run----------------------------------------------------------------------------------------------------------------------------------------------
    #newObject = StockInfo(ticker, YYYY-MM-DD, HH:MM:00)            ex. StockInfo('tsla', '2020-05-12', '13:17:00')
    #newDict = newObject.getData()                                  check if returned value is None, if so, there was an error

#GLOBAL VARIABLES------------------------------------------------------------------------------------------------------------------------------------
TIME_TOCHECK = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60]  #which minutes to get data from

#StockInfo Class-------------------------------------------------------------------------------------------------------------------------------------
class StockInfo:
    def __init__(self, _ticker, _date, _time):
        self.ticker = _ticker
        self.date = _date
        self.time = _time[:-2] + '00'

        #verify that the given input is valid
        if not (self.__validStockTicker() and self.__validDate() and self.__validTime()):
            print("Failed to create object " + _ticker + ", " + _date + ", " + _time)
            return None

        #stock history with relevant table values for one hour after given time
        self.relData = None
        #average volume for the day
        self.avgVolume = 0

        #ratio of trade volume for 10 minutes after time to avg for the day
        self.volumeRatio = 0
        #price of the stock at the start time
        self.startPrice = None
        #TODO value to represent stock change over first 10 minutes, TBD - currently 
        self.tenMinSD = None
        #stock price delta after 10, 20, 30... 60 minutes
        self.nextHourDelta = []
        #stock price after 1 hour
        self.oneHourPrice = None

        #generate previous variables
        if self.__getBaseInfo():
            self.__getMainInfo()

    def __validStockTicker(self):
        try:
            yf.Ticker(self.ticker)
            return True
        except:
            return False

    def __validDate(self):
        try:
            if (
                self.date == dt.datetime.strptime(self.date, utils.DATE_FORMAT).strftime(utils.DATE_FORMAT)
                and dt.datetime.strptime(self.date, utils.DATE_FORMAT).weekday() < 5
            ): return True
            else: return False
        except:
            return False
    
    def __validTime(self):
        try:
            if (
                self.time == dt.datetime.strptime(self.time, utils.TIME_FORMAT).strftime(utils.TIME_FORMAT)
                and dt.datetime.strptime(self.time, utils.TIME_FORMAT) <= dt.datetime.strptime('15:00:00', utils.TIME_FORMAT)
                and dt.datetime.strptime(self.time, utils.TIME_FORMAT) > dt.datetime.strptime('09:30:00', utils.TIME_FORMAT)
            ): return True
            else: return False
        except:
            return False

    def __validateData(self):
        try:
            if (
                self.avgVolume == 0
                or self.volumeRatio == 0
                or self.startPrice == None
                or self.tenMinSD == None
                or len(self.nextHourDelta) == 0
                or self.oneHourPrice == None
            ): return False
            else:
                return True
        except:
            return False

    #get relData and avgVolume
    def __getBaseInfo(self):
        try:
            #get table
            nextDay = dt.datetime.strptime(self.date, utils.DATE_FORMAT) + dt.timedelta(days=1)        
            data = yf.download(tickers=self.ticker, interval='1m', prepost=True, start=self.date, end=nextDay)
            #get average price for the stock every minute, and average volume
            avgPrice = []
            numTradeMin = 0
            for index, row in data.iterrows():
                #get average price
                avg = (float(row['High']) + float(row['Low'])) / 2
                avgPrice.append(avg)
                #get average volume
                if row['Volume'] > 0:
                    numTradeMin += 1
                    self.avgVolume += row['Volume']
            #calc avg volume
            self.avgVolume /= numTradeMin
            #remove unnecessary rows
            reducedData = pd.DataFrame(data=data, columns=['Open', 'Volume'])
            #add average price column
            reducedData['Average'] = avgPrice
            #get appropriate rows
            time = dt.datetime.strftime(dt.datetime.strptime(self.time, utils.TIME_FORMAT) + dt.timedelta(hours=1), utils.TIME_FORMAT)
            self.relData = reducedData.loc[self.date + " " + self.time : self.date + " " + time]
            return True
        except:
            print("Unknown error in getBaseInfo")
            return False

    #get rest of values
    def __getMainInfo(self):
        if len(self.relData.index) != 61:
            print("Error in length of relData, len=" + str(len(self.relData)))
            return
        self.startPrice = self.relData.iloc[0]['Open']
        self.nextHourDelta.append(100 * (self.relData.iloc[10]['Average'] - self.startPrice) / self.startPrice)
        first10Min = []
        for i in TIME_TOCHECK:
            curRow = self.relData.iloc[i]
            if i <= 10:
                #get vals volumeRatio
                self.volumeRatio += (curRow['Volume']) / 10
                #get vals for tenMinChange
                first10Min.append(curRow['Average'])
            else:
                self.nextHourDelta.append(100 * (self.relData.iloc[i]['Average'] - self.startPrice) / self.startPrice)
        #set volumeRatio
        self.volumeRatio /= self.avgVolume
        #set tenMinChange
        self.tenMinSD = st.stdev(first10Min) * 100 / self.startPrice
        #set oneHourPrice
        self.oneHourPrice = self.relData.iloc[60]['Average']

    #return data in a dictionary
    def getData(self):
        #validate that all variables were set properly
        if not self.__validateData():
            print("Error validating data")
            return None

        data = {}
        data['ticker'] = self.ticker
        data['date'] = self.date
        data['time'] = self.time
        data['volumeRatio'] = self.volumeRatio
        data['startPrice'] = self.startPrice
        data['tenMinSD'] = self.tenMinSD
        data['nextHourDelta'] = self.nextHourDelta
        data['oneHourPrice'] = self.oneHourPrice
        return data
