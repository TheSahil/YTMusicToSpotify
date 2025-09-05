# YTMusicToSpotify
Facilitates movement of a playlist from YouTube Music to Spotify

## Overview
This tool helps you migrate your liked songs from YouTube Music to Spotify by:
1. Reading a CSV file containing your YouTube Music liked songs
2. Searching for each song on Spotify
3. Adding found songs to your Spotify Liked Songs
4. Providing verification to check which songs were successfully added

## Prerequisites
- Python 3.7 or higher
- A Spotify Developer account
- A CSV file with your YouTube Music liked songs

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Spotify App Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Note down your `CLIENT_ID` and `CLIENT_SECRET`
4. Add a redirect URI (e.g., `http://localhost:8080/callback`)

### 3. Environment Configuration
1. Copy `PLACEHOLDER.env` to `.env`
2. Fill in your Spotify credentials:
```
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
REDIRECT_URI=http://localhost:8080/callback
```

### 4. Prepare Your Data
- Export your YouTube Music liked songs as a CSV file
- Name it `liked_songs.csv`
- Ensure it has columns: `Title` and `Artist`
- Place it in the project root directory

## Usage

### Running the Main Program
```bash
python main.py
```

This will:
- Read your `liked_songs.csv` file
- Search for each song on Spotify
- Add found songs to your Spotify Liked Songs in batches of 50
- Save any songs not found to `not_found_songs.csv`
- Display progress and results

### Running Verification
```bash
python verification.py
```

This will:
- Check which songs from your CSV are already in your Spotify Liked Songs
- Identify missing songs that weren't successfully added
- Save missing songs to `missing_songs.csv`
- Provide a summary of verification results

## Output Files
- `not_found_songs.csv` - Songs that couldn't be found on Spotify
- `missing_songs.csv` - Songs that were found but not added to Liked Songs
- Console output shows real-time progress and results

## Notes
- The program includes rate limiting to avoid Spotify API limits
- Songs are added in batches of 50 for efficiency
- Make sure your Spotify account is properly authenticated when running
- The verification script helps ensure all songs were successfully migrated

## Troubleshooting
- If you get authentication errors, check your Spotify app settings and redirect URI
- Ensure your `.env` file is properly configured
- Check that your CSV file has the correct format and encoding
- Verify your Spotify account has the necessary permissions
