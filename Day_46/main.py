'''
Scrape billboard hot 100 for a date input by user.
Use spotify API to create and save a playlist for
that date.
https://www.billboard.com/charts/hot-100/1981-06-27/
'''

import requests
import re
from bs4 import BeautifulSoup

# Get the releveant date and form the request url; ensure that cannot enter rediculous numbers
# not sure about exactly how to go about easily checking that date falls within correct number
# of days for the partucular month short of checking each of the short months individually.
# Probably some way to do it using regex.


date_reg = re.compile('^\\d{4}-\\d{2}-\\d{2}$')
chart_date = input('Please enter a date of interest (\'yyy-mm-dd\') -> ')
match = date_reg.match(chart_date)
while date_reg.match(chart_date) is None:
    chart_date = input('Please enter a date of interest (\'yyy-mm-dd\') -> ')
URL = f'https://www.billboard.com/charts/hot-100/{chart_date}/'
print(URL)  # Check the url will work by printing and copying into browser

# # Make the request
response = requests.get(url=URL)
response.raise_for_status()
# print(response.status_code)  # Check that response works with the produced URL
