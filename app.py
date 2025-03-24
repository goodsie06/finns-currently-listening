from flask import Flask, render_template, jsonify
import requests
import threading
import time

currently_listening = Flask(__name__)

CLIENT_ID = "d190a9c01acd4930a83cb046e434b175"
CLIENT_SECRET = "2ac4ffa48da04717ad5f3097ccbd489b"
REDIRECT_URI = "http://localhost:8888/callback"

ACCESS_TOKEN = "BQBr5Y6TXJZSynxTcQG_T38ITjn4z0VlrN04-yNbmOVIlUdwbsO-rz3swV5d7Cto9blseLpCvKQpMZAhc5LWWcobsDS5sdt-4mbrz9BCqXXfq5Pnhmy4glaCNAYtqohDeAga2l5iewyyVeap93W628xo_tbjNNiM34sCtAWwsYhvOo52NlcEt5bi52K8661_MtSaWQLoAZ9DL58AKVy2OpxPbuDUTQEdY9VapdB9PfcIj8U"
REFRESH_TOKEN = "AQCPP1dLrWHu4-4s2jVbbH6PRiZEqqroU_ww3GHUKNKUljse8cp-3AI4OKYeOl2GqMkQaQok08tu6xFhDou47J5LATojYJJxtw8GDAFE9K5qyRjtEX2SUeBfoKsO1MQaPUA"

TOKEN_EXPIRATION_TIME = 3600  # 1 hour

def refresh_access_token():
    """Refresh Spotify access token."""
    global ACCESS_TOKEN
    url = "https://accounts.spotify.com/api/token"
    
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        new_token_info = response.json()
        ACCESS_TOKEN = new_token_info["access_token"]
        print("Access token refreshed successfully!")
    else:
        print(f"Failed to refresh token: {response.status_code} - {response.text}")

def auto_refresh_token():
    """Automatically refresh token before expiration."""
    while True:
        time.sleep(TOKEN_EXPIRATION_TIME - 60)
        refresh_access_token()

def get_currently_playing():
    """Fetch the currently playing song and its progress from Spotify API."""
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data and "item" in data:
            song_name = data["item"]["name"]
            artist_name = ", ".join(artist["name"] for artist in data["item"]["artists"])
            
            # Track progress (in milliseconds)
            progress_ms = data["progress_ms"]
            duration_ms = data["item"]["duration_ms"]
            
            # Convert to minutes and seconds
            progress_min = progress_ms // 60000
            progress_sec = (progress_ms % 60000) // 1000
            
            return {
                "track": song_name,
                "artist": artist_name,
                "progress": f"{progress_min:02}:{progress_sec:02}" 
            }
        else:
            return {"message": "No song is currently playing."}
    
    elif response.status_code == 401:  # Token expired
        print("Access token expired unexpectedly. Refreshing token...")
        refresh_access_token()
        return get_currently_playing()  # Retry after refreshing token
    
    else:
        return {"error": f"{response.status_code} - {response.text}"}

@currently_listening.route('/')
def home():
    return render_template('index.html')

@currently_listening.route('/currently-playing')
def currently_playing():
    """API route to return currently playing track and progress."""
    return jsonify(get_currently_playing())

if __name__ == '__main__':
    refresh_thread = threading.Thread(target=auto_refresh_token, daemon=True)
    refresh_thread.start()
    
    currently_listening.run(debug=True)


