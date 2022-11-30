import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os


load_dotenv()
ask = input("What year you would like to travel to in YYYY-MM-DD format. ")
URL = "https://www.billboard.com/charts/hot-100/"

ID = os.getenv('MY_ID')
SECRET = os.getenv('MY_SECRET')

data = requests.get(URL+ask)
datas = data.text
soup = BeautifulSoup(datas, "html.parser")
a = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
b = [i.getText().strip("\n\t") for i in a]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback",
        client_id=ID,
        client_secret=SECRET,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = ask.split("-")[0]
for song in b:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

play_list = sp.user_playlist_create(user=user_id, name=f"{ask} Billboard 100", public=False)
sp.user_playlist_add_tracks(user=user_id, playlist_id=play_list["id"], tracks=song_uris)
