## Next Song Program

This is a program that utilizes the Spotipy library to generate song recommendations based on user input. The program allows users to enter their Spotify client ID and client secret, along with a song name, target tempo, and target key in Camelot notation. It then retrieves recommendations from Spotify's API and displays them in a list.

### Prerequisites

To run this program, you need to have Python installed on your system. Additionally, you need to install the following libraries:

- spotipy
- tkinter

You can install these libraries using pip:

```
pip install spotipy
pip install tkinter
```

### Obtaining Spotify Client ID and Client Secret

To use the Spotify API, you need to obtain a client ID and client secret from the Spotify Developer Dashboard. Here's how you can acquire your own Spotify credentials:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and log in with your Spotify account or create a new account if you don't have one.

2. Create a new application by clicking on the "Create an App" button.

3. Fill in the required information for your application, including the name and description. You can also add a logo if you wish.

4. After creating the application, you will be redirected to the application dashboard. Here, you can find your client ID and client secret under the "Client ID" and "Client Secret" sections, respectively.

### Usage

1. Import the necessary libraries:

```python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
```

2. Define the function to display song information:

```python
def show_song_info(event):
    song = recommended_songs.get(recommended_songs.curselection())
    if isinstance(song, dict):
        info = f"Name: {song['name']}\nArtist: {song['artists'][0]['name']}\nAlbum: {song['album']['name']}\nDuration: {song['duration_ms'] / 1000} seconds"
        messagebox.showinfo('Song Info', info)
        webbrowser.open(song['external_urls']['spotify'])  # open the song on Spotify
```

3. Define the mapping for Camelot key notation and Spotify key values:

```python
camelot_key_mapping = {
    '1A': 0, '1B': 7,
    '2A': 1, '2B': 8,
    '3A': 2, '3B': 9,
    '4A': 3, '4B': 10,
    '5A': 4, '5B': 11,
    '6A': 5, '6B': 0,
    '7A': 6, '7B': 1,
    '8A': 7, '8B': 2,
    '9A': 8, '9B': 3,
    '10A': 9, '10B': 4,
    '11A': 10, '11B': 5,
    '12A': 11, '12B': 6
}

spotify_key_to_camelot = {v: k for k, v in camelot_key_mapping.items()}
```

4. Define the function to get song recommendations:

```python
def get_recommendation():
    client_id = client_id_entry.get()
    client_secret = client_secret_entry.get()
    song_name = song_name_entry.get()
    target_tempo = tempo_entry.get()
    target_key = camelot_key_mapping.get(key_entry.get().upper())

    if not client_id or not

 client_secret:
        messagebox.showerror('Error', 'Please enter your Spotify client ID and client secret.')
        return

    if not song_name:
        messagebox.showerror('Error', 'Please enter a song name.')
        return

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    try:
        results = sp.search(q=song_name, limit=1)  # search for the song
    except Exception as e:
        messagebox.showerror('Error', str(e))
        return

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        recs = sp.recommendations(seed_tracks=[track['id']], target_tempo=target_tempo, target_key=target_key)  # get recommendations based on the song
        if recs['tracks']:
            recommended_songs.delete(0, tk.END)
            for song in recs['tracks']:
                audio_features = sp.audio_features([song['id']])[0]  # get the audio features for the song
                if audio_features:
                    song_key = spotify_key_to_camelot.get(audio_features['key'], 'Unknown')
                    song_tempo = audio_features['tempo']
                else:
                    song_key = 'Unknown'
                    song_tempo = 'Unknown'

                song_info = f"{song['name']} by {song['artists'][0]['name']}, Key: {song_key}, Tempo: {song_tempo} BPM"
                recommended_songs.insert(tk.END, song_info)
        else:
            recommended_songs.delete(0, tk.END)
            recommended_songs.insert(tk.END, 'No recommendations found.')
    else:
        recommended_songs.delete(0, tk.END)
        recommended_songs.insert(tk.END, 'Song not found.')
```

5. Set up the GUI using tkinter:

```python
root = tk.Tk()
root.title('Next Song')
style = ttk.Style(root)
style.theme_use('clam')

# GUI elements...

root.mainloop()
```

### Obtaining Your Spotify Client ID and Client Secret

To use the Next Song program, you need to obtain your own Spotify client ID and client secret. Follow these steps to acquire your credentials:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and log in with your Spotify account or create a new account if you don't have one.

2. Click on the "Create an App" button to create a new application.

3. Provide a name and description for your application, and optionally, upload a logo.

4. Once your application is created, you will see your client ID and client secret on the application dashboard.

5. Copy your client ID and client secret and use them when running the Next Song program.

Make sure to keep your client secret secure and avoid sharing it publicly or committing it to version control.

### Conclusion

This program allows you to generate song recommendations based on a given song name, target tempo, and target key. To use the program, you need to obtain your own Spotify client ID and client secret from the Spotify Developer Dashboard. Follow the instructions provided in the README to obtain your credentials and run the program successfully.

Feel free to customize and improve the program according to your needs. Enjoy exploring new music with the Next Song program!

For more information, please visit [mrdjnyc.com](www.mrdjnyc.com).
