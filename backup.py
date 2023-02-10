import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import pandas as pd
import csv
import jieba.analyse

def techflowpost_get_title_and_date(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    article_title = soup.find_all("div", {"class": "articleTitle___3B-E_"})
    article_title = str(article_title).split(">")[1].split("<")[0]

    post_date = soup.find_all("div", {"class": "articlePubDate___1aR28"})
    post_date = str(post_date).split(">")[1].split("<")[0]
    post_date = datetime.strptime(post_date, '%Y.%m.%d %H:%M:%S')
    return (article_title, post_date)

def foresightnews_get_title_and_date(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    article_title = soup.find_all("div", {"class": "topic-body-title"})
    article_title = str(article_title).split(">")[1].split("<")[0]

    post_date = soup.find_all("div", {"class": "topic-time"})
    post_date = str(post_date).split(">")[1].split("<")[0]
    post_date = datetime.strptime(post_date, '%Y-%m-%d %H:%M')
    return (article_title, post_date)

def get_keywords(para, topK = 3):
    keywords = jieba.analyse.extract_tags(para, topK, withWeight = True, allowPOS = ())
    return keywords

def get_url_id(website):
    df = pd.read_csv("get_article_links\websites_url_id.csv")
    n = len(df)
    return df.loc[n-1,website]

def get_url_prefix(website):
    df = pd.read_csv("get_article_links\websites_url_prefix.csv")
    return df.loc[0, website]

def pull_data(website):
    web_id = get_url_id(website) + 1
    while True:
        try:
            url = get_url_prefix(website) + str(web_id)
            if website == "foresightnews":
                (article_title, post_date) = foresightnews_get_title_and_date(url)
            elif website == "foresightnews":
                (article_title, post_date) = techflowpost_get_title_and_date(url)


            if post_date.date() == date.today():
                print(f"all the articles at {website} in yesterday has been pulled")
                # break
                web_id += 1
            elif post_date.date() < date.today() + timedelta(days = -1):
                print(article_title, post_date)
                print("pass")
                web_id += 1
            else:
                with open(r'get_article_links\articles1.csv', 'a', encoding='UTF8', newline='') as f:
                    print(article_title, post_date)
                    keywords = get_keywords(article_title, 3)
                    writer = csv.writer(f)
                    writer.writerow([website, article_title, post_date, keywords, url])
                web_id += 1
        except:
            print(f"{url}, something wrong, {website} may have not post any article")
            web_id += 1
            pass
        
pull_data("foresightnews")