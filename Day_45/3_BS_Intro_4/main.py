import requests
from bs4 import BeautifulSoup

response = requests.get('https://appbrewery.github.io/news.ycombinator.com/')
response.raise_for_status()
yc_webpage = response.text

soup = BeautifulSoup(yc_webpage, 'html.parser')

# print(soup.title)
# title = soup.find(name='span', class_='titleline')
# print(title.getText())

articles = soup.findAll(name='a', class_='storylink')
article_texts = []
article_links = []
for article_tag in articles:
    text = article_tag.getText()
    link = article_tag.get('href')
    article_links.append(link)
    article_texts.append(text)
# print(article_links)
# print(article_texts)
article_upvotes = [int(upvotes.getText().split()[0])
                   for upvotes in soup.find_all(name='span', class_='score')]
# print(article_upvotes)
max_votes = max(article_upvotes)
max_index = article_upvotes.index(max_votes)
print(f'The article with the most upvotes can be read at: {article_links[max_index]} the heading is: {
      article_texts[max_index]} and has recorded {article_upvotes[max_index]} upvotes')
