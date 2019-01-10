from bs4 import BeautifulSoup
import requests
import csv
import math
math.ceil(346/100)

def scrape_all_regions(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content)
    items = soup.find_all('a',class_ = "regionLink")
    links = [link.get('href') for link in items]

    return links



def find_number_of_trail_pages(region):
    trails =  region + 'trails/'
    r = requests.get(trails)
    soup =  BeautifulSoup(r.content)
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
            soup = BeautifulSoup(r.content)
            trail_rows = soup.find_all('a',{'class':'green'})
            trail_list.extend([link.get('href') for link in trail_rows])
            print('scraped',str(i*100),'trails!')
    return trail_list


def write_to_csvs(region):
    trails = scrape_region(region)
    name = re.findall('\w+/+$',region)[0][:-1]
    with open(name + '_trails.csv','w') as f:
        wrtr = csv.writer(f)
        for trail in trails:
            wrtr.writerow([trail])
    print('Finished scraping {}!'.format(name))



def main():

    regions = scrape_all_regions('https://www.trailforks.com/trails/')
    # with open('regions.csv','w') as f:
    #     write = csv.writer(f)
    #     for reg in regions:
    #         write.writerow([reg])

    # with open('regions.csv','r') as f:
    #     regions = [reg.strip() for reg in f]

    for reg in regions:
        write_to_csvs(reg)








#
# def trail_info_maker(box):
#      ...:     trail_info_dict = {}
#      ...:     for item in box:
#      ...:         term = item.find(class_='term').text.strip()
#      ...:         definition = item.find(class_='definition').text.strip()
#      ...:         trail_info_dict[term]=definition
#      ...:     return trail_info_dict
