import requests
import sqlite3
import os
import json

# [PART 2]: Gather the data and save it to a single database

# Access and store at least 100 items in your database from each API/website (10 points) in at least one table per API/website. 
# For at least one API you must have two tables that share a key (20 points)
# You must not have duplicate data in your database! Do not split data from one table into two! 
# Also, there should be only one database!

# You must limit how much data you store from an API into the database each time you execute your code to 25 or fewer items (60 points). 
# The data must be stored in a SQLite database. 
# This means that you must run the code that stores the data multiple times to gather at least 100 items total without duplicating existing data or changing it.

#######################################################
################### Yelp Fusion API ###################
#######################################################

def get_business_data (location,offset=0):
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
    #if the price is not indicated, it should say "none" 
    businesses_dict={}
    for business in businesses_info['businesses']:
        businesses_dict[business['name']] = [business['rating'],business['review_count']]
    return (businesses_dict)

# set up the database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def database(location,offset=0): 
    # create database and create table
    cur, conn = setUpDatabase('restaurants.db') 

    cur.execute("DROP TABLE IF EXISTS restaurants_names")
    cur.execute("CREATE TABLE restaurants_names (id INTEGER PRIMARY KEY,name TEXT)")

    cur.execute("DROP TABLE IF EXISTS yelp_restaurants_info")
    cur.execute("CREATE TABLE yelp_restaurants_info (restaurant_id INTEGER PRIMARY KEY,rating FLOAT,review_count INTEGER)")

    # insert values to the table
    num_restaurants=0
    for n in range(4):
        dictionary=get_business_data(location,num_restaurants)
        counts=num_restaurants+1
        for restaurant in dictionary.items():
            #for table "restaurants_names"
            cur.execute("INSERT OR IGNORE INTO restaurants_names (id,name) VALUES (?,?)",(counts,restaurant[0]))
            #for table "yelp_restaurants_info"
            cur.execute("SELECT restaurants_names.id FROM restaurants_names WHERE name=?",(restaurant[0], ))
            restaurant_id=cur.fetchone()
            cur.execute("INSERT OR IGNORE INTO yelp_restaurants_info (restaurant_id,rating,review_count) VALUES (?,?,?)",(restaurant_id[0],restaurant[1][0],restaurant[1][1]))
            counts+=1
        num_restaurants+=25
        conn.commit()

def main (): 
    database("Ann Arbor")


if __name__ == "__main__":
    main()