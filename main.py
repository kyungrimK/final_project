import yelp, zomato, google_places
import calculation, visualization

def main():
    # you have to run the code for 5 times to get all the data
    # it will take approximately 3 mins for each run
    yelp.adding_25_items_database("Ann Arbor")
    zomato.database(zomato.getZomatoInfo(zomato.api_key, "ann-arbor", zomato.restaurants_name, zomato.rating_reviews))
    google_places.adding_25_items_database()

if __name__ == "__main__":
	main()
