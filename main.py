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
    scope="user-library-modify"
))

batch_size = 50
track_uris = []
not_found_songs = []

# --- Read CSV ---
with open("liked_songs.csv", newline='', encoding='utf-8') as csvfile:
    reader = list(csv.DictReader(csvfile))
    total_songs = len(reader)
    print(f"Total songs to process: {total_songs}")

    for idx, row in enumerate(reader, start=1):
        raw = row['Title']
        if '-' in raw:
            artist_part, title_part = raw.rsplit('-', 1)
            artist = artist_part.strip()
            title = title_part.strip()
        else:
            title = raw.strip()
            artist = row['Artist'].strip() if 'Artist' in row else ''

        # Build search query (max 250 chars)
        query = f"{title} {artist}".strip()
        if len(query) > 250:
            query = query[:250]

        print(f"[{idx}/{total_songs}] Searching: '{title}' by '{artist}'")

        try:
            result = sp.search(q=query, type='track', limit=1)
            if result['tracks']['items']:
                track_uris.append(result['tracks']['items'][0]['uri'])
                print(f"    ✅ Queued: {title}")
            else:
                not_found_songs.append(f"{title} - {artist}")
                print(f"    ⚠️ Not found")
        except Exception as e:
            print(f"    ❌ Error for '{title}': {e}")

        # Add tracks in batches of 50 immediately
        if len(track_uris) >= batch_size:
            try:
                sp.current_user_saved_tracks_add(track_uris[:batch_size])
                print(f"    💾 Added batch of {batch_size} tracks to Liked Songs")
                track_uris = track_uris[batch_size:]  # keep leftover tracks
            except Exception as e:
                print(f"    ❌ Error adding batch: {e}")

        time.sleep(0.1)  # avoid rate limits

# --- Add any remaining tracks less than batch_size ---
if track_uris:
    sp.current_user_saved_tracks_add(track_uris)
    print(f"    💾 Added final batch of {len(track_uris)} tracks")

# --- Summary ---
print("\n✅ All done!")
print(f"Total tracks added: {total_songs - len(not_found_songs)}")
print(f"Total tracks not found: {len(not_found_songs)}")

# Save not found songs
if not_found_songs:
    with open("not_found_songs.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Title - Artist"])
        for track in not_found_songs:
            writer.writerow([track])
    print("List of not found songs saved to 'not_found_songs.csv'")