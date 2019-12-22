<<<<<<< HEAD
from torrequest import TorRequest
from bs4 import BeautifulSoup
import numpy as np
import time
import csv
import random
import re
import pandas as pd


_HOST = 'https://scholar.google.com'

title = []
author = []
urls = []
year = []
source_publication = []
source = []

# truncate number of scrapped citations to match google scholar's display of pages
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

# get page using Tor and send make a BeautifulSoup object
def _get_soup(url):
    tr = TorRequest(proxy_port=9050, ctrl_port=9051, password='slotting11')
    tr.reset_identity()
    t = random.randrange(8, 12) # choose time to wait from 8 to 12 seconds
    time.sleep(t) # lag requests to prevent google blocks
    page = tr.get(url)
    content = page.text # scrap text
    return BeautifulSoup(content, 'html.parser')

# get all necessary data: source article, which is cited, e.g. source multiverse article - Steegen et al. (2016);
# titles of articles that cite soruce article, their year of publication, authors and url
def _get_data(soup):
    for x in soup.find_all('h2', attrs = {'class': 'gs_rt'}):
        source_publication = x.get_text()
    # Titles
    for entry in soup.find_all('h3', attrs = {'class': 'gs_rt'}):
        if re.match('\[', entry.get_text()) != None:
            sub = re.sub('\[.+?\] ', '', entry.get_text())
            title.append(sub)
        else:
            title.append(entry.get_text())
        source.append(source_publication)
    # Authors
    for i in soup.find_all('div', class_='gs_a'):
        match_author = re.match('(.*?)-', i.get_text()).group()
        remove_hyphen = re.sub('-$', '', match_author)
        author.append(remove_hyphen)

    # Publication year
    for i in soup.find_all('div', class_='gs_a'):
        if re.findall(r'\D(\d{4})\D', i.get_text()) != []:
            y = re.findall(r'\D(\d{4})\D', i.get_text())[-1]
            year.append(y)
        else:
            y = "NA"
            year.append(y)
    # URLs
    for entry in soup.find_all('h3', attrs = {'class': 'gs_rt'}):
        for link in entry.find_all('a'):
            urls.append(link.get('href'))

    return title, author, year, urls, source

# main function
def scrap(url):
    soup = _get_soup(url) #
    _get_data(soup)
    # Extracting all the <a> tags into a list.
    tags = soup.find_all('a')
    # Extracting URLs from the attribute href in the <a> tags.
    links = [tag.get('href') for tag in tags]

    needed_links = [] # extract links to for loop
    for link in links:
        if "/scholar?start=" in link:
            needed_links.append(link)
        else:
            pass

    first_link = needed_links[0]
    url_to_loop = _HOST + first_link

    for i in soup.body.find_all('div', attrs = {'class': 'gs_ab_mdw'}):
        cit = re.findall(r'\d+', i.get_text())
    n = truncate(int(cit[0]))
    print(n)
    page_nums = np.arange(10, n, 10).tolist()
    str_page_nums = [str(x) for x in page_nums]
    split = re.split(r'\d+', url_to_loop, 1)
    print(split[0])
    print(str_page_nums[0])
    print(split[1])

    for i in str_page_nums:
        page_url = split[0] + i + split[1]
        soup = _get_soup(page_url)
        _get_data(soup)


# Steegen et al.; Spec Curve Analysis; One data set, many aalysts
# IMPORTANT: urls from the first page with UNCTICKED button "display citations" to avoid redundant positions
google_first_page = ["https://scholar.google.pl/scholar?as_vis=1&hl=pl&as_sdt=2005&sciodt=0,5&cites=1876944506735412470&scipsc=", "https://scholar.google.pl/scholar?as_vis=1&hl=pl&as_sdt=2005&sciodt=0,5&cites=13886672327921788744&scipsc=",
"https://scholar.google.pl/scholar?as_vis=1&hl=pl&as_sdt=2005&sciodt=0,5&cites=10005641543062285998&scipsc=", "https://scholar.google.pl/scholar?as_vis=1&hl=pl&as_sdt=2005&sciodt=0,5&cites=4814461758332255763&scipsc="]

for i in google_first_page:
    scrap(i)

# save data
d = {'source': source, 'title': title, 'author': author, 'year': year, 'URLs': urls}
df = pd.DataFrame(data=d)
df.to_excel("output.xlsx", encoding = 'utf-8', index = False)
=======
from torrequest import TorRequest
from bs4 import BeautifulSoup
import numpy as np
import time
import csv
import random
import re
import pandas as pd


_HOST = 'https://scholar.google.com'

title = []
author = []
urls = []
year = []
source_publication = []
source = []

# truncate number of scrapped citations to match google scholar's display of pages
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

# get page using Tor and send make a BeautifulSoup object
def _get_soup(url):
    tr = TorRequest(proxy_port=9050, ctrl_port=9051, password='slotting11')
    tr.reset_identity()
    t = random.randrange(8, 12) # choose time to wait from 8 to 12 seconds
    time.sleep(t) # lag requests to prevent google blocks
    page = tr.get(url)
    content = page.text # scrap text
    return BeautifulSoup(content, 'html.parser')

# get all necessary data: source article, which is cited, e.g. source multiverse article - Steegen et al. (2016);
# titles of articles that cite soruce article, their year of publication, authors and url
def _get_data(soup):
    for x in soup.find_all('h2', attrs = {'class': 'gs_rt'}):
        source_publication = x.get_text()
    # Titles
    for entry in soup.find_all('h3', attrs = {'class': 'gs_rt'}):
        if re.match('\[', entry.get_text()) != None:
            sub = re.sub('\[.+?\] ', '', entry.get_text())
            title.append(sub)
        else:
            title.append(entry.get_text())
        source.append(source_publication)
    # Authors
    for i in soup.find_all('div', class_='gs_a'):
        match_author = re.match('(.*?)-', i.get_text()).group()
        remove_hyphen = re.sub('-$', '', match_author)
        author.append(remove_hyphen)

    # Publication year
    for i in soup.find_all('div', class_='gs_a'):
        if re.findall(r'\D(\d{4})\D', i.get_text()) != []:
            y = re.findall(r'\D(\d{4})\D', i.get_text())[-1]
            year.append(y)
        else:
            y = "NA"
            year.append(y)
    # URLs
    for entry in soup.find_all('h3', attrs = {'class': 'gs_rt'}):
        for link in entry.find_all('a'):
            urls.append(link.get('href'))

    return title, author, year, urls, source

# main function
def scrap(url):
    soup = _get_soup(url) #
    _get_data(soup)
    # Extracting all the <a> tags into a list.
    tags = soup.find_all('a')
    # Extracting URLs from the attribute href in the <a> tags.
    links = [tag.get('href') for tag in tags]

    needed_links = [] # extract links to for loop
    for link in links:
        if "/scholar?start=" in link:
            needed_links.append(link)
        else:
            pass

    first_link = needed_links[0]
    url_to_loop = _HOST + first_link

    for i in soup.body.find_all('div', attrs = {'class': 'gs_ab_mdw'}):
        cit = re.findall(r'\d+', i.get_text())
    n = truncate(int(cit[0]))
    print(n)
    page_nums = np.arange(10, n, 10).tolist()
    str_page_nums = [str(x) for x in page_nums]
    split = re.split(r'\d+', url_to_loop, 1)
    print(split[0])
    print(str_page_nums[0])
    print(split[1])

    for i in str_page_nums:
        page_url = split[0] + i + split[1]
        soup = _get_soup(page_url)
        _get_data(soup)


# Steegen et al.; Spec Curve Analysis; One data set, many aalysts
# IMPORTANT: urls from the first page with UNCTICKED button "display citations" to avoid redundant positions
google_first_page = ["https://scholar.google.pl/scholar?as_vis=1&hl=pl&as_sdt=2005&sciodt=0,5&cites=1876944506735412470&scipsc=", "https://scholar.google.pl/scholar?as_vis=1&hl=pl&as_sdt=2005&sciodt=0,5&cites=13886672327921788744&scipsc=",
"https://scholar.google.pl/scholar?as_vis=1&hl=pl&as_sdt=2005&sciodt=0,5&cites=10005641543062285998&scipsc=", "https://scholar.google.pl/scholar?as_vis=1&hl=pl&as_sdt=2005&sciodt=0,5&cites=4814461758332255763&scipsc="]

for i in google_first_page:
    scrap(i)

# save data
d = {'source': source, 'title': title, 'author': author, 'year': year, 'URLs': urls}
df = pd.DataFrame(data=d)
df.to_excel("output.xlsx", encoding = 'utf-8', index = False)
>>>>>>> 4a59d7add1e2f07b93e5cc75be32ceb9f02602d5
