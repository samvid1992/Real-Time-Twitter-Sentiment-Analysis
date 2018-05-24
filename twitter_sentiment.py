import re, csv, sys, os
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from nltk.corpus import stopwords
import matplotlib.pyplot as plt


class TwitterClient(object):

    def __init__(self):
        #keys and tokens from the twitter api
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''
        try:
            # creating object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        #function to remove links and special characters
         return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", '', tweet).split())

    def remove_urls(self, tweets):
        #remove urls
        return re.sub("http.?://[^\s]+[\s]?", '', tweets)

    def emotion_finder(self, sentence):
        stop = set(stopwords.words('english'))
        English_word_list = os.path.join('Word_List')
        # POS_WORDS_FILE = os.path.join(English_word_list, 'positive-words.txt')
        # NEG_WORDS_FILE = os.path.join(English_word_list, 'negative-words.txt')

        happy = ["contented", "content", "cheerful", "won",
                 "cheery", "joyful", "jovial","prompt",
                 "jolly", "joking", "gleeful","appreciated",
                 "carefree", "untroubled", "delighted",
                 "smiling", "beaming", "grinning", "glowing",
                 "satisfied", "gratified", "buoyant", "radiant","happiness", "great",
                 "gay", "joyous", "lucky", "fortunate", "overjoyed", "enjoy",
                  "important","special", "festive","safe," "ecstatic", "satisfied", "cheerful", "sunny", "merry",
                 "elated", "jubilant","excited","heroic","thank", "upgrade", "rocks", "excellent","wohoo","yay"]

        surprise = ["shock", "amaze", "amazing", "revelation", "eye-opener","pleasantly", "shocker","surprised", "upgrade"]

        sad = ["unhappy","lied","sorrowful", "dejected", "regretful", "depressed",
               "downcast", "miserable", "downhearted", "down", "despondent", "despairing",
                "gloomy", "funeral", "tearful", "pained", "grief",
               "desolate", "desperate", " pessimistic", "blocking","lonely", "grieved", "mournful", "dismayed"]

        angry = ["angry","bullied","stay away","hating","stolen","broken","late","rage", "annoyed", "cross", "vexed", "irritated", "exasperated", "irritate", "temper",
                 "indignant","aggrieved", "irked", "piqued", "displeased","delay" "provoked","canceled",
                 "galled", "resentful","weak", "furious", "enraged","needless", "infuriated","worst","lost","overbooked",
                 "lenghty", "raging", "incandescent","fail","hated","suck","delayed", "sucks","never", "horrbile", "terrible","messed","mess",
                 "wrathful","long","fatal","Ugh","restriction","broken","horrendous","miss","errors","loose","death","cant","annoy","last","down","fuming", "ranting", "annoying", "annoy", "frustrated"]


        list = [x for x in sentence.lower().split() if x not in stop]
        H =SU= S = A= 0
        for x in list:
            for y in happy:
                if (x == y):
                     H+= 1

            for y in surprise:
                if (x == y):
                    SU+= 1

            for y in sad:
                if (x == y):
                    S += 1

            for y in angry:
                if (x == y):
                    A += 1



        if (H> S and H > A and H > SU):
            print("the emotion of sentence is happy")
            print("\n")
        elif (S > H and S > A and S > SU):
            print("sad emotion")
            print("\n")
        elif (A > H and A > S and A > SU):
            print("angry emotion")
            print("\n")
        elif (SU> H and SU > S and SU > A):
            print("surprised")
            print("\n")


    def get_tweet_sentiment(self, tweet):
        #building sentiment extractor
        # Utility function to classify sentiment of passed tweet
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count):

        #function to fetch tweets and parse them.
        # empty list to store parsed tweets
        tweets = []

        try:
            # to fetch tweets call twitter api
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    print("\n\t===> Start-------------:\n")
    topic = ["DeltaAirlines", "UnitedAirlines", "Southwest Airlines", "FrontierAirlines", "AmericanAirline",
              "VirginAmerica","SpiritAirlines"]
    Postive_percentage = []
    Negative_percentage = []
    # calling function to get tweets
    positivelist = [0]
    for i in range(0, 7):

        tweets = api.get_tweets(topic[i], count=500)
        print("\t\t\t\t\tSTARTS HERE")
        print("Airline Name: "+topic[i])
        print(tweets)
        print("\n")



        # picking positive tweets and printing the percentage
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
        positive_tweet_percentage = 10 * len(ptweets) / len(tweets)
        Postive_percentage.append(positive_tweet_percentage)

        # picking negative tweets from tweets and printing the percentage
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
        negative_tweets_percentage = 100 * len(ntweets) / len(tweets)
        Negative_percentage.append(negative_tweets_percentage)

        #picking neutral tweets
        nutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']

        print("\n\nPositive tweets:")
        for tweet in ptweets[:]:
            psentence = api.remove_urls(tweet['text'])
            newpsentence = psentence.encode("utf-8", errors='ignore')
            print(newpsentence)
            print("\n")
            api.emotion_finder(psentence)
            print("\n\nNegative tweets:")

        for tweet in ntweets[:]:
            nsentence = api.remove_urls(tweet['text'])
            newnsentence = nsentence.encode("utf-8", errors='ignore')
            print(newnsentence)
            print("\n")
            api.emotion_finder(nsentence)

        for tweet in nutweets[:]:
            nusentence = api.remove_urls(tweet['text'])
            newnusentence = nusentence.encode("utf-8", errors='ignore')
            print(newnusentence)
            print("\n")
            api.emotion_finder(nusentence)
            print("\n\nNeutral tweets:")

    #plotting positive tweets pie chart
    plt.figure(1)
    positive_title = "Positive Tweets"
    sizes = list(Postive_percentage)
    labels = list(topic)
    print(labels)
    colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
    plt.pie(sizes, explode=None, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.title(positive_title)
    plt.legend()

    # plotting positive tweets pie chart
    plt.figure(2)
    Negative_title = "Negative Tweets"
    sizes = list(Negative_percentage)
    labels = list(topic)
    print(labels)
    colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
    plt.pie(sizes, explode=None, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.title(Negative_title)
    plt.legend()
    plt.tight_layout()

    plt.show()



if __name__ == '__main__':
    main()
