from bs4 import BeautifulSoup
from datetime import datetime
import requests
from typing import List
from fastapi import FastAPI
import re
import json
import uvicorn

# create a const base url
BASE_URL = "https://www.hellenictrain.gr"
app = FastAPI()

class ArticlePreview:
    def __init__(self, title: str, url: str, preview: str, id: int):
        self.title = title
        self.url = url
        self.preview = preview
        self.id = id

class Article:
    def __init__(self, baseArticle : ArticlePreview,content: str):
        self.title = baseArticle.title.strip(" \n\t\r")
        self.url = baseArticle.url
        self.content = content.strip(" \n\t\r")
        self.id = baseArticle.id
        self.date = extractTimestamp(baseArticle.title)
    def to_json(self):
        return json.dumps(self.__dict__)

def getUrls(page: int = 0,english : bool = False) -> List[ArticlePreview]:
    news_subpath = "/anakoinoseis-ht" if (not english) else "/en/announcements"
    url = BASE_URL + news_subpath + ("?page=" + str(page) if page > 0 else "")
    doc = requests.get(url)
    soup = BeautifulSoup(doc.text, 'html.parser')
    articles = soup.find_all('article')
    result = []
    for article in articles:
        firstChild = article.find()
        if firstChild and firstChild.get('class') == ['node--news--teaser']:
            article_url = BASE_URL + article.get('about')
            title = article.find(class_='news-title').text if article.find(class_='news-title') else "No title"
            content = article.find(class_='news-body').text if article.find(class_='news-body') else "No preview"
            id = int(article.get('data-history-node-id'))
            result.append(ArticlePreview(title, article_url, content, id))
    return result

def extractTimestamp(title: str) -> int:
    match = re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{4}', title)
    if match:
        date = match.group()
        return toTimestamp(date)
    else:
        print("No date found")
        return None

def toTimestamp(date: str) -> int:
    date_str = date.replace('-', '/')
    date = datetime.strptime(date_str, '%d/%m/%Y')
    return int(date.timestamp())

def extractArticle(preview: ArticlePreview) -> Article:
    doc = requests.get(preview.url)
    soup = BeautifulSoup(doc.text, 'html.parser')
    content = soup.find(class_='news-body').text if soup.find(class_='news-body') else ""
    return Article(preview, content)

# get the latest article
@app.get("/latest")
async def get_articles(en: bool = False):
    return extractArticle((getUrls(english=en)[0]))

# get the latest page of articles
@app.get("/")
async def get_articles(page: int = 0, en: bool = False):
    urls = getUrls(page, en)
    articles = []
    for url in urls:
        articles.append(extractArticle(url))
    return articles

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)