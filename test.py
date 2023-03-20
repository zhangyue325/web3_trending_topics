import requests
from bs4 import BeautifulSoup

url = "https://www.coindesk.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all article titles on the page
article_titles = soup.find_all("h4", class_="heading")

# Print out the titles
for title in article_titles:
    print(title.text.strip())
