import zomato
import yelp
import sqlite3
import os

def setUpData(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

def average(avgdict):
    avg_dict = {}
    for key in avgdict:
        avg_dict[key] = (avgdict[key][0] + avgdict[key][1])/len(avgdict[key])      
    return avg_dict 

def calculate():
    cur, conn = setUpData('restaurants.db') 

    # calculate rating average
    rating_dict={}
    cur.execute("SELECT yelp_restaurants_info.restaurant_id, zomato_restaurants_info.restaurant_id, yelp_restaurants_info.rating, zomato_restaurants_info.rating "+
                "FROM yelp_restaurants_info, zomato_restaurants_info "+ 
                "WHERE yelp_restaurants_info.restaurant_id=zomato_restaurants_info.restaurant_id AND yelp_restaurants_info.rating>0 AND zomato_restaurants_info.rating>0")
    for row in cur:
        rating_dict[row[0]] = [row[2], row[3]]
    avg_rating_dict = average(rating_dict)
    
    # calculate prive average
    price_dict={}
    cur.execute("SELECT yelp_restaurants_info.restaurant_id, zomato_restaurants_info.restaurant_id, yelp_restaurants_info.price_range, zomato_restaurants_info.price_range "+
                "FROM yelp_restaurants_info, zomato_restaurants_info "+
                "WHERE yelp_restaurants_info.restaurant_id= zomato_restaurants_info.restaurant_id AND yelp_restaurants_info.price_range>0 AND zomato_restaurants_info.price_range>0")
    for row in cur:
        price_dict[row[0]] = [row[2], row[3]]
    avg_price_dict = average(price_dict)
    
    conn.commit()
    return avg_rating_dict, avg_price_dict


def main():
    setUpData("restaurants.db")
    print(calculate())


if __name__ == "__main__":
	main()
