'''
Project to scrape the 100
best movies from site:
https://web.archive.org/web/20240718191218/https://www.empireonline.com/movies/features/best-movies-2/
had to move back down the dates as  several of the later dates
had most of the numbers followed by a ')' except for 100, so the site was inconsistent.
Turns out that wasn't overly important as only need the number and
the title to produce a text file with the movie titles and the number.
From the previous lectures thought that this project would push us a little more.
'''

import requests
from bs4 import BeautifulSoup

response = requests.get(
    url=r'https://web.archive.org/web/20231008153715/https://www.empireonline.com/movies/features/best-movies-2/')
# response.raise_for_status()
# print(response.text)
soup = BeautifulSoup(response.text, 'html.parser')

# Get the titles first:
all_titles_lst: list = []

all_titles = soup.findAll(
    name='h3', class_='listicleItem_listicle-item__title__hW_Kn')
for title in all_titles:
    find_title = title.getText()
    all_titles_lst.append(find_title)
all_titles_lst = all_titles_lst[::-1]
#  print(all_titles_lst)
with open(r'./top100movies.txt', 'w') as file:
    for movie in all_titles_lst:
        file.write(f'{movie}\n')
