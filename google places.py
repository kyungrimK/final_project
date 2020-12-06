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
    ########results=get_restaurant_info()
    results = {'The Jagged Fork': [2, 4.6], 'Frita Batidos': [2, 4.7], 'LaLa’s': [2, 3.6], "Anna's House - Ann Arbor": [2, 4.2], "Zingerman's Delicatessen": [2, 4.6], 'Bao Boys': [0, 4.9], 'Northside Grill': [2, 4.5], 'Chapala Mexican Restaurant': [2, 4.1], "Sava's": [2, 4.5], 'Juicy Kitchen': [2, 4.7], 'Yee Siang Dumplings': [1, 4.2], 'eat': [0, 4], 'Tomukun Noodle Bar': [2, 4.5], 'Hola Seoul': [0, 0], "Dimo's Deli and Donuts": [1, 4.8], "Monahan's Seafood Market": [0, 4.6], 'Biercamp': [2, 4.8], 'Ricewood': [2, 4.8], 'Jolly Pumpkin Cafe & Brewery': [2, 4.5], 'The Songbird Cafe': [0, 4.9], 'First Bite': [0, 0], 'Tomukun Korean Barbeque': [2, 4.5], 'Isalita': [2, 4.4], 'Cardamom': [0, 4.1], 'Spencer': [0, 0.0], 'Loomi Cafe': [0, 4.6], 'Avalon Cafe and Kitchen': [2, 4.4], "Zingerman's Roadhouse": [3, 4.4], 'Mani Osteria & Bar': [2, 4.5], 'Barry Bagels Ann Arbor': [1, 4.5], 'Detroit Street Filling Station': [2, 4.7], 'Tacos El Mariachi Loco': [2, 4.2], 'Aventura': [0, 4.5], 'Momo Sushi': [2, 4.2], "Aamani's Smokehouse & Pizza": [0, 5], "Weber's Restaurant": [0, 4.4], "Chela's": [2, 4.5], 'Blue LLama Jazz Club': [0, 4.8], "Knight's Steak House": [3, 4.4], "Angelo's Restaurant": [0, 0], 'Pacific Rim': [0, 0], 'Cafe Zola': [2, 4.5], 'V Kitchen Vietnamese Cuisine': [0, 4.3], 'The Chop House': [0, 3.9], 'Lan City Hand Pulled Noodle': [1, 4.6], 'JJ’s Crab House Hibachi & Seafood': [1, 4.4], 'Jim Brady’s': [2, 4.3], 'Taste Kitchen': [0, 4.4], 'Bewon': [2, 4.6], 'Mediterrano': [2, 4.4], 'The Lunch Room - Bakery & Cafe': [2, 4.7], 'Fresh Forage': [2, 4.6], "Nick's Original House of Pancakes": [2, 4.5], 'Gandy Dancer': [0, 3.3], 'Village Kitchen': [2, 4.7], 'Afternoon Delight': [2, 4.6], 'Of Rice & Men': [0, 4.8], "Frank's Restaurant": [0, 0], 'Jerusalem Garden': [0, 3.5], 'The West End Grill': [4, 4.4], 'Fleetwood Diner': [1, 4.3], 'Amadeus': [0, 5], "Kang's Korean Restaurant": [0, 2.7], 'Broadway Cafe & Hoagie': [1, 4.6], 'York': [0, 0.0], 'Moon Cafe': [0, 0], 'Seva Restaurant': [2, 3.7], 'Poke Fish': [2, 4.7], 'Arirang': [0, 3.9], 'Dalat': [0, 0.0], 'Jamaican Jerk Pit': [2, 4.6], 'Everest Sherpa Restaurant': [2, 4.5], 'Seoul Street': [1, 4], "Bell's Diner": [1, 4.6], 'Syrian Cuisine & Exotic Bakeries': [0, 4.8], 'Maize N Blue Deli': [2, 4.6], "Ashley's Restaurant": [0, 0.0], 'Hutkay Fusion': [1, 4.6], 'Social House South U': [0, 4.4], 'Miss Kim': [3, 4.4], 'Haymaker Public House': [2, 4.3], 'Vinology Restaurant & Event Space': [0, 4.4], "KOSMO'S Bop Shop": [1, 4.8], 'TAQ - Taqueria Restaurant & Bar': [1, 4.2], 'Zamaan Cafe': [2, 4.6], "Star's Cafe": [1, 4.8], 'Palm Palace': [2, 4.5], 'Cosa Sabrosa': [0, 4.7], "Metzger's German Restaurant": [2, 4.6], 'Rich Jc Korean Restaurant': [0, 4.5], 'Bellflower': [0, 0.0], 'Bopjib': [0, 4.7], 'Poke Poke - Sushi Unrolled': [0, 4.5], 'Shake Shack': [3, 3.9], 'Madras Masala': [2, 4.2], 'Sushi Town': [0, 3.8], 'RAPPOURT': [2, 4.6], 'Share Wine Lounge and Small Plate Bistro': [4, 4.2], "Pilar's Tamales": [1, 4.8]}

    # create database and create table
    cur, conn = setUpDatabase('restaurants.db') 

    cur.execute("DROP TABLE IF EXISTS google_restaurants_info")
    cur.execute("CREATE TABLE google_restaurants_info (restaurant_id INTEGER PRIMARY KEY,price INTEGER,rating FLOAT)")

    # insert values to the table
    for n in range(len(results)+1):
        for restaurant in results.items():
            cur.execute("SELECT restaurants_names.id FROM restaurants_names WHERE name=?",(restaurant[0], ))
            restaurant_id=cur.fetchone()
            cur.execute("INSERT OR IGNORE INTO google_restaurants_info (restaurant_id,price,rating) VALUES (?,?,?)",(restaurant_id[0],restaurant[1][0],restaurant[1][1]))    
        conn.commit()
    

def main (): 
    print(database())


if __name__ == "__main__":
    main()