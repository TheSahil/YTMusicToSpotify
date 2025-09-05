import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv
import time
from dotenv import load_dotenv
import os
load_dotenv()


# --- Spotify credentials ---
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI") # Must match Spotify app settings

# --- Initialize Spotify client ---
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-library-read"
))

# --- Read original CSV ---
with open("liked_songs.csv", newline='', encoding='utf-8') as csvfile:
    reader = list(csv.DictReader(csvfile))
    total_songs = len(reader)
    print(f"Total songs in CSV: {total_songs}")

missing_songs = []

# Spotify API allows checking 50 tracks at a time
for idx, row in enumerate(reader, start=1):
    raw = row['Title']
    if '-' in raw:
        artist_part, title_part = raw.rsplit('-', 1)
        artist = artist_part.strip()
        title = title_part.strip()
    else:
        title = raw.strip()
        artist = row['Artist'].strip() if 'Artist' in row else ''

    # Search for track URI in Spotify
    query = f"{title} {artist}".strip()
    if len(query) > 250:
        query = query[:250]

    print(f"[{idx}/{total_songs}] Checking: '{title}' by '{artist}'")

    try:
        result = sp.search(q=query, type='track', limit=1)
        if result['tracks']['items']:
            track_uri = result['tracks']['items'][0]['uri']
            # Check if track is already in Liked Songs
            is_saved = sp.current_user_saved_tracks_contains([track_uri])[0]
            if not is_saved:
                missing_songs.append(f"{title} - {artist}")
                print(f"    ⚠️ Not in Liked Songs")
            else:
                print(f"    ✅ Already in Liked Songs")
        else:
            missing_songs.append(f"{title} - {artist}")
            print(f"    ⚠️ Track not found on Spotify")
    except Exception as e:
        print(f"    ❌ Error: {e}")

    time.sleep(0.1)  # prevent rate limits

# --- Save missing songs to CSV ---
if missing_songs:
    with open("missing_songs.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Title - Artist"])
        for track in missing_songs:
            writer.writerow([track])
    print(f"\nTotal missing songs: {len(missing_songs)}")
    print("List saved to 'missing_songs.csv'")
else:
    print("\nAll CSV songs are in Liked Songs!")
