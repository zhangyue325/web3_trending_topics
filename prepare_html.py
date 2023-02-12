import pandas as pd
from datetime import timedelta, date
import matplotlib.pyplot as plt 
from scipy.interpolate import make_interp_spline
import numpy as np
import os
import shutil

def prapapre_the_graph(y, slope, keyword):
    x = np.array(range(1, 8))
    X_Y_Spline = make_interp_spline(x, y)
    
    X_Y_Spline = make_interp_spline(x, y)
    
    # Returns evenly spaced numbers
    # over a specified interval.
    X_ = np.linspace(x.min(), x.max(), 500)
    Y_ = X_Y_Spline(X_)

    plt.figure(figsize=(3,1))
    
    fig, ax1 = plt.subplots()
    # # Plotting the Graph
    if slope > 0:
        color = "red"
    else:
        color = "green"
    ax1.set_ylim([-3, 10])
    ax1.plot(X_, Y_, color = color, linewidth= 9)

    ax2 = ax1.twinx()
    ax2.set_ylim([-3, 10])
    ax2.scatter(x, y, marker = "o", s = 26**2)

    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0,
                hspace = 0, wspace = 0)

    fig.savefig(rf"statics/graph/{keyword}.png")


def generate_all_the_graph(dt):
    df = pd.read_csv(rf'trending_table\{dt}.csv')
    n = len(df)

    shutil.rmtree('statics/graph')
    os.mkdir('statics/graph')
    for i in range(n):
        x = df.iloc[i, 2:2+7].tolist()[::-1]
        slope = df.iloc[i, -1]
        keyword = df.iloc[i, 0]
        prapapre_the_graph(x, slope, keyword)    


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
    n = len(t)
    for i in range(n):
        t.loc[i, "trending"] = f'<img src="D:\work_experience\dethings\web3_trending_topics_project\statics\graph\{t.loc[i, "main_keyword"]}.png" width = "100"  />'
        
        if t.loc[i, "Occurrence"] >= 7:
            t.loc[i, "Occurrence_display"] = "🔥🔥🔥<br>" + str(t.loc[i, "Occurrence"])
        elif t.loc[i, "Occurrence"] >= 4:
            t.loc[i, "Occurrence_display"] = "🔥🔥<br>" + str(t.loc[i, "Occurrence"])
        else:
            t.loc[i, "Occurrence_display"] = "🔥<br>" + str(t.loc[i, "Occurrence"])

        if t.loc[i, "slope"] >= 0.5:
            t.loc[i, "slope_display"] = "📈📈📈<br>" + str(t.loc[i, "slope"])
        elif t.loc[i, "slope"] >= 0.3:
            t.loc[i, "slope_display"] = "📈📈<br>" + str(t.loc[i, "slope"])
        elif t.loc[i, "slope"] >= 0:
            t.loc[i, "slope_display"] = "📈<br>" + str(t.loc[i, "slope"])
        elif t.loc[i, "slope"] >= -0.3:
            t.loc[i, "slope_display"] = "📉<br>" + str(t.loc[i, "slope"])
        elif t.loc[i, "slope"] >= -0.5:
            t.loc[i, "slope_display"] = "📉📉<br>" + str(t.loc[i, "slope"])
        else:
            t.loc[i, "slope_display"] = "📉📉📉<br>" + str(t.loc[i, "slope"])

    t = t[["main_keyword", "Occurrence_display", "slope_display", "trending", "article_title", "English hot articles", "hot tweets"]]

    t.to_csv("statics/data.csv",index = False)
    t.to_html("statics/data.html", index = False, escape=False)



if __name__ == "__main__":
    y = [7.8431372549019605,0.0,0.0,0.0,4.807692307692308,2.5,2.5]
    dt = date.today() - timedelta(days = 1)
    # generate_all_the_graph(dt)

    prepare_the_html_data(dt)