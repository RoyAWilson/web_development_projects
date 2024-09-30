'''
Scrape billboard hot 100 for a date input by user.
Use spotify API to create and save a playlist for
that date.
https://www.billboard.com/charts/hot-100/1981-06-27/
'''

import re
import requests
from bs4 import BeautifulSoup

# Get the releveant date and form the request url; ensure that cannot enter rediculous numbers
# not sure about exactly how to go about easily checking that date falls within correct number
# of days for the partucular month short of checking each of the short months individually.
# Probably some way to do it using regex.


def get_url() -> str:
    '''
    Get a date for the chart and grab the URL for that date
    returns str
    no arguments
    '''
    date_reg: str = re.compile('^\\d{4}-\\d{2}-\\d{2}$')
    chart_date: str = input(
        'Please enter a date of interest (\'yyyy-mm-dd\') -> ')
    # match: str = date_reg.match(chart_date)
    while date_reg.match(chart_date) is None:
        chart_date = input(
            'Please enter a date of interest (\'yyyy-mm-dd\') -> ')
    uri: str = f'https://www.billboard.com/charts/hot-100/{chart_date}/'
    return uri
# print(response.status_code)  # Check that response works with the produced URL


def check_url(url_to_check) -> bool:
    '''
    argument URL
    returns bool
    Check if the URL is good or not.
    '''
    # Damn! The site doesn't seem to care about out of bounds dates.
    # Take to a date before or after they have data for and brings up
    # a random year for the day and month entered!
    response = requests.get(url=url_to_check, timeout=5.0)
    response.raise_for_status()
    if response.status_code == 200:
        return True
    else:
        return False


def get_html(url_to_soup) -> str:
    '''
    arguments url_to_soup - should be a URL
    returns string
    To get URL contents with bs4
    '''
    cont_to_scrape = requests.get(url=url_to_soup, timeout=5.0)
    soup = BeautifulSoup(cont_to_scrape.text, 'html.parser')
    return soup


# Check all working and returning sensible data
URL = get_url()
print(URL)
GOOD = check_url(url_to_check=URL)
print(GOOD)
contents = get_html(URL)
print(contents)

# TODO get a list of the top 100
# TODO pass contents to spotify API
# TODO set up playlist
