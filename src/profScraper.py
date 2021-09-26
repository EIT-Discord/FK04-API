from bs4 import BeautifulSoup
import requests

sourceUrl = 'https://www.ee.hm.edu/fk04/profs/professoren.de.html'
baseUrl = 'https://www.ee.hm.edu/fk04/profs/'

file = requests.get(sourceUrl)

soup = BeautifulSoup(file.text, 'html.parser')
tables = soup.select('td a')


