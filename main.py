import requests

def get_all_urls():
  r = requests.get("https://genius.com/api/artists/29743/songs?page=1 &sort=popularity")