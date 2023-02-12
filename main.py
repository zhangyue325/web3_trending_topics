from web_crawler import *
from keywords_ranking import *
from link_trending_to_article import *
from prepare_html import *

dt = date.today() - timedelta(days = 1)


get_data()
move_article_csv()
print("articles has been successfully collected")

dt = date.today() - timedelta(days = 1)
get_topics_hash(dt)
keyword_table = get_slope(dt)
print(keyword_table)
print("keywords table been successfully generated")

match_keywords_with_article(dt)
print("keywords table been successfully linked with articles")

generate_all_the_graph(dt)
prepare_the_html_data(dt)
print("html table been successfully prepared")