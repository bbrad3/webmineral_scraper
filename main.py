from bs4 import BeautifulSoup
import requests
import re
import csv
import time

# Time run
start_time = int(round(time.time(), 2))

source = requests.get('http://www.webmineral.com/data/index.html').text

soup = BeautifulSoup(source, 'lxml')

# open the file you want to write to
# change the filename to create a new one
csv_file = open('webmineral_scrape.csv', 'w')

# initialize writer
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['webmineral.com'])

# find a tags
a_tags = soup.find_all('a')
mineral_names = []
# extract mineral name
for tag in a_tags:
    mineral_names.append(tag.get('href'))
mineral_names.remove('?C=N;O=D')
mineral_names.remove('/')

# --HELPER FUNCTIONS--


# format and write chem formula to csv
def get_chem_formula(string: str):
    split_text = string.split(':')
    csv_writer.writerow([split_text[0], split_text[1]])
    # print(split_text)

# format and write molecular weight to csv


def get_mol_wt(string: str):
    s = string.split(':')
    mol_wt = s[1].strip().split('=')
    val = mol_wt[1].split(' ')
    csv_writer.writerow([mol_wt[0], val[0], val[2]])
    # print(mol_wt)

# format and write composition to csv


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
            csv_writer.writerow([elem, sym, val, '%'])
            # print(f'{elem}({sym}, %) {val}')


# this will be the total number of pages scraped
success = 0
# total Exceptions thrown
fail = 0
for mineral in mineral_names:
    try:
        # soup-ify each link
        link = 'http://www.webmineral.com/data/{0}#.YTEkIdPnNqs'.format(
            mineral)
        mineral_source = requests.get(link).text
        mineral_soup = BeautifulSoup(mineral_source, 'lxml')
        # get the html elements we want
        td_25 = mineral_soup.find_all("td", width="25%", limit=10)
        # trim the text to an acceptable format
        all_text = []
        for td in td_25:
            found_text = td.parent.text
            trimmed_text = found_text.strip().replace('\n', '').replace('\xa0', '')
            all_text.append(trimmed_text)

        mineral_name = str(mineral[:-6]).replace('%20', ' ')
        print(mineral_name)
        # use helper functions to extract needed data
        csv_writer.writerow([mineral_name])
        get_chem_formula(all_text[0])
        get_mol_wt(all_text[1])
        get_composition(all_text[0:10])
        # get_img
        csv_writer.writerow([])
        success += 1
        # uncomment to restrict loop
        # if success >= 5:
        #     break

    except Exception as err:
        fail += 1
        print(err)

end_time = int(round(time.time(), 2))
# total_time is in min
total_time = (end_time - start_time) / 60
print(f'DONE! Total Time: {total_time} min')
print(f'Total success: {success}')
print(f'Total fail: {fail}')
# close file
csv_file.close()
