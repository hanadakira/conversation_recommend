import json#標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions, KeywordsOptions, EntitiesOptions
#from watson_developer_cloud import ToneAnalyzerV3
#from googletrans import Translator


class NaturalLanguageUnderstanding():
    def __init__(self):
        #インスタンス生成
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2018-12-09',
            iam_apikey={},
            url={}
        )
    def analyze_sentence(self, sentence:str):
        """
        sentence: 会話文
        return: list
        """
        result = []
        print(sentence)
        #文字列から感情分析
        response = self.natural_language_understanding.analyze(
            text=sentence,
            #text= 'I like dog, but i don\'t ,nooooooooooooooooooooooo',
            features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=10))).get_result()

        for sentiment in response["keywords"]:
            senti_dict = {
                "keyword":sentiment["text"],
                "label": sentiment["sentiment"]["label"]
            }
            result.append(senti_dict)

        print(result)
        return result

'''
class ToneAnalyzer():
    def __init__(self):
        #インスタンス生成
        self.tone_analyzer = ToneAnalyzerV3(
            version='2018-12-09',
            iam_apikey='L894FkIfgeauSmiTlEvBqgrVg25QZfpWOnsN49pPgnRL',
            url='https://gateway.watsonplatform.net/tone-analyzer/api'
        )
    def analyze_sentence(self, sentence, content_type="text/plain;charset=utf-8"):
    #def analyze_sentence(self, sentence):
        #翻訳
        print("---")
        print(sentence)
        print("---")
        #sentence = "【 #ランチタイムベストアンサー】 世間で話題になってることをトークレゼントを何にするか… https://t.co/RaL1EoPEgl"
        translator = Translator()
        try:
            print("翻訳開始")
            text_en = translator.translate(sentence, dest='en')
            print(text_en)
            text_data = text_en.text
        except:
            print("やばい")
            sentence = "【 #ランチタイムベストアンサー】 世間で話題になってることをトークレゼントを何にするか… https://t.co/RaL1EoPEgl"
            text_en = translator.translate(sentence, dest='en')
            print(text_en)
            text_data = text_en.text
        #文字列から感情分析
        response = self.tone_analyzer.tone(tone_input=text_data, content_type=content_type)
        #response = self.tone_analyzer.tone(tone_input=sentence)
        #print(response)
        response = response.result["document_tone"]["tones"][0]
        score = response["score"]
        tone_name = response["tone_name"]
        result = [score, tone_name]
        return result
'''

class recommend_tweet():
    def __init__(self):
        CK = {}
        CS = {}
        AT = {}
        ATS = {}
        self.twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

    def select_tweet(self, info):
        #analyze = ToneAnalyzer()        # 感情分析のAPIを呼び出す
        analyze = NaturalLanguageUnderstanding()        # 自然言語処理のAPIを呼び出す

        url = "https://api.twitter.com/1.1/search/tweets.json"  # REST APIの読み込み

        #feelings = list(dic.keys())
        #val = list(dic.values())
        #i = val.index(max(val))
        feeling = info["label"]
        kw = info["keyword"]
        '''
        if feeling == "negative":
            add_key = "クソ"
        elif feeling == "positive":
            add_key = "たのしみ"
        '''

        #params = {"q" : "クリスマス 話題" + " min_faves:100", "lang" : "ja", "locale" : "ja", "result_type" : "popular", 'count' : 30}
        params = {"q" : "クリスマス" + kw, "lang" : "ja", "locale" : "ja", "result_type" : "popular", 'count' : 100}

        req = self.twitter.get(url, params = params)

        if req.status_code == 200:
            tweets = json.loads(req.text)
            tweet_url = [];id_n = [];text_data = []
            for tweet in tweets['statuses']:
                screen_name = tweet['user']['screen_name']
                id_num = tweet['id']
                text = tweet['text']
                #print(text)

                result = analyze.analyze_sentence(text) # watson APIでtweet内容を解析
                cnt = 0
                for label in result[0].values():
                    if label == feeling:
                        cnt += 1

                if cnt:
                    tweet_url.append("https://twitter.com/" + screen_name + "/status/" + str(id_num))
        else:
            print("ERROR: %d" % req.status_code)

        #print(tweet_url)
        return tweet_url

#analyze = ToneAnalyzer()

#text = "Yay! I bought an Android phone!"
#dic = analyze.analyze_sentence(text)

#feelings = [[0.835268, "Joy"], [0.235268, "Sad"]]
info = [
    {
        "keyword" : "犬",
        "label" : "negative"
    },
    {
        "keyword" : "ねこ",
        "label" : "pogitive"
    }
]

twitter = recommend_tweet()
tweet = twitter.select_tweet(info[0])
