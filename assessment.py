
from twython import TwythonStreamer
import csv
import json


credentials = {}
with open("credentials.json", "r") as file:
    credentials = json.load(file)

def process_tweet(tweet):
    d = {}
    d["hashtags"] = [hashtag["text"] for hashtag in tweet["entities"]["hashtags"]]
    d["text"] = tweet["text"]
    d["user"] = tweet["user"]["screen_name"]
    d["user_loc"] = tweet["user"]["location"]
    return d

    
class MyStreamer(TwythonStreamer):

    def on_success(self, data):

        if data["lang"] == "en":
            tweet_data = process_tweet(data)
            self.save_to_csv(tweet_data)
            self.disconnect()

    def save_to_csv(self, tweet):
        with open(r'live_saved_tweets.csv', "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(list(tweet.values()))

    # def on_error(self, status_code, data,**kargs):
    #     print(status_code,data)
    #     self.disconnect()




stream = MyStreamer(credentials["API_KEY"], credentials["API_SECRET"], credentials["ACCESS_TOKEN"], credentials["ACCESS_TOKEN_SECRET"])


stream.statuses.filter(track="twitter")

