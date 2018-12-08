#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_search_results_df(keyword):
  columns = ['rank','title','url']
  df = pd.DataFrame(columns=columns)
  html_doc = requests.get('https://www.google.co.jp/search?num=10&q=' +keyword).text
  soup = BeautifulSoup(html_doc, 'html.parser') # BeautifulSoupの初期化
  tags = soup.find_all('h3',{'class':'r'})
  rank = 1
  for tag in tags:
    title = tag.text
    #print(title)
    url = query_string_remove(tag.select("a")[0].get("href").replace("/url?q=",""))
    se = pd.Series([rank, title, url], columns)
    df = df.append(se, ignore_index=True)
    rank += 1
  return df

def query_string_remove(url):
  return url[:url.find('&')]

keyword = "クリスマス"
search_results_df = get_search_results_df(keyword)
csv_data = search_results_df.to_csv("Christmas_data.csv", encoding="utf-8_sig")