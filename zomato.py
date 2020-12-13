import requests
import sqlite3
import json
import os

restaurants_name=[]
rating_reviews=[]
api_key = "d6c597785fed953a02eba404f366d0bf"

def setUpData(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

def getZomatoInfo(api_key, location, restaurants_name, rating_reviews):

    # get restaurant names from restaurants_names.db
    cur, conn = setUpData('restaurants.db') 
    cur.execute("SELECT * FROM restaurants_names")
    for row in cur:
        restaurants_name.append(row[1])

    # get location id
    url = "https://developers.zomato.com/api/v2.1/locations"
    header1={"User-agent": "curl/7.43.0", 
            "Accept": "application/json", 
            "user-key": api_key}
    params1={'query': location}
    req1 = requests.get(url, headers=header1, params = params1)
    r1 = json.loads(req1.text)
    print (r1["location_suggestions"][0]["entity_id"], r1["location_suggestions"][0]["entity_type"])

    # get restaurant details
    url_detail = "https://developers.zomato.com/api/v2.1/search" 
    for item in restaurants_name:
        params2={'entity_id': r1["location_suggestions"][0]["entity_id"], 'entity_type': r1["location_suggestions"][0]["entity_type"], "q": item}
        req2 = requests.get(url_detail, headers=header1, params=params2)
        try: 
            r2 = json.loads(req2.text)
            if r2['results_found'] == 0:
                rating_reviews.append((item, 0.0, 0, 0))
                continue
            else:
                rating_reviews.append((item, float(r2['restaurants'][0]['restaurant']['user_rating']['aggregate_rating']), r2['restaurants'][0]['restaurant']['user_rating']['votes'], r2['restaurants'][0]['restaurant']['price_range']))
        except: 
            return rating_reviews
    return rating_reviews

def database(rating_reviews):
    
    cur, conn = setUpData("restaurants.db")
    # create a table zomato_restaurants_info
    cur.execute("CREATE TABLE IF NOT EXISTS zomato_restaurants_info (restaurant_id INTEGER PRIMARY KEY, name TEXT, rating FLOAT, reviews_count INTEGER, price_range INTEGER)")

    count = 0
    for i in rating_reviews:
        if count == 25:
            break
        # get restaurant_id from yelp_restaurants_names
        cur.execute("SELECT name FROM zomato_restaurants_info WHERE name = ?", (i[0], ))
        if len(cur.fetchall()) == 0:
            cur.execute("SELECT restaurants_names.id FROM restaurants_names WHERE name=?", (i[0],) )
            restaurant_id = cur.fetchone()
            cur.execute("INSERT OR IGNORE INTO zomato_restaurants_info (restaurant_id, name, rating, reviews_count, price_range) VALUES (?,?,?,?,?)", (restaurant_id[0], i[0], i[1], i[2], i[3]))
            count += 1
    conn.commit()
