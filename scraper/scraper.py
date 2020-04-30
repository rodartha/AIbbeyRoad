from bs4 import BeautifulSoup as bs
import selenium
import csv
import os

driver = webdriver.Chrome()

driver.get('https://genius.com/artists/The-beatles')

# FIXME: may need to find this by class or something else
display_songs_button = driver.find_element_by_name("Show all songs by The Beatles ")

display_songs_button.click()

# NOTE: may be able to do all of this by interacting with the genius api rather than scrapping their website