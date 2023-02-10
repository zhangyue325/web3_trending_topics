import pandas as pd
import json
from datetime import timedelta, date
from scipy import stats

def convert_string_to_list(list_like_string):
    data = list_like_string[1:-1].split("), (")
    if len(data) in (2, 3):
        data[0] = data[0][1:]
        data[-1] = data[-1][:-1]
        res = []
    else:
        print("keyword len is not 2 or 3")
    for ele in data:
        keyword = ele.split(",")[0][1:-1]
        res.append(keyword)
    return res

def get_topics_hash(date):
    hash = {}
    df = pd.read_csv(rf"get_article_links\articles\{date}.csv")
    n = len(df)

    for i in range(n):
        data = df.loc[i, "keywords"]
        kw = convert_string_to_list(data)
        for ele in kw:
            if ele in hash:
                hash[ele] += 1
            else:
                hash[ele] = 1
    with open(rf"get_article_links\topics\{date}.json", "w") as fp:
        json.dump(hash, fp) 
    return hash


def get_occurance_for_topics():
    dt = date.today() - timedelta(days = 1)
    with open(rf"get_article_links\topics\{dt}.json") as json_file:
        data = json.load(json_file)
    df = pd.DataFrame()

    article_df = pd.read_csv(rf"get_article_links\articles\{dt}.csv")
    article_len = len(article_df)

    for k, v in data.items():
        if v > 2:
            to_df = {"keyword":k, "Occurrence": v/article_len*100, dt: v/article_len*100}
            to_df = pd.DataFrame([to_df])
            df = pd.concat([df, to_df], ignore_index=True)
    return df
    

def get_historical_data_for_topics():
    df = get_occurance_for_topics()
    for delta in range(2, 8):
        dt = date.today() - timedelta(days = delta)
        with open(rf"get_article_links\topics\{dt}.json") as json_file:
            data = json.load(json_file)
        
        article_df = pd.read_csv(rf"get_article_links\articles\{dt}.csv")
        article_len = len(article_df)

        for kwd in df["keyword"].tolist():
            if kwd in data:
                df.loc[df["keyword"] == kwd, dt] = data[kwd] / article_len * 100
            else:
                df.loc[df["keyword"] == kwd, dt] = 0
    return df


def get_slope():
    df = get_historical_data_for_topics()

    for i in range(len(df)):
        y = df.iloc[i, 2:9].tolist()[::-1]
        X = list(range(1, 8))
        slope, intercept, r, p, std_err = stats.linregress(X, y)
        
        df.loc[i, "slope"] = slope
    
    df.sort_values("slope", ascending=False,  inplace=True)

    yesterday = date.today() + timedelta(days = -1)
    df.to_csv(rf"get_article_links\trending_table\{yesterday}.csv", index = False)
    return df

