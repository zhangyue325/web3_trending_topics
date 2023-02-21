from bs4 import BeautifulSoup
import requests
import pandas as pd
from markdownify import markdownify as md
from datetime import timedelta, date
import os 
import shutil


def add_article_md_foresightnews(url):
    article_md = ""
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for data in soup.findAll('div',{'class':'detail-body ql-editor'}):
        break

    print("get article md foresightnews")
    for ele in data:
        ele = str(ele)
        if ele == "<p><br/></p>" or ele.startswith("<blockquote>") or ele.startswith("<p><strong>"):
            continue

        try:
            ele = md(ele)
            article_md += ele
        except:
            pass
    return article_md


def add_all_articles_md(dt):
    shutil.rmtree('full_articles')
    os.mkdir('full_articles')

    df = pd.read_csv(rf"trending_articles\{dt}.csv")
    n = len(df)

    for i in range(n):
        if df.loc[i, "source"] == "foresightnews":
            url = df.loc[i, "url"]
            article_md = add_article_md_foresightnews(url)
            # df.loc[i, "article"] = article_md

            with open(rf"full_articles\{i}.txt", "w+", encoding="utf-8") as f:
                f.write(article_md)

    df.to_csv(rf"trending_articles\{dt}.csv", index = False)



if __name__ == "__main__":
    yesterday = date.today() + timedelta(days = -1)
    add_all_articles_md(yesterday)
