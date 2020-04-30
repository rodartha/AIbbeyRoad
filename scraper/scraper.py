from bs4 import BeautifulSoup as bs
import selenium
import csv
import os
from rauth import OAuth1Service
import requests
import time
from secret import ACCESS_TOKEN


class Genius_API():

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'application': 'AIbbeyRoad',
            'User-Agent': 'https://github.com/rodartha',
            'authorization': 'Bearer ' + ACCESS_TOKEN
        }
        self.root = 'https://api.genius.com/'

        # Necessary so the api is Doxing the genius api
        self.sleep_time = 0.1

        self.timeout = 7

        # Genius artist id for the beatles
        self.BEATLES_ID = 586

    def get_beatles_songs(self, page=1):
        uri = self.root + "artists/{}/songs".format(self.BEATLES_ID)
        params = {
            'text_format': 'plain',
            'sort': 'title',
            'per_page': 30,
            'page': page
        }

        response  = self.session.request('GET', uri, timeout=self.timeout, params=params)
        time.sleep(self.sleep_time)

        return response.json()['response']


def scrape():
    genius = Genius_API()

    """
    response = genius.get_beatles_songs()

    #print(response['songs'][0])

    print(response['next_page'])
    """
    songs = []
    page = 1
    while page:
        response = genius.get_beatles_songs(page=page)
        for song in response['songs']:
            title = song['title'].replace(' ', '_')
            title = title.replace("’", '')
            title = title.replace('[', '')
            title = title.replace(']', '')
            songs.append([title, song['id']])

        page = response['next_page']

    for song in songs:
        # get song_lyrics
        lyrics = genius.get_song_lyrics(id=song[1])
        # save to .txt file
        lyric_file = open("data/{}.txt".format(song[0]), "w")
        lyric_file.write(lyrics)
        lyric_file.close()


scrape()
