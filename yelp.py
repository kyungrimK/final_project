import requests
import sqlite3
import os
import json

def get_business_data (location,offset):
    API_KEY= "e4mT1N4ZT1VWSQ7-XdwuW1K6bNOA4wo2hZtNAweEOSqnLR0X9YEPCQoM7RWi3eIR4WHpI1mWuHQ30Wc8OXl4RjGBK7DYxciUC8AYJsm1cp4RhyPiyZ14vwre0u3KX3Yx"
    URL="https://api.yelp.com/v3/businesses/search"
    HEADERS={'Authorization':'bearer %s' % API_KEY}
    PARAMS = {'limit':25,
        'offset':offset,
        'term':'restaurant',
        'location':location}
    
    #requesting to Yelp API
    api_return=requests.get(url=URL,params=PARAMS,headers=HEADERS)

    #converting from JSON to dictionary 
    #the result is sorted by best match
    businesses_info=api_return.json()

    #creating dictionary, restaurant/business name as key and price for value
    #if the price is not indicated, it should say 0 
    businesses_dict={}
    for business in businesses_info['businesses']:
        try: 
            businesses_dict[business['name']] = [business['rating'],business['review_count'],len(business['price'])]
        except:
            businesses_dict[business['name']] = [business['rating'],business['review_count'],0]
    return (businesses_dict)

# set up the database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# adds item to database
def adding_item_database(dictionary,curr_id_num):
    cur, conn = setUpDatabase('restaurants.db') 
    counts=curr_id_num+1
    for restaurant in dictionary.items():
    #for table "restaurants_names"
        cur.execute("INSERT OR IGNORE INTO restaurants_names (id,name) VALUES (?,?)",(counts,restaurant[0]))
    #for table "yelp_restaurants_info"
        cur.execute("SELECT restaurants_names.id FROM restaurants_names WHERE name=?",(restaurant[0], ))
        restaurant_id=cur.fetchone()
        cur.execute("INSERT OR IGNORE INTO yelp_restaurants_info (restaurant_id,rating,review_count,price_range) VALUES (?,?,?,?) ",(restaurant_id[0],restaurant[1][0],restaurant[1][1],restaurant[1][2]))
        counts+=1  
    conn.commit()

def adding_25_items_database(location): 
    cur, conn = setUpDatabase('restaurants.db') 
    # If table exists, it will return 1. If not, it will return 0.
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='restaurants_names'")
    returned_num=cur.fetchone() 
    if returned_num[0] == 1:
        #If exists, select restaurants ids and find its length
        cur.execute("SELECT restaurants_names.id FROM restaurants_names")
        ids=cur.fetchall()
        # If the length of items are greater than 0 and less than 101, add items to the existing table
        if len(ids)>0 and len(ids)<101:
            offset=len(ids)
            business_dict=get_business_data(location,offset)
            adding_item_database(business_dict,offset)
            # If there is more than 101 items, drop table 
        else: 
            cur.execute("DROP TABLE IF EXISTS restaurants_names")
            cur.execute("DROP TABLE IF EXISTS yelp_restaurants_info")
    # If there is no existing table, create table
    # then add items to the table
    else: 
        cur.execute("CREATE TABLE restaurants_names (id INTEGER PRIMARY KEY,name TEXT NOT NULL UNIQUE)")
        cur.execute("CREATE TABLE yelp_restaurants_info (restaurant_id INTEGER PRIMARY KEY,rating FLOAT,review_count INTEGER,price_range INTEGER)")
        business_dict=get_business_data(location,0)
        adding_item_database(business_dict,0)

