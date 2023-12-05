import os
import json
from auth import (twitter_consumer_key,
                  twitter_consumer_secret,
                  twitter_access_token,
                  twitter_access_token_secret)
import tweepy
MIN_DL = 749.908 #Mbps
MIN_UP = 673.175 #Mbps
CMD = "./speedtest --ca-certificate=./cacert.pem -f json"
PROVIDER = "@orange_es"

class InternetTwitterBot():
    def __init__(self):
        self.down = 0
        self.up = 0
        print("Performing test in background...")
        self.st = json.loads((os.popen(CMD).read()))
        self.dl_mbps = round(self.st["download"]["bandwidth"] * 8 / 1000000, 3)
        self.up_mbps = round(self.st["upload"]["bandwidth"] * 8 / 1000000, 3)
        self.url = self.st["result"]["url"]

    def get_internet_speed(self):
        print(f"Download speed: {self.dl_mbps} Mbps")
        print(f"Upload speed: {self.up_mbps} Mbps")

    def tweet_at_provider(self):
        """Send a tweet to the provider if not having the minimum speed.
        Otherwise, tweet to brag about your great Internet connection!"""

        client = tweepy.Client(consumer_key=twitter_consumer_key,
                               consumer_secret=twitter_consumer_secret,
                               access_token=twitter_access_token,
                               access_token_secret=twitter_access_token_secret)

        if self.dl_mbps < MIN_DL or self.up_mbps < MIN_UP:
            print("Minimum values not met:"
                  f"{MIN_DL} (down) / {MIN_UP} (up) (Mbps)")
            message = f"""
            ¡Hola {PROVIDER} !
            ¿Por qué cuando se garantizan {MIN_DL} (down) / {MIN_UP} (up)
            (Mbps), me sale este test?
            {self.url}
            """
        else:
            print("Speed according to contract minimum values: "
                  f"{MIN_DL} (down) / {MIN_UP} (up) (Mbps)")
            print("Sending dummy tweet")
            message = f"""
            Tengo garantizados {MIN_DL} (down) / {MIN_UP} (up) (Mbps). Mi test: {self.url}
            """

        client.create_tweet(text=message)
        print(f"Tweeted: {message}")

bot = InternetTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()
