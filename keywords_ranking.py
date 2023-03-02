import pandas as pd
import json
from datetime import timedelta, date
from scipy import stats

BLACKWORDS = ["教程", "veDAO", "2023", "2022","Crypto", "概览", "加密", "比特", 
"笔记", "叙事", "探会","Web3", "减半", "窒息", "以太", "Hashed", "哪些项目", 
"进军", "日报", "预测", "赛道", "机遇", "挑战", "聊起", "链上", "一文","宇宙",
"v3", "Capital", "哪些项目", "官网", "Bankless", "探寻", "今生", "哪些",
"Weekly", "速览", "之辩", "读懂", "好生意", "盘点", "代币"]

def convert_string_to_list(list_like_string):
    data = list_like_string[1:-1].split("), (")
    if len(data) in (2, 3):
        data[0] = data[0][1:]
        data[-1] = data[-1][:-1]
        res = []
    else:
        print("keyword len is not 2 or 3")
        return []
    for ele in data:
        keyword = ele.split(",")[0][1:-1]
        res.append(keyword)
        return res

def get_topics_hash(date):
    hash = {}
    df = pd.read_csv(rf"articles\{date}.csv")
    n = len(df)

    for i in range(n):
        data = df.loc[i, "keywords"]
        kw = convert_string_to_list(data)
        for ele in kw:
            if ele in BLACKWORDS:
                continue
            if ele in hash:
                hash[ele] += 1
            else:
                hash[ele] = 1
    with open(rf"topics\{date}.json", "w") as fp:
        json.dump(hash, fp) 
    print(hash)
    return hash


def get_occurance_for_topics(dt):
    with open(rf"topics\{dt}.json") as json_file:
        data = json.load(json_file)
    df = pd.DataFrame()

    article_df = pd.read_csv(rf"articles\{dt}.csv")
    article_len = len(article_df)

    for k, v in data.items():
        if v >= 2:
            to_df = {"keyword":k, "Occurrence": v/article_len*100, dt: v/article_len*100}
            to_df = pd.DataFrame([to_df])
            df = pd.concat([df, to_df], ignore_index=True)
    return df
    

def get_historical_data_for_topics(yesterday): 
    df = get_occurance_for_topics(yesterday)
    for delta in range(1, 7):
        dt = yesterday - timedelta(days = delta)
        with open(rf"topics\{dt}.json") as json_file:
            data = json.load(json_file)
        
        article_df = pd.read_csv(rf"articles\{dt}.csv")
        article_len = len(article_df)

        for kwd in df["keyword"].tolist():
            if kwd in data:
                df.loc[df["keyword"] == kwd, dt] = data[kwd] / article_len * 100
            else:
                df.loc[df["keyword"] == kwd, dt] = 0
    return df


def get_slope(yesterday):
    df = get_historical_data_for_topics(yesterday)

    for i in range(len(df)):
        y = df.iloc[i, 2:9].tolist()[::-1]
        X = list(range(1, 8))
        slope, intercept, r, p, std_err = stats.linregress(X, y)
        
        df.loc[i, "slope"] = slope
    
    df.sort_values("Occurrence", ascending=False,  inplace=True)
    df.to_csv(rf"trending_table\{yesterday}.csv", index = False)
    return df

if __name__ == "__main__":
    dt = date.today() - timedelta(days = 1)
    get_topics_hash(dt)
    a = get_occurance_for_topics(dt)
    print(a)