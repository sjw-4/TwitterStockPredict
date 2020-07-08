import textClassifier as TxC
import tweetClassifier as TwC
import combinedData as CD

#for quick debug
#twitHandle = 'elonmusk'
#stockTick = 'tsla'

if __name__ == '__main__':
    uInput = 't'
    model = None
    while uInput != 'q':
        while uInput != 't' and uInput != 'p' and uInput != 'q':
            uInput = input("Train or predict or quit? (t/p/q): ")
        if uInput == 't':
            twitHandle = input("Enter twitter username: ")
            stockTick = input("Enter stock ticiker: ")
            data = CD.CombinedData(twitHandle, stockTick).getData()
            clasifData = TwC.TweetClassifier(data, twitHandle)
            model = TxC.TextClassifier(clasifData.classifiedTweets, twitHandle)
            print("Model trained")
            uInput = ''
        elif uInput == 'p' and model != None:
            newTweet = input("Enter tweet text: ")
            result = model.predict(newTweet)
            if result == 0: print("Do nothing")
            elif result == 1: print("Buy")
            elif result == 2: print("Sell")
            else: print("This should never appear")
            uInput = ''
            