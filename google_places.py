import requests
import sqlite3
import os
import json

API_KEY="AIzaSyBO4cyhLKuHxsvA2byE73HI1oZzCsiLkO0"

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

def get_restaurant_names():
    # get restaurant names from restaurants_names.db
    #return as a list
    restaurant_names=[]
    cur, conn = setUpDatabase('restaurants.db') 
    cur.execute("SELECT restaurants_names.name FROM restaurants_names")
    for restaurant in cur:
        restaurant_names.append(restaurant[0])
    return restaurant_names

def restaurant_search (input):
    PARAMS = {'key':API_KEY,
        'input':input,
        'inputtype':'textquery',
        'fields':'rating,price_level'}
    URL=f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"

    #requesting to Google Places API
    #this finds a list of price level and rating
    api_return=requests.get(url=URL,params=PARAMS)
    dictionary=api_return.json()
    values=dictionary['candidates']

    #if both price level and rating doesn't exist, replace both as 0
    if values == []:
        return [0,0.0]
    elif bool(values[0]) == False: 
        return [0,0.0]
    
    #if only rating exists, replace price level as 0 
    else:
        info=values[0]
        if "price_level" not in info.keys():
            info["price_level"]=0 
        return [info["price_level"],info["rating"]]
        
# uses the returned restaurant list from database
# finds price level and rating for each restaurant
# returns all of the info into dictionary
def get_restaurant_info():
    restaurant_dict={}
    for restaurant in get_restaurant_names():
        result=restaurant_search(restaurant)
        restaurant_dict[restaurant]=result
    return(restaurant_dict)

def adding_items_database(dictionary):
    # insert values to the table
    cur, conn = setUpDatabase('restaurants.db') 
    for restaurant in dictionary.items():
        cur.execute("SELECT restaurants_names.id FROM restaurants_names WHERE name=?",(restaurant[0], ))
        restaurant_id=cur.fetchone()
        cur.execute("INSERT OR IGNORE INTO google_restaurants_info (restaurant_id,price,rating) VALUES (?,?,?)",(restaurant_id[0],restaurant[1][0],restaurant[1][1])) 
    conn.commit()

def adding_25_items_database(): 
    # get returned restaurants' info
    results=get_restaurant_info()
    items=results.items()
    
    cur, conn = setUpDatabase('restaurants.db') 

    # If table exists, it will return 1. If not, it will return 0.
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='google_restaurants_info'")
    returned_num=cur.fetchone() 
    if returned_num[0] == 1:
        #If exists, select restaurants ids and find its length
        cur.execute("SELECT google_restaurants_info.restaurant_id FROM google_restaurants_info")
        ids=cur.fetchall()
        current_num=len(ids)
        # If the length of items are greater than 0 and less than 101, add items to the existing table
        if current_num>0 and current_num<101:
            new_dict={}
            n=current_num
            item_lst=list(items)
            for item in item_lst[n:n+25]:
                if n==n+25:
                    break
                else:
                    key=item[0]
                    value=item[1]
                    new_dict[key]=value
                    n+=1
            adding_items_database(new_dict)
            # If there is more than 101 items, drop table 
        else: 
            cur.execute("DROP TABLE IF EXISTS google_restaurants_info")
    # If there is no existing table, create table
    # then add items to the table
    else: 
        cur.execute("CREATE TABLE google_restaurants_info (restaurant_id INTEGER PRIMARY KEY,price INTEGER,rating FLOAT)")
        new_dict={}
        n=0
        for item in items:
            if n==25:
                break
            else:
                key=item[0]
                value=item[1]
                new_dict[key]=value
                n+=1
        adding_items_database(new_dict)
