'''
Introduction to beautifulsoup lesson 1
'''

from bs4 import BeautifulSoup

with open(r'./website.html', 'r') as file:
    content = file.read()

soup = BeautifulSoup(content, 'html.parser')
print(soup.title)
print(soup.title.name)
print(soup.title.string)
print(soup)
print(soup.prettify())
