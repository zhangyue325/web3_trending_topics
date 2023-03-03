import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"trending_articles\2023-02-28.csv")


hour = df["post_date"].str[11:13].value_counts().sort_index()

x = hour.index.tolist()
y = hour.values.tolist()

plt.bar(x, y)
plt.show()