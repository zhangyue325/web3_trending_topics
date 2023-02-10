import pandas as pd
import json
from datetime import timedelta, date
from keywords_ranking import convert_string_to_list


def short_the_trending_table():
    yesterday = date.today() + timedelta(days = -1)
    df = pd.read_csv(rf"trending_table\{yesterday}.csv")
    df = df[(df["slope"]>0.2) & (df["Occurrence"] > 2)]
    
    blacklist = ["教程", "veDAO", "2023", "Crypto", "概览", "加密", "比特", "笔记", "叙事", "探会","Web3", "减半", "窒息", "以太", "Hashed"]
    df = df[~df["keyword"].isin(blacklist)]
    return df.head(30)

def match_keywords_with_article():
    yesterday = date.today() + timedelta(days = -1)
    article_df = pd.read_csv(rf"articles\{yesterday}.csv")
    trending_df = short_the_trending_table()
    hot_kw = trending_df["keyword"].tolist()

    for i in list(range(len(article_df)))[::-1]:
        keyword_in_articles = convert_string_to_list(article_df.loc[i, "keywords"])
        for kw in keyword_in_articles:
            if kw in hot_kw:
                article_df.loc[i, "Occurrence"] = trending_df.loc[trending_df["keyword"] == kw, "Occurrence"].tolist()[0]
                article_df.loc[i, "slope"] = trending_df.loc[trending_df["keyword"] == kw, "slope"].tolist()[0]
                article_df.loc[i, "main_keyword"] = kw
    print(article_df)
    article_df = article_df.sort_values(by = ["slope", "Occurrence"], ascending=False)
    article_df = article_df[["source", "main_keyword", "slope", "Occurrence", "article_title", "keywords", "post_date", "url"]]
    article_df["Occurrence"] = article_df["Occurrence"].round(2)
    article_df["slope"] = article_df["slope"].round(2)

    article_df.to_csv(rf'trending_articles\{yesterday}.csv', index = False)



a = short_the_trending_table()
print(a)
