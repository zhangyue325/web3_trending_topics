import pandas as pd
import json
from datetime import timedelta, date
from keywords_ranking import convert_string_to_list


def short_the_trending_table(dt):
    df = pd.read_csv(rf"trending_table\{dt}.csv")
    df = df[(df["Occurrence"] > 1.1)]
    
    return df.head(30)


def match_keywords_with_article(dt):
    article_df = pd.read_csv(rf"articles\{dt}.csv")
    trending_df = short_the_trending_table(dt)
    hot_kw = trending_df["keyword"].tolist()

    article_df["Occurrence"] = 100
    for i in list(range(len(article_df))):
        keyword_in_articles = convert_string_to_list(article_df.loc[i, "keywords"])
        for kw in keyword_in_articles:
            if kw in hot_kw:
                if article_df.loc[i, "Occurrence"] > trending_df.loc[trending_df["keyword"] == kw, "Occurrence"].tolist()[0]:
                    article_df.loc[i, "Occurrence"] = trending_df.loc[trending_df["keyword"] == kw, "Occurrence"].tolist()[0]
                    article_df.loc[i, "slope"] = trending_df.loc[trending_df["keyword"] == kw, "slope"].tolist()[0]
                    article_df.loc[i, "main_keyword"] = kw
    print(article_df)
    article_df = article_df.sort_values(by = ["Occurrence", "main_keyword"], ascending=[False, False])
    article_df = article_df[["source", "main_keyword", "slope", "Occurrence", "article_title", "keywords", "post_date", "url"]]
    article_df["Occurrence"] = article_df["Occurrence"].round(2)
    article_df["slope"] = article_df["slope"].round(2)
    article_df["Occurrence"] = article_df["Occurrence"].replace(100, None)

    df1 = article_df[~article_df["Occurrence"].isna()]
    df2 = article_df[article_df["Occurrence"].isna()]
    df = pd.concat([df1, df2])

    df["article_title"] = df["article_title"].str.replace(" ", "")
    df = df.drop_duplicates(subset = ["article_title"], keep = "first")

    df.to_csv(rf'trending_articles\{dt}.csv', index = False)



if __name__ == "__main__":
    yesterday = date.today() + timedelta(days = -1)
    a = match_keywords_with_article(yesterday)
    print(a)