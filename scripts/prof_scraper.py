# (c) 2021 Yannic Breiting, Martin Kistler

import re

import requests
from bs4 import BeautifulSoup

from src.app import db
from src.db_models import Professor


sourceUrl = 'https://www.ee.hm.edu/fk04/profs/professoren.de.html'
baseUrl = 'https://www.ee.hm.edu/fk04/profs/'

# create soup
file = requests.get(sourceUrl)
soup = BeautifulSoup(file.text, 'html.parser')
table = soup.select('td a')

# parse urls
htmls = []
for entry in table:
    url = entry.attrs['href']
    if not url.startswith('http'):
        url = baseUrl + url
    htmls.append(url)

for url in htmls:
    # fetch resources from html
    file = requests.get(url)
    soup = BeautifulSoup(file.text, 'html.parser')
    person_detail = soup.find('h2', class_='normal')
    contact = soup.find('div', class_='contact-person-detail-contact')
    faculty = soup.find('div', class_='contact-person-detail-faculty')
    image = soup.find('img', class_='portrait')
    email_tag = soup.find("a", class_="emailLink")

    # parse emails
    email_tag_string = str(email_tag)
    # Mit Regex nur die Email extrahieren bsp. rel="xyz@hm.edu"> --> xyz@hm.edu
    try:
        email = re.search(r"rel=\"(.*)\">", email_tag_string).group(1)
        # Email-Adresse umdrehen / mit . und // mit @ ersetzen
        email = email[::-1]
        email = email.replace("//", "@")
        email = email.replace("/", ".")
    except AttributeError:
        email = ''

    # parse courses
    try:
        moodle_courses = soup.find('a', href=re.compile(r'https://moodle.hm.edu/course')).attrs['href']
    except AttributeError:
        moodle_courses = ''

    # parse description
    try:
        person_description = soup.find(class_='list-contact-person-detail')
        description = person_description.text
    except AttributeError:
        description = ''

    name = person_detail.text
    phone, fax = (re.sub(r'[^0-9 -]', '', field) for field in contact.text.strip().split('\n')[:2])
    image_url = image.attrs['src']

    # parse adresse
    room = ''
    address = ''
    for string in faculty.text.strip().split('\n'):
        if 'Raum:' in string:
            room = string[string.find(' '):].lstrip()
        if 'Adresse' in string:
            address = string[string.find(' '):].lstrip()

    # create new prof
    new_prof = Professor(name=name, email=email, phone=phone, fax=fax, address=address, room=room, moodleCourses=moodle_courses,
                         description=description, imageUrl=image_url)
    db.session.add(new_prof)

db.session.commit()
