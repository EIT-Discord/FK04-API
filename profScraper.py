import re

from bs4 import BeautifulSoup
import requests
from app import Professor, db

sourceUrl = 'https://www.ee.hm.edu/fk04/profs/professoren.de.html'
baseUrl = 'https://www.ee.hm.edu/fk04/profs/'

file = requests.get(sourceUrl)

soup = BeautifulSoup(file.text, 'html.parser')
table = soup.select('td a')

htmls = []
for entry in table:
    url = entry.attrs['href']
    if not url.startswith('http'):
        url = baseUrl + url
    htmls.append(url)

for url in htmls:
    file = requests.get(url)
    soup = BeautifulSoup(file.text, 'html.parser')
    contact = soup.find('div', class_='contact-person-detail-contact')
    faculty = soup.find('div', class_='contact-person-detail-faculty')
    image = soup.find('img', class_='portrait')

    phone, fax = (re.sub(r'[^0-9 -]', '', field) for field in contact.text.strip().split('\n')[:2])
    image_url = image.attrs['src']

    new_prof = Professor(phone=phone, fax=fax, image_url=image_url)
    db.session.add(new_prof)

db.session.commit()