#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_search_results():
  keyword = "クリスマス 話題"
  html_doc = requests.get('https://www.google.co.jp/search?num=10&q=' +keyword).text
  soup = BeautifulSoup(html_doc, 'html.parser') # BeautifulSoupの初期化
  tags = soup.find_all('h3',{'class':'r'})
  titles = [];urls = []
  for tag in tags:
    titles.append(tag.text)
    urls.append(query_string_remove(tag.select("a")[0].get("href").replace("/url?q=","")))
  print([titles,urls])
  return [titles, urls]

def query_string_remove(url):
  return url[:url.find('&')]

#keyword = "クリスマス 話題"
#data = get_search_results()
