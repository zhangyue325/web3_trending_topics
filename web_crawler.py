import requests
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
import csv
import jieba.analyse
import pandas as pd
from bs4 import BeautifulSoup
import time
import shutil


def get_keywords(para, topK = 3):
    keywords = jieba.analyse.extract_tags(para, topK, withWeight = True, allowPOS = ())
    return keywords

def get_blockbeats_article():
    url_prefix = "https://api.theblockbeats.info/v3/Information/newsall?page="
    page_id = 1
    while True:
        url = url_prefix + str(page_id)
        d = requests.get(url).json()["data"]
        for ele in d:
            title = ele["title"]
            source = ele["im_source"]
            article_id = ele["id"]
            article_url = "https://www.theblockbeats.info/news/" + str(article_id)
            post_date = datetime.utcfromtimestamp(ele["add_time"]) + timedelta(hours = 8)
            topic_title = ele["topic_title"]
            if datetime.date(post_date) == date.today():
                continue
            elif datetime.date(post_date) < date.today() - timedelta(days = 1):
                break
            else:
                with open(r'articles.csv', 'a', encoding='UTF8', newline='') as f:
                    print(title, post_date)
                    keywords = get_keywords(title, 3)
                    writer = csv.writer(f)
                    writer.writerow(["blockbeats", title, post_date, keywords, article_url])
        if datetime.date(post_date) < date.today() - timedelta(days = 1):
            break
        page_id += 1

def get_odaily_article():
    url = f"https://www.odaily.news/api/pp/api/app-front/feed-stream?feed_id=280&per_page=200"
    d = requests.get(url).json()["data"]["items"]
    for ele in d:
        if ele["entity_type"] != "post":
            continue
        title = ele["title"]
        article_id = ele["entity_id"]
        article_url = "https://www.odaily.news/post/" + str(article_id)
        post_date = datetime.strptime(ele["published_at"], '%Y-%m-%d %H:%M:%S')
        own_keywords = ele["secondary_tag"]
        if datetime.date(post_date) == date.today():
            continue
        elif datetime.date(post_date) < date.today() - timedelta(days = 1):
            break
        else:
            with open(r'articles.csv', 'a', encoding='UTF8', newline='') as f:
                print(title, post_date)
                keywords = get_keywords(title, 3)
                writer = csv.writer(f)
                writer.writerow(["odaily", title, post_date, keywords, article_url])


def foresightnews_get_title_and_date(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    article_title = soup.find_all("div", {"class": "topic-body-title"})
    article_title = str(article_title).split(">")[1].split("<")[0]

    post_date = soup.find_all("div", {"class": "topic-time"})
    post_date = str(post_date).split(">")[1].split("<")[0]
    post_date = datetime.strptime(post_date, '%Y-%m-%d %H:%M')
    return (article_title, post_date)

def get_foresightnews_article():
    df = pd.read_csv("websites_url_id.csv")
    n = len(df)
    web_id = df.loc[n-1,"foresightnews"] + 1
    url = "https://foresightnews.pro/article/detail/" + str(web_id)
    print(url)

    err = 0
    while True:
        if err >100:
            print("loop breaked")
            break
        try:
            url = "https://foresightnews.pro/article/detail/" + str(web_id)
            (article_title, post_date) = foresightnews_get_title_and_date(url)
            if post_date.date() == date.today():
                print("PASS:", post_date, article_title)
                web_id += 1
                err += 1
            elif post_date.date() < date.today() + timedelta(days = -1):
                print("PASS:", post_date, article_title)
                web_id += 1
                err += 1
            else:
                with open(r'articles.csv', 'a', encoding='UTF8', newline='') as f:
                    print(post_date, article_title)
                    keywords = get_keywords(article_title, 3)
                    writer = csv.writer(f)
                    writer.writerow(["foresightnews", article_title, post_date, keywords, url])
                web_id += 1
        except:
            print(f"{url}, invalid url")
            err += 1
            web_id += 1
    
    df = pd.read_csv(r"articles.csv")
    n = len(df)
    last_id = int(df.iloc[n-1, 4][-5:])
    with open("websites_url_id.csv", 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date.today()+ timedelta(days = -1), last_id])
        print("index updated succefully")

def get_panewslab_article():
    # dt = str(date.today()) + " 00:00:01"
    # dt = int(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timestamp())
    dt = int(datetime.today().timestamp())

    while True:
        url = f"https://www.panewslab.com/webapi/depth/list?LId=1&Rn=20&LastTime={dt}&TagId=&tw=0"

        d = requests.get(url).json()["data"]
        for ele in d:
            title = ele["title"]
            article_url = ele["share"]["url"]
            post_date = datetime.fromtimestamp(ele["publishTime"])
        
            if datetime.date(post_date) == date.today():
                continue
            elif datetime.date(post_date) < date.today() - timedelta(days = 1):
                break
            else:
                with open(r'articles.csv', 'a', encoding='UTF8', newline='') as f:
                    print(post_date, title)
                    keywords = get_keywords(title, 3)
                    writer = csv.writer(f)
                    writer.writerow(["panewslab", title, post_date, keywords, article_url])

        if datetime.date(post_date) < date.today() - timedelta(days = 1):
            break
        dt = int(post_date.timestamp())

def get_techflowpost_article():
    i = 1
    while True:
        url = f"https://data.techflowpost.com/api/pc/home/more?pageIndex={i}&pageSize=1"
        d = requests.get(url).json()["content"]

        for ele in d:
            title = ele["title"]
            post_date = ele["createTime"]
            article_url = "https://www.techflowpost.com/article/" + str(ele["id"])

        if datetime.date(datetime.strptime(post_date, "%Y-%m-%d %H:%M:%S")) == date.today():
            i+= 1
            continue
        elif datetime.date(datetime.strptime(post_date, "%Y-%m-%d %H:%M:%S")) < date.today() - timedelta(days = 1):
            break
        else:
            with open(r'articles.csv', 'a', encoding='UTF8', newline='') as f:
                print(post_date, title)
                keywords = get_keywords(title, 3)
                writer = csv.writer(f)
                writer.writerow(["techflowpost", title, post_date, keywords, article_url])
            i+= 1

def get_marsbit_article():
    dt = str(date.today()) + " 08:00:00" # GMT +0 timezone
    dt = int(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
    print(dt)

    while True:
        url = f"https://api.marsbit.co/info/news/shownews?currentPage=2&pageSize=15&channelId=0&refreshTime={dt}"
        d = requests.get(url).json()['obj']['inforList']

        for ele in d:
            post_date = int(str(ele['publishTime'])[:-3])
            post_date = datetime.utcfromtimestamp(post_date) + timedelta(hours=8)
            article_url = f"https://news.marsbit.cc/{ele['id']}.html"
            title = ele['title']


            if datetime.date(post_date) == date.today():
                print("PASS:", post_date, title, article_url)
            elif datetime.date(post_date) < date.today() - timedelta(days = 1):
                print("PASS:", post_date, title, article_url)
                break
            else:
                with open(r'articles.csv', 'a', encoding='UTF8', newline='') as f:
                    print(post_date, title, article_url)
                    keywords = get_keywords(title, 3)
                    writer = csv.writer(f)
                    writer.writerow(["marsbit", title, post_date, keywords, article_url])

        if datetime.date(post_date) < date.today() - timedelta(days = 1):
            break

        dt = str(ele['publishTime'] - 1000)


def get_data():
    get_blockbeats_article()
    get_odaily_article()
    get_foresightnews_article()
    get_panewslab_article()
    get_techflowpost_article()
    get_marsbit_article()

def move_article_csv():
    yesterday = date.today() + timedelta(days = -1)
    shutil.move("articles.csv", rf"articles\{yesterday}.csv")
    with open(r'articles.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["source","article_title","post_date","keywords","url"])


if __name__ == "__main__":
    get_foresightnews_article()
    # print(111)