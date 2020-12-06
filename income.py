import requests
import sqlite3
import json
import os

restaurants_name=[]
rating_reviews=[]
api_key = "17fe0fd42a0a236c6e6b4a7966ab24ae"

"""def getData(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM restaurants_names")
    for row in cur:
        restaurants_name.append(row[1])
    return restaurants_name"""

def setUpData(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

"""def getZomatoInfo(api_key, location, restaurants_name, rating_reviews):

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
        r2 = json.loads(req2.text)
        if r2['results_found'] == 0:
            rating_reviews.append((item, 0.0, 0))
            continue
        else:
            rating_reviews.append((r2['restaurants'][0]['restaurant']['name'], float(r2['restaurants'][0]['restaurant']['user_rating']['aggregate_rating']), r2['restaurants'][0]['restaurant']['user_rating']['votes']))
    print(rating_reviews)
    return rating_reviews"""

def database(rating_reviews):
    cur, conn = setUpData("restaurants.db")

    cur.execute("DROP TABLE IF EXISTS zomato_restaurants_info")
    cur.execute("CREATE TABLE zomato_restaurants_info (restaurant_id INTEGER PRIMARY KEY, name TEXT, rating FLOAT, reviews_count INTEGER)")
    rating_reviews = [('Frita Batidos', 3.7, 4), ('Bao Boys', 3.7, 4), ('Yee Siang Dumplings', 3.7, 4)]
    count = 0
    for i in rating_reviews:
        # get restaurant_id from yelp_restaurants_names
        print(i[0])
        cur.execute("SELECT restaurants_names.id FROM restaurants_names WHERE name=?", (i[0],) )
        restaurant_id = cur.fetchone()
        cur.execute("INSERT INTO zomato_restaurants_info (restaurant_id, name, rating, reviews_count) VALUES (?,?,?,?)",(restaurant_id[count], i[0], i[1], i[2]))
        count += 1
    conn.commit()


def main():
    database(rating_reviews)
    #database(getZomatoInfo(api_key, "ann-arbor", restaurants_name, rating_reviews))
    #data = getZomatoInfo(api_key, "ann-arbor", restaurants_name)


if __name__ == "__main__":
	main()