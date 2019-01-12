from bs4 import BeautifulSoup
import requests
import csv
import math
from sys import argv
import pdb
import re
"""
-------------------------------------------------

Made to scrape trails names for each region

url to use is: https://www.trailforks.com/regions/directory/?r=usa








-------------------------------------------------
"""

def get_region_names(country):
    link_tags = country.findParent().next_sibling
    return [link.get('href') for link in link_tags.findAll('a')]


def scrape_all_regions(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "lxml")
    # items = soup.find_all('a',{"class": "regionLink")
    mega_regions = soup.findAll('a',{"class": "regionLink","data-rid":["country_3001","country_3000"]})
    all_links = []
    for item in mega_regions:
        all_links.extend(get_region_names(item))

    with open('./data/regions/regions.csv','w') as f:
        wrtr = csv.writer(f)
        for region in all_links:
            wrtr.writerow([region])

    return all_links



def find_number_of_trail_pages(region):
    trails =  region + 'trails/'
    r = requests.get(trails)
    soup =  BeautifulSoup(r.content, "lxml")
    try:
        num_trails = int(soup.find('div',class_="resultTotal").strong.text)
        num_pages = range(1,math.ceil(num_trails/100)+1)
    except:
        num_pages = 'no trails'
    return num_pages


def scrape_region(region):
    result_pages = find_number_of_trail_pages(region)
    if result_pages == 'no trails':
        trail_list = ['no_trails']
        return trail_list
    else:
        trail_list = []
        for i in result_pages:
            page = region + 'trails/?page=' + str(i)
            r = requests.get(page)
            soup = BeautifulSoup(r.content, "lxml")
            trail_rows = soup.find_all('a',{'class':'green'})
            trail_list.extend([link.get('href') for link in trail_rows])
            print('scraped',str(i*100),'trails!')
    return trail_list


def write_to_csvs(region):
    trails = scrape_region(region)
    # name = re.findall('\w+/+$',region)[0][:-1]
    name = re.findall('((\w+-)*\w+\/+)$',region)[0][0][:-1]
    # pdb.set_trace()
    with open('./data/regions' + name + '_trails.csv','w') as f:
        wrtr = csv.writer(f)
        for trail in trails:
            wrtr.writerow([trail])
    print('Finished scraping {}!'.format(name))



def main():

    regions = scrape_all_regions('https://www.trailforks.com/trails/')
    print(regions)
    with open('regions.csv','w') as f:
        write = csv.writer(f)
        for reg in regions:
            write.writerow([reg])

    with open('regions.csv','r') as f:
        regions = [reg.strip() for reg in f]

    for reg in regions:
        write_to_csvs(reg)


# if __name__ == "__main__":
#     main()
#


#
# def trail_info_maker(trail_box):
#     trail_info_dict = {}
#      for item in box:
#          term = item.find(class_='term').text.strip()
#          definition = item.find(class_='definition').text.strip()
#          trail_info_dict[term]=definition
#      return trail_info_dict
#
#
# trail_info_dict = {}
#
# trails_stats_1 = trail_info_maker(url,trail_info_dict)
# trail_stats_2 = trail_info_maker(url2,trail_info_dict)
# find_number_of_trail_pages(url)
#
#
# def scrape_user_info(url):
#     num_pages = find_number_of_trail_pages(url)
#     user_list = []
#     for i in num_pages:
#         user_profile_urls = soup.find_all(href=re.compile('profile'))
#         user_list.extend([user.text for user in user_profile_urls])
#     return Counter(user_list)
