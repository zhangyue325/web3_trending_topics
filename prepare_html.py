import pandas as pd
from datetime import timedelta, date

def prepare_the_html_data(dt):
    df = pd.read_csv(rf"trending_articles\{dt}.csv")
    df = df[~df["Occurrence"].isna()]

    n = len(df)

    for i in range(n):
        df.loc[i, "article_title"] = f'{df.loc[i, "source"]}({df.loc[i, "post_date"][5:-3]}): <a href="{df.loc[i, "url"]}" target="_blank">{df.loc[i, "article_title"]}</a>'
        t = df.groupby(['main_keyword', "Occurrence", "slope"])['article_title'].apply(lambda x: '<br>'.join(x)).reset_index()
        t = t.sort_values(by = ["Occurrence", "main_keyword"], ascending=[False, False])

    t["English hot articles"] = "to be completed"
    t["hot tweets"] = "to be completed"
    t["trending"] = '<img src="D:\work_experience\dethings\web3_trending_topics_project\statics\images.png"  />'

    t.to_csv("statics/data.csv",index = False)

    t.to_html("statics/data.html", index = False, escape=False)

if __name__ == "__main__":
    dt = date.today() - timedelta(days = 1)
    prepare_the_html_data(dt)