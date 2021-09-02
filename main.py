from bs4 import BeautifulSoup
import requests
import re
import csv

source = requests.get('http://www.webmineral.com/data/index.html').text

soup = BeautifulSoup(source, 'lxml')

# open the file you want to write to
csv_file = open('portfolio_scraper', 'w')

# initialize writer
csv_writer = csv.writer(csv_file)

# find a tags
a_tags = soup.find_all('a')
mineral_names = []
# extract mineral name
for tag in a_tags:
    mineral_names.append(tag.get('href'))
mineral_names.remove('?C=N;O=D')
mineral_names.remove('/')

# --HELPER FUNCTIONS--


def get_chem_formula(string: str):
    split_text = string.split(':')
    # WRITE CHEM_FORMULA TO CSV
    csv_writer.writerow([split_text[0], split_text[1]])
    # print(split_text)


def get_mol_wt(string: str):
    s = string.split(':')
    mol_wt = s[1].strip().split('=')
    csv_writer.writerow([mol_wt[0], mol_wt[1]])
    # print(mol_wt)


def get_composition(arr: list):
    csv_writer.writerow(['Composition'])
    for s in arr:
        if s.find('%') > 0:
            split_s = re.split('(\d+|\W{2,})', s)
            elem = split_s[0]
            val = split_s[1] + split_s[2] + split_s[3]
            sym = split_s[4].replace('%', '')
            if elem == '':
                elem = 'Total'
            csv_writer.writerow([elem, sym, '%', val])
            print(f'{elem}({sym}, %) {val}')


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
            all_text.append(trimmed_text)

        # print(all_text)
        csv_writer.writerow([mineral[:-6]])
        csv_writer.writerow([])
        get_chem_formula(all_text[0])
        get_mol_wt(all_text[1])
        csv_writer.writerow([])
        get_composition(all_text[0:10])
        break
    except Exception as err:
        print(err)
