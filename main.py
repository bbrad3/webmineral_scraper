from bs4 import BeautifulSoup
import requests
import re
import csv

source = requests.get('http://www.webmineral.com/data/index.html').text

soup = BeautifulSoup(source, 'lxml')

# open the file you want to write to
csv_file = open('portfolio_scrape', 'w')

csv_writer = csv.writer(csv_file)
# headers
csv_writer.writerow([])

# find a tags
a_tags = soup.find_all('a')
mineral_names = []
# extract mineral name
for tag in a_tags:
    mineral_names.append(tag.get('href'))
mineral_names.remove('?C=N;O=D')
mineral_names.remove('/')

for mineral in mineral_names:
    try:
        # scrape each link
        link = 'http://www.webmineral.com/data/{0}#.YTEkIdPnNqs'.format(
            mineral)
        mineral_source = requests.get(link).text
        mineral_soup = BeautifulSoup(mineral_source, 'lxml')
        td_25 = mineral_soup.find_all("td", width="25%", limit=10)
        all_text = []
        for td in td_25:
            found_text = td.parent.text
            trimmed_text = found_text.strip().replace('\n', '').replace('\xa0', '')
            split_text = trimmed_text.split(' ')
            # print(trimmed_text)
            all_text.append(split_text)

        print(all_text)
        break
    except Exception as err:
        print(err)
