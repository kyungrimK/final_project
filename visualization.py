import matplotlib.pyplot as plt


def txtreader(filename):
    # reading txt file
    f=open(filename,"r")
    # inserting information from file into a list of tuples
    result = []
    for line in f.readlines():
        line = (line.rstrip()).split(', ')
        tup = tuple(line)
        result.append(tup)
    f.close()
    return result

def bargraph():
    # getting a returned list 
    ratings = txtreader("calculation_ratio")
    
    # creating visualization
    restaurants = []
    ratio = []
    # getting top 7 restaurants
    for i in ratings[:7]:
        restaurants.append(i[0])
        ratio.append(float(i[1]))
    # setting a bar graph
    plt.bar(restaurants, ratio, align="center", alpha=0.5, color=("#6CC2BD", "#5A809E", "#7C79A2", "#F57D7C", "#FFC1A6", "#FEE4C4", "#DEFEC4"))
    # naming the y axis
    plt.title('Top 7 Restaurants in Ann Arbor')
    plt.ylabel("Ratio")
    plt.ylim([4, 4.6])
    plt.xticks(fontsize = 8)
    
    plt.show()
        
    return 0

def scatterplot():
    # getting a returned list 
    avgs = txtreader("calculation_avgs")

    # creating visualization
    restaurants_rating = []
    restaurants_price = []
    # getting values 
    for i in avgs:
        restaurants_rating.append(float(i[1]))
        restaurants_price.append(float(i[2]))
    # setting a scatter plot
    plt.title('Scatterplot of the Average Price Range and Rating of Restaurants')
    plt.xlabel("Price Ranges")
    plt.ylabel("Ratings")
    plt.scatter(restaurants_price, restaurants_rating, color='hotpink')
    plt.show()

    return 0


def main():
    bargraph()
    scatterplot()

if __name__ == "__main__":
	main()
