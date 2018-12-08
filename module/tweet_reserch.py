import json, twitter_config #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

CK = twitter_config.CONSUMER_KEY
CS = twitter_config.CONSUMER_SECRET
AT = twitter_config.ACCESS_TOKEN
ATS = twitter_config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

url = "https://api.twitter.com/1.1/search/tweets.json"

params = {'q' : 'クリスマス', 'count' : 10}

req = twitter.get(url, params = params)

if req.status_code == 200:
    tweets = json.loads(req.text)
    for tweet in tweets['statuses']:
        print('name: ' + tweet['user']['name'])
        print('text: ' + tweet['text'])
        print('created_at: ' + tweet['created_at'])
        print('----------------------------------------------------')
else:
    print("ERROR: %d" % req.status_code)