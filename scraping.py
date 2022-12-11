import urllib
from selenium import webdriver

def getPageSourceFromGoogleSearch(query):
    query = urllib.parse.quote_plus(query)
    url = "https://google.com/search?q=" + query
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome(options=option)
    browser.get(url)
    return browser.page_source

    