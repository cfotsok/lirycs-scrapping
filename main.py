import requests
from pprint import pprint

from bs4 import BeautifulSoup


def extract_lyrics(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        print("Unable to load the page")
        return []
    soup = BeautifulSoup(r.content, "html.parser")
    lyrics = soup.find_all("div", class_="Lyrics__Container-sc-1ynbvzw-1 kUgSbL")
    lyrics = [item.stripped_strings for item in lyrics]

    lyrics = [[elt.split() for elt in item] for item in lyrics]
    all_words = []
    for elt in lyrics:
        for sentence in elt:
            all_words.extend([word.strip(",").strip(".") for word in sentence if len(word) > 2])

    pprint(all_words)


def get_all_urls():
    page_number = 1
    links = []
    while True:
        r = requests.get(f"https://genius.com/api/artists/29743/songs?page={page_number}&sort=popularity")
        if r.status_code == 200:
            response = r.json().get("response", {})
            next_page = response.get("next_page")

            songs = response.get("songs")
            links.extend([song.get("url") for song in songs])

            page_number += 1

            if not next_page:
                print("No more pages to fetch")
                break
    return links


urls = get_all_urls()
extract_lyrics(url="https://genius.com/Patrick-bruel-perlimpinpin-lyrics")
