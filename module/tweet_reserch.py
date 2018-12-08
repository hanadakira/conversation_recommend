import json, twitter_config #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

def recommend_tweet(dic):
    CK = twitter_config.CONSUMER_KEY
    CS = twitter_config.CONSUMER_SECRET
    AT = twitter_config.ACCESS_TOKEN
    ATS = twitter_config.ACCESS_TOKEN_SECRET
    twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

    url = "https://api.twitter.com/1.1/search/tweets.json"  # REST APIの読み込み

    feelings = list(dic.keys())
    val = list(dic.values())
    i = val.index(max(val))
    feeling = feelings[i]

    if feeling == "sadness":
        feeling = "かなしい"
    elif feeling == "joy":
        feeling = "うれしい"
    elif feeling == "fear":
        feeling = "こわい"
    elif feeling == "disgust":
        feeling = "クソ"
    elif feeling == "anger":
        feeling = "げきおこ"

    params = {"q" : "クリスマス" + feeling, "lang" : "ja", "locale" : "ja", "result_type" : "popular", 'count' : 10}

    req = twitter.get(url, params = params)

    if req.status_code == 200:
        tweets = json.loads(req.text)
        tweet_url = []
        for tweet in tweets['statuses']:
            screen_name = tweet['user']['screen_name']
            id_num = tweet['id']
            tweet_url.append("https://twitter.com/" + screen_name + "/status/" + str(id_num))
    else:
        print("ERROR: %d" % req.status_code)

    #print(tweet_url)
    return tweet_url

'''
dic = {
        "sadness":0.32665,
        "joy":0.563273,
        "fear": 0.033387,
        "disgust": 0.022637,
        "anger": 0.041796
    }
'''
#recommend_tweet()
