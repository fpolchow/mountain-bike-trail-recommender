from collections import Counter
from bs4 import BeautifulSoup
import requests
import math
import re
import csv
import pandas as pymongo
import

def make_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content,'lxml')

def get_trail_stats_box(url):

    stats_url = url + 'stats/'
    soup = make_soup(stats_url)
    trail_stats = soup.find('ul',{'id':'trailstats_display'})
    return trail_stats

def extract_trail_details_stats(trail_stats):
    trail_details = {}
    if trail_stats:
        ## have to do -1 indexing to account for section that you don't want

        list_items = trail_stats.findChildren('li')
        for idx,item in enumerate(list_items):
            print(idx, item)
            if item.find(class_='term'):
                term = item.find(class_='term').text.strip()
                definition = item.find(class_='definition').text.strip()
                trail_details[term]=definition

    return trail_details

def find_gps_coords(soup):
    map_data = soup.find('div',class_='mapinside')
    try:
        coors = map_data.findChildren('span',class_='grey2')[1].text
    except (IndexError, AttributeError):
        coors = None
    return coors

def find_trail_id(soup):
    try:
        map_data = soup.find('div',class_='mapinside')
        messy_link = map_data.findChildren('span',class_='grey2')[0]['onclick']
        trail_id = re.findall('\d+',messy_link)[0]
    except (IndexError,AttributeError):
        trail_id = None
    return trail_id


def find_description(soup):
    description_soup = soup.find('p',{'id':'trail_description'})
    if description_soup:
        description_text = description_soup.text
    else:
        description_text = None
    return description_text


def scrape_user_info(url):
    user_url = url + 'ridelogs/'
    soup =  make_soup(user_url)
    # print(soup.find('div',class_="resultTotal").strong.text)
    try:
        num_trails = int(soup.find('div',class_="resultTotal").strong.text)
        num_pages = range(1,math.ceil(num_trails/100)+2)
    except:
        return 'no_logs'
    user_list = []
    for i in num_pages:
        page = url + 'ridelogs/?page=' + str(i)
        soup = make_soup(page)
        user_profile_urls = soup.find_all(href=re.compile('profile'))
        user_list.extend([user.text for user in user_profile_urls])
    return Counter(user_list)


def trail_info_maker(trail_url):
    """ type_info : either '' for basic trail, 'stats/ for' """
    print('--------------------------------')
    print(trail_url)
    print('--------------------------------')
    trail_info_dict = {}
    soup = make_soup(trail_url)

    trail_info_dict['url'] = trail_url
    trail_info_dict['latlng'] = find_gps_coords(soup)
    trail_info_dict['description'] = find_description(soup)
    trail_info_dict['trail_id'] = find_trail_id(soup)
    trail_info_dict['logs'] = scrape_user_info(trail_url)
    trail_info = soup.find('ul',{'id':'traildetails_display'})
    trail_details = extract_trail_details_stats(trail_info)
    trail_stats_page = get_trail_stats_box(trail_url)
    trail_statistics = extract_trail_details_stats(trail_stats_page)
    trail_info_dict.update(trail_details)
    trail_info_dict.update(trail_statistics)
    print(trail_info_dict)
    return trail_info_dict

def main_trail_scraper(trails):
    with open('test.csv','w') as f:
        fieldnames = ['url', 'latlng', 'description', 'trail_id', 'logs',
         'Riding Area', 'Difficulty Rating', 'Trail Type', 'Trail Usage',
          'Direction', 'Climb Difficulty', 'Physical Rating', 'Global Ranking',
           'Land Manager', 'Distance', 'Altitude change', 'Altitude min',
            'Altitude max', 'Altitude start', 'Altitude end', 'Grade',
             'Grade max', 'Grade min', 'Vertical climb', 'Vertical descent',
              'Distance climb', 'Distance descent', 'Distance Flat','Bike Type',
               'Avg time', 'eBike Allowed', 'TTFs on Trail','Avg reverse time',
               'Season','AKA','Alpine Trail','Family Friendly','Year Opened',
               'Ride in Rain','Voted Difficulty','OSM Way', 'Local Popularity','Distance flat',
               'Distance down']
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        for trail in trails:
            writer.writerow(trail_info_maker(trail))
            print('just scraped {}'.format(trail))

df = pd.read_csv('./data/trails_lists/carolina_trails.csv',header=None)
cal_trails = df[0]

if __name__ == "__main__":
    main_trail_scraper(cal_trails)
