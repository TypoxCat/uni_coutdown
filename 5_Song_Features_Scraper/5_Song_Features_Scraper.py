# Get the authority to read Spotify account
# Input one user playlist url link
# extract each track in playlist's ID
# get the features from musicstax by web scraping
# store in object
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from selenium.webdriver.common.by import By
from selenium import webdriver

URL = input("Link to playlist: ")
BASE_URL = "https://musicstax.com/track/na/"
YOUR_CLIENT_ID = ""
YOUR_CLIENT_SECRET = ""

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=YOUR_CLIENT_ID,
    client_secret=YOUR_CLIENT_SECRET,
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-read-private user-library-read",
    open_browser=False
))

def get_playlist_ID(url):
    return url.split("playlist/")[1].split("?")[0]

def get_tracks_ID(playlist_id):
    track_ids = []
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for item in tracks:
        track = item['track']
        if track and track['id']:
            track_ids.append(track['id'])
    
    return track_ids

def get_features(track_ID):
    # set chrome options to: allow multiple download, save in a new directory
    chrome_options = webdriver.ChromeOptions()
    
    # run the webdriver headlessly (not open the web window)
    # chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # create the webdriver object.
    driver = webdriver.Chrome(options = chrome_options)

    # run the web and download
    FEATURES = [
        "Tempo", "Key", "Loudness", "Time Signature",
        "Popularity", "Energy", "Danceability", "Positiveness",
        "Speechiness", "Liveness", "Acousticness", "Instrumentalness"
    ]
    all_tracks_data = []

    for id in track_ID:
        song_URL = f"{BASE_URL}{id}"
        print(song_URL)
        try:
            driver.get(song_URL)
            time.sleep(6)
            track_data = {}

            # Get the features data
            title = driver.find_element(By.CLASS_NAME, "song-title").text.strip()
            artist = driver.find_element(By.CLASS_NAME, "song-artist").text.strip()

            stats1 = driver.find_elements(By.CLASS_NAME, "song-fact-container-stat")
            values1 = [stat.text.strip() for stat in stats1 if stat.text.strip()]

            stats2 = driver.find_elements(By.CLASS_NAME, "song-bar-statistic-number")
            values2 = [stat.text.strip() for stat in stats2 if stat.text.strip()]

            values = values1 + values2

            if len(values) == len(FEATURES):
                track_data = {
                    "Title": title,
                    "Artist": artist,
                    "Track ID": id,
                }
                track_data.update(dict(zip(FEATURES, values)))
                all_tracks_data.append(track_data)

            else:
                print(f"Skipping {track_ID} due to missing/extra features.")

        except Exception as e:
            print(f"Error: {e}")
    
    driver.quit()
    print(all_tracks_data)

ID = get_playlist_ID(URL)
track_ID = get_tracks_ID(ID)
get_features(track_ID)  
