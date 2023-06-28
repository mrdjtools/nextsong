# nextsong
Next Song

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

    if not client_id or not client_secret:
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
        recs = sp.recommendations(seed_tracks=[track['id']], target_tempo=target_tempo

, target_key=target_key)  # get recommendations based on the song
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

main_frame = ttk.Frame(root, padding="10")
main_frame.pack()

# GUI elements...

root.mainloop()
```

### Conclusion

This program allows you to generate song recommendations based on a given song name, target tempo, and target key. It utilizes the Spotipy library to interact with Spotify's API and retrieve recommendations. The program also provides functionality to display detailed information about each recommended song and open it on Spotify.

Feel free to customize and improve the program according to your needs. Enjoy exploring new music with the Next Song program!

For more information, please visit [mrdjnyc.com](www.mrdjnyc.com).
