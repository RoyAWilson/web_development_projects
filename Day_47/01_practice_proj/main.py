'''
Practice grabbing price from a
static version of the website.
protonmail api https://pypi.org/project/protonmail-api-client/
'''
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from protonmail import ProtonMail

load_dotenv()

URL: str = 'https://appbrewery.github.io/instant_pot/'

contents: str = requests.get(url=URL, timeout=5.0)
contents.raise_for_status()

soup = contents.text
all_contents = BeautifulSoup(soup, 'html.parser')
#  print(all_contents)
price: str = BeautifulSoup.find(
    all_contents, name='span', class_='aok-offscreen')
price: float = float(price.text.split('$')[1])
if price < 100:
    message_text = f'The price of the item of interest has fallen to${
        price}. Link: {URL}'

    OUTMAIL = os.getenv('FROM_EMAIL')
    PASSWORD = os.getenv('FROM_PASSWORD')
    TO_ADDY = os.getenv('TO_EMAIL')

    # set up email:

    proton = ProtonMail()
    proton.login(username=OUTMAIL, password=PASSWORD)

    new_message = proton.create_message(
        recipients=[TO_ADDY],
        subject='Price dropped',
        body=message_text
    )
    proton.send_message(new_message)
    proton.save_session('session.pickle')
