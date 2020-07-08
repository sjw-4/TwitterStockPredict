#TODO actually implement

import utils

from dotenv import load_dotenv
import os
import tweepy as tw
import string
import datetime as dt

#GLOBAL VARIABLES------------------------------------------------------------------------------------------------------------------------------------
load_dotenv()
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
access_key = os.getenv('ACCESS_KEY')
access_secret = os.getenv('ACCESS_SECRET')

#TweetData Class-------------------------------------------------------------------------------------------------------------------------------------
class TweetData:
    def __init__(self, _username):
        self.username = _username
        self.jsonPath = "Data/TweetData/" + self.username + ".json"
        self.tweets = utils.loadData(self.jsonPath)      #tweet = {text, date, time}

        if self.tweets == []:
            auth = tw.OAuthHandler(api_key, api_secret)
            auth.set_access_token(access_key, access_secret)
            self.api = tw.API(auth)
            self.__getTweets()
            utils.saveData(self.jsonPath, self.tweets)
    
    def __splitDate(self, dateTime):
        dtSplit = dateTime.split(' ')
        time = dt.datetime.strptime(dtSplit[1], utils.TIME_FORMAT) - dt.timedelta(hours=4)
        result = {'date': dtSplit[0], 'time': dt.datetime.strftime(time, utils.TIME_FORMAT)}
        return result

    def __getTweets(self):
        for tweet in tw.Cursor(self.api.user_timeline, id=self.username).items():
            newTweet = self.__splitDate(str(tweet.created_at))
            newTweet['text'] = tweet.text
            if not newTweet['text'].startswith('RT'):
                self.tweets.append(newTweet)