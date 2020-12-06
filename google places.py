import requests
import sqlite3
import os
import json

API_KEY="Api_key"

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
    #this returns price level and rating as a list
    api_return=requests.get(url=URL,params=PARAMS)
    dictionary=api_return.json()
    values=dictionary['candidates']

    #if both price level and rating doesn't exist, replace both as 0
    if values == []:
        return [0,0.0]
    elif bool(values[0]) == False: 
        return [0,0.0]
    
    #if more than one of them exists
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


def database(): 
    # get returned restaurants' info
    results=get_restaurant_info()

    # create database and create table
    cur, conn = setUpDatabase('restaurants.db') 

    cur.execute("DROP TABLE IF EXISTS google_restaurants_info")
    cur.execute("CREATE TABLE google_restaurants_info (restaurant_id INTEGER PRIMARY KEY,price INTEGER,rating FLOAT)")

    # insert values to the table
    for n in range(len(results)):
        for restaurant in results.items():
            cur.execute("SELECT restaurants_names.id FROM restaurants_names WHERE name=?",(restaurant[0], ))
            restaurant_id=cur.fetchone()
            cur.execute("INSERT OR IGNORE INTO google_restaurants_info (restaurant_id,price,rating) VALUES (?,?,?)",(restaurant_id[0],restaurant[1][0],restaurant[1][1])) 
        conn.commit()
    
def main (): 
    database()


if __name__ == "__main__":
    main()
