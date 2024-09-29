from bs4 import BeautifulSoup

with open(r'../1_BS_Intro/website.html', 'r') as file:
    content = file.read()
soup = BeautifulSoup(content, 'html.parser')

# Find all anchor tags:

all_anchors = soup.find_all(name='a')  # also works as .findAll(...)
print(all_anchors)
# find all paras
all_ps = soup.find_all(name='p')  # also works as .findAll(...)
print(all_ps)

# With text only:
for tag in all_anchors:
    print(tag.getText())
    print(tag.get('href'))

# search by id:

# can be used also with findAll/find_all
heading = soup.find(name='h1', id='name')
print(heading)

# by class:

setting = soup.find(name='h3', class_='heading')  # Note the underscore
print(setting)
print(setting.getText())
print(setting.name)
print(setting.value)
print(setting.get('class'))

# drill down using CSS selectors:

# can also use the class or ID in selector.
company = soup.select_one(selector='p a')
print(company)
name = soup.select_one(selector='#name')
# All tages that have a class of heading:
heading = soup.select_one(selector='.heading')
