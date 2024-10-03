'''
Scrape billboard hot 100 for a date input by user.
Use spotify API to create and save a playlist for
that date.
https://www.billboard.com/charts/hot-100/1981-06-27/
'''

import re
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()

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
    uri: str = f'https://www.billboard.com/charts/hot-100/{chart_date}'
    return uri
# print(response.status_code)  # Check that response works with the produced URL


# def check_url(url_to_check) -> bool:
# This stopped working with an error meesaage not allowed for this url so removed as couldn't find a way to get it working.

# argument URL
# returns bool
# Check if the URL is good or not.

    # Damn! The site doesn't seem to care about out of bounds dates.
    # Request a date before or after they have data for and brings up
    # a random year for the day and month entered!
    # response: str = requests.get(url=url_to_check, timeout=5.0, headers={
    #                              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
    # response.raise_for_status()
    # if response.status_code == 200:
    #     return True
    # else:
    #     return False


def get_html(url_to_soup) -> str:
    '''
    arguments url_to_soup - should be an URL
    returns string
    To get URL contents with bs4
    '''
    cont_to_scrape: str = requests.get(url=url_to_soup, timeout=5.0, headers={
                                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(cont_to_scrape.text, 'html.parser')
    return soup


def get_titles(all_content: str) -> list:
    '''
    Grab the titles of the songs in the top 100
    argument all_content str
    returns list
    '''
    song_names_spans: str = all_content.select("li ul li h3")
    song_names: list = [song.getText().strip() for song in song_names_spans]
    # print(song_names)
    return song_names


URL: str = get_url()
# GOOD: bool = check_url(url_to_check=URL)
print(URL)
# if GOOD is True:
contents: str = get_html(URL)
titles: str = get_titles(contents)
print(titles)
if len(titles) == 0:
    print('This query returned nothing.  Maybe the site is updating.')

# Build up the playlist:
# Get all relevant auth codes first

CLIENT_ID: str = os.getenv('CLIENT_ID')
CLIENT_SECRET: str = os.getenv('CLIENT_SECRET')
USER_NAME: str = os.getenv('USER_NAME')

# Deal with authorisation

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope='playlist-modify-private',
        redirect_uri='http://localhost:3000/api/auth/callback/spotify',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path='token.txt',
        username=USER_NAME
    )
)
user_id = sp.current_user()['id']

# Grab a list of song uris

song_urls: list = []
song_date: str = URL[-10:-6]
# print(song_date)
for song in titles:
    song_result = sp.search(q=f'track:{song} year:{song_date}', type='track')
    try:
        uri = song_result['tracks']['items'][0]['uri']
        song_urls.append(uri)
    except IndexError:
        print(f'{song} does not exist in Spotify.  Song has been skipped')
# print(song_urls)

# Make and upload the playlist to spotify:
# Authorise and give playlist a title

playlist = sp.user_playlist_create(
    user=user_id, name=f'{song_date} Billboard 100', public=False)

# Add songs and create playlist

sp.playlist_add_items(playlist_id=playlist['id'], items=song_urls)
