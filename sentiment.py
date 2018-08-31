import csv
import pytz
import re
from textblob import TextBlob
import tweepy
from unidecode import unidecode

# import sys
#
# reload(sys)
# sys.setdefaultencoding('utf8')

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key = "yILM5E8L2NHNIWomphvEXsvuv"
consumer_secret = "kYXgT9atlJxijVJie1aqfIXop27gpOvjbAFqj0o0HyrT287pN3"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token = "723745583463161857-FnZwzT3UeoV62pE6hSC6DFVNXe5myq0"
access_token_secret = "WaBB3UWtcwAzWg8Dxqxob4Otxjtef6yVN7aGMKvlWdxBc"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


def change_time_zone(utc_dt):
    local_tz = pytz.timezone('America/Vancouver')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


def clean_tweet(tweet):
    """
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    """
    return ' '.join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", unidecode(tweet)).split())


def get_tweet_sentiment(tweet_text):
    """
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    """
    # create TextBlob object of passed tweet text
    analysis = TextBlob(tweet_text)
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def format_tweet(tweet):
    cleaned_tweet = clean_tweet(tweet.text)

    return [change_time_zone(tweet.created_at),
            change_time_zone(tweet.created_at).hour,
            get_tweet_sentiment(cleaned_tweet),
            tweet.user.id,
            tweet.user.lang,
            clean_tweet(tweet.user.location) if tweet.user.location else "none",
            cleaned_tweet]


def save_twitter(filename):
    api = tweepy.API(auth)
    csv_file = open(filename, 'a')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["datetime,hour,sentiment,user_id,user_lang,user_location,tweet"])
    for tweet in tweepy.Cursor(api.search,
                               q="#OSSummit",
                               count=100,
                               since="2018-08-30").items():
        result = format_tweet(tweet)
        print(result)
        csv_writer.writerow(result)


if __name__ == "__main__":
    save_twitter("tweets_sentiment.csv")
