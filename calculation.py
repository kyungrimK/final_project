import sqlite3
import os

def setUpData(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

# finding the average
def average(avgdict):
    avg_dict = {}
    for key in avgdict:
        avg_dict[key] = round((avgdict[key][0] + avgdict[key][1] + avgdict[key][2])/len(avgdict[key]), 2)      
    return avg_dict 

def calculate():
    cur, conn = setUpData('restaurants.db') 

    # calculate rating average
    rating_dict={}
    cur.execute("SELECT restaurants_names.name, yelp_restaurants_info.restaurant_id , zomato_restaurants_info.restaurant_id, google_restaurants_info.restaurant_id, yelp_restaurants_info.rating, zomato_restaurants_info.rating , google_restaurants_info.rating\
                FROM yelp_restaurants_info, zomato_restaurants_info, google_restaurants_info\
                JOIN restaurants_names ON yelp_restaurants_info.restaurant_id=restaurants_names.id\
                WHERE yelp_restaurants_info.restaurant_id=zomato_restaurants_info.restaurant_id AND yelp_restaurants_info.restaurant_id=google_restaurants_info.restaurant_id AND yelp_restaurants_info.rating>0 AND zomato_restaurants_info.rating>0 AND google_restaurants_info.rating>0")

    for row in cur:
        rating_dict[row[0]] = [row[4], row[5], row[6]]
    avg_rating_dict = average(rating_dict)
    
    # calculate prive average
    price_dict={}
    cur.execute("SELECT restaurants_names.name, yelp_restaurants_info.restaurant_id , zomato_restaurants_info.restaurant_id, google_restaurants_info.restaurant_id, yelp_restaurants_info.price_range, zomato_restaurants_info.price_range , google_restaurants_info.price\
                FROM yelp_restaurants_info, zomato_restaurants_info, google_restaurants_info\
                JOIN restaurants_names ON yelp_restaurants_info.restaurant_id=restaurants_names.id\
                WHERE yelp_restaurants_info.restaurant_id=zomato_restaurants_info.restaurant_id AND yelp_restaurants_info.restaurant_id=google_restaurants_info.restaurant_id AND yelp_restaurants_info.price_range>0 AND zomato_restaurants_info.price_range>0 AND google_restaurants_info.price>0")

    for row in cur:
        price_dict[row[0]] = [row[4], row[5], row[6]]
    avg_price_dict = average(price_dict)
    
    conn.commit()

    # format avg_rating_dict and avg_price_dict into one dictionary
    name_r_p_dict = {}
    for key in avg_price_dict:
        if key in avg_rating_dict.keys():
            name_r_p_dict[key] = [avg_rating_dict[key], avg_price_dict[key]]
    return name_r_p_dict

def find_ratio():
    dictionary=calculate()
    ratio_dict={}
    for item in dictionary.items(): 
        rating=item[1][0]
        price=item[1][1]
        # as rating increases and price decreases, the ratio will be greater
        # high ratio indicates better restaurants than other
        ratio=round((rating/price),3)
        ratio_dict[item[0]]=ratio
    #sorting the dictionary with its value(ratio)
    final_dict=sorted(ratio_dict.items(),key=lambda x:x[1], reverse=True)
    return final_dict

def write_txt(dictionaries):
    # writing out the calculated data to a file as text
    string=str(dictionaries)
    f=open("calculation_result","w")
    f.write(string)
    f.close()

def main():
    print(find_ratio())
    write_txt(find_ratio())

if __name__ == "__main__":
	main()
