from bs4 import BeautifulSoup as bs
import csv
import os
import requests
import time
from secret import ACCESS_TOKEN
import re


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

    def get_song_lyrics(self, url):
        song_page = requests.get(url)

        # Make sure the page still exists
        if song_page.status_code == 404:
            return None

        page_html = bs(song_page.text, "html.parser")

        lyric_section = page_html.find('div', class_="lyrics")
        if not lyric_section:
            return None

        lyrics = self.clean_lyrics(lyric_section.get_text())

        time.sleep(self.sleep_time)

        return lyrics

    def clean_lyrics(self, lyrics):
        lyrics = re.sub('(\[.*?\])*', '', lyrics)
        lyrics = re.sub('(\{.*?\})*', '', lyrics)
        lyrics = re.sub('(\{.*?\])*', '', lyrics)
        lyrics = re.sub('(\[.*?\})*', '', lyrics)
        lyrics.strip()

        return lyrics.lower()


def scrape():
    genius = Genius_API()

    song_lengths = []

    songs = []
    page = 1
    while page:
        response = genius.get_beatles_songs(page=page)
        for song in response['songs']:
            if song['primary_artist']['id'] != genius.BEATLES_ID:
                continue

            songs.append([clean_title(song['title']), song['url']])

        page = response['next_page']

    for song in songs:
        # get song_lyrics
        lyrics = genius.get_song_lyrics(url=song[1])
        # save to .txt file
        if lyrics:
            with open("../data/unstructured/{}.txt".format(song[0]), "w") as lyric_file:
                lyric_file.write(lyrics)
                lyric_file.close()

            # Save length of song
            song_lengths.append(len(lyrics.split()))

    with open('../data/meta/song_lengths.csv', "w") as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        writer.writerows(song_lengths)


def clean_title(title):
    title = title.replace(' ', '_')
    title = title.replace('[', '')
    title = title.replace(']', '')
    title = title.replace('(', '')
    title = title.replace(')', '')
    title = title.replace('’', '')
    title = title.replace('+', '')
    title = title.replace('\"', '')
    title = title.replace('/', '')
    title = title.replace('\\', '')
    title = title.replace(',', '')
    title = title.replace('-', '')
    title = title.replace('*', '')
    title = title.replace('{', '')
    title = title.replace('}', '')
    title = title.replace('.', '')
    title = title.replace('!', '')
    title = title.replace('#', '')
    title = re.sub('_{2}', '_', title)

    return title

scrape()
