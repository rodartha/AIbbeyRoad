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

    num_lines = []

    songs = []
    page = 1
    while page:
        response = genius.get_beatles_songs(page=page)
        for song in response['songs']:
            if song['primary_artist']['id'] != genius.BEATLES_ID:
                continue

            cleaned_title = clean_title(song['title'])

            # remove the beatles' movie scripts
            if "script" in cleaned_title:
                continue
            songs.append([cleaned_title, song['url']])

        page = response['next_page']

    print("Found {} songs".format(len(songs)))

    max_line_length = 0

    for song in songs:
        # get song_lyrics
        lyrics = genius.get_song_lyrics(url=song[1])
        # save to .txt file
        if lyrics:
            # Skip this file if it contains this
            if "lyrics for this song have yet to be released. please check back once the song has been released." in lyrics:
                continue

            with open("../data/unstructured/{}.txt".format(song[0]), "w") as lyric_file:
                lyric_file.write(lyrics)
                lyric_file.close()

            # Save length of song in words
            song_lengths.append(len(lyrics.replace('\n', '').split()))

            # Save length of song in lines
            num_lines.append(len(lyrics.split('\n')))

            lines = lyrics.split('\n')
            for line in lines:
                # +5 because of the newline character and the possible 3 digit line encoding
                if len(line) + 5 > max_line_length:
                    max_line_length = len(line) + 5


    print("Done Writing Song Lyrics")

    with open('../data/meta/song_lengths.csv', "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(song_lengths)

    with open('../data/meta/line_lengths.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(num_lines)

    with open('../data/meta/longest_line.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(max_line_length)

    print("Done Writing Meta Data")


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

    title = title.lower()

    return title

scrape()
