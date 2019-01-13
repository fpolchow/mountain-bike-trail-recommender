from pymongo import MongoClient
from scraping_trails import *
import glob


client = MongoClient('localhost',27017)
db = client.mountain_biking
regions = glob.glob('./data/regions/*.csv')

def add_to_database(region):
    print('-------------------------------')
    print(region)
    print('-------------------------------')
    with open(region,'r') as f:
        trails = [reg.strip() for reg in f]

        for trail in trails:
            print(trails)
            db.biking_trails.insert_one(trail_info_maker(trail))
    return None

if __name__ == "__main__":
    for region in regions:
        add_to_database(region)
