import collections
import json

import requests
from pprint import pprint

from bs4 import BeautifulSoup


def extract_lyrics(url: str, word_length=5 ):
    r = requests.get(url)
    if r.status_code != 200:
        print("Unable to load the page")
        return []
    print(f"Fetching url: {url}")
    soup = BeautifulSoup(r.content, "html.parser")
    lyrics = soup.find_all("div", class_="Lyrics__Container-sc-1ynbvzw-1 kUgSbL")
    lyrics = [item.stripped_strings for item in lyrics]

    lyrics = [[elt.split() for elt in item] for item in lyrics]
    all_words = []
    for elt in lyrics:
        for sentence in elt:
            all_words.extend([word.strip(",").strip(".").lower() for word in sentence if
                              len(word) > word_length and "[" not in word and "]" not in word])

    return all_words


def get_all_urls():
    page_number = 1
    links = []
    while True:
        r = requests.get(f"https://genius.com/api/artists/2300/songs?page={page_number}&sort=popularity")
        if r.status_code == 200:
            print(f"Fetching page {page_number}")
            response = r.json().get("response", {})
            next_page = response.get("next_page")

            songs = response.get("songs")
            links.extend([song.get("url") for song in songs])

            page_number += 1

            if not next_page:
                print("No more pages to fetch")
                break
    return links


def get_all_words():
    urls = get_all_urls()
    words = []
    for url in urls:
        lyrics = extract_lyrics(url)
        words.extend(lyrics)

    with open("datas-adele.json", "w") as f:
        json.dump(words, f, indent=4)

    counter = collections.Counter(words)
    most_common_words = counter.most_common(15)

    pprint(most_common_words)


get_all_words()
