from bs4 import BeautifulSoup
from scraping import getPageSourceFromGoogleSearch

def get_restaurants(query):
    html = getPageSourceFromGoogleSearch(query=query)
    
    class_restaurant_element = 'cXedhc'
    soup = BeautifulSoup(html, 'lxml')
    restaurant_infos = soup.find_all('div', class_=class_restaurant_element)
    #OSrXXb: class for name
    #yi40Hd YrbPuc: class for rating
    #RDApEe YrbPuc: number of ratings
    restaurants = []
    for restaurant_info in restaurant_infos:
        restaurant_info_details = restaurant_info.find('div', class_='rllt__details').find_all(string=True)

        img_url = restaurant_info.find('img', class_="YQ4gaf zr758c wA1Bge")["src"]
        restaurants.append({
            "name": restaurant_info_details[0],
            "rating_of_five": restaurant_info_details[1],
            "number_of_rating": restaurant_info_details[2][1:-1],
            "specific_location": restaurant_info_details[6],
            "current_state": restaurant_info_details[7],
            "img_url": img_url
        })
    
    return restaurants

def getWeather(query):
    html = getPageSourceFromGoogleSearch(query=query)
    soup = BeautifulSoup(html, 'lxml')
    weather_info = soup.find('div', id='wob_wc')
    return {
        "location": weather_info.find(id="wob_loc").text,
        "date": weather_info.find(id="wob_dts").text,
        "state": weather_info.find(id="wob_dc").text,
        "precipitation": "Precipitation: " + weather_info.find(id="wob_pp").text,
        "humidity": "Humidity:" + weather_info.find(id="wob_pp").text,
        "wind": "Wind: " + weather_info.find(id="wob_ws").text,
        "temperature": "Temperature: " + weather_info.find(id="wob_tm").text,
        "img_url": weather_info.find(id="wob_tci")["src"]
    }
