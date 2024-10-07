'''
Grab an actual product from Amazon and get an update
when the product falls below a certain price.
protonmail api https://pypi.org/project/protonmail-api-client/
'''
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from protonmail import ProtonMail

load_dotenv()

URL: str = 'https://www.amazon.co.uk/Bosch-WGG244F9GB-Automatic-SpeedPerfect-Freestanding/dp/B0C2QJWT8K/ref=sr_1_1_sspa?crid=C8IZU3HB8V3R&dib=eyJ2IjoiMSJ9.rWiVJ3mNPHSj1KFnVE8MpjIhxyorlU2nhuMVU3Nx7FCy94y9uYrLc4dsoneCqdPLY3YX6kIo7PE7P13MFE7hwk0lSMJVlUjKtlor6-ajnCwpdetpg3fQycaSMB00UgZA2_hsCGsZCueFI7z4zdomf_CMGvpB3eQaHt4IykrABRA4BLH_vDeAvxj8z-wriEgZ4EZTYeWfHJu1qgHkbY4wNsUxG0y8V_zjSxCfzakCDhs.B8hZtEMii6omNnP3mHs0cWJjiF-6P2sueH6kW3JMRew&dib_tag=se&keywords=washing+machines&qid=1728326650&sprefix=washing+machine%2Caps%2C165&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1'
HEADERS: dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Dnt': '1',
    'Priority': 'u=1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrage-Insecure-Requests': '1',
}

contents: str = requests.get(url=URL, timeout=5.0, headers=HEADERS)
contents.raise_for_status()

soup = contents.text
all_contents = BeautifulSoup(soup, 'html.parser')
#  print(all_contents)
price_whole: str = BeautifulSoup.find(
    all_contents, name='span', class_='a-price-whole').text
price_dec: str = BeautifulSoup.find(
    all_contents, name='span', class_='a-price-decimal').text
# price: float = float(price_whole)
if price_dec == '.':
    price_dec.strip('.')
    price_dec = '0.00'

full_price: float = float(price_whole) + float(price_dec)

if full_price < 629.99:
    message_text = f'The price of the item of the washing machine has fallen to £{
        full_price}. Link: {URL}'

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
# proton.save_session('session.pickle')
